# anima-toolkit-langchain

Anima tools for [LangChain](https://python.langchain.com/). Provides LangChain `BaseTool` implementations that wrap the Anima SDK for email and agents.

## Installation

```bash
pip install anima-toolkit-langchain
```

## Quick Start

```python
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate
from anima_toolkit_langchain import get_anima_tools

os.environ["ANIMA_API_KEY"] = "sk-..."

tools = get_anima_tools()
llm = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You help users manage their email."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_openai_tools_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

result = executor.invoke({"input": "List agents"})
print(result["output"])
```

## Available Tools

| Tool | Description |
|------|-------------|
| `SendEmailTool` | Send an email from an agent inbox |
| `ListMessagesTool` | List messages in an inbox |
| `GetMessageTool` | Get a specific message by ID |
| `SearchMessagesTool` | Search messages in an inbox |
| `CreateAgentTool` | Create a new agent with an email inbox |
| `ListAgentsTool` | List existing agents |

## Configuration

Set your API key via environment variable:

```bash
export ANIMA_API_KEY=sk-...
```

## Documentation

See [docs.useanima.sh](https://docs.useanima.sh) for the full API reference.
