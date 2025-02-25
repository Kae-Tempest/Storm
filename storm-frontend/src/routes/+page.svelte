<script lang="ts">
	import Navbar from '$lib/components/navbar.svelte';
	import PostCard from '$lib/components/card/postCard.svelte';
	import { onMount } from 'svelte';
	import { postStore } from '$lib/stores/posts/posts';
	import type { Posts } from '$lib/types/posts';

	let posts: Posts[] = [];
	let loading = false;
	let error: string | null = null;

	postStore.subscribe(state => {
		posts = state.posts;
		loading = state.loading;
		error = state.error;
	});

	onMount(() => {
		postStore.fetchPosts();
	});
</script>

<section class="h-screen w-full flex">
	<!-- NAV -->
	<Navbar />
	<!-- Content -->
	{#if loading}
		<div class="flex justify-center items-center h-full w-full p-4">
			<span class="text-lg">Chargement en cours...</span>
		</div>
	{:else if error}
		<div class="flex justify-center items-center h-full w-full p-4 text-red-500">
			{error}
		</div>
	{:else}
		<div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 overflow-y-auto h-full
        2xl:grid-cols-5 3xl:grid-cols-6 5xl:grid-cols-7 gap-3 p-4 grid-flow-row-dense w-full">
			{#each posts as post}
				<PostCard post={post} />
			{/each}
		</div>
	{/if}
</section>