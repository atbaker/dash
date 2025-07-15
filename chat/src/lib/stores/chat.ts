import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

export interface ChatMessage {
	id: string;
	role: 'user' | 'assistant';
	content: string;
	timestamp: Date;
	streaming?: boolean;
}

export interface ChatState {
	messages: ChatMessage[];
	isStreaming: boolean;
	isConnected: boolean;
	currentStreamingId: string | null;
}

// Storage key for persisting chat history
const STORAGE_KEY = 'dash-chat-history';

// Load initial state from localStorage
function loadInitialState(): ChatState {
	if (browser) {
		try {
			const stored = localStorage.getItem(STORAGE_KEY);
			if (stored) {
				const parsed = JSON.parse(stored);
				// Convert timestamp strings back to Date objects
				const messages = parsed.messages.map((msg: any) => ({
					...msg,
					timestamp: new Date(msg.timestamp)
				}));
				return {
					messages,
					isStreaming: false,
					isConnected: false,
					currentStreamingId: null
				};
			}
		} catch (error) {
			console.warn('Failed to load chat history from localStorage:', error);
		}
	}
	
	return {
		messages: [],
		isStreaming: false,
		isConnected: false,
		currentStreamingId: null
	};
}

// Save state to localStorage
function saveToStorage(state: ChatState) {
	if (browser) {
		try {
			// Only save completed messages (not streaming state)
			const persistState = {
				messages: state.messages.filter(msg => !msg.streaming)
			};
			localStorage.setItem(STORAGE_KEY, JSON.stringify(persistState));
		} catch (error) {
			console.warn('Failed to save chat history to localStorage:', error);
		}
	}
}

// Create the main chat store
function createChatStore() {
	const { subscribe, update, set } = writable<ChatState>(loadInitialState());

	return {
		subscribe,
		
		// Add any message
		addMessage: (message: ChatMessage) => {
			update(state => {
				const newState = {
					...state,
					messages: [...state.messages, message]
				};
				saveToStorage(newState);
				return newState;
			});
		},

		// Add a user message
		addUserMessage: (content: string) => {
			const message: ChatMessage = {
				id: crypto.randomUUID(),
				role: 'user',
				content,
				timestamp: new Date()
			};
			
			update(state => {
				const newState = {
					...state,
					messages: [...state.messages, message]
				};
				saveToStorage(newState);
				return newState;
			});
			
			return message.id;
		},
		
		// Start streaming an assistant message
		startAssistantMessage: () => {
			const messageId = crypto.randomUUID();
			const message: ChatMessage = {
				id: messageId,
				role: 'assistant',
				content: '',
				timestamp: new Date(),
				streaming: true
			};
			
			update(state => ({
				...state,
				messages: [...state.messages, message],
				isStreaming: true,
				currentStreamingId: messageId
			}));
			
			return messageId;
		},
		
		// Append content to the streaming message
		appendStreamingContent: (content: string) => {
			update(state => {
				if (!state.currentStreamingId) return state;
				
				const updatedMessages = state.messages.map(msg => 
					msg.id === state.currentStreamingId 
						? { ...msg, content: msg.content + content }
						: msg
				);
				
				return {
					...state,
					messages: updatedMessages
				};
			});
		},
		
		// Complete the streaming message
		completeStreaming: () => {
			update(state => {
				const updatedMessages = state.messages.map(msg => 
					msg.id === state.currentStreamingId 
						? { ...msg, streaming: false }
						: msg
				);
				
				const newState = {
					...state,
					messages: updatedMessages,
					isStreaming: false,
					currentStreamingId: null
				};
				
				// Save to storage when message is completed
				saveToStorage(newState);
				return newState;
			});
		},
		
		// Add an error message
		addErrorMessage: (error: string) => {
			const message: ChatMessage = {
				id: crypto.randomUUID(),
				role: 'assistant',
				content: `Sorry, there was an error: ${error}`,
				timestamp: new Date()
			};
			
			update(state => {
				const newState = {
					...state,
					messages: [...state.messages, message],
					isStreaming: false,
					currentStreamingId: null
				};
				saveToStorage(newState);
				return newState;
			});
		},
		
		// Set connection status
		setConnected: (connected: boolean) => {
			update(state => ({ ...state, isConnected: connected }));
		},
		
		// Clear all messages
		clearMessages: () => {
			// First clear everything
			const clearedState = {
				messages: [],
				isStreaming: false,
				isConnected: false,
				currentStreamingId: null
			};
			
			// Then add a fresh welcome message
			const welcomeMessage: ChatMessage = {
				id: crypto.randomUUID(),
				role: 'assistant',
				content: 'Hello! I\'m DASH, your AI assistant. I can help you with business data and web searches. What would you like to know?',
				timestamp: new Date()
			};
			
			const newState = {
				...clearedState,
				messages: [welcomeMessage]
			};
			
			set(newState);
			saveToStorage(newState);
		}
	};
}

export const chatStore = createChatStore();

// Derived store for the current streaming message
export const currentStreamingMessage = derived(
	chatStore,
	$chatStore => $chatStore.messages.find(msg => msg.id === $chatStore.currentStreamingId)
);

// Derived store for non-streaming messages
export const completedMessages = derived(
	chatStore,
	$chatStore => $chatStore.messages.filter(msg => !msg.streaming)
);