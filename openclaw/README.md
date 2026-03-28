# Anima for OpenClaw

Give your [OpenClaw](https://github.com/openclaw/openclaw) agents real-world identity with Anima — email, virtual cards, phone numbers, credential vault, and addresses.

## Installation

Copy the `SKILL.md` file to your OpenClaw skills directory:

```bash
# Clone and copy
git clone https://github.com/anima-labs-ai/toolkit.git
cp toolkit/openclaw/SKILL.md ~/.openclaw/skills/anima/SKILL.md
```

Or submit as a PR to the [OpenClaw skills directory](https://github.com/openclaw/openclaw/tree/main/skills).

## Configuration

Set your Anima API key:

```bash
export ANIMA_API_KEY=ak_...
```

The MCP server (`@anima-labs/mcp`) will be started automatically by OpenClaw when an Anima tool is needed.

## What Your Agents Can Do

| Capability | Example |
|-----------|---------|
| **Email** | Send messages, monitor inbox, search emails |
| **Cards** | Create virtual cards with spending limits, freeze after use |
| **Vault** | Store CRM logins, API keys, generate passwords |
| **Phone** | Provision numbers, send SMS |
| **Address** | Create billing/shipping addresses, validate via USPS |
| **Browser** | Auto-fill checkout forms, execute payments |

## Links

- [Anima Documentation](https://docs.anima.email)
- [MCP Server](https://github.com/anima-labs-ai/mcp)
- [Full Skill Reference](https://github.com/anima-labs-ai/skill)
