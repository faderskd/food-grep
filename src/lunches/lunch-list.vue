<template>
    <div class="container">
        <div class="row row-cols-2">
            <div class="col" v-for="lunchInfo in this.lunchList">
                <div class="card">
                    <img v-bind:src="lunchInfo.imageUrl" class="card-img-top" v-bind:alt="lunchInfo.name + ' photo'">
                    <div class="card-body">
                        <h5 class="card-title">{{lunchInfo.name}}</h5>
                        <p class="card-text">{{lunchInfo.description}}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
  export default {
    props: {
      lunchClient: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        lunchList: [],
      };
    },
    async created() {
      this.lunchList = await this.lunchClient.fetchLunchesToday();
    },
  };
</script>

<style>
    img {
        max-height: 200px;
        object-fit: cover;
    }
</style>
