<script lang="ts">
	import type { Posts } from '$lib/types/posts';
	import DOMPurify from 'dompurify';
	import { browser } from '$app/environment';

	export let post: Posts;
	$: sanitizedContent = browser && DOMPurify.sanitize(post.content);
</script>


<section id="post_card">
	<div id="card">

		{#if post.media_url}
			<div class="media">
				<img
					src={post.media_url}
					alt="Media content"
				/>
			</div>


			<div class="media_content">
				<div class="content">
					{#if sanitizedContent}
						<div class="content" contenteditable="false" bind:innerHTML={sanitizedContent}></div>
					{/if}
				</div>
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
