<script setup lang="ts">
</script>

<template>

<div class="app-shell">

    <header>
        <h1>
            Energy Management Dashboard
        </h1>

        <nav class="app-tabs">
            <RouterLink
                to="/"
                :class="['app-tab', $route.path === '/' ? 'app-tab-active' : '']"
            >
                Assets
            </RouterLink>
            <RouterLink
                to="/market"
                :class="['app-tab', $route.path === '/market' ? 'app-tab-active' : '']"
            >
                Market
            </RouterLink>
        </nav>
    </header>

    <main>
        <RouterView />
    </main>

</div>

</template>


<style scoped>

.app-shell {

    display: flex;

    flex-direction: column;

    min-height: 100vh;

}


header {

    padding: 1rem 1rem 0 1rem;

}


.app-tabs {

    display: flex;

    gap: 0.25rem;

    border-bottom: 1px solid #d0d0d0;

}


.app-tab {

    padding: 0.5rem 1.25rem;

    border: 1px solid #d0d0d0;

    border-bottom: none;

    border-radius: 6px 6px 0 0;

    margin-bottom: -1px;

    background: #f5f5f5;

    color: #333;

    text-decoration: none;

}


.app-tab-active {

    background: #ffffff;

    font-weight: 600;

    color: #111;

}


main {

    flex: 1;

    padding: 1rem;

}

</style>
