<template>
    <div class="container">
        <navbar></navbar>
        <div class="row">
            <div class="col-sm-6">
                <add-restaurant-form></add-restaurant-form>
            </div>
            <div class="col-sm-6">
                <restaurant-list></restaurant-list>
            </div>
        </div>
    </div>
</template>

<script>
  import Navbar from './navbar';
  import AddRestaurantForm from './add-restaurant';
  import RestaurantList from './restaurant-list';

  export default {
    name: 'restaurnants',
    components: {Navbar, AddRestaurantForm, RestaurantList},
  };
</script>

<style scoped>

</style>
