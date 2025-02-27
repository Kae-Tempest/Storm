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

<section id="home_page">
	<!-- NAV -->
	<Navbar />
	<!-- Content -->
	{#if loading}
		<div class="loading">
			<span>Chargement en cours...</span>
		</div>
	{:else if error}
		<div class="error">
			{error}
		</div>
	{:else}
		<div class="grid_wrapper">
			{#each posts as post}
				<PostCard post={post} />
			{/each}
		</div>
	{/if}
</section>