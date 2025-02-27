<script lang="ts">
	import { AtSign, LockKeyhole, User, UserSearch } from 'lucide-svelte';
	import { RegisterStore } from '$lib/stores/register/register';


	let email: string = '';
	let password: string = '';
	let confirm_password: string = '';
	let username: string = '';
	let display_name: string = '';

	let isSubmitting = false;
	let error: Error | string | null = null;

	async function handleRegister() {
		isSubmitting = true;
		error = null;

		try {
			await RegisterStore.register({
				email,
				password,
				confirm_password,
				username,
				display_name
			});
			email = '';
			password = '';
			confirm_password = '';
			username = '';
			display_name = '';
		} catch (err) {
			error = err as Error;
		} finally {
			isSubmitting = false;
		}
	}

</script>

<section id="register">
	<div class="container">
		<form on:submit|preventDefault={handleRegister}>
			<div class="field">
				<!--  icon  -->
				<div class="icon">
					<UserSearch />
				</div>
				<input type="text" placeholder="Username" bind:value={username} required disabled={isSubmitting}>
			</div>

			<div class="field">
				<!--  icon  -->
				<div class="icon">
					<User />
				</div>
				<input type="text" placeholder="Display Name" bind:value={display_name} disabled={isSubmitting}>
			</div>

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

			<div class="field">
				<!--  icon  -->
				<div class="icon">
					<LockKeyhole />
				</div>
				<input type="password" placeholder="Password" bind:value={confirm_password} required disabled={isSubmitting}>
			</div>
			{#if error}
				{#if typeof error === 'object' && typeof error !== 'string'}
					<span class="error">{error.message}</span>
				{:else}
					<span class="error">{error}</span>
				{/if}
			{/if}
			<button type="submit" disabled={isSubmitting || !email.trim() || !password.trim() || !username.trim()}>
				{#if isSubmitting}
					Register in progress
				{:else}
					Resgister
				{/if}
			</button>
			<div class="action_container">
				<span><a href="/login">Already have an account ? Log in</a></span>
			</div>
		</form>
	</div>
</section>