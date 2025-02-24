<script lang="ts">
    import {AtSign, LockKeyhole, User, UserSearch} from "lucide-svelte";
    import {RegisterStore} from "$lib/stores/register/register";


    let email: string = ""
    let password: string = ""
    let confirm_password: string = ""
    let username: string = ""
    let display_name: string = ""

    let isSubmitting = false
    let error: Error | string | null = null

    async function handleRegister() {
        isSubmitting = true;
        error = null;

        try {
            await RegisterStore.register({
                email,
                password,
                confirm_password,
                username,
                display_name,
            })
            email = ""
            password = ""
            confirm_password = ""
            username = ""
            display_name = ""
        } catch (err) {
            error = err as Error;
        } finally {
            isSubmitting = false;
        }
    }

</script>

<section class="h-full w-full">
    <div class="w-full h-full flex justify-center items-center">
        <form class="w-lg p-4 flex flex-col" on:submit|preventDefault={handleRegister}>
            <div class="flex mb-2">
                <!--  icon  -->
                <div class="flex items-center justify-center w-13 h-13 bg-slate-900 rounded-l">
                    <UserSearch/>
                </div>
                <input type="text" placeholder="Username" bind:value={username} required disabled={isSubmitting}
                       class="w-full h-13 bg-slate-800 px-2 rounded-r">
            </div>

            <div class="flex my-2">
                <!--  icon  -->
                <div class="flex items-center justify-center w-13 h-13 bg-slate-900 rounded-l">
                    <User/>
                </div>
                <input type="text" placeholder="Display Name" bind:value={display_name} disabled={isSubmitting}
                       class="w-full h-13 bg-slate-800 px-2 rounded-r">
            </div>

            <div class="flex my-2">
                <!--  icon  -->
                <div class="flex items-center justify-center w-13 h-13 bg-slate-900 rounded-l">
                    <AtSign/>
                </div>
                <input type="email" placeholder="Email" bind:value={email} required disabled={isSubmitting}
                       class="w-full h-13 bg-slate-800 px-2 rounded-r">
            </div>

            <div class="flex my-2">
                <!--  icon  -->
                <div class="flex items-center justify-center w-13 h-13 bg-slate-900 rounded-l">
                    <LockKeyhole/>
                </div>
                <input type="password" placeholder="Password" bind:value={password} required disabled={isSubmitting}
                       class="w-full h-13 bg-slate-800 px-2 rounded-r">
            </div>

            <div class="flex my-2">
                <!--  icon  -->
                <div class="flex items-center justify-center w-13 h-13 bg-slate-900 rounded-l">
                    <LockKeyhole/>
                </div>
                <input type="password" placeholder="Password" bind:value={confirm_password} required
                       disabled={isSubmitting}
                       class="w-full h-13 bg-slate-800 px-2 rounded-r">
            </div>
            {#if error}
                {#if typeof error === 'object' && typeof error !== 'string'}
                    <span class="text-center text-red-500">{error.message}</span>
                {:else}
                    <span class="text-center text-red-500">{error}</span>
                {/if}
            {/if}
            <button type="submit" disabled={isSubmitting || !email.trim() || !password.trim() || !username.trim()}
                    class="bg-blue-900 w-full rounded-md p-2 my-2">
                {#if isSubmitting}
                    Register in progress
                {:else}
                    Resgister
                {/if}
            </button>
            <div class="flex justify-end text-xs text-stone-100/50 w-full">
                <span class="hover:text-stone-100 cursor-pointer">
                    <a href="/login">Already have an account ? Log in</a>
                </span>
            </div>
        </form>
    </div>
</section>