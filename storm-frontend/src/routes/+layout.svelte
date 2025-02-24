<script lang="ts">
	import {i18n} from "$lib/i18n";
	import {ParaglideJS} from "@inlang/paraglide-sveltekit";
	import '../app.css';
	import logo from "$lib/assets/logo.png";

	let {children} = $props();
</script>

<ParaglideJS {i18n}>
    <img src="{logo}" alt="project logo" class="h-full opacity-25 absolute top-0 left-0 w-full -z-1"/>
    {@render children()}
</ParaglideJS>
