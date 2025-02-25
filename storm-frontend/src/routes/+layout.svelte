<script lang="ts">
	import { i18n } from '$lib/i18n';
	import { ParaglideJS } from '@inlang/paraglide-sveltekit';
	import '../app.css';

	let { children } = $props();
</script>

<ParaglideJS {i18n}>
    <span
			class="h-full w-full bg-fixed bg-[url($lib/assets/logo.png)] opacity-25 bg-no-repeat bg-center bg-contain absolute top-0 left-0 -z-1">
    </span>
	{@render children()}
</ParaglideJS>
