<script lang="ts">
	import { browser } from '$app/environment';
	import QuillEditor from '$lib/components/quill/QuillEditor.svelte';

	export let dialogCreatePost;
	let textPost: boolean = true;
	let mediaPost: boolean = false;

	let editorContent = '';

	function handleEditorChange(event: { detail: { html: string } }) {
		editorContent = event.detail.html;
	}

</script>


<dialog bind:this={dialogCreatePost} on:close id="create_post_dialog">
	<section class="modal">
		<header>
			<button
				class:textPost
				class:active={textPost}
				on:click={() => {
					textPost = true;
					mediaPost = false;
				}}
			>
				Text
			</button>
			<span class="separator"></span>
			<button
				class:mediaPost
				class:active={mediaPost}
				on:click={() => {
					textPost = false;
					mediaPost = true;
				}}
			>
				Image
			</button>
		</header>
		<section class="content">
			{#if textPost}
				<div class="text_container">
					{#if browser}
						<div class="editor">
							<QuillEditor
								bind:content={editorContent}
								placeholder="Start typing your content..."
								on:change={handleEditorChange}
							/>
						</div>
						<div class="preview">
							<div>{@html editorContent}</div>
						</div>
					{/if}
				</div>
			{:else if mediaPost}
				<div class="media_container">MEDIA</div>
			{/if}
		</section>
		<footer>
			FOOTER
		</footer>
	</section>
</dialog>
