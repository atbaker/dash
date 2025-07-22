<script lang="ts">
	import MessageList from '$lib/components/MessageList.svelte';
	import ChatInput from '$lib/components/ChatInput.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import NewConversationButton from '$lib/components/NewConversationButton.svelte';
	import { Card } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import { chatStore } from '$lib/stores/chat.js';

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
					content: 'Hello! I\'m DASH, your AI business intelligence assistant for Gator. I can help you Gator\'s usage data, research new users, and qualify promising customers as leads. Try asking about recent workspace installs, user growth metrics, or industry insights to get started!',
					timestamp: new Date()
				});
			}
		});
	});
</script>

<svelte:head>
	<title>DASH Chat - AI Assistant</title>
	<meta name="description" content="Chat with your AI assistant powered by DigitalOcean GradientAI" />
</svelte:head>

<div class="min-h-screen bg-gray-50 dark:bg-gray-900">
	<div class="max-w-4xl mx-auto py-4 md:py-8 px-4">
		<!-- Header -->
		<div class="relative text-center mb-6 md:mb-8">
			<!-- Theme toggle in top right -->
			<div class="absolute top-0 right-0">
				<ThemeToggle />
			</div>
			
			<h1 class="text-3xl md:text-4xl font-bold text-blue-600 dark:text-blue-400 mb-3">DASH Chat</h1>
			<p class="text-gray-600 dark:text-gray-400 text-base md:text-lg leading-relaxed max-w-2xl mx-auto px-4">
				Chat with your AI assistant powered by DigitalOcean GradientAI
			</p>
		</div>
		
		<!-- New Conversation Button -->
		<div class="flex justify-start mb-6">
			<NewConversationButton />
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
		

		<!-- Footer -->
		<div class="text-center text-sm text-gray-500 dark:text-gray-400 pt-8 border-t border-gray-200 dark:border-gray-700">
			<p>Powered by DigitalOcean GradientAI</p>
		</div>
	</div>
</div>