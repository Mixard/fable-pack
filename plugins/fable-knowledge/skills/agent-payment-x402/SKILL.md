---
name: agent-payment-x402
description: Use when adding x402 payment execution to AI agents - paying 402-gated APIs, enforcing per-task spending budgets, or charging agents for an API. Covers the agentwallet-sdk MCP server (Base), OKX Agent Payments Protocol (X Layer, eip155:196), seller SDK doc locations per language, and fail-closed budget enforcement.
---

# Agent Payment Execution (x402)

x402 extends HTTP 402 (Payment Required) into a machine-negotiable flow: when a server returns `402`, the agent's payment tool negotiates price, checks budget, signs a transaction, and retries - all inside a policy boundary set by the orchestrator. Agents hold their own keys via ERC-4337 smart accounts (non-custodial).

Protocol spec: x402.org

## Integration Decision Tree

| Need | Path |
|------|------|
| Agent pays a 402-gated API on Base (or other agentwallet-supported chain) | `agentwallet-sdk` as an MCP payment server with strict spending policy |
| Agent pays a 402-gated API on X Layer | OKX Agent Payments Protocol from `okx/onchainos-skills`; `okx-x402-payment` is a deprecated legacy alias |
| Your TypeScript API charges agents | OKX Payments TypeScript seller SDK (Express, Hono, Fastify, Next.js) |
| Your Go API charges agents | OKX Payments Go seller SDK (Gin, Echo, `net/http`) |
| Your Rust API charges agents | OKX Payments Rust seller SDK (Axum) |
| Your Java API charges agents | OKX Payments Java seller SDK (Spring Boot 2/3, Java EE, Jakarta) |
| Your Python API charges agents | Check the current `okx/payments` repo first; a Python seller guide may not exist |

Networks:
- `agentwallet-sdk`: Base Sepolia is the safest development default; Base mainnet for production. Confirm current network coverage in the package docs.
- OKX Payments / X Layer: seller docs target X Layer (`eip155:196`) with USDT0 settlement. Fetch current SDK docs before generating production code - packages and facilitator behavior change quickly.

## MCP Setup: agentwallet-sdk

Pin the version - this tool manages private keys, and unpinned `npx` installs are a supply-chain risk. Install globally first (`npm install -g agentwallet-sdk@6.0.0`), because `npx` without `-y` prompts for confirmation and hangs in non-interactive environments.

```json
{
  "mcpServers": {
    "agentpay": {
      "command": "npx",
      "args": ["agentwallet-sdk@6.0.0"]
    }
  }
}
```

Agent-callable tools:

| Tool | Purpose |
|------|---------|
| `get_balance` | Check agent wallet balance |
| `send_payment` | Send payment to address or ENS |
| `check_spending` | Query remaining budget |
| `list_transactions` | Audit trail of all payments |

`set_policy` is orchestrator-only: spending policy must be set by the orchestration layer before delegating, never exposed as an agent-callable tool, or the agent could escalate its own limits.

A `SpendingPolicy` enforces: per-task budget, per-session budget, allowlisted recipients, and rate limits (max transactions per minute/hour).

## OKX Agent Payments Protocol (X Layer)

Buyer-side agent flows:
1. Reference the current `okx/onchainos-skills` repository.
2. Use `skills/okx-agent-payments-protocol/SKILL.md` as the dispatcher; treat `skills/okx-x402-payment/SKILL.md` as a deprecated compatibility alias.
3. Require explicit user confirmation before wallet status checks or payment actions.

Seller-side guides (fetch current versions, do not copy from older docs):

| Runtime | Guide |
|---------|-------|
| TypeScript | `https://raw.githubusercontent.com/okx/payments/main/typescript/SELLER.md` |
| Go | `https://raw.githubusercontent.com/okx/payments/main/go/x402/SELLER.md` |
| Rust | `https://raw.githubusercontent.com/okx/payments/main/rust/x402/SELLER.md` |
| Java | `https://raw.githubusercontent.com/okx/payments/main/java/SELLER.md` |

## Fail-Closed Budget Enforcement (orchestrator side)

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const walletKey = process.env.WALLET_PRIVATE_KEY;
if (!walletKey) throw new Error("WALLET_PRIVATE_KEY not set - refusing to start payment server");

// Whitelist env vars - never forward all of process.env to a subprocess holding keys
const transport = new StdioClientTransport({
  command: "npx",
  args: ["agentwallet-sdk@6.0.0"],
  env: { PATH: process.env.PATH ?? "", WALLET_PRIVATE_KEY: walletKey },
});
const agentpay = new Client({ name: "orchestrator", version: "1.0.0" });
await agentpay.connect(transport);

// Set policy BEFORE delegating; verify success - silent failure means no controls
const policyResult = await agentpay.callTool({
  name: "set_policy",
  arguments: {
    per_task_budget: 0.50,
    per_session_budget: 5.00,
    allowlisted_recipients: ["api.example.com"],
  },
});
if (policyResult.isError) throw new Error("Failed to set spending policy - do not delegate");

// Pre-tool budget check: every failure path blocks the paid action
async function preToolCheck(apiCost: number): Promise<void> {
  // NaN/Infinity would bypass a < comparison
  if (!Number.isFinite(apiCost) || apiCost < 0) throw new Error(`Invalid apiCost: ${apiCost}`);

  let result;
  try {
    result = await agentpay.callTool({ name: "check_spending" });
  } catch (err) {
    throw new Error(`Payment service unreachable - action blocked: ${err}`);
  }
  if (result.isError) throw new Error("check_spending failed - action blocked");

  const parsed = JSON.parse((result.content as Array<{ text: string }>)[0].text);
  if (!Number.isFinite(parsed?.remaining)) throw new Error("check_spending returned unexpected format - action blocked");
  if (parsed.remaining < apiCost) {
    throw new Error(`Budget exceeded: need $${apiCost}, only $${parsed.remaining} remaining`);
  }
}
```

## Rules

- Set budgets before delegation; never give an agent unlimited spend.
- Fail closed: if the payment tool is unreachable, block the paid action - never fall back to unmetered access.
- Use `list_transactions` in post-task hooks for audit trails.
- Test on Base Sepolia first; switch to mainnet for production.
- Pin exact package versions in MCP configs and verify package integrity before production.
