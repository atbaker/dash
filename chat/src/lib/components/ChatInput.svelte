<script lang="ts">
	import { onMount } from 'svelte';
	import { chatAPI } from '../api/chat.js';
	import { chatStore } from '../stores/chat.js';
	import { Send, Loader2 } from 'lucide-svelte';

	let message = $state('');
	let inputElement: HTMLTextAreaElement;
	
	// Subscribe to chat state
	const isStreaming = $derived($chatStore.isStreaming);
	const isConnected = $derived($chatStore.isConnected);

	// Handle form submission
	async function handleSubmit(event: Event) {
		event.preventDefault();
		
		const trimmedMessage = message.trim();
		if (!trimmedMessage || isStreaming) {
			return;
		}

		// Clear input immediately
		const messageToSend = trimmedMessage;
		message = '';

		try {
			await chatAPI.sendMessage(messageToSend);
		} catch (error) {
			console.error('Failed to send message:', error);
		}

		// Focus input after sending
		if (inputElement) {
			inputElement.focus();
		}
	}

	// Handle key press for submit on Enter (but not Shift+Enter)
	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			handleSubmit(event);
		}
	}

	// Set up event listener after component mounts
	onMount(() => {
		if (inputElement) {
			inputElement.addEventListener('keydown', (e) => {
				if (e.key === 'Enter' && !e.shiftKey) {
					e.preventDefault();
					handleSubmit(e);
				}
			});
		}
	});

	// Auto-resize textarea based on content
	function autoResize(element: HTMLTextAreaElement) {
		element.style.height = 'auto';
		element.style.height = Math.min(element.scrollHeight, 120) + 'px';
	}

	// Handle input changes
	function handleInput(event: Event) {
		const target = event.target as HTMLTextAreaElement;
		autoResize(target);
	}
</script>

<div class="p-6">
	<form onsubmit={handleSubmit} class="flex items-end gap-3">
		<textarea
			bind:this={inputElement}
			bind:value={message}
			oninput={handleInput}
			onkeydown={handleKeyDown}
			placeholder="Type here..."
			disabled={isStreaming}
			rows="1"
			class="flex-1 resize-none border border-gray-300 rounded-lg px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-gray-50 transition-colors shadow-sm h-12 scrollbar-hide"
		></textarea>
		<button
			type="submit"
			disabled={!message.trim() || isStreaming}
			class="inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed disabled:text-gray-500 text-white font-medium px-6 py-3 rounded-lg transition-all duration-200 shadow-sm hover:shadow-md h-12 flex-shrink-0"
		>
			{#if isStreaming}
				<Loader2 class="w-5 h-5 animate-spin" />
				<span>Sending</span>
			{:else}
				<Send class="w-5 h-5" />
				<span>Send</span>
			{/if}
		</button>
	</form>

	<!-- Helper Text -->
	<div class="mt-3 text-sm text-gray-500">
		Press Enter to send, Shift+Enter for a new line
	</div>
</div>

<style>
	/* Hide scrollbar for textarea */
	.scrollbar-hide {
		-ms-overflow-style: none; /* Internet Explorer 10+ */
		scrollbar-width: none; /* Firefox */
	}
	
	.scrollbar-hide::-webkit-scrollbar {
		display: none; /* Safari and Chrome */
	}
</style>