<template>
    <div class="container">
        <navbar></navbar>
        <div class="row">
            <div class="col col-sm-12">
                <add-restaurant-form :event-bus=eventBus :lunch-client=lunchClient></add-restaurant-form>
            </div>
            <div class="col col-sm-12">
                <edit-restaurant-form :event-bus=eventBus :lunch-client=lunchClient></edit-restaurant-form>
            </div>
            <div class="col col-sm-12">
                <delete-restaurant-form :event-bus=eventBus :lunch-client=lunchClient></delete-restaurant-form>
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
  import EditRestaurantForm from './edit-restaurant';
  import RestaurantList from './restaurant-list';
  import DeleteRestaurantForm from './delete-restaurant';

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
    components: {Navbar, AddRestaurantForm, EditRestaurantForm, RestaurantList, DeleteRestaurantForm},
  };
</script>

<style scoped>

</style>
