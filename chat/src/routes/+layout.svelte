<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	
	let { children } = $props();

	onMount(async () => {
		const { initFlowbite } = await import('flowbite');
		initFlowbite();
	});
</script>

{@render children()}