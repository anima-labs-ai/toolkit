from __future__ import annotations

import os
from typing import Optional

from agents import function_tool
from anima import Anima


def _get_client(api_key: Optional[str] = None) -> Anima:
    return Anima(api_key=api_key or os.environ.get("ANIMA_API_KEY"))


@function_tool
def send_email(
    agent_id: str,
    to: list[str],
    subject: str,
    body: str,
    api_key: Optional[str] = None,
) -> str:
    """Send an email from an Anima agent inbox.

    Args:
        agent_id: The agent whose inbox to send from.
        to: List of recipient email addresses.
        subject: Email subject line.
        body: Email body text.
    """
    client = _get_client(api_key)
    result = client.messages.send_email(
        agent_id=agent_id,
        to=to,
        subject=subject,
        body=body,
    )
    return f"Email sent. Message ID: {result.id}"


@function_tool
def list_messages(
    agent_id: str,
    limit: int = 20,
    api_key: Optional[str] = None,
) -> list[dict]:
    """List messages in an agent's inbox.

    Args:
        agent_id: The agent whose inbox to read.
        limit: Max number of messages to return.
    """
    client = _get_client(api_key)
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


@function_tool
def get_message(
    agent_id: str,
    message_id: str,
    api_key: Optional[str] = None,
) -> dict:
    """Get a specific message by ID.

    Args:
        agent_id: The agent whose inbox contains the message.
        message_id: The message ID to retrieve.
    """
    client = _get_client(api_key)
    m = client.messages.get(agent_id=agent_id, message_id=message_id)
    return {
        "id": m.id,
        "from": m.from_address,
        "to": m.to_address,
        "subject": m.subject,
        "body": m.body,
        "date": m.created_at,
    }


@function_tool
def search_messages(
    agent_id: str,
    query: str,
    limit: int = 10,
    api_key: Optional[str] = None,
) -> list[dict]:
    """Search messages in an agent's inbox.

    Args:
        agent_id: The agent whose inbox to search.
        query: Search query string.
        limit: Max number of results to return.
    """
    client = _get_client(api_key)
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


@function_tool
def create_agent(
    name: str,
    domain: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """Create a new Anima agent with an email inbox.

    Args:
        name: Display name for the agent.
        domain: Optional custom domain for the agent's email.
    """
    client = _get_client(api_key)
    agent = client.agents.create(name=name, domain=domain)
    return {
        "id": agent.id,
        "name": agent.name,
        "email": agent.email,
    }


@function_tool
def list_agents(
    limit: int = 20,
    api_key: Optional[str] = None,
) -> list[dict]:
    """List existing Anima agents.

    Args:
        limit: Max number of agents to return.
    """
    client = _get_client(api_key)
    agents = client.agents.list(limit=limit)
    return [
        {"id": a.id, "name": a.name, "email": a.email}
        for a in agents.data
    ]


@function_tool
def create_card(
    agent_id: str,
    amount_cents: int,
    api_key: Optional[str] = None,
) -> dict:
    """Create a virtual card for an agent.

    Args:
        agent_id: The agent to create the card for.
        amount_cents: Funding amount in cents (e.g. 1000 = $10.00).
    """
    client = _get_client(api_key)
    card = client.cards.create(agent_id=agent_id, amount_cents=amount_cents)
    return {
        "id": card.id,
        "last4": card.last4,
        "amount_cents": card.amount_cents,
        "status": card.status,
    }


@function_tool
def list_cards(
    agent_id: str,
    api_key: Optional[str] = None,
) -> list[dict]:
    """List virtual cards for an agent.

    Args:
        agent_id: The agent whose cards to list.
    """
    client = _get_client(api_key)
    cards = client.cards.list(agent_id=agent_id)
    return [
        {"id": c.id, "last4": c.last4, "status": c.status}
        for c in cards.data
    ]


ALL_TOOLS = [
    send_email,
    list_messages,
    get_message,
    search_messages,
    create_agent,
    list_agents,
    create_card,
    list_cards,
]


class AnimaToolkit:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def tools(self) -> list:
        return list(ALL_TOOLS)


def anima_tools() -> list:
    """Return all Anima tools for use with OpenAI Agents SDK."""
    return AnimaToolkit().tools()
