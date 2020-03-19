<template>
    <div class="container">
        <navbar></navbar>
        <div class="row">
            <div class="col col-sm-12">
                <add-restaurant-form :event-bus=eventBus :lunch-client=lunchClient></add-restaurant-form>
            </div>
            <div class="col col-sm-6">
                <restaurant-list :event-bus=eventBus :lunch-client=lunchClient></restaurant-list>
            </div>
        </div>
    </div>
</template>

<script>
  import Navbar from './navbar';
  import AddRestaurantForm from './add-restaurant';
  import RestaurantList from './restaurant-list';

  export default {
    props: {
      lunchClient: {
        required: true,
        type: Object,
      },
      eventBus: {
        required: true,
        type: Object,
      },
    },
    name: 'restaurnants',
    components: {Navbar, AddRestaurantForm, RestaurantList},
  };
</script>

<style scoped>

</style>
