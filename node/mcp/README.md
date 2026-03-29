# Anima MCP Server

The official Model Context Protocol (MCP) server for Anima is maintained in a separate repository.

## Installation

```bash
npx @anima-labs/mcp
```

Or install globally:

```bash
npm install -g @anima-labs/mcp
```

## Repository

See **[anima-labs-ai/mcp](https://github.com/anima-labs-ai/mcp)** for source, configuration, and documentation.

## Quick Start

Add to your MCP client configuration (e.g. Claude Desktop):

```json
{
  "mcpServers": {
    "anima": {
      "command": "npx",
      "args": ["@anima-labs/mcp"],
      "env": {
        "ANIMA_API_KEY": "sk-..."
      }
    }
  }
}
```

## Available Tools

The MCP server exposes the same tools as other Anima integrations:

- `send_email` — Send an email from an agent inbox
- `list_messages` — List messages in an inbox
- `get_message` — Get a specific message by ID
- `search_messages` — Search messages in an inbox
- `create_agent` — Create a new agent with an email inbox
- `list_agents` — List existing agents
- `create_card` — Create a virtual card
- `list_cards` — List virtual cards

## Documentation

See [docs.useanima.sh](https://docs.useanima.sh) for the full API reference.
