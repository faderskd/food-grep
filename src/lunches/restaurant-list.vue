<template>
    <div class="accordion" id="restaurantsCollapse">
        <div v-for="(rest, index) in restaurantList" class="card">
            <div class="card-header" :id="'heading' + index">
                <h2 class="mb-0">
                    <button class="btn btn-link" type="button" data-toggle="collapse" :data-target="'#collapse' + index"
                            aria-expanded="true" aria-controls="collapseOne">
                        {{rest.name}}
                    </button>
                    <a href="#">
                        <span v-on:click="emitRestaurantEditingEvent(rest, index)" style=" font-size: 20px;">
                        <i class="fa fa-pencil"></i>
                        </span>
                    </a>
                </h2>
            </div>

            <div :id="'collapse' + index" class="collapse"
                 data-parent="#restaurantsCollapse">
                <div class="card-body">
                    {{rest.url}}
                    {{rest.lunchRegex}}
                    {{rest.imageUrlRegex}}
                    {{rest.time}}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
  import {RestaurantEditingEvent} from '../Events';

  export default {
    name: 'RestaurantList',
    props: {
      eventBus: {
        required: true,
        type: Object,
      },
      lunchClient: {
        required: true,
        type: Object,
      },
    },
    data() {
      return {
        restaurantList: [],
      };
    },
    async mounted() {
      this.restaurantList = await this.lunchClient.getRestaurants();
      this.eventBus.$on('restaurant-created', event => {
        if (!this.restaurantList.includes(event.restaurant)) {
          this.restaurantList.push(event.restaurant);
        }
      });
    },
    methods: {
      emitRestaurantEditingEvent(restaurant, index) {
        this.eventBus.$emit('restaurant-editing', new RestaurantEditingEvent(restaurant, index));
      },
    },
  };
</script>

<style scoped>

</style>