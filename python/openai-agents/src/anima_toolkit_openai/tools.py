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


# ---------------------------------------------------------------------------
# Card Management (expanded)
# ---------------------------------------------------------------------------


@function_tool
def freeze_card(card_id: str, api_key: Optional[str] = None) -> str:
    """Freeze a virtual card to temporarily block all transactions.

    Args:
        card_id: The card ID to freeze.
    """
    client = _get_client(api_key)
    client.cards.freeze(card_id=card_id)
    return f"Card {card_id} frozen"


@function_tool
def unfreeze_card(card_id: str, api_key: Optional[str] = None) -> str:
    """Unfreeze a card to re-enable transactions.

    Args:
        card_id: The card ID to unfreeze.
    """
    client = _get_client(api_key)
    client.cards.unfreeze(card_id=card_id)
    return f"Card {card_id} unfrozen"


@function_tool
def list_transactions(
    card_id: str,
    limit: int = 20,
    api_key: Optional[str] = None,
) -> list[dict]:
    """List transactions on a virtual card.

    Args:
        card_id: The card ID to list transactions for.
        limit: Max number of transactions to return.
    """
    client = _get_client(api_key)
    txns = client.cards.list_transactions(card_id=card_id, limit=limit)
    return [
        {
            "id": t.id,
            "amount": t.amount,
            "merchant": t.merchant_name,
            "status": t.status,
            "date": t.created_at,
        }
        for t in txns.data
    ]


# ---------------------------------------------------------------------------
# Vault / Credential Management
# ---------------------------------------------------------------------------


@function_tool
def provision_vault(agent_id: str, api_key: Optional[str] = None) -> str:
    """Provision an encrypted credential vault for an agent.

    Args:
        agent_id: The agent to provision a vault for.
    """
    client = _get_client(api_key)
    client.vault.provision(agent_id=agent_id)
    return f"Vault provisioned for agent {agent_id}"


@function_tool
def store_credential(
    agent_id: str,
    name: str,
    type: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    uris: Optional[list[str]] = None,
    notes: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """Store an encrypted credential in the agent's vault.

    Args:
        agent_id: The agent whose vault to store in.
        name: Name/label for the credential.
        type: Credential type: login, secure_note, card, identity.
        username: Username (for login type).
        password: Password (for login type).
        uris: Associated URIs.
        notes: Free-form notes.
    """
    client = _get_client(api_key)
    kwargs = {}
    if username is not None:
        kwargs["username"] = username
    if password is not None:
        kwargs["password"] = password
    if uris is not None:
        kwargs["uris"] = uris
    if notes is not None:
        kwargs["notes"] = notes
    cred = client.vault.create_credential(
        agent_id=agent_id, name=name, type=type, **kwargs
    )
    return {"id": cred.id, "name": cred.name, "type": cred.type}


@function_tool
def get_credential(
    agent_id: str,
    credential_id: str,
    api_key: Optional[str] = None,
) -> dict:
    """Retrieve a credential from the agent's vault.

    Args:
        agent_id: The agent whose vault to read from.
        credential_id: The credential ID to retrieve.
    """
    client = _get_client(api_key)
    cred = client.vault.get_credential(
        agent_id=agent_id, credential_id=credential_id
    )
    return {
        "id": cred.id,
        "name": cred.name,
        "type": cred.type,
        "username": getattr(cred, "username", None),
    }


@function_tool
def list_credentials(
    agent_id: str,
    api_key: Optional[str] = None,
) -> list[dict]:
    """List all credentials in the agent's vault.

    Args:
        agent_id: The agent whose vault to list.
    """
    client = _get_client(api_key)
    creds = client.vault.list(agent_id=agent_id)
    return [{"id": c.id, "name": c.name, "type": c.type} for c in creds]


@function_tool
def generate_password(
    length: int = 20,
    api_key: Optional[str] = None,
) -> str:
    """Generate a strong random password.

    Args:
        length: Password length.
    """
    client = _get_client(api_key)
    result = client.vault.generate_password(length=length)
    return result.value


# ---------------------------------------------------------------------------
# Phone / SMS
# ---------------------------------------------------------------------------


@function_tool
def provision_phone(
    agent_id: str,
    number: str,
    api_key: Optional[str] = None,
) -> dict:
    """Provision a phone number for an agent.

    Args:
        agent_id: The agent to provision a phone for.
        number: Phone number to provision (E.164 format).
    """
    client = _get_client(api_key)
    phone = client.phone.provision(agent_id=agent_id, number=number)
    return {"number": phone.number, "status": phone.status}


@function_tool
def send_sms(
    agent_id: str,
    to: str,
    body: str,
    api_key: Optional[str] = None,
) -> str:
    """Send an SMS message from an agent's phone number.

    Args:
        agent_id: The agent to send SMS from.
        to: Recipient phone number (E.164 format).
        body: SMS message text.
    """
    client = _get_client(api_key)
    msg = client.phone.send_sms(agent_id=agent_id, to=to, body=body)
    return f"SMS sent. Message ID: {msg.id}"


@function_tool
def list_phones(
    agent_id: str,
    api_key: Optional[str] = None,
) -> list[dict]:
    """List phone numbers provisioned for an agent.

    Args:
        agent_id: The agent whose phone numbers to list.
    """
    client = _get_client(api_key)
    phones = client.phone.list(agent_id=agent_id)
    return [{"number": p.number, "status": p.status} for p in phones.data]


# ---------------------------------------------------------------------------
# Address Management
# ---------------------------------------------------------------------------


@function_tool
def create_address(
    agent_id: str,
    type: str,
    street1: str,
    city: str,
    state: str,
    postal_code: str,
    country: str,
    street2: Optional[str] = None,
    label: Optional[str] = None,
    api_key: Optional[str] = None,
) -> dict:
    """Create a billing, shipping, or mailing address for an agent.

    Args:
        agent_id: The agent to create the address for.
        type: Address type: BILLING, SHIPPING, MAILING, REGISTERED.
        street1: Street address line 1.
        city: City.
        state: State/province.
        postal_code: Postal/ZIP code.
        country: ISO 3166-1 alpha-2 country code (e.g. US).
        street2: Street address line 2.
        label: Optional label (e.g. 'Office').
    """
    client = _get_client(api_key)
    kwargs = {}
    if street2 is not None:
        kwargs["street2"] = street2
    if label is not None:
        kwargs["label"] = label
    addr = client.addresses.create(
        agent_id=agent_id, type=type, street1=street1, city=city,
        state=state, postal_code=postal_code, country=country, **kwargs
    )
    return {
        "id": addr.id, "type": addr.type, "street1": addr.street1,
        "city": addr.city, "state": addr.state, "country": addr.country,
        "validated": addr.validated,
    }


@function_tool
def list_addresses(
    agent_id: str,
    type: Optional[str] = None,
    api_key: Optional[str] = None,
) -> list[dict]:
    """List addresses for an agent.

    Args:
        agent_id: The agent whose addresses to list.
        type: Optional filter by type (BILLING, SHIPPING, etc.).
    """
    client = _get_client(api_key)
    addrs = client.addresses.list(agent_id=agent_id, type=type)
    return [
        {
            "id": a.id, "type": a.type, "street1": a.street1,
            "city": a.city, "state": a.state, "country": a.country,
            "validated": a.validated,
        }
        for a in addrs.data
    ]


@function_tool
def validate_address(
    agent_id: str,
    address_id: str,
    api_key: Optional[str] = None,
) -> dict:
    """Validate and standardize an agent's address via USPS/provider.

    Args:
        agent_id: The agent who owns the address.
        address_id: The address ID to validate.
    """
    client = _get_client(api_key)
    result = client.addresses.validate(
        agent_id=agent_id, address_id=address_id
    )
    return {
        "valid": result.valid,
        "confidence": result.confidence,
    }


# ---------------------------------------------------------------------------
# Tool Registry
# ---------------------------------------------------------------------------

ALL_TOOLS = [
    # Email / Messaging
    send_email,
    list_messages,
    get_message,
    search_messages,
    # Agent
    create_agent,
    list_agents,
    # Cards
    create_card,
    list_cards,
    freeze_card,
    unfreeze_card,
    list_transactions,
    # Vault
    provision_vault,
    store_credential,
    get_credential,
    list_credentials,
    generate_password,
    # Phone
    provision_phone,
    send_sms,
    list_phones,
    # Address
    create_address,
    list_addresses,
    validate_address,
]


class AnimaToolkit:
    """Toolkit providing the full Anima unified surface for OpenAI Agents SDK."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def tools(self) -> list:
        return list(ALL_TOOLS)


def anima_tools() -> list:
    """Return all Anima tools for use with OpenAI Agents SDK."""
    return AnimaToolkit().tools()
