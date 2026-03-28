---
name: anima
description: "Anima AI agent identity platform: email, virtual cards, phone/SMS, credential vault, addresses, webhooks. Use when: (1) sending or reading emails for agents, (2) creating virtual cards for purchases, (3) storing or retrieving credentials, (4) provisioning phone numbers or sending SMS, (5) managing agent addresses. NOT for: general web browsing (use browser tools), non-agent identity tasks, or direct payment processing outside Anima."
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

Give your OpenClaw agents real-world identity: email addresses, virtual debit cards, phone numbers, encrypted credential storage, and validated addresses.

## When to Use

✅ **USE this skill when:**

- Sending or receiving emails from an AI agent
- Creating virtual cards with spending limits for purchases
- Storing or retrieving login credentials, API keys, or secrets
- Provisioning phone numbers or sending SMS
- Creating and validating billing/shipping addresses
- Managing webhooks for real-time event notifications
- Automating browser checkout with card + address auto-fill

❌ **DO NOT use for:**

- General web browsing (use browser tools)
- Tasks unrelated to agent identity or communication
- Direct payment processing outside the Anima platform

## Setup

1. Get an API key at [console.anima.email](https://console.anima.email)
2. Set `ANIMA_API_KEY` in your environment
3. The MCP server starts automatically when needed

## Available Tools (133+)

### Agent Management
- `create_agent` — Create a new agent with email identity
- `list_agents` — List all agents in your organization
- `get_agent` — Get agent details
- `delete_agent` — Remove an agent

### Email (24 tools)
- `send_email` — Send an email from an agent
- `list_messages` / `get_message` — Read inbox messages
- `search_messages` — Full-text and semantic search
- Plus: domains, contacts, spam management, signatures

### Virtual Cards (18 tools)
- `create_card` — Issue a virtual card with spending limits
- `freeze_card` / `unfreeze_card` — Toggle card status
- `list_transactions` — View card transactions
- Plus: spending policies, approval workflows, auto-approve rules

### Credential Vault (10 tools)
- `provision_vault` — Set up encrypted storage for an agent
- `store_credential` — Save logins, API keys, cards, identities
- `get_credential` / `list_credentials` — Retrieve credentials
- `generate_password` — Create strong random passwords
- Plus: TOTP codes, search, sync

### Phone & SMS (6 tools)
- `provision_phone` — Get a phone number for an agent
- `send_sms` — Send SMS messages
- `list_phones` — List provisioned numbers

### Addresses (6 tools)
- `create_address` — Create billing/shipping/mailing addresses
- `validate_address` — Validate via USPS/provider
- `list_addresses` — List agent addresses

### Webhooks (7 tools)
- `create_webhook` — Subscribe to real-time events
- `webhook_test` — Test webhook delivery
- `list_deliveries` — Inspect delivery logs

### Browser Payments (4 tools)
- `browser_detect_checkout` — Detect checkout forms
- `browser_fill_card` / `browser_fill_address` — Auto-fill payment forms
- `browser_pay_checkout` — Execute checkout

### Security (5 tools)
- Content scanning, policy enforcement, event audit logs

## Example Workflows

### 1. Create an agent and send email
```
Create a new agent called "Assistant" → send_email to user@example.com
```

### 2. Purchase something online
```
create_card with $50 limit → create_address (shipping) →
browser_detect_checkout → browser_fill_card → browser_fill_address →
browser_pay_checkout → freeze_card after purchase
```

### 3. Store and use credentials
```
provision_vault → store_credential (CRM login) →
get_credential when needed → generate_password for new accounts
```

## Links

- [Documentation](https://docs.anima.email)
- [Console](https://console.anima.email)
- [GitHub](https://github.com/anima-labs-ai)
- [MCP Server](https://github.com/anima-labs-ai/mcp)
