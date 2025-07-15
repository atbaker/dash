<script lang="ts">
	import type { ChatMessage } from '../stores/chat.js';
	import { Avatar } from 'flowbite-svelte';
	import { fly } from 'svelte/transition';
	import { Bot, User } from 'lucide-svelte';
	import { marked } from 'marked';
	import { browser } from '$app/environment';
	
	let DOMPurify: any = null;
	
	// Initialize DOMPurify only in browser
	if (browser) {
		import('dompurify').then(module => {
			DOMPurify = module.default;
		});
	}

	interface Props {
		message: ChatMessage;
	}

	let { message }: Props = $props();

	// Format timestamp for display
	function formatTime(date: Date): string {
		return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
	}

	// Convert markdown to HTML and sanitize
	function formatContent(content: string): string {
		// Configure marked for better output
		marked.setOptions({
			breaks: true, // Convert line breaks to <br>
			gfm: true, // GitHub Flavored Markdown
		});
		
		// Parse markdown
		const rawHtml = marked.parse(content) as string;
		
		// Sanitize only in browser environment
		if (browser && DOMPurify) {
			return DOMPurify.sanitize(rawHtml);
		}
		
		// Return raw HTML for SSR (marked output is generally safe)
		return rawHtml;
	}
</script>

{#if message.role === 'user'}
	<!-- User message - right aligned -->
	<div class="flex items-start justify-end gap-3" in:fly={{ y: 20, duration: 300 }}>
		<div class="flex flex-col max-w-[85%] sm:max-w-[320px] items-end">
			<div class="flex items-center space-x-2 justify-end mb-1">
				<span class="text-xs font-normal text-gray-500 dark:text-gray-400">{formatTime(message.timestamp)}</span>
				<span class="text-sm font-medium text-gray-900 dark:text-white">You</span>
			</div>
			<div class="p-3 bg-blue-500 text-white rounded-xl">
				<div class="text-base whitespace-pre-wrap">{message.content}</div>
			</div>
		</div>
		<Avatar class="w-8 h-8 bg-blue-500 text-white">
			<User class="w-5 h-5" />
		</Avatar>
	</div>
{:else}
	<!-- AI message - left aligned -->
	<div class="flex items-start gap-3" in:fly={{ y: 20, duration: 300 }}>
		<Avatar class="w-8 h-8 bg-gray-500 text-white">
			<Bot class="w-5 h-5" />
		</Avatar>
		<div class="flex-1">
			<div class="flex items-center space-x-2 mb-1">
				<span class="text-sm font-medium text-gray-900 dark:text-white">DASH</span>
				<span class="text-xs font-normal text-gray-500 dark:text-gray-400">{formatTime(message.timestamp)}</span>
			</div>
			<div class="bg-gray-100 dark:bg-gray-700 rounded-lg p-3 max-w-full">
				<div class="text-base text-gray-900 dark:text-gray-100 format dark:format-invert max-w-none">
					{@html formatContent(message.content)}
					{#if message.streaming}
						<span class="inline-block w-2 h-4 bg-gray-600 dark:bg-gray-400 animate-pulse ml-1"></span>
					{/if}
				</div>
			</div>
		</div>
	</div>
{/if}