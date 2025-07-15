<script lang="ts">
	import MessageList from '$lib/components/MessageList.svelte';
	import ChatInput from '$lib/components/ChatInput.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import NewConversationButton from '$lib/components/NewConversationButton.svelte';
	import { Card } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import { chatStore } from '$lib/stores/chat.js';
	import { Database, Search } from 'lucide-svelte';

	// Add welcome message on component mount if no messages exist
	onMount(() => {
		// Use get to check current state without subscribing
		import('svelte/store').then(({ get }) => {
			const currentState = get(chatStore);
			if (currentState.messages.length === 0) {
				// Add a welcome message only if chat is completely empty
				chatStore.addMessage({
					id: crypto.randomUUID(),
					role: 'assistant',
					content: 'Hello! I\'m DASH, your AI assistant. I can help you with business data and web searches. What would you like to know?',
					timestamp: new Date()
				});
			}
		});
	});
</script>

<svelte:head>
	<title>DASH Chat - AI Assistant</title>
	<meta name="description" content="Chat with your AI assistant powered by DigitalOcean's GenAI Platform" />
</svelte:head>

<div class="min-h-screen bg-gray-50 dark:bg-gray-900">
	<div class="max-w-4xl mx-auto py-4 md:py-8 px-4">
		<!-- Header -->
		<div class="relative text-center mb-6 md:mb-8">
			<!-- Top Controls -->
			<div class="absolute top-0 left-0">
				<NewConversationButton />
			</div>
			<div class="absolute top-0 right-0">
				<ThemeToggle />
			</div>
			
			<h1 class="text-3xl md:text-4xl font-bold text-blue-600 dark:text-blue-400 mb-3">DASH Chat</h1>
			<p class="text-gray-600 dark:text-gray-400 text-base md:text-lg leading-relaxed max-w-2xl mx-auto px-4">
				Chat with your AI assistant powered by DigitalOcean's GenAI Platform
			</p>
		</div>
		
		<!-- Chat Interface -->
		<Card class="!w-full !max-w-none mb-8 md:mb-12 flex flex-col h-[500px] md:h-[600px] shadow-lg">
			<div class="flex-1 overflow-hidden">
				<MessageList />
			</div>
			<div class="border-t border-gray-200 dark:border-gray-700">
				<ChatInput />
			</div>
		</Card>
		
		<!-- Features -->
		<div class="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8 mb-8 md:mb-12">
			<Card class="!w-full !max-w-none h-full shadow-md hover:shadow-lg transition-shadow">
				<div class="flex items-start space-x-4 p-2">
					<div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center dark:bg-blue-900 flex-shrink-0">
						<Database class="w-6 h-6 text-blue-600 dark:text-blue-300" />
					</div>
					<div>
						<h5 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Business Data</h5>
						<p class="text-gray-700 dark:text-gray-400 leading-relaxed">Ask about workspaces, users, or any data in your Gator database.</p>
					</div>
				</div>
			</Card>
			
			<Card class="!w-full !max-w-none h-full shadow-md hover:shadow-lg transition-shadow">
				<div class="flex items-start space-x-4 p-2">
					<div class="w-12 h-12 bg-teal-100 rounded-xl flex items-center justify-center dark:bg-teal-900 flex-shrink-0">
						<Search class="w-6 h-6 text-teal-600 dark:text-teal-300" />
					</div>
					<div>
						<h5 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Web Search</h5>
						<p class="text-gray-700 dark:text-gray-400 leading-relaxed">Search the web for the latest information and news.</p>
					</div>
				</div>
			</Card>
		</div>

		<!-- Footer -->
		<div class="text-center text-sm text-gray-500 dark:text-gray-400 pt-8 border-t border-gray-200 dark:border-gray-700">
			<p>Powered by DigitalOcean's GenAI Platform</p>
		</div>
	</div>
</div>