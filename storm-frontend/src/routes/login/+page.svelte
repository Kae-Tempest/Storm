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


<section class="h-full w-full">
	<div class="w-full h-full flex justify-center items-center">
		<form class="w-lg p-4 flex flex-col" on:submit|preventDefault={handleLogin}>
			<div class="flex mb-2">
				<!--  icon  -->
				<div class="flex items-center justify-center w-13 h-13 bg-slate-900 rounded-l">
					<AtSign />
				</div>
				<input type="email" placeholder="Email" bind:value={email} required disabled={isSubmitting}
							 class="w-full h-13 bg-slate-800 px-2 rounded-r">
			</div>
			<div class="flex my-2">
				<!--  icon  -->
				<div class="flex items-center justify-center w-13 h-13 bg-slate-900 rounded-l">
					<LockKeyhole />
				</div>
				<input type="password" placeholder="Password" bind:value={password} required disabled={isSubmitting}
							 class="w-full h-13 bg-slate-800 px-2 rounded-r">
			</div>
			{#if error}
				{#if typeof error === 'object' && typeof error !== 'string'}
					<span class="text-center text-red-500">{error.message}</span>
				{:else}
					<span class="text-center text-red-500">{error}</span>
				{/if}
			{/if}
			<button type="submit" disabled={isSubmitting || !email.trim() || !password.trim()}
							class="bg-blue-900 w-full rounded-md p-2 my-2">
				{#if isSubmitting}
					Login in progress
				{:else}
					Login
				{/if}
			</button>
			<div class="flex justify-between text-xs text-stone-100/50">
				<span class="hover:text-stone-100 cursor-pointer">Forgotten password ?</span>
				<span class="hover:text-stone-100 cursor-pointer"><a href="/register">No Account ? Sign Up !</a></span>
			</div>
		</form>
	</div>
</section>