<script lang="ts">
	import ChatMessage from './ChatMessage.svelte';
	import { chatStore } from '../stores/chat.js';
	import { ChevronDown } from 'lucide-svelte';
	import { onMount } from 'svelte';

	let messagesContainer: HTMLDivElement;
	let autoScroll = $state(true);

	// Subscribe to chat store
	const messages = $derived($chatStore.messages);
	const isStreaming = $derived($chatStore.isStreaming);

	// Auto-scroll to bottom when new messages arrive
	function scrollToBottom() {
		if (messagesContainer && autoScroll) {
			messagesContainer.scrollTop = messagesContainer.scrollHeight;
		}
	}

	// Check if user has scrolled up
	function handleScroll() {
		if (!messagesContainer) return;
		
		const { scrollTop, scrollHeight, clientHeight } = messagesContainer;
		const isNearBottom = scrollTop + clientHeight >= scrollHeight - 50;
		autoScroll = isNearBottom;
	}

	// Use effect to scroll when messages change
	$effect(() => {
		// Watch messages for changes
		messages;
		scrollToBottom();
	});

	onMount(() => {
		scrollToBottom();
	});
</script>

<div 
	bind:this={messagesContainer}
	class="h-full w-full overflow-y-auto p-4 md:p-6 space-y-4"
	onscroll={handleScroll}
>
	<!-- Chat Messages -->
	{#each messages as message (message.id)}
		<ChatMessage {message} />
	{/each}

	<!-- Scroll to bottom button (shown when user scrolled up) -->
	{#if !autoScroll && messages.length > 0}
		<div class="absolute bottom-4 right-4">
			<button
				type="button"
				class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm p-2 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 shadow-lg"
				onclick={() => {
					autoScroll = true;
					scrollToBottom();
				}}
				aria-label="Scroll to bottom"
			>
				<ChevronDown class="w-4 h-4" />
			</button>
		</div>
	{/if}
</div>

<style>
	/* Custom scrollbar styling */
	div::-webkit-scrollbar {
		width: 6px;
	}

	div::-webkit-scrollbar-track {
		background: #f1f1f1;
		border-radius: 3px;
	}

	div::-webkit-scrollbar-thumb {
		background: #c1c1c1;
		border-radius: 3px;
	}

	div::-webkit-scrollbar-thumb:hover {
		background: #a8a8a8;
	}
</style>