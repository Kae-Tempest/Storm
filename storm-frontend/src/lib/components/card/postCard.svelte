<script lang="ts">
	import type { Posts } from '$lib/types/posts';

	export let post: Posts;

</script>


<section class="">
	<div id="card"
			 class="relative group h-[323px] w-[323px] rounded-[10%] border border-blue-900 overflow-hidden overflow-y-auto
                         bg-gradient-to-b from-base-100 to-base-300 shadow-lg transition-all duration-300 hover:scale-105 my-2">

		{#if post.media_url}
			<div class="absolute inset-0 w-full h-full">
				<img
					src={post.media_url}
					alt="Media content"
					class="w-full h-full object-cover"
				/>
			</div>

			<div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-70 transition-opacity duration-300"></div>

			<div
				class="absolute inset-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center">
				<div class="text-white break-words overflow-y-auto max-h-full">
					{post.content}
				</div>
			</div>

		{:else}
			<div class="p-4 h-full flex items-center justify-center">
				<div class="break-words overflow-y-auto max-h-full">
					{post.content}
				</div>
			</div>
		{/if}
	</div>
</section>
