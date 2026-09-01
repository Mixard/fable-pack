---
name: evm-gotchas
description: Use when reading ERC-20 balances, pricing tokens, or hashing Ethereum data in JS/TS/Python/Solidity. Covers per-chain token decimal drift with runtime decimals() lookup and WAD normalization, and the Node sha3-256 vs Keccak-256 mismatch with correct ethers/viem/web3 APIs.
---

# EVM Gotchas

## Token decimals vary per chain and bridge

The same symbol does not imply the same decimals across chains or bridge deployments. Hardcoding a divisor (e.g. `1_000_000` because a stablecoin has 6 decimals on one chain) produces balances and USD values off by orders of magnitude with no error thrown. Bridged and wrapped tokens can change precision relative to the origin asset.

Rules:

- Query `decimals()` at runtime, never assume by symbol
- Cache keyed by `(chain_id, token_address)`, not by symbol
- Use exact math (`Decimal`, `BigInt`), not floats
- Re-query decimals after bridging or wrapper changes
- Normalize internal accounting to one precision before comparison or pricing

### Runtime lookup (Python / web3.py)

```python
from decimal import Decimal
from web3 import Web3

ERC20_ABI = [
    {"name": "decimals", "type": "function", "inputs": [],
     "outputs": [{"type": "uint8"}], "stateMutability": "view"},
    {"name": "balanceOf", "type": "function",
     "inputs": [{"name": "account", "type": "address"}],
     "outputs": [{"type": "uint256"}], "stateMutability": "view"},
]

def get_token_balance(w3: Web3, token_address: str, wallet: str) -> Decimal:
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    decimals = contract.functions.decimals().call()
    raw = contract.functions.balanceOf(Web3.to_checksum_address(wallet)).call()
    return Decimal(raw) / Decimal(10 ** decimals)
```

### Cache by (chain, token)

```python
from functools import lru_cache

@lru_cache(maxsize=512)
def get_decimals(chain_id: int, token_address: str) -> int:
    w3 = get_web3_for_chain(chain_id)
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    return contract.functions.decimals().call()
```

Non-standard tokens exist where `decimals()` reverts; a logged, visible fallback to 18 keeps them handled without hiding the anomaly:

```python
try:
    decimals = contract.functions.decimals().call()
except Exception:
    logging.warning("decimals() reverted on %s (chain %s), defaulting to 18",
                    token_address, chain_id)
    decimals = 18
```

### WAD normalization (Solidity)

```solidity
interface IERC20Metadata {
    function decimals() external view returns (uint8);
}

function normalizeToWad(address token, uint256 amount) internal view returns (uint256) {
    uint8 d = IERC20Metadata(token).decimals();
    if (d == 18) return amount;
    if (d < 18) return amount * 10 ** (18 - d);
    return amount / 10 ** (d - 18);
}
```

### TypeScript (ethers v6)

```typescript
import { Contract, formatUnits } from 'ethers';

const ERC20_ABI = [
  'function decimals() view returns (uint8)',
  'function balanceOf(address) view returns (uint256)',
];

async function getBalance(provider: any, tokenAddress: string, wallet: string): Promise<string> {
  const token = new Contract(tokenAddress, ERC20_ABI, provider);
  const [decimals, raw] = await Promise.all([token.decimals(), token.balanceOf(wallet)]);
  return formatUnits(raw, decimals);
}
```

### Quick on-chain check

```bash
cast call <token_address> "decimals()(uint8)" --rpc-url <rpc>
```

## Node sha3-256 is not Keccak-256

Ethereum uses original Keccak-256. Node's `crypto.createHash('sha3-256')` is the NIST-standardized SHA3 variant (different padding), so it produces different digests for the same input with no warning. This silently breaks function selectors, event topics, EIP-712 hashes, Merkle trees, storage-slot derivation, and address derivation.

```javascript
import crypto from 'crypto';
import { keccak256, toUtf8Bytes } from 'ethers';

const data = 'hello';
const nistSha3 = crypto.createHash('sha3-256').update(data).digest('hex');
const keccak = keccak256(toUtf8Bytes(data)).slice(2);
console.log(nistSha3 === keccak); // false
```

For Ethereum contexts, use Keccak-aware helpers from `ethers`, `viem`, `web3`, or another explicit Keccak implementation — not Node crypto.

### ethers v6

```typescript
import { keccak256, toUtf8Bytes, solidityPackedKeccak256, id } from 'ethers';

const hash = keccak256(new Uint8Array([0x01, 0x02]));
const hash2 = keccak256(toUtf8Bytes('hello'));
const topic = id('Transfer(address,address,uint256)');       // event topic
const packed = solidityPackedKeccak256(
  ['address', 'uint256'],
  ['0x742d35Cc6634C0532925a3b8D4C9B569890FaC1c', 100n],
);
```

### viem

```typescript
import { keccak256, toBytes } from 'viem';

const hash = keccak256(toBytes('hello'));
```

### web3.js

```javascript
const hash = web3.utils.keccak256('hello');
const packed = web3.utils.soliditySha3(
  { type: 'address', value: '0x742d35Cc6634C0532925a3b8D4C9B569890FaC1c' },
  { type: 'uint256', value: '100' },
);
```

### Selectors, type hashes, mapping slots

```typescript
import { id, keccak256, toUtf8Bytes, AbiCoder } from 'ethers';

const selector = id('transfer(address,uint256)').slice(0, 10);
const typeHash = keccak256(toUtf8Bytes('Transfer(address from,address to,uint256 value)'));

// Storage slot of mapping[key] at declared slot mappingSlot
function getMappingSlot(key: string, mappingSlot: number): string {
  return keccak256(
    AbiCoder.defaultAbiCoder().encode(['address', 'uint256'], [key, mappingSlot]),
  );
}
```

### Address from public key

```typescript
import { keccak256 } from 'ethers';

function pubkeyToAddress(pubkeyBytes: Uint8Array): string {
  const hash = keccak256(pubkeyBytes.slice(1));  // drop 0x04 prefix
  return '0x' + hash.slice(-40);
}
```

### Auditing a codebase for the bug

```bash
grep -rn "createHash.*sha3" --include="*.ts" --include="*.js" --exclude-dir=node_modules .
grep -rn "keccak256" --include="*.ts" --include="*.js" . | grep -v node_modules
```
