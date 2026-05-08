# anima-toolkit-openai

Anima tools for the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python). Gives your agents the ability to send emails, manage inboxes, and search messages.

## Installation

```bash
pip install anima-toolkit-openai
```

## Quick Start

```python
import os
from agents import Agent, Runner
from anima_toolkit_openai import anima_tools

os.environ["ANIMA_API_KEY"] = "sk-..."

agent = Agent(
    name="Email Assistant",
    instructions="You help users manage their email.",
    tools=anima_tools(),
)

result = Runner.run_sync(agent, "List the last 5 messages in agent_abc123's inbox")
print(result.final_output)
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

## Configuration

Set your API key via environment variable:

```bash
export ANIMA_API_KEY=sk-...
```

Or pass it when creating the toolkit:

```python
from anima_toolkit_openai import AnimaToolkit

toolkit = AnimaToolkit(api_key="sk-...")
agent = Agent(name="assistant", tools=toolkit.tools())
```

## Documentation

See [docs.useanima.sh](https://docs.useanima.sh) for the full API reference.
