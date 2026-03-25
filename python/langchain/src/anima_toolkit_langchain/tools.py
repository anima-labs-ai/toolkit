from __future__ import annotations

import os
from typing import Any, Optional, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from anima import Anima


def _get_client(api_key: Optional[str] = None) -> Anima:
    return Anima(api_key=api_key or os.environ.get("ANIMA_API_KEY"))


class SendEmailInput(BaseModel):
    agent_id: str = Field(description="The agent whose inbox to send from")
    to: list[str] = Field(description="List of recipient email addresses")
    subject: str = Field(description="Email subject line")
    body: str = Field(description="Email body text")


class SendEmailTool(BaseTool):
    name: str = "send_email"
    description: str = "Send an email from an Anima agent inbox"
    args_schema: Type[BaseModel] = SendEmailInput

    def _run(self, agent_id: str, to: list[str], subject: str, body: str) -> str:
        client = _get_client()
        result = client.messages.send_email(
            agent_id=agent_id, to=to, subject=subject, body=body
        )
        return f"Email sent. Message ID: {result.id}"


class ListMessagesInput(BaseModel):
    agent_id: str = Field(description="The agent whose inbox to read")
    limit: int = Field(default=20, description="Max number of messages to return")


class ListMessagesTool(BaseTool):
    name: str = "list_messages"
    description: str = "List messages in an agent's inbox"
    args_schema: Type[BaseModel] = ListMessagesInput

    def _run(self, agent_id: str, limit: int = 20) -> list[dict]:
        client = _get_client()
        messages = client.messages.list(agent_id=agent_id, limit=limit)
        return [
            {
                "id": m.id,
                "from": m.from_address,
                "subject": m.subject,
                "snippet": m.snippet,
                "date": m.created_at,
            }
            for m in messages.data
        ]


class GetMessageInput(BaseModel):
    agent_id: str = Field(description="The agent whose inbox contains the message")
    message_id: str = Field(description="The message ID to retrieve")


class GetMessageTool(BaseTool):
    name: str = "get_message"
    description: str = "Get a specific message by ID"
    args_schema: Type[BaseModel] = GetMessageInput

    def _run(self, agent_id: str, message_id: str) -> dict:
        client = _get_client()
        m = client.messages.get(agent_id=agent_id, message_id=message_id)
        return {
            "id": m.id,
            "from": m.from_address,
            "to": m.to_address,
            "subject": m.subject,
            "body": m.body,
            "date": m.created_at,
        }


class SearchMessagesInput(BaseModel):
    agent_id: str = Field(description="The agent whose inbox to search")
    query: str = Field(description="Search query string")
    limit: int = Field(default=10, description="Max number of results")


class SearchMessagesTool(BaseTool):
    name: str = "search_messages"
    description: str = "Search messages in an agent's inbox"
    args_schema: Type[BaseModel] = SearchMessagesInput

    def _run(self, agent_id: str, query: str, limit: int = 10) -> list[dict]:
        client = _get_client()
        results = client.messages.search(
            agent_id=agent_id, query=query, limit=limit
        )
        return [
            {
                "id": m.id,
                "from": m.from_address,
                "subject": m.subject,
                "snippet": m.snippet,
            }
            for m in results.data
        ]


class CreateAgentInput(BaseModel):
    name: str = Field(description="Display name for the agent")
    domain: Optional[str] = Field(
        default=None, description="Optional custom domain for the agent's email"
    )


class CreateAgentTool(BaseTool):
    name: str = "create_agent"
    description: str = "Create a new Anima agent with an email inbox"
    args_schema: Type[BaseModel] = CreateAgentInput

    def _run(self, name: str, domain: Optional[str] = None) -> dict:
        client = _get_client()
        agent = client.agents.create(name=name, domain=domain)
        return {"id": agent.id, "name": agent.name, "email": agent.email}


class ListAgentsInput(BaseModel):
    limit: int = Field(default=20, description="Max number of agents to return")


class ListAgentsTool(BaseTool):
    name: str = "list_agents"
    description: str = "List existing Anima agents"
    args_schema: Type[BaseModel] = ListAgentsInput

    def _run(self, limit: int = 20) -> list[dict]:
        client = _get_client()
        agents = client.agents.list(limit=limit)
        return [
            {"id": a.id, "name": a.name, "email": a.email}
            for a in agents.data
        ]


class CreateCardInput(BaseModel):
    agent_id: str = Field(description="The agent to create the card for")
    amount_cents: int = Field(
        description="Funding amount in cents (e.g. 1000 = $10.00)"
    )


class CreateCardTool(BaseTool):
    name: str = "create_card"
    description: str = "Create a virtual card for an agent"
    args_schema: Type[BaseModel] = CreateCardInput

    def _run(self, agent_id: str, amount_cents: int) -> dict:
        client = _get_client()
        card = client.cards.create(agent_id=agent_id, amount_cents=amount_cents)
        return {
            "id": card.id,
            "last4": card.last4,
            "amount_cents": card.amount_cents,
            "status": card.status,
        }


class ListCardsInput(BaseModel):
    agent_id: str = Field(description="The agent whose cards to list")


class ListCardsTool(BaseTool):
    name: str = "list_cards"
    description: str = "List virtual cards for an agent"
    args_schema: Type[BaseModel] = ListCardsInput

    def _run(self, agent_id: str) -> list[dict]:
        client = _get_client()
        cards = client.cards.list(agent_id=agent_id)
        return [
            {"id": c.id, "last4": c.last4, "status": c.status}
            for c in cards.data
        ]


ALL_TOOLS = [
    SendEmailTool,
    ListMessagesTool,
    GetMessageTool,
    SearchMessagesTool,
    CreateAgentTool,
    ListAgentsTool,
    CreateCardTool,
    ListCardsTool,
]


class AnimaToolkit:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def get_tools(self) -> list[BaseTool]:
        return [tool_cls() for tool_cls in ALL_TOOLS]


def get_anima_tools() -> list[BaseTool]:
    """Return all Anima tools as LangChain Tool instances."""
    return AnimaToolkit().get_tools()
