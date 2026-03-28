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


# ---------------------------------------------------------------------------
# Card Management (expanded)
# ---------------------------------------------------------------------------


class FreezeCardInput(BaseModel):
    card_id: str = Field(description="The card ID to freeze")


class FreezeCardTool(BaseTool):
    name: str = "freeze_card"
    description: str = "Freeze a virtual card to temporarily block all transactions"
    args_schema: Type[BaseModel] = FreezeCardInput

    def _run(self, card_id: str) -> str:
        client = _get_client()
        client.cards.freeze(card_id=card_id)
        return f"Card {card_id} frozen"


class UnfreezeCardTool(BaseTool):
    name: str = "unfreeze_card"
    description: str = "Unfreeze a card to re-enable transactions"
    args_schema: Type[BaseModel] = FreezeCardInput

    def _run(self, card_id: str) -> str:
        client = _get_client()
        client.cards.unfreeze(card_id=card_id)
        return f"Card {card_id} unfrozen"


class ListTransactionsInput(BaseModel):
    card_id: str = Field(description="The card ID to list transactions for")
    limit: int = Field(default=20, description="Max number of transactions")


class ListTransactionsTool(BaseTool):
    name: str = "list_transactions"
    description: str = "List transactions on a virtual card"
    args_schema: Type[BaseModel] = ListTransactionsInput

    def _run(self, card_id: str, limit: int = 20) -> list[dict]:
        client = _get_client()
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


class ProvisionVaultInput(BaseModel):
    agent_id: str = Field(description="The agent to provision a vault for")


class ProvisionVaultTool(BaseTool):
    name: str = "provision_vault"
    description: str = "Provision an encrypted credential vault for an agent"
    args_schema: Type[BaseModel] = ProvisionVaultInput

    def _run(self, agent_id: str) -> str:
        client = _get_client()
        client.vault.provision(agent_id=agent_id)
        return f"Vault provisioned for agent {agent_id}"


class StoreCredentialInput(BaseModel):
    agent_id: str = Field(description="The agent whose vault to store in")
    name: str = Field(description="Name/label for the credential")
    type: str = Field(description="Credential type: login, secure_note, card, identity")
    username: Optional[str] = Field(default=None, description="Username (for login type)")
    password: Optional[str] = Field(default=None, description="Password (for login type)")
    uris: Optional[list[str]] = Field(default=None, description="Associated URIs")
    notes: Optional[str] = Field(default=None, description="Free-form notes")


class StoreCredentialTool(BaseTool):
    name: str = "store_credential"
    description: str = "Store an encrypted credential in the agent's vault"
    args_schema: Type[BaseModel] = StoreCredentialInput

    def _run(self, agent_id: str, name: str, type: str, **kwargs: Any) -> dict:
        client = _get_client()
        cred = client.vault.create_credential(
            agent_id=agent_id, name=name, type=type, **kwargs
        )
        return {"id": cred.id, "name": cred.name, "type": cred.type}


class GetCredentialInput(BaseModel):
    agent_id: str = Field(description="The agent whose vault to read from")
    credential_id: str = Field(description="The credential ID to retrieve")


class GetCredentialTool(BaseTool):
    name: str = "get_credential"
    description: str = "Retrieve a credential from the agent's vault"
    args_schema: Type[BaseModel] = GetCredentialInput

    def _run(self, agent_id: str, credential_id: str) -> dict:
        client = _get_client()
        cred = client.vault.get_credential(
            agent_id=agent_id, credential_id=credential_id
        )
        return {
            "id": cred.id,
            "name": cred.name,
            "type": cred.type,
            "username": getattr(cred, "username", None),
        }


class ListCredentialsInput(BaseModel):
    agent_id: str = Field(description="The agent whose vault to list")


class ListCredentialsTool(BaseTool):
    name: str = "list_credentials"
    description: str = "List all credentials in the agent's vault"
    args_schema: Type[BaseModel] = ListCredentialsInput

    def _run(self, agent_id: str) -> list[dict]:
        client = _get_client()
        creds = client.vault.list(agent_id=agent_id)
        return [
            {"id": c.id, "name": c.name, "type": c.type}
            for c in creds
        ]


class GeneratePasswordInput(BaseModel):
    length: int = Field(default=20, description="Password length")


class GeneratePasswordTool(BaseTool):
    name: str = "generate_password"
    description: str = "Generate a strong random password"
    args_schema: Type[BaseModel] = GeneratePasswordInput

    def _run(self, length: int = 20) -> str:
        client = _get_client()
        result = client.vault.generate_password(length=length)
        return result.value


# ---------------------------------------------------------------------------
# Phone / SMS
# ---------------------------------------------------------------------------


class ProvisionPhoneInput(BaseModel):
    agent_id: str = Field(description="The agent to provision a phone for")
    number: str = Field(description="Phone number to provision (E.164 format)")


class ProvisionPhoneTool(BaseTool):
    name: str = "provision_phone"
    description: str = "Provision a phone number for an agent"
    args_schema: Type[BaseModel] = ProvisionPhoneInput

    def _run(self, agent_id: str, number: str) -> dict:
        client = _get_client()
        phone = client.phone.provision(agent_id=agent_id, number=number)
        return {"number": phone.number, "status": phone.status}


class SendSmsInput(BaseModel):
    agent_id: str = Field(description="The agent to send SMS from")
    to: str = Field(description="Recipient phone number (E.164 format)")
    body: str = Field(description="SMS message text")


class SendSmsTool(BaseTool):
    name: str = "send_sms"
    description: str = "Send an SMS message from an agent's phone number"
    args_schema: Type[BaseModel] = SendSmsInput

    def _run(self, agent_id: str, to: str, body: str) -> str:
        client = _get_client()
        msg = client.phone.send_sms(agent_id=agent_id, to=to, body=body)
        return f"SMS sent. Message ID: {msg.id}"


class ListPhonesInput(BaseModel):
    agent_id: str = Field(description="The agent whose phone numbers to list")


class ListPhonesTool(BaseTool):
    name: str = "list_phones"
    description: str = "List phone numbers provisioned for an agent"
    args_schema: Type[BaseModel] = ListPhonesInput

    def _run(self, agent_id: str) -> list[dict]:
        client = _get_client()
        phones = client.phone.list(agent_id=agent_id)
        return [
            {"number": p.number, "status": p.status}
            for p in phones.data
        ]


# ---------------------------------------------------------------------------
# Address Management
# ---------------------------------------------------------------------------


class CreateAddressInput(BaseModel):
    agent_id: str = Field(description="The agent to create the address for")
    type: str = Field(description="Address type: BILLING, SHIPPING, MAILING, REGISTERED")
    street1: str = Field(description="Street address line 1")
    street2: Optional[str] = Field(default=None, description="Street address line 2")
    city: str = Field(description="City")
    state: str = Field(description="State/province")
    postal_code: str = Field(description="Postal/ZIP code")
    country: str = Field(description="ISO 3166-1 alpha-2 country code (e.g. US)")
    label: Optional[str] = Field(default=None, description="Optional label (e.g. 'Office')")


class CreateAddressTool(BaseTool):
    name: str = "create_address"
    description: str = "Create a billing, shipping, or mailing address for an agent"
    args_schema: Type[BaseModel] = CreateAddressInput

    def _run(self, agent_id: str, type: str, street1: str, city: str,
             state: str, postal_code: str, country: str, **kwargs: Any) -> dict:
        client = _get_client()
        addr = client.addresses.create(
            agent_id=agent_id, type=type, street1=street1, city=city,
            state=state, postal_code=postal_code, country=country, **kwargs
        )
        return {
            "id": addr.id,
            "type": addr.type,
            "street1": addr.street1,
            "city": addr.city,
            "state": addr.state,
            "country": addr.country,
            "validated": addr.validated,
        }


class ListAddressesInput(BaseModel):
    agent_id: str = Field(description="The agent whose addresses to list")
    type: Optional[str] = Field(default=None, description="Filter by type (BILLING, SHIPPING, etc.)")


class ListAddressesTool(BaseTool):
    name: str = "list_addresses"
    description: str = "List addresses for an agent"
    args_schema: Type[BaseModel] = ListAddressesInput

    def _run(self, agent_id: str, type: Optional[str] = None) -> list[dict]:
        client = _get_client()
        addrs = client.addresses.list(agent_id=agent_id, type=type)
        return [
            {
                "id": a.id,
                "type": a.type,
                "street1": a.street1,
                "city": a.city,
                "state": a.state,
                "country": a.country,
                "validated": a.validated,
            }
            for a in addrs.data
        ]


class ValidateAddressInput(BaseModel):
    agent_id: str = Field(description="The agent who owns the address")
    address_id: str = Field(description="The address ID to validate")


class ValidateAddressTool(BaseTool):
    name: str = "validate_address"
    description: str = "Validate and standardize an agent's address via USPS/provider"
    args_schema: Type[BaseModel] = ValidateAddressInput

    def _run(self, agent_id: str, address_id: str) -> dict:
        client = _get_client()
        result = client.addresses.validate(
            agent_id=agent_id, address_id=address_id
        )
        return {
            "valid": result.valid,
            "confidence": result.confidence,
            "standardized": result.standardized,
        }


# ---------------------------------------------------------------------------
# Tool Registry
# ---------------------------------------------------------------------------

ALL_TOOLS = [
    # Email / Messaging
    SendEmailTool,
    ListMessagesTool,
    GetMessageTool,
    SearchMessagesTool,
    # Agent
    CreateAgentTool,
    ListAgentsTool,
    # Cards
    CreateCardTool,
    ListCardsTool,
    FreezeCardTool,
    UnfreezeCardTool,
    ListTransactionsTool,
    # Vault
    ProvisionVaultTool,
    StoreCredentialTool,
    GetCredentialTool,
    ListCredentialsTool,
    GeneratePasswordTool,
    # Phone
    ProvisionPhoneTool,
    SendSmsTool,
    ListPhonesTool,
    # Address
    CreateAddressTool,
    ListAddressesTool,
    ValidateAddressTool,
]


class AnimaToolkit:
    """LangChain toolkit providing the full Anima unified surface."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def get_tools(self) -> list[BaseTool]:
        """Return all Anima tools as LangChain BaseTool instances."""
        return [tool_cls() for tool_cls in ALL_TOOLS]


def get_anima_tools() -> list[BaseTool]:
    """Return all Anima tools as LangChain Tool instances."""
    return AnimaToolkit().get_tools()
