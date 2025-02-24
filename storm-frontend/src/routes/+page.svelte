<script lang="ts">
    import {onMount} from 'svelte';
    import {postStore} from '$lib/stores/posts/posts';
    import type {Posts} from '$lib/types/posts';

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

    function handleLike(postId: number): void {
        postStore.likePost(postId);
    }

</script>

<div class="post-list">
    {#if loading}
        <div>Chargement...</div>
    {:else if error}
        <div>{error}</div>
    {:else}
        {#each posts as post (post.id)}
            <div class="post">
                <div class="post-content">{post.content}</div>
                <div class="post-actions">
                    <button
                            on:click={() => handleLike(post.id)}
                            class:liked={post.is_liked}
                    >
                        ❤️ {post.likes_count}
                    </button>
                </div>
            </div>
        {/each}
    {/if}
</div>

<style>
    .post {
        border: 1px solid #ddd;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .post-actions button {
        background: none;
        border: none;
        cursor: pointer;
    }

    .post-actions button.liked {
        color: red;
    }
</style>