---
name: defi-amm-security
description: Use when writing or auditing Solidity AMMs, LP vaults, or swap/deposit/withdraw flows. Covers vulnerable-vs-hardened pairs for reentrancy/CEI, donation-inflation share math, TWAP oracles, slippage and deadlines, SafeERC20/Ownable2Step/FullMath, and slither/echidna/forge fuzz commands.
---

# DeFi AMM Security

Vulnerability patterns with hardened counterparts for Solidity AMM contracts, LP vaults, and swap functions.

## Reentrancy: CEI ordering

External call before state update lets a malicious token or receiver re-enter and drain.

```solidity
// Vulnerable: effects after interaction
function withdraw(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    token.transfer(msg.sender, amount);
    balances[msg.sender] -= amount;
}
```

```solidity
// Hardened: checks-effects-interactions + guard + SafeERC20
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

using SafeERC20 for IERC20;

function withdraw(uint256 amount) external nonReentrant {
    require(balances[msg.sender] >= amount, "Insufficient");
    balances[msg.sender] -= amount;
    token.safeTransfer(msg.sender, amount);
}
```

OpenZeppelin's guard over a hand-rolled one; `SafeERC20` also handles non-standard tokens that return no bool.

## Donation / inflation attack

Share math based on raw `token.balanceOf(address(this))` lets an attacker inflate the denominator by sending tokens directly to the contract, skewing share prices (classic first-depositor / vault-inflation exploit).

```solidity
// Vulnerable: balanceOf as denominator
function deposit(uint256 assets) external returns (uint256 shares) {
    shares = (assets * totalShares) / token.balanceOf(address(this));
}
```

```solidity
// Hardened: internal accounting + measure actual tokens received
uint256 private _totalAssets;

function deposit(uint256 assets) external nonReentrant returns (uint256 shares) {
    uint256 balBefore = token.balanceOf(address(this));
    token.safeTransferFrom(msg.sender, address(this), assets);
    uint256 received = token.balanceOf(address(this)) - balBefore;

    shares = totalShares == 0 ? received : (received * totalShares) / _totalAssets;
    _totalAssets += received;
    totalShares += shares;
}
```

The before/after balance diff also handles fee-on-transfer tokens correctly.

## Oracle manipulation

Spot prices are flash-loan manipulable within a single block. Uniswap V3 TWAP via `observe()`:

```solidity
uint32[] memory secondsAgos = new uint32[](2);
secondsAgos[0] = 1800;
secondsAgos[1] = 0;
(int56[] memory tickCumulatives,) = IUniswapV3Pool(pool).observe(secondsAgos);
int24 twapTick = int24(
    (tickCumulatives[1] - tickCumulatives[0]) / int56(uint56(30 minutes))
);
uint160 sqrtPriceX96 = TickMath.getSqrtRatioAtTick(twapTick);
```

## Slippage and deadlines

Every swap path takes caller-provided `amountOutMin` and `deadline`; without them, transactions can be sandwiched or executed at stale prices.

```solidity
function swap(
    uint256 amountIn,
    uint256 amountOutMin,
    uint256 deadline
) external returns (uint256 amountOut) {
    require(block.timestamp <= deadline, "Expired");
    amountOut = _calculateOut(amountIn);
    require(amountOut >= amountOutMin, "Slippage exceeded");
    _executeSwap(amountIn, amountOut);
}
```

## Safe reserve math

Naive `a * b / c` overflows on large reserves before the division applies. `FullMath.mulDiv` computes the full 512-bit intermediate:

```solidity
import {FullMath} from "@uniswap/v3-core/contracts/libraries/FullMath.sol";

uint256 result = FullMath.mulDiv(a, b, c);
```

## Admin controls

`Ownable2Step` requires explicit acceptance by the new owner, preventing transfers to a mistyped address. Every privileged path (fee setters, pausers, oracle updates) gets an access modifier.

```solidity
import {Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";

contract MyAMM is Ownable2Step {
    function setFee(uint256 fee) external onlyOwner { ... }
    function pause() external onlyOwner { ... }
}
```

## Review checklist

- Reentrancy-exposed entrypoints use `nonReentrant`; CEI ordering holds
- Share math independent of raw `balanceOf(address(this))`; deposits measure actual tokens received
- ERC-20 transfers via `SafeERC20`
- Oracle reads use TWAP or another manipulation-resistant source
- Swaps require `amountOutMin` and `deadline`
- Overflow-sensitive reserve math uses `mulDiv`-style primitives
- Admin functions access-controlled; emergency pause exists and is tested
- Static analysis and fuzzing run before production

## Tooling

```bash
pip install slither-analyzer
slither . --exclude-dependencies

echidna-test . --contract YourAMM --config echidna.yaml

forge test --fuzz-runs 10000
```
