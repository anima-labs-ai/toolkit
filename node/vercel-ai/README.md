# @anima-labs/toolkit-vercel-ai

Anima tools for the [Vercel AI SDK](https://sdk.vercel.ai/). Provides tool definitions compatible with Vercel AI's `tool()` API for email, agents, and virtual cards.

## Installation

```bash
npm install @anima-labs/toolkit-vercel-ai
```

## Quick Start

```typescript
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";
import { animaTools } from "@anima-labs/toolkit-vercel-ai";

const result = await generateText({
  model: openai("gpt-4o"),
  tools: animaTools({ apiKey: process.env.ANIMA_API_KEY }),
  maxSteps: 5,
  prompt: "Send an email from agent_abc123 to hello@example.com saying hi",
});

console.log(result.text);
```

## Available Tools

| Tool | Description |
|------|-------------|
| `send_email` | Send an email from an agent inbox |
| `list_messages` | List messages in an inbox |
| `get_message` | Get a specific message by ID |
| `search_messages` | Search messages in an inbox |
| `create_agent` | Create a new agent with an email inbox |
| `list_agents` | List existing agents |
| `create_card` | Create a virtual card |
| `list_cards` | List virtual cards |

## Configuration

Pass your API key directly:

```typescript
const tools = animaTools({ apiKey: "sk-..." });
```

Or set it via environment variable:

```bash
export ANIMA_API_KEY=sk-...
```

```typescript
const tools = animaTools();
```

## Using with `streamText`

```typescript
import { streamText } from "ai";
import { openai } from "@ai-sdk/openai";
import { animaTools } from "@anima-labs/toolkit-vercel-ai";

const result = streamText({
  model: openai("gpt-4o"),
  tools: animaTools(),
  maxSteps: 5,
  prompt: "Check my inbox for agent_abc123",
});

for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}
```

## Documentation

See [docs.useanima.sh](https://docs.useanima.sh) for the full API reference.
