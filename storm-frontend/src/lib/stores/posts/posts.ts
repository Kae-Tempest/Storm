import { writable, type Writable } from 'svelte/store';
import type { Posts } from '$lib/types/posts';
import { AuthStore } from '$lib/stores/login/login';

interface PostState {
	posts: Posts[];
	loading: boolean;
	error: string | null;
}

const initialState: PostState = {
	posts: [],
	loading: false,
	error: null
};

function createPostStore() {
	const { subscribe, update }: Writable<PostState> = writable(initialState);

	return {
		subscribe,
		fetchPosts: async (): Promise<void> => {
			update((state) => ({ ...state, loading: true }));
			try {
				const response = await AuthStore.fetchWithAuth('/api/posts');
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}
				const data = (await response.json()) as Posts[];
				update((state) => ({
					...state,
					posts: data,
					loading: false,
					error: null
				}));
			} catch (err) {
				const error = err as Error;
				update((state) => ({
					...state,
					error: error.message,
					loading: false
				}));
			}
		},

		createPost: async (content: string): Promise<void> => {
			try {
				const response = await AuthStore.fetchWithAuth('/api/posts', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({ content })
				});

				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}

				const newPost = (await response.json()) as Posts;
				update((state) => ({
					...state,
					posts: [newPost, ...state.posts],
					error: null
				}));
			} catch (err) {
				const error = err as Error;
				update((state) => ({
					...state,
					error: error.message
				}));
			}
		},

		likePost: async (postId: number): Promise<void> => {
			try {
				const response = await AuthStore.fetchWithAuth(`/api/posts/${postId}/like`, {
					method: 'POST'
				});

				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}

				update((state) => ({
					...state,
					posts: state.posts.map((post) =>
						post.id === postId
							? {
									...post,
									likes_count: post.likes_count + 1,
									is_liked: true
								}
							: post
					),
					error: null
				}));
			} catch (err) {
				const error = err as Error;
				update((state) => ({
					...state,
					error: error.message
				}));
			}
		}
	};
}

export const postStore = createPostStore();
