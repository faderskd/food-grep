<template>
    <div class="container">
        <div class="row">
            <div v-for="lunchInfo in this.lunchList">
                <div class="card">
                    <img class="card-img-top" src="" alt="">
                    <div class="card-body">
                        <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
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
        required: true
      },
    },
    data() {
      return {
        lunchList: this.lunchClient.fetchLunchesToday()
      }
    }
  }
</script>
