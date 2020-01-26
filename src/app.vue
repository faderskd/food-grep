<template>
    <div>
        <router-link :to="{ name: 'LunchList' }">Lunches today </router-link>
        <router-view class="view"></router-view>
    </div>
</template>

<script>
  export default {
    name: 'app'
  }
</script>
