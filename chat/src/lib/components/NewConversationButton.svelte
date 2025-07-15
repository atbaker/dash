<script lang="ts">
	import { Plus } from 'lucide-svelte';
	import { chatAPI } from '$lib/api/chat.js';

	function handleNewConversation() {
		chatAPI.clearConversation();
	}
</script>

<button 
	on:click={handleNewConversation}
	class="flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:outline-none dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-600"
>
	<Plus class="w-4 h-4" />
	New Conversation
</button>