import { writable, type Writable } from 'svelte/store';
import type { CreatePost, Posts } from '$lib/types/posts';
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
			update((state: PostState): PostState => ({ ...state, loading: true }));
			try {
				const response: Response = await AuthStore.fetchWithAuth('/api/posts');
				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}
				const data = (await response.json()) as Posts[];
				update((state: PostState): PostState => ({
					...state,
					posts: data,
					loading: false,
					error: null
				}));
			} catch (err) {
				const error = err as Error;
				update((state: PostState): PostState => ({
					...state,
					error: error.message,
					loading: false
				}));
			}
		},

		createPost: async (payload: CreatePost | FormData, contentType: string): Promise<void> => {
			try {
				const requestOptions: RequestInit = {
					method: 'POST'
				};

				if (contentType === 'multipart/form-data') {
					if (payload instanceof FormData) {
						requestOptions.body = payload;
					} else {
						throw new Error('Payload doit être FormData pour multipart/form-data');
					}
				} else {
					// Pour JSON, définir le Content-Type et stringifier le body
					requestOptions.headers = { 'Content-Type': contentType };
					requestOptions.body = JSON.stringify(payload);
				}

				const response: Response = await AuthStore.fetchWithAuth('/api/posts/', requestOptions);

				// Log de la réponse pour le débogage
				const responseText = await response.text();

				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}, message: ${responseText}`);
				}

				// Convertir le texte en JSON
				const newPost = JSON.parse(responseText) as Posts;

				update((state: PostState): PostState => ({
					...state,
					posts: [newPost, ...state.posts],
					error: null
				}));
			} catch (err) {
				const error = err as Error;
				update((state: PostState): PostState => ({
					...state,
					error: error.message
				}));
			}
		},

		likePost: async (postId: number): Promise<void> => {
			try {
				const response: Response = await AuthStore.fetchWithAuth(`/api/posts/${postId}/like`, {
					method: 'POST'
				});

				if (!response.ok) {
					throw new Error(`HTTP error! status: ${response.status}`);
				}

				update((state: PostState): PostState => ({
					...state,
					posts: state.posts.map((post: Posts): Posts =>
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
				update((state: PostState): PostState => ({
					...state,
					error: error.message
				}));
			}
		}
	};
}

export const postStore = createPostStore();
