---
name: anima
description: "Anima AI agent identity platform: email, phone/SMS, credential vault, addresses, webhooks. Use when: (1) sending or reading emails for agents, (2) storing or retrieving credentials, (3) provisioning phone numbers or sending SMS, (4) managing agent addresses. NOT for: general web browsing (use browser tools), non-agent identity tasks."
metadata:
  {
    "openclaw":
      {
        "emoji": "🦋",
        "requires": { "bins": ["npx"], "env": ["ANIMA_API_KEY"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@anima-labs/mcp",
              "bins": ["anima-mcp"],
              "label": "Install Anima MCP Server (npm)",
            },
          ],
        "mcp":
          {
            "command": "npx",
            "args": ["-y", "@anima-labs/mcp"],
            "env": { "ANIMA_API_KEY": "${ANIMA_API_KEY}" },
          },
      },
  }
---

# Anima — Agent Identity Platform

Give your OpenClaw agents real-world identity: email addresses, phone numbers, encrypted credential storage, and validated addresses.

## When to Use

USE this skill when:

- Sending or receiving emails from an AI agent
- Storing or retrieving login credentials, API keys, or secrets
- Provisioning phone numbers or sending SMS
- Creating and validating billing/shipping addresses
- Managing webhooks for real-time event notifications

DO NOT use for:

- General web browsing (use browser tools)
- Tasks unrelated to agent identity or communication

## Setup

1. Get an API key at [console.useanima.sh](https://console.useanima.sh)
2. Set `ANIMA_API_KEY` in your environment
3. The MCP server starts automatically when needed

## Available Tools

### Agent Management
- `create_agent` — Create a new agent with email identity
- `list_agents` — List all agents in your organization
- `get_agent` — Get agent details
- `delete_agent` — Remove an agent

### Email
- `send_email` — Send an email from an agent
- `list_messages` / `get_message` — Read inbox messages
- `search_messages` — Full-text and semantic search
- Plus: domains, contacts, spam management, signatures

### Credential Vault
- `provision_vault` — Set up encrypted storage for an agent
- `store_credential` — Save logins, API keys, identities
- `get_credential` / `list_credentials` — Retrieve credentials
- `generate_password` — Create strong random passwords
- Plus: TOTP codes, search, sync

### Phone & SMS
- `provision_phone` — Get a phone number for an agent
- `send_sms` — Send SMS messages
- `list_phones` — List provisioned numbers

### Addresses
- `create_address` — Create billing/shipping/mailing addresses
- `validate_address` — Validate via USPS/provider
- `list_addresses` — List agent addresses

### Webhooks
- `create_webhook` — Subscribe to real-time events
- `webhook_test` — Test webhook delivery
- `list_deliveries` — Inspect delivery logs

### Security
- Content scanning, policy enforcement, event audit logs

## Example Workflows

### 1. Create an agent and send email
```
Create a new agent called "Assistant" → send_email to user@example.com
```

### 2. Store and use credentials
```
provision_vault → store_credential (CRM login) →
get_credential when needed → generate_password for new accounts
```

## Links

- [Documentation](https://docs.useanima.sh)
- [Console](https://console.useanima.sh)
- [GitHub](https://github.com/anima-labs-ai)
- [MCP Server](https://github.com/anima-labs-ai/mcp)
