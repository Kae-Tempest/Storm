import { derived, get, writable, type Writable } from 'svelte/store';
import { goto } from '$app/navigation';
import { browser } from '$app/environment';
import type { User } from '$lib/types/user';

interface ILogin {
	access_token: string;
	token_type: string;
	user: User;
	loading: boolean;
	error: string | null;
}

const getInitialState: () => ILogin = (): ILogin => {
	if (browser) {
		const savedToken: string | null = localStorage.getItem('auth_token');
		const savedTokenType: string | null = localStorage.getItem('token_type');
		const savedUser: string | null = localStorage.getItem('user');
		const parsedSavedUser: User | null = savedUser ? JSON.parse(savedUser) : null;

		if (savedToken && savedTokenType && parsedSavedUser) {
			return {
				access_token: savedToken,
				token_type: savedTokenType,
				user: parsedSavedUser,
				loading: false,
				error: null
			};
		}
	}
	return {
		access_token: '',
		token_type: 'Bearer',
		user: {
			id: 0,
			email: '',
			username: '',
			display_name: '',
			avatar: '',
			bio: '',
			date__of_birth: new Date(),
			updated_at: new Date()
		},
		loading: false,
		error: null
	};
};

function createAuthStore() {
	const { subscribe, update, set }: Writable<ILogin> = writable(getInitialState());

	const authHeader = derived({ subscribe }, ($state) =>
		$state.access_token ? `${$state.token_type} ${$state.access_token}` : null
	);

	async function fetchWithAuth(url: string, options: RequestInit = {}) {
		const token = get({ subscribe }).access_token;
		const tokenType = get({ subscribe }).token_type;

		if (!token) {
			throw new Error('No authentication token available.');
		}

		const headers = {
			...options.headers,
			Authorization: `${tokenType} ${token}`
		};

		return fetch(url, { ...options, headers });
	}

	return {
		subscribe,
		authHeader,
		fetchWithAuth,
		login: async (email: string, password: string): Promise<void> => {
			try {
				const resp = await fetch('/api/auth/login', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						email,
						password
					})
				});

				if (!resp.ok) {
					const { detail } = await resp.json();
					throw new Error(detail);
				}

				const { access_token, token_type, user } = await resp.json();

				// Sauvegarder dans le localStorage
				if (browser) {
					localStorage.setItem('auth_token', access_token);
					localStorage.setItem('token_type', token_type);
					localStorage.setItem('user', JSON.stringify(user));
				}

				update((state) => ({
					...state,
					access_token,
					token_type,
					user,
					loading: false,
					error: null
				}));

				await goto('/');
			} catch (err) {
				const error = err as Error;
				update((state) => ({
					...state,
					loading: false,
					error: error.message
				}));
			}
		},
		logout: async () => {
			// Nettoyer le localStorage
			if (browser) {
				localStorage.removeItem('auth_token');
				localStorage.removeItem('token_type');
				localStorage.removeItem('user');
			}

			set({
				access_token: '',
				token_type: 'Bearer',
				user: {
					id: 0,
					email: '',
					username: '',
					display_name: '',
					avatar: '',
					bio: '',
					date__of_birth: new Date(),
					updated_at: new Date()
				},
				loading: false,
				error: null
			});

			await goto('/login');
		}
	};
}

export const AuthStore = createAuthStore();
