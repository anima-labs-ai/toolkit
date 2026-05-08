/**
 * @anima-labs/opencode-plugin
 *
 * Anima plugin for OpenCode — gives agents real-world identity:
 * email, phone/SMS, credential vault, and addresses.
 */

import type { Plugin } from "@opencode-ai/plugin";
import { tool } from "@opencode-ai/plugin";
import { Anima } from "@anima-labs/sdk";

export const animaPlugin: Plugin = async (ctx) => {
	const apiKey = process.env.ANIMA_API_KEY;
	if (!apiKey) {
		throw new Error("ANIMA_API_KEY environment variable is required");
	}

	const anima = new Anima({ apiKey });

	return {
		tool: {
			// --- Agent ---
			create_agent: tool({
				description: "Create a new Anima AI agent with an email inbox",
				args: {
					name: tool.schema.string().describe("Display name for the agent"),
					domain: tool.schema.string().optional().describe("Optional custom domain"),
				},
				async execute(args) {
					const agent = await anima.agents.create({ name: args.name, domain: args.domain });
					return JSON.stringify(agent, null, 2);
				},
			}),

			list_agents: tool({
				description: "List existing Anima agents",
				args: {
					limit: tool.schema.number().optional().describe("Max agents to return"),
				},
				async execute(args) {
					const agents = await anima.agents.list({ limit: args.limit });
					return JSON.stringify(agents, null, 2);
				},
			}),

			// --- Email ---
			send_email: tool({
				description: "Send an email from an Anima agent inbox",
				args: {
					agent_id: tool.schema.string().describe("Agent whose inbox to send from"),
					to: tool.schema.string().describe("Comma-separated recipient emails"),
					subject: tool.schema.string().describe("Email subject"),
					body: tool.schema.string().describe("Email body (plain text or HTML)"),
				},
				async execute(args) {
					const result = await useanima.shs.send({
						agentId: args.agent_id,
						to: args.to.split(",").map((e) => e.trim()),
						subject: args.subject,
						body: args.body,
					});
					return JSON.stringify(result, null, 2);
				},
			}),

			list_messages: tool({
				description: "List messages in an agent's inbox",
				args: {
					agent_id: tool.schema.string().describe("Agent whose inbox to read"),
					limit: tool.schema.number().optional().describe("Max messages to return"),
				},
				async execute(args) {
					const messages = await anima.messages.list({
						agentId: args.agent_id,
						limit: args.limit,
					});
					return JSON.stringify(messages, null, 2);
				},
			}),

			search_messages: tool({
				description: "Search messages in an agent's inbox",
				args: {
					agent_id: tool.schema.string().describe("Agent whose inbox to search"),
					query: tool.schema.string().describe("Search query"),
					limit: tool.schema.number().optional().describe("Max results"),
				},
				async execute(args) {
					const results = await anima.messages.search({
						agentId: args.agent_id,
						query: args.query,
						limit: args.limit,
					});
					return JSON.stringify(results, null, 2);
				},
			}),

			// --- Vault ---
			provision_vault: tool({
				description: "Provision an encrypted credential vault for an agent",
				args: {
					agent_id: tool.schema.string().describe("Agent to provision vault for"),
				},
				async execute(args) {
					const vault = await anima.vault.provision({ agentId: args.agent_id });
					return JSON.stringify(vault, null, 2);
				},
			}),

			store_credential: tool({
				description: "Store an encrypted credential in the agent's vault",
				args: {
					agent_id: tool.schema.string().describe("Agent whose vault to store in"),
					name: tool.schema.string().describe("Credential name/label"),
					type: tool.schema.enum(["login", "secure_note", "card", "identity"]).describe("Credential type"),
					username: tool.schema.string().optional().describe("Username (login type)"),
					password: tool.schema.string().optional().describe("Password (login type)"),
					uris: tool.schema.string().optional().describe("Comma-separated URIs"),
					notes: tool.schema.string().optional().describe("Free-form notes"),
				},
				async execute(args) {
					const cred = await anima.vault.storeCredential({
						agentId: args.agent_id,
						name: args.name,
						type: args.type,
						username: args.username,
						password: args.password,
						uris: args.uris?.split(",").map((u) => u.trim()),
						notes: args.notes,
					});
					return JSON.stringify(cred, null, 2);
				},
			}),

			get_credential: tool({
				description: "Retrieve a credential from the agent's vault",
				args: {
					agent_id: tool.schema.string().describe("Agent whose vault to read"),
					credential_id: tool.schema.string().describe("Credential ID"),
				},
				async execute(args) {
					const cred = await anima.vault.getCredential(args.agent_id, args.credential_id);
					return JSON.stringify(cred, null, 2);
				},
			}),

			list_credentials: tool({
				description: "List all credentials in the agent's vault",
				args: {
					agent_id: tool.schema.string().describe("Agent whose vault to list"),
				},
				async execute(args) {
					const creds = await anima.vault.listCredentials({ agentId: args.agent_id });
					return JSON.stringify(creds, null, 2);
				},
			}),

			generate_password: tool({
				description: "Generate a strong random password",
				args: {
					length: tool.schema.number().optional().describe("Password length (default 20)"),
				},
				async execute(args) {
					const result = await anima.vault.generatePassword({ length: args.length });
					return JSON.stringify(result, null, 2);
				},
			}),

			// --- Phone / SMS ---
			provision_phone: tool({
				description: "Provision a phone number for an agent",
				args: {
					agent_id: tool.schema.string().describe("Agent to provision phone for"),
				},
				async execute(args) {
					const phone = await anima.phones.provision({ agentId: args.agent_id });
					return JSON.stringify(phone, null, 2);
				},
			}),

			send_sms: tool({
				description: "Send an SMS message from an agent's phone number",
				args: {
					agent_id: tool.schema.string().describe("Agent to send from"),
					to: tool.schema.string().describe("Recipient phone (E.164)"),
					body: tool.schema.string().describe("SMS text"),
				},
				async execute(args) {
					const result = await anima.phones.sendSms({
						agentId: args.agent_id,
						to: args.to,
						body: args.body,
					});
					return JSON.stringify(result, null, 2);
				},
			}),

			list_phones: tool({
				description: "List phone numbers for an agent",
				args: {
					agent_id: tool.schema.string().describe("Agent whose phones to list"),
				},
				async execute(args) {
					const phones = await anima.phones.list({ agentId: args.agent_id });
					return JSON.stringify(phones, null, 2);
				},
			}),

			// --- Address ---
			create_address: tool({
				description: "Create a billing, shipping, or mailing address for an agent",
				args: {
					agent_id: tool.schema.string().describe("Agent to create address for"),
					type: tool.schema.enum(["BILLING", "SHIPPING", "MAILING", "REGISTERED"]).describe("Address type"),
					street1: tool.schema.string().describe("Street line 1"),
					street2: tool.schema.string().optional().describe("Street line 2"),
					city: tool.schema.string().describe("City"),
					state: tool.schema.string().describe("State/province"),
					postal_code: tool.schema.string().describe("ZIP/postal code"),
					country: tool.schema.string().describe("ISO 3166-1 alpha-2 (e.g. US)"),
					label: tool.schema.string().optional().describe("Optional label"),
				},
				async execute(args) {
					const address = await anima.addresses.create({
						agentId: args.agent_id,
						type: args.type,
						street1: args.street1,
						street2: args.street2,
						city: args.city,
						state: args.state,
						postalCode: args.postal_code,
						country: args.country,
						label: args.label,
					});
					return JSON.stringify(address, null, 2);
				},
			}),

			list_addresses: tool({
				description: "List addresses for an agent",
				args: {
					agent_id: tool.schema.string().describe("Agent whose addresses to list"),
					type: tool.schema.enum(["BILLING", "SHIPPING", "MAILING", "REGISTERED"]).optional().describe("Filter by type"),
				},
				async execute(args) {
					const addresses = await anima.addresses.list({
						agentId: args.agent_id,
						type: args.type,
					});
					return JSON.stringify(addresses, null, 2);
				},
			}),

			validate_address: tool({
				description: "Validate and standardize an address via USPS/provider",
				args: {
					agent_id: tool.schema.string().describe("Agent who owns the address"),
					address_id: tool.schema.string().describe("Address ID to validate"),
				},
				async execute(args) {
					const result = await anima.addresses.validate(args.address_id, {
						agentId: args.agent_id,
					});
					return JSON.stringify(result, null, 2);
				},
			}),
		},
	};
};

export default animaPlugin;
