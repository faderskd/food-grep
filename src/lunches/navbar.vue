<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Lunches today</a>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item active">
                    <router-link class="nav-link" to="home">Lunches</router-link>
                </li>
                <li class="nav-item active">
                    <router-link class="nav-link" to="restaurants">Restaurants</router-link>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
  export default {
    name: 'navbar',
  };
</script>

<style scoped>
</style>
