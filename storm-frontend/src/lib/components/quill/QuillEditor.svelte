<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { browser } from '$app/environment';
	import type Quill from 'quill';

	export let content = '';
	export let placeholder = 'Write something...';
	export let theme = 'snow';
	export let readOnly = false;

	let quill: Quill;
	let quillElement: HTMLDivElement;

	onMount(() => {
		if (browser) {
			import('quill').then(module => {
				const Quill = module.default;

				const defaultModules = {
					toolbar: [
						[{ header: [2, 3, 4, 5, 6, false] }],
						['bold', 'italic', 'underline', 'strike'],
						['blockquote', 'code-block']
					]
				};

				quill = new Quill(quillElement, {
					modules: defaultModules,
					theme,
					placeholder,
					readOnly
				});

				if (content) {
					quill.clipboard.dangerouslyPasteHTML(content);
				}

				quill.on('text-change', () => {
					content = quill.root.innerHTML;
					dispatch('change', {
						html: quill.root.innerHTML,
						text: quill.getText(),
						delta: quill.getContents()
					});
				});
			});
		}
	});

	onDestroy(() => {
		if (quill) {
			quill.off('text-change');
		}
	});

	// Create a function to dispatch events
	function dispatch(name: string, detail: object) {
		quillElement.dispatchEvent(new CustomEvent(name, { detail }));
	}
</script>

<div class="quill-editor-container">
	<div bind:this={quillElement}></div>
</div>

