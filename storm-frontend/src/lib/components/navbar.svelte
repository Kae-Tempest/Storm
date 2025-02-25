<script>
	import logo from '$lib/assets/logo.png';
	import { AuthStore } from '$lib/stores/login/login.js';
	import { House, MessagesSquare, Plus, Search } from 'lucide-svelte';

	let showMenu = false;
</script>

<nav class="h-full max-w-3xs border-r border-r-blue-900 flex flex-col sticky mr-2 pr-4">
	<section>
		<a href="/" class="flex w-full items-center">
			<img src="{logo}" alt="project logo" class="max-w-[123px]" />
			<h1 class="text-4xl font-black">Storm</h1>
		</a>
	</section>
	<section class="flex flex-col w-full items-center mb-auto ">
		<ul class="h-full flex flex-col text-xl w-2/3">
			<li class="hover:bg-stone-100/20 w-full p-2 rounded cursor-pointer">
				<a href="/" class="flex gap-2">
					<House />
					Home
				</a>
			</li>
			<li class="hover:bg-stone-100/20 w-full p-2 rounded cursor-pointer">
				<a href="/chat" class="flex gap-2">
					<MessagesSquare />
					Chat
				</a>
			</li>
			<li class="hover:bg-stone-100/20 w-full p-2 rounded cursor-pointer">
				<button class="cursor-pointer flex gap-2">
					<Search />
					Search
				</button>
			</li>
			<li class="hover:bg-stone-100/20 w-full p-2 rounded cursor-pointer">
				<button class="cursor-pointer flex gap-2">
					<Plus />
					Post
				</button>
			</li>
		</ul>
	</section>
	<section class="flex w-full justify-center relative">
		{#if showMenu}
			<div class="absolute bottom-30 left-11 rounded p-5 text-xl w-2/3 text-center
             bg-slate-800 border border-blue-900 ">
				<ul class="flex flex-col gap-2">
					<li>
						<button on:click={() => AuthStore.logout()} class="cursor-pointer">Logout</button>
					</li>
					<li>
						<a href="/profile/">Profile</a>
					</li>
					<li>
						<a href="/support">Support</a>
					</li>
					<li>
						<hr>
					</li>
					<li>Kae</li>
				</ul>
			</div>
		{/if}
		<button on:click={() => showMenu = !showMenu} class="cursor-pointer">
			<img src="{logo}" alt="project logo" class="max-w-[123px]" />
		</button>
	</section>
</nav>