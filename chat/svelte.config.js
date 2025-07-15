import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://svelte.dev/docs/kit/integrations
	// for more information about preprocessors
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter({
			// Generate a single-page app (SPA) for better client-side routing
			fallback: 'index.html',
			// Output directory for static files
			pages: 'build',
			assets: 'build'
		}),
		// Configure paths for deployment
		paths: {
			base: process.env.NODE_ENV === 'production' ? '' : ''
		},
		alias: {
			'@': './src'
		}
	}
};

export default config;
