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

		create_card: tool({
			description: "Create a virtual card for an agent",
			parameters: z.object({
				agentId: z.string().describe("The agent to create the card for"),
				amountCents: z.number().describe("Funding amount in cents (e.g. 1000 = $10.00)"),
			}),
			execute: async ({ agentId, amountCents }) => {
				const card = await client.cards.create({ agentId, amountCents });
				return {
					id: card.id,
					last4: card.last4,
					amountCents: card.amountCents,
					status: card.status,
				};
			},
		}),

		list_cards: tool({
			description: "List virtual cards for an agent",
			parameters: z.object({
				agentId: z.string().describe("The agent whose cards to list"),
			}),
			execute: async ({ agentId }) => {
				const cards = await client.cards.list({ agentId });
				return cards.data.map((c) => ({
					id: c.id,
					last4: c.last4,
					status: c.status,
				}));
			},
		}),
	};
}
