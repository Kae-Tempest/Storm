<script lang="ts">
	import { AtSign, LockKeyhole } from 'lucide-svelte';
	import { AuthStore } from '$lib/stores/login/login';
	import { onMount } from 'svelte';

	let email: string = '';
	let password: string = '';
	let isSubmitting = false;
	let error: Error | string | null = null;

	onMount(() => {
		AuthStore.subscribe(state => {
			isSubmitting = state.loading;
			error = state.error;
		});
	});

	async function handleLogin() {
		isSubmitting = true;
		error = null;

		try {
			await AuthStore.login(email, password);
			email = '';
			password = '';
		} catch (err) {
			error = err as Error;
		} finally {
			isSubmitting = false;
		}
	}

</script>


<section id="login">
	<div class="container">
		<form on:submit|preventDefault={handleLogin}>
			<div class="field">
				<!--  icon  -->
				<div class="icon">
					<AtSign />
				</div>
				<input type="email" placeholder="Email" bind:value={email} required disabled={isSubmitting}>
			</div>
			<div class="field">
				<!--  icon  -->
				<div class="icon">
					<LockKeyhole />
				</div>
				<input type="password" placeholder="Password" bind:value={password} required disabled={isSubmitting}>
			</div>
			{#if error}
				{#if typeof error === 'object' && typeof error !== 'string'}
					<span class="error">{error.message}</span>
				{:else}
					<span class="error">{error}</span>
				{/if}
			{/if}
			<button type="submit" disabled={isSubmitting || !email.trim() || !password.trim()}>
				{#if isSubmitting}
					Login in progress
				{:else}
					Login
				{/if}
			</button>
			<div class="action_container">
				<span>Forgotten password ?</span>
				<span><a href="/register">No Account ? Sign Up !</a></span>
			</div>
		</form>
	</div>
</section>