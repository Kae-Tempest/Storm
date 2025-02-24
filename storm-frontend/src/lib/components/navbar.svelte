<script>
    import logo from "$lib/assets/logo.png";
    import {AuthStore} from "$lib/stores/login/login.js";

    let showMenu = false;
</script>

<nav class="h-full max-w-2xs border-r border-r-blue-900 flex flex-col justify-between sticky">
    <section>
        <a href="/" class="flex w-full items-center">
            <img src="{logo}" alt="project logo" class="max-w-[123px]"/>
            <h1 class="text-4xl px-4 font-black font-[Arial]">Storm</h1>
        </a>
    </section>
    <section class="flex flex-col w-full items-center font-black font-[Arial]">
        <ul class="h-full flex flex-col text-center gap-10 text-2xl">
            <li><a href="/home">HOME</a></li>
            <li><a href="/chat">CHAT</a></li>
            <li>
                <button>SEARCH</button>
            </li>
            <li>
                <button>POST</button>
            </li>
        </ul>
    </section>
    <section class="flex w-full justify-center">
        {#if showMenu}
            <div class="absolute bottom-30 left-13 rounded p-5 text-xl w-2/3 text-center
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
            <img src="{logo}" alt="project logo" class="max-w-[123px]"/>
        </button>
    </section>
</nav>