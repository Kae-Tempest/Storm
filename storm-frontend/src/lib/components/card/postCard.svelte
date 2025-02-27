<script lang="ts">
	import type { Posts } from '$lib/types/posts';

	export let post: Posts;

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
					{post.content}
				</div>
			</div>

		{:else}
			<div class="text_content">
				<div class="content">
					{post.content}
				</div>
			</div>
		{/if}
	</div>
</section>
