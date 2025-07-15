import { chatStore } from '../stores/chat.js';
import { browser } from '$app/environment';
import { get } from 'svelte/store';

// Get API base URL from environment
const API_BASE_URL = browser 
	? import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
	: 'http://localhost:8000';

export interface StreamingResponse {
	content?: string;
	error?: string;
	complete?: boolean;
}

export class ChatAPI {
	private controller: AbortController | null = null;

	/**
	 * Send a message and handle streaming response
	 */
	async sendMessage(message: string): Promise<void> {
		// Cancel any existing request
		this.cancelRequest();
		this.controller = new AbortController();

		try {
			// Add user message to store
			chatStore.addUserMessage(message);
			
			// Start streaming assistant message
			const streamingId = chatStore.startAssistantMessage();
			chatStore.setConnected(true);

			// Get conversation history from store
			const history = this.getConversationHistory();

			// Make request to streaming endpoint
			const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ message, history }),
				signal: this.controller.signal
			});

			if (!response.ok) {
				throw new Error(`HTTP ${response.status}: ${response.statusText}`);
			}

			if (!response.body) {
				throw new Error('No response body received');
			}

			// Process streaming response
			await this.processStream(response.body);

		} catch (error) {
			console.error('Chat API error:', error);
			
			if (error instanceof Error) {
				if (error.name === 'AbortError') {
					// Request was cancelled, don't show error
					return;
				}
				chatStore.addErrorMessage(error.message);
			} else {
				chatStore.addErrorMessage('An unknown error occurred');
			}
		} finally {
			chatStore.completeStreaming();
			chatStore.setConnected(false);
			this.controller = null;
		}
	}

	/**
	 * Process the streaming response body
	 */
	private async processStream(body: ReadableStream<Uint8Array>): Promise<void> {
		const reader = body.getReader();
		const decoder = new TextDecoder();
		let buffer = '';

		console.log('Starting stream processing...');

		try {
			while (true) {
				const { done, value } = await reader.read();
				
				if (done) {
					console.log('Stream done');
					break;
				}

				// Decode chunk and add to buffer
				const chunk = decoder.decode(value, { stream: true });
				console.log('Received chunk:', chunk);
				buffer += chunk;

				// Process complete lines
				const lines = buffer.split('\n');
				buffer = lines.pop() || ''; // Keep incomplete line in buffer

				console.log('Processing lines:', lines);
				for (const line of lines) {
					await this.processStreamLine(line);
				}
			}

			// Process any remaining buffer content
			if (buffer.trim()) {
				console.log('Processing remaining buffer:', buffer);
				await this.processStreamLine(buffer);
			}

		} finally {
			reader.releaseLock();
		}
	}

	/**
	 * Process a single line from the stream
	 */
	private async processStreamLine(line: string): Promise<void> {
		const trimmed = line.trim();
		if (!trimmed) return;

		try {
			// Try to parse as JSON
			const data: StreamingResponse = JSON.parse(trimmed);
			
			if (data.error) {
				throw new Error(data.error);
			}
			
			if (data.content) {
				chatStore.appendStreamingContent(data.content);
			}
			
			if (data.complete) {
				chatStore.completeStreaming();
			}
			
		} catch (parseError) {
			// Log parse errors for debugging
			console.warn('Failed to parse JSON line:', trimmed, parseError);
			
			// If not valid JSON, treat as raw content
			if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
				// Looks like malformed JSON, skip it
				return;
			}
			
			// Treat as raw text content
			chatStore.appendStreamingContent(trimmed);
		}
	}

	/**
	 * Cancel the current request
	 */
	cancelRequest(): void {
		if (this.controller) {
			this.controller.abort();
			this.controller = null;
		}
	}

	/**
	 * Get conversation history from store in OpenAI format
	 */
	private getConversationHistory(): Array<{role: 'user' | 'assistant', content: string}> {
		// Get current store state
		const storeValue = get(chatStore);

		// Convert completed messages to OpenAI format
		const history: Array<{role: 'user' | 'assistant', content: string}> = [];
		
		// Only include completed messages (not currently streaming ones)
		const completedMessages = storeValue.messages.filter((msg: any) => !msg.streaming);
		
		for (const message of completedMessages) {
			history.push({
				role: message.role,
				content: message.content
			});
		}

		return history;
	}

	/**
	 * Clear conversation history
	 */
	clearConversation(): void {
		chatStore.clearMessages();
	}

	/**
	 * Check if currently streaming
	 */
	get isStreaming(): boolean {
		return this.controller !== null;
	}
}

// Export singleton instance
export const chatAPI = new ChatAPI();