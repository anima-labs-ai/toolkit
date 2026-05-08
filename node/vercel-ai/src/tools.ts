import Anima from "@anima-labs/sdk";
import { tool } from "ai";
import { z } from "zod";

function getClient(apiKey?: string): Anima {
	return new Anima({ apiKey: apiKey ?? process.env.ANIMA_API_KEY });
}

export interface AnimaToolsConfig {
	apiKey?: string;
}

export function animaTools(config: AnimaToolsConfig = {}) {
	const client = getClient(config.apiKey);

	return {
		send_email: tool({
			description: "Send an email from an Anima agent inbox",
			parameters: z.object({
				agentId: z.string().describe("The agent whose inbox to send from"),
				to: z.array(z.string()).describe("List of recipient email addresses"),
				subject: z.string().describe("Email subject line"),
				body: z.string().describe("Email body text"),
			}),
			execute: async ({ agentId, to, subject, body }) => {
				const result = await client.messages.sendEmail({
					agentId,
					to,
					subject,
					body,
				});
				return { messageId: result.id, status: "sent" };
			},
		}),

		list_messages: tool({
			description: "List messages in an agent's inbox",
			parameters: z.object({
				agentId: z.string().describe("The agent whose inbox to read"),
				limit: z.number().optional().default(20).describe("Max number of messages"),
			}),
			execute: async ({ agentId, limit }) => {
				const messages = await client.messages.list({ agentId, limit });
				return messages.data.map((m) => ({
					id: m.id,
					from: m.fromAddress,
					subject: m.subject,
					snippet: m.snippet,
					date: m.createdAt,
				}));
			},
		}),

		get_message: tool({
			description: "Get a specific message by ID",
			parameters: z.object({
				agentId: z.string().describe("The agent whose inbox contains the message"),
				messageId: z.string().describe("The message ID to retrieve"),
			}),
			execute: async ({ agentId, messageId }) => {
				const m = await client.messages.get({ agentId, messageId });
				return {
					id: m.id,
					from: m.fromAddress,
					to: m.toAddress,
					subject: m.subject,
					body: m.body,
					date: m.createdAt,
				};
			},
		}),

		search_messages: tool({
			description: "Search messages in an agent's inbox",
			parameters: z.object({
				agentId: z.string().describe("The agent whose inbox to search"),
				query: z.string().describe("Search query string"),
				limit: z.number().optional().default(10).describe("Max number of results"),
			}),
			execute: async ({ agentId, query, limit }) => {
				const results = await client.messages.search({
					agentId,
					query,
					limit,
				});
				return results.data.map((m) => ({
					id: m.id,
					from: m.fromAddress,
					subject: m.subject,
					snippet: m.snippet,
				}));
			},
		}),

		create_agent: tool({
			description: "Create a new Anima agent with an email inbox",
			parameters: z.object({
				name: z.string().describe("Display name for the agent"),
				domain: z.string().optional().describe("Optional custom domain for the agent's email"),
			}),
			execute: async ({ name, domain }) => {
				const agent = await client.agents.create({ name, domain });
				return { id: agent.id, name: agent.name, email: agent.email };
			},
		}),

		list_agents: tool({
			description: "List existing Anima agents",
			parameters: z.object({
				limit: z.number().optional().default(20).describe("Max number of agents"),
			}),
			execute: async ({ limit }) => {
				const agents = await client.agents.list({ limit });
				return agents.data.map((a) => ({
					id: a.id,
					name: a.name,
					email: a.email,
				}));
			},
		}),

		// --- Vault / Credential Management ---

		provision_vault: tool({
			description: "Provision an encrypted credential vault for an agent",
			parameters: z.object({
				agentId: z.string().describe("The agent to provision a vault for"),
			}),
			execute: async ({ agentId }) => {
				await client.vault.provision({ agentId });
				return { agentId, status: "provisioned" };
			},
		}),

		store_credential: tool({
			description: "Store an encrypted credential in the agent's vault",
			parameters: z.object({
				agentId: z.string().describe("The agent whose vault to store in"),
				name: z.string().describe("Name/label for the credential"),
				type: z.enum(["login", "secure_note", "card", "identity"]).describe("Credential type"),
				username: z.string().optional().describe("Username (for login type)"),
				password: z.string().optional().describe("Password (for login type)"),
				uris: z.array(z.string()).optional().describe("Associated URIs"),
				notes: z.string().optional().describe("Free-form notes"),
			}),
			execute: async ({ agentId, name, type, ...rest }) => {
				const cred = await client.vault.createCredential({ agentId, name, type, ...rest });
				return { id: cred.id, name: cred.name, type: cred.type };
			},
		}),

		get_credential: tool({
			description: "Retrieve a credential from the agent's vault",
			parameters: z.object({
				agentId: z.string().describe("The agent whose vault to read from"),
				credentialId: z.string().describe("The credential ID to retrieve"),
			}),
			execute: async ({ agentId, credentialId }) => {
				const cred = await client.vault.getCredential({ agentId, credentialId });
				return { id: cred.id, name: cred.name, type: cred.type, username: cred.username };
			},
		}),

		list_credentials: tool({
			description: "List all credentials in the agent's vault",
			parameters: z.object({
				agentId: z.string().describe("The agent whose vault to list"),
			}),
			execute: async ({ agentId }) => {
				const creds = await client.vault.list({ agentId });
				return creds.map((c) => ({ id: c.id, name: c.name, type: c.type }));
			},
		}),

		generate_password: tool({
			description: "Generate a strong random password",
			parameters: z.object({
				length: z.number().optional().default(20).describe("Password length"),
			}),
			execute: async ({ length }) => {
				const result = await client.vault.generatePassword({ length });
				return { password: result.value };
			},
		}),

		// --- Phone / SMS ---

		provision_phone: tool({
			description: "Provision a phone number for an agent",
			parameters: z.object({
				agentId: z.string().describe("The agent to provision a phone for"),
				number: z.string().describe("Phone number to provision (E.164 format)"),
			}),
			execute: async ({ agentId, number }) => {
				const phone = await client.phone.provision({ agentId, number });
				return { number: phone.number, status: phone.status };
			},
		}),

		send_sms: tool({
			description: "Send an SMS message from an agent's phone number",
			parameters: z.object({
				agentId: z.string().describe("The agent to send SMS from"),
				to: z.string().describe("Recipient phone number (E.164 format)"),
				body: z.string().describe("SMS message text"),
			}),
			execute: async ({ agentId, to, body }) => {
				const msg = await client.phone.sendSms({ agentId, to, body });
				return { messageId: msg.id, status: "sent" };
			},
		}),

		list_phones: tool({
			description: "List phone numbers provisioned for an agent",
			parameters: z.object({
				agentId: z.string().describe("The agent whose phone numbers to list"),
			}),
			execute: async ({ agentId }) => {
				const phones = await client.phone.list({ agentId });
				return phones.data.map((p) => ({ number: p.number, status: p.status }));
			},
		}),

		// --- Address Management ---

		create_address: tool({
			description: "Create a billing, shipping, or mailing address for an agent",
			parameters: z.object({
				agentId: z.string().describe("The agent to create the address for"),
				type: z.enum(["BILLING", "SHIPPING", "MAILING", "REGISTERED"]).describe("Address type"),
				street1: z.string().describe("Street address line 1"),
				street2: z.string().optional().describe("Street address line 2"),
				city: z.string().describe("City"),
				state: z.string().describe("State/province"),
				postalCode: z.string().describe("Postal/ZIP code"),
				country: z.string().length(2).describe("ISO 3166-1 alpha-2 country code"),
				label: z.string().optional().describe("Optional label (e.g. 'Office')"),
			}),
			execute: async ({ agentId, type, street1, city, state, postalCode, country, ...rest }) => {
				const addr = await client.addresses.create({
					agentId, type, street1, city, state, postalCode, country, ...rest,
				});
				return {
					id: addr.id, type: addr.type, street1: addr.street1,
					city: addr.city, state: addr.state, country: addr.country,
					validated: addr.validated,
				};
			},
		}),

		list_addresses: tool({
			description: "List addresses for an agent",
			parameters: z.object({
				agentId: z.string().describe("The agent whose addresses to list"),
				type: z.enum(["BILLING", "SHIPPING", "MAILING", "REGISTERED"]).optional().describe("Filter by type"),
			}),
			execute: async ({ agentId, type }) => {
				const addrs = await client.addresses.list({ agentId, type });
				return addrs.data.map((a) => ({
					id: a.id, type: a.type, street1: a.street1,
					city: a.city, state: a.state, country: a.country,
					validated: a.validated,
				}));
			},
		}),

		validate_address: tool({
			description: "Validate and standardize an agent's address via USPS/provider",
			parameters: z.object({
				agentId: z.string().describe("The agent who owns the address"),
				addressId: z.string().describe("The address ID to validate"),
			}),
			execute: async ({ agentId, addressId }) => {
				const result = await client.addresses.validate({ agentId, addressId });
				return { valid: result.valid, confidence: result.confidence };
			},
		}),
	};
}
