# Anima Toolkit

Framework integrations for [Anima](https://docs.anima.email) with popular AI agent SDKs.

Give your AI agents the ability to send emails, manage inboxes, create virtual cards, and more — using the framework you already work with.

## Available Integrations

### Python

| Package | Framework | Install |
|---------|-----------|---------|
| [anima-toolkit-openai](./python/openai-agents/) | OpenAI Agents SDK | `pip install anima-toolkit-openai` |
| [anima-toolkit-langchain](./python/langchain/) | LangChain | `pip install anima-toolkit-langchain` |

### Node.js

| Package | Framework | Install |
|---------|-----------|---------|
| [@anima-labs/toolkit-vercel-ai](./node/vercel-ai/) | Vercel AI SDK | `npm install @anima-labs/toolkit-vercel-ai` |
| [MCP Server](./node/mcp/) | Model Context Protocol | See [anima-labs-ai/mcp](https://github.com/anima-labs-ai/mcp) |

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

## Available Tools

All integrations expose the same core set of Anima tools:

- **send_email** — Send an email from an agent inbox
- **list_messages** — List messages in an inbox
- **get_message** — Get a specific message by ID
- **create_agent** — Create a new Anima agent with an inbox
- **list_agents** — List existing agents
- **create_card** — Create a virtual card for payments
- **list_cards** — List virtual cards
- **search_messages** — Search messages across inboxes

## Documentation

Full API reference and guides at **[docs.anima.email](https://docs.anima.email)**.

## License

MIT
