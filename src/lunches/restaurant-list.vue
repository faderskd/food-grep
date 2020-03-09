<template>
    <div class="accordion" id="restaurantsCollapse">
        <div v-for="(rest, index) in items" class="card">
            <div class="card-header" :id="'heading' + index">
                <h2 class="mb-0">
                    <button class="btn btn-link" type="button" data-toggle="collapse" :data-target="'#collapse' + index"
                            aria-expanded="true" aria-controls="collapseOne">
                        Restaurant {{index}}
                    </button>
                </h2>
            </div>

            <div :id="'collapse' + index" class="collapse"
                 data-parent="#restaurantsCollapse">
                <div class="card-body">
                    Restaurant {{index}} description
                </div>
            </div>
        </div>
    </div>
</template>

<script>
  export default {
    name: 'RestaurantList',
    props: {
      restaurantList: {
        required: true,
        type: Array,
      },
      lunchClient: {
        required: true,
        type: Object,
      },
    },
    data() {
      return {
        items: [1, 2, 3],
      };
    },
  };
</script>

<style scoped>

</style>