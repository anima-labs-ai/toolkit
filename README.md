# Anima Toolkit

Framework integrations for [Anima](https://docs.anima.email) — the AI agent identity platform. Give your agents real-world identity: email, virtual cards, phone/SMS, credential vault, and addresses.

## Available Integrations

### Python

| Package | Framework | Install |
|---------|-----------|---------|
| [anima-toolkit-openai](./python/openai-agents/) | OpenAI Agents SDK | `pip install anima-toolkit-openai` |
| [anima-toolkit-langchain](./python/langchain/) | LangChain | `pip install anima-toolkit-langchain` |

### Node.js / TypeScript

| Package | Framework | Install |
|---------|-----------|---------|
| [@anima-labs/toolkit-vercel-ai](./node/vercel-ai/) | Vercel AI SDK | `npm install @anima-labs/toolkit-vercel-ai` |
| [@anima-labs/toolkit-codex](./codex/) | OpenAI Codex / Function Calling | `npm install @anima-labs/toolkit-codex` |
| [@anima-labs/opencode-plugin](./opencode/) | OpenCode | `npm install @anima-labs/opencode-plugin` |

### Agent Platforms

| Integration | Platform | Setup |
|------------|----------|-------|
| [SKILL.md](./openclaw/) | OpenClaw | Copy `SKILL.md` to skills directory |
| [Cowork](./cowork/) | Claude Cowork | MCP config (deferred — API not yet public) |

### Protocol

| Package | Protocol | Details |
|---------|----------|---------|
| [@anima-labs/mcp](https://github.com/anima-labs-ai/mcp) | Model Context Protocol | 133+ tools, stdio + HTTP transports |
| [SKILL.md](https://github.com/anima-labs-ai/skill) | Claude Code Skill | Native Claude Code integration |

## Quick Example

```python
# OpenAI Agents SDK
from anima_toolkit_openai import anima_tools
from agents import Agent

agent = Agent(
    name="Email Assistant",
    tools=anima_tools(),
)
```

```typescript
// Vercel AI SDK
import { animaTools } from "@anima-labs/toolkit-vercel-ai";
import { generateText } from "ai";

const result = await generateText({
  model: openai("gpt-4o"),
  tools: animaTools({ apiKey: process.env.ANIMA_API_KEY }),
  prompt: "Send an email to hello@example.com",
});
```

## Unified Tool Surface (23 tools)

All integrations expose the same capabilities across the full Anima platform:

### Agent Management
- `create_agent` — Create a new AI agent with email identity
- `list_agents` — List existing agents

### Email
- `send_email` — Send an email from an agent inbox
- `list_messages` — List messages in an inbox
- `search_messages` — Search messages across inboxes

### Virtual Cards
- `create_card` — Create a virtual card with spending limits
- `list_cards` — List virtual cards
- `freeze_card` / `unfreeze_card` — Toggle card status
- `list_transactions` — View card transactions

### Credential Vault
- `provision_vault` — Set up encrypted storage
- `store_credential` — Save logins, API keys, secrets
- `get_credential` / `list_credentials` — Retrieve credentials
- `generate_password` — Create strong random passwords

### Phone / SMS
- `provision_phone` — Get a phone number for an agent
- `send_sms` — Send SMS messages
- `list_phones` — List provisioned numbers

### Addresses
- `create_address` — Create billing/shipping/mailing addresses
- `list_addresses` — List agent addresses
- `validate_address` — Validate via USPS/provider

## Documentation

Full API reference and guides at **[docs.anima.email](https://docs.anima.email)**.

## License

MIT
