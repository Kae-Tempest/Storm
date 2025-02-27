<script lang="ts">
	import logo from '$lib/assets/logo.png';
	import { AuthStore } from '$lib/stores/login/login.js';
	import { House, MessagesSquare, Plus, Search } from 'lucide-svelte';
	import CreatePostModal from '$lib/components/modals/createPostModal.svelte';

	let showMenu = false;
	let dialogCreatePost: HTMLDialogElement;
	let dialogIsOpen = false;

	function handleOpenModal(): void {
		dialogIsOpen = true;
		setTimeout(() => {
			dialogCreatePost.showModal();
		}, 0);

	}

</script>
{#if dialogIsOpen}
	<CreatePostModal bind:dialogCreatePost on:close={() => dialogIsOpen = false} />
{/if}

<nav id="navbar">
	<section class="header">
		<a href="/">
			<img src="{logo}" alt="project logo" />
			<h1>Storm</h1>
		</a>
	</section>
	<section class="content">
		<ul class="list">
			<li class="puce">
				<a href="/">
					<House />
					Home
				</a>
			</li>
			<li class="puce">
				<a href="/chat">
					<MessagesSquare />
					Chat
				</a>
			</li>
			<li class="puce">
				<button>
					<Search />
					Search
				</button>
			</li>
			<li class="puce">
				<button on:click={handleOpenModal}>
					<Plus />
					Post
				</button>
			</li>
		</ul>
	</section>
	<section class="footer">
		{#if showMenu}
			<div class="menu">
				<ul class="list">
					<li>
						<button on:click={() => AuthStore.logout()}>Logout</button>
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
		<button on:click={() => showMenu = !showMenu} class="user_logo">
			<img src="{logo}" alt="project logo" />
		</button>
	</section>
</nav>
