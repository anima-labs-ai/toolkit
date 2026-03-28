# Anima for OpenCode

Give your [OpenCode](https://github.com/opencode-ai/opencode) agents real-world identity with Anima — email, virtual cards, phone numbers, credential vault, and addresses.

## Installation

```bash
npm install @anima-labs/opencode-plugin
```

## Configuration

Add to your OpenCode plugin configuration:

```ts
import { animaPlugin } from "@anima-labs/opencode-plugin";

export default {
  plugins: [animaPlugin],
};
```

Set your Anima API key:

```bash
export ANIMA_API_KEY=ak_...
```

## Available Tools (21)

| Category | Tools |
|----------|-------|
| **Agent** | `create_agent`, `list_agents` |
| **Email** | `send_email`, `list_messages`, `search_messages` |
| **Cards** | `create_card`, `list_cards`, `freeze_card`, `unfreeze_card`, `list_transactions` |
| **Vault** | `provision_vault`, `store_credential`, `get_credential`, `list_credentials`, `generate_password` |
| **Phone** | `provision_phone`, `send_sms`, `list_phones` |
| **Address** | `create_address`, `list_addresses`, `validate_address` |

## Links

- [Anima Documentation](https://docs.anima.email)
- [OpenCode](https://github.com/opencode-ai/opencode)
- [MCP Server](https://github.com/anima-labs-ai/mcp)
