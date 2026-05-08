/**
 * @anima-labs/toolkit-codex
 *
 * Anima tool definitions for OpenAI Codex and any OpenAI-compatible
 * function-calling agent. Covers the full unified surface: email,
 * vault, phone, and address.
 */

import type { ChatCompletionTool } from "openai/resources/chat/completions";

export const animaTools: ChatCompletionTool[] = [
	// --- Agent ---
	{
		type: "function",
		function: {
			name: "create_agent",
			description: "Create a new Anima AI agent with an email inbox",
			parameters: {
				type: "object",
				properties: {
					name: { type: "string", description: "Display name for the agent" },
					domain: { type: "string", description: "Optional custom domain" },
				},
				required: ["name"],
			},
		},
	},
	{
		type: "function",
		function: {
			name: "list_agents",
			description: "List existing Anima agents",
			parameters: {
				type: "object",
				properties: {
					limit: { type: "number", description: "Max agents to return", default: 20 },
				},
			},
		},
	},

	// --- Email ---
	{
		type: "function",
		function: {
			name: "send_email",
			description: "Send an email from an Anima agent inbox",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent whose inbox to send from" },
					to: { type: "array", items: { type: "string" }, description: "Recipient emails" },
					subject: { type: "string", description: "Email subject" },
					body: { type: "string", description: "Email body" },
				},
				required: ["agent_id", "to", "subject", "body"],
			},
		},
	},
	{
		type: "function",
		function: {
			name: "list_messages",
			description: "List messages in an agent's inbox",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent whose inbox to read" },
					limit: { type: "number", description: "Max messages", default: 20 },
				},
				required: ["agent_id"],
			},
		},
	},
	{
		type: "function",
		function: {
			name: "search_messages",
			description: "Search messages in an agent's inbox",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent whose inbox to search" },
					query: { type: "string", description: "Search query" },
					limit: { type: "number", description: "Max results", default: 10 },
				},
				required: ["agent_id", "query"],
			},
		},
	},

	// --- Vault ---
	{
		type: "function",
		function: {
			name: "provision_vault",
			description: "Provision an encrypted credential vault for an agent",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent to provision vault for" },
				},
				required: ["agent_id"],
			},
		},
	},
	{
		type: "function",
		function: {
			name: "store_credential",
			description: "Store an encrypted credential in the agent's vault",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent whose vault to store in" },
					name: { type: "string", description: "Credential name/label" },
					type: { type: "string", enum: ["login", "secure_note", "card", "identity"], description: "Credential type" },
					username: { type: "string", description: "Username (login type)" },
					password: { type: "string", description: "Password (login type)" },
					uris: { type: "array", items: { type: "string" }, description: "Associated URIs" },
					notes: { type: "string", description: "Free-form notes" },
				},
				required: ["agent_id", "name", "type"],
			},
		},
	},
	{
		type: "function",
		function: {
			name: "get_credential",
			description: "Retrieve a credential from the agent's vault",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent whose vault to read" },
					credential_id: { type: "string", description: "Credential ID" },
				},
				required: ["agent_id", "credential_id"],
			},
		},
	},
	{
		type: "function",
		function: {
			name: "list_credentials",
			description: "List all credentials in the agent's vault",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent whose vault to list" },
				},
				required: ["agent_id"],
			},
		},
	},
	{
		type: "function",
		function: {
			name: "generate_password",
			description: "Generate a strong random password",
			parameters: {
				type: "object",
				properties: {
					length: { type: "number", description: "Password length", default: 20 },
				},
			},
		},
	},

	// --- Phone / SMS ---
	{
		type: "function",
		function: {
			name: "provision_phone",
			description: "Provision a phone number for an agent",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent to provision phone for" },
					number: { type: "string", description: "Phone number (E.164 format)" },
				},
				required: ["agent_id", "number"],
			},
		},
	},
	{
		type: "function",
		function: {
			name: "send_sms",
			description: "Send an SMS message from an agent's phone number",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent to send from" },
					to: { type: "string", description: "Recipient phone (E.164)" },
					body: { type: "string", description: "SMS text" },
				},
				required: ["agent_id", "to", "body"],
			},
		},
	},
	{
		type: "function",
		function: {
			name: "list_phones",
			description: "List phone numbers for an agent",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent whose phones to list" },
				},
				required: ["agent_id"],
			},
		},
	},

	// --- Address ---
	{
		type: "function",
		function: {
			name: "create_address",
			description: "Create a billing, shipping, or mailing address for an agent",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent to create address for" },
					type: { type: "string", enum: ["BILLING", "SHIPPING", "MAILING", "REGISTERED"], description: "Address type" },
					street1: { type: "string", description: "Street line 1" },
					street2: { type: "string", description: "Street line 2" },
					city: { type: "string", description: "City" },
					state: { type: "string", description: "State/province" },
					postal_code: { type: "string", description: "ZIP/postal code" },
					country: { type: "string", description: "ISO 3166-1 alpha-2 (e.g. US)" },
					label: { type: "string", description: "Optional label" },
				},
				required: ["agent_id", "type", "street1", "city", "state", "postal_code", "country"],
			},
		},
	},
	{
		type: "function",
		function: {
			name: "list_addresses",
			description: "List addresses for an agent",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent whose addresses to list" },
					type: { type: "string", enum: ["BILLING", "SHIPPING", "MAILING", "REGISTERED"], description: "Filter by type" },
				},
				required: ["agent_id"],
			},
		},
	},
	{
		type: "function",
		function: {
			name: "validate_address",
			description: "Validate and standardize an address via USPS/provider",
			parameters: {
				type: "object",
				properties: {
					agent_id: { type: "string", description: "Agent who owns the address" },
					address_id: { type: "string", description: "Address ID to validate" },
				},
				required: ["agent_id", "address_id"],
			},
		},
	},
];

/**
 * Get all Anima tool definitions for use with OpenAI function calling.
 *
 * Usage with OpenAI:
 * ```ts
 * import { animaTools } from "@anima-labs/toolkit-codex";
 * const response = await openai.chat.completions.create({
 *   model: "gpt-4o",
 *   messages: [...],
 *   tools: animaTools,
 * });
 * ```
 */
export function getAnimaTools(): ChatCompletionTool[] {
	return animaTools;
}
