# Anima for Claude Cowork

> **Status:** Deferred — Claude Cowork API is not yet publicly available. This integration will be activated when Anthropic opens the Cowork integration surface.

## Planned Integration

When Claude Cowork's multi-agent collaboration API becomes available, Anima will provide:

- **MCP server connection** from Cowork workspaces — any agent in a Cowork session can provision emails, cards, phones, and store credentials
- **Shared agent identity** — agents in a Cowork session share the same Anima organization
- **Full unified surface** — email, phone, cards, vault, address via natural language

## Planned Configuration

```json
{
  "cowork": {
    "mcpServers": {
      "anima": {
        "command": "npx",
        "args": ["-y", "@anima-labs/mcp"],
        "env": {
          "ANIMA_API_KEY": "ak_..."
        }
      }
    }
  }
}
```

## Example Use Case

A multi-agent Cowork session where:
1. **Research Agent** searches for products via email
2. **Purchasing Agent** creates a virtual card with spending limits
3. **Finance Agent** stores receipts in vault and reconciles transactions
4. All agents share the same Anima organization identity

## Monitoring

We're tracking Cowork's public API availability. When ready:
- MCP config template will work out of the box
- Full documentation will be published at docs.useanima.sh
- Example Cowork sessions will be added to the examples repo

## Links

- [Claude Cowork](https://claude.ai/cowork)
- [Anima MCP Server](https://github.com/anima-labs-ai/mcp)
- [Anima Documentation](https://docs.useanima.sh)
