import { writable, type Writable } from 'svelte/store';
import { browser } from '$app/environment';
import { goto } from '$app/navigation';
import type { User } from '$lib/types/user';

interface IResgister {
	access_token: string;
	token_type: string;
	user: User;
	loading: boolean;
	error: string | null;
}

const getInitialState: IResgister = {
	access_token: '',
	token_type: '',
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

type RegisterPayload = {
	email: string;
	password: string;
	confirm_password: string;
	username: string;
	display_name: string;
};

function createRegistetStore() {
	const { subscribe, update }: Writable<IResgister> = writable(getInitialState);

	return {
		subscribe,
		register: async ({
			email,
			password,
			confirm_password,
			display_name,
			username
		}: RegisterPayload) => {
			if (password !== confirm_password) {
				throw new Error("Passwords don't match");
			}
			if (display_name.toLowerCase() !== username.toLowerCase()) {
				throw new Error('Display name must be same as username');
			}

			try {
				username = username.toLowerCase();
				const resp = await fetch('/api/auth/register', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						email,
						password,
						username,
						display_name
					})
				});

				if (!resp.ok) {
					const { detail } = await resp.json();
					throw new Error(detail);
				}
				// TODO: Voir si on recupere aussi le user
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
					error: error.message,
					loading: false
				}));
			}
		}
	};
}

export const RegisterStore = createRegistetStore();
