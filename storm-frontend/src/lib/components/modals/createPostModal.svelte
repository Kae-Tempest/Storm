<script lang="ts">
	import { browser } from '$app/environment';
	import QuillEditor from '$lib/components/quill/QuillEditor.svelte';
	import DOMPurify from 'dompurify';

	export let dialogCreatePost;

	let privacyOptions: string[] = ['public', 'friend Only', 'private'];
	let isTextOnly: boolean = false;
	let post_media: string, fileinput;

	let editorContent = '';
	$: sanitizedContent = browser && DOMPurify.sanitize(editorContent);
	$: if (isTextOnly) post_media = '';

	const onFileSelected = (e: Event) => {
		let input = e.target as HTMLInputElement;
		if (input.files && input.files[0]) {
			let image = input.files[0];
			let reader = new FileReader();
			reader.readAsDataURL(image);
			reader.onload = e => {
				if (e.target !== null && e.target.result && typeof e.target.result === 'string') post_media = e.target.result;
			};
		}
	};
</script>


<dialog bind:this={dialogCreatePost} on:close id="create_post_dialog">
	<section class="modal">
		<header>
			Post Creation
		</header>
		<section class="content">
			<form class="text_container">
				{#if browser}
					<div class="editor">
						<QuillEditor
							bind:content={editorContent}
							placeholder="Start typing your content..."
						/>
					</div>
					<div class="preview">
						<div class="params">
							<ul class="list">
								<li>Text-only : <input type="checkbox" bind:checked={isTextOnly}></li>
								<li>Media :
									<input type="file" disabled={isTextOnly} on:change={(e)=>onFileSelected(e)} bind:this={fileinput}>
								</li>
								<li>Privacy :
									<select>
										{#each privacyOptions as privacyOption}
											<option value={privacyOption} label={privacyOption}></option>
										{/each}
									</select></li>
							</ul>
						</div>
						<div class="card_img">
							<section id="post_card">
								<div id="card">
									{#if post_media}
										<div class="media">
											<img
												src={post_media}
												alt="Media content"
											/>
										</div>
										<div class="media_content">
											{#if sanitizedContent}
												<div class="content" contenteditable="false" bind:innerHTML={sanitizedContent}></div>
											{/if}
										</div>
									{:else}
										<div class="text_content">
											{#if sanitizedContent}
												<div class="content" contenteditable="false" bind:innerHTML={sanitizedContent}></div>
											{/if}
										</div>
									{/if}
								</div>
							</section>
						</div>
					</div>

					<div class="action-buttons">
						<button type="reset" class="reset">Cancel</button>
						<button type="submit" class="submit">Post</button>
					</div>
				{/if}
			</form>
		</section>
	</section>
</dialog>
