import { writable, type Writable } from 'svelte/store';
import axios, { AxiosError } from 'axios';
import type { Posts } from '$lib/types/posts';

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
    const { subscribe, set, update }: Writable<PostState> = writable(initialState);

    return {
        subscribe,
        fetchPosts: async (): Promise<void> => {
            update(state => ({ ...state, loading: true }));
            try {
                const response = await axios.get<Posts[]>('/api/posts');
                update(state => ({
                    ...state,
                    posts: response.data,
                    loading: false,
                    error: null
                }));
            } catch (err) {
                const error = err as AxiosError;
                update(state => ({
                    ...state,
                    error: error.message,
                    loading: false
                }));
            }
        },

        createPost: async (content: string): Promise<void> => {
            try {
                const response = await axios.post<Posts>('/api/posts', { content });
                update(state => ({
                    ...state,
                    posts: [response.data, ...state.posts],
                    error: null
                }));
            } catch (err) {
                const error = err as AxiosError;
                update(state => ({
                    ...state,
                    error: error.message
                }));
            }
        },

        likePost: async (postId: number): Promise<void> => {
            try {
                await axios.post(`/api/posts/${postId}/like`);
                update(state => ({
                    ...state,
                    posts: state.posts.map(post =>
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
                const error = err as AxiosError;
                update(state => ({
                    ...state,
                    error: error.message
                }));
            }
        }
    };
}

export const postStore = createPostStore();