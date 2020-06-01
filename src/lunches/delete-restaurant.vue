<template>
    <div>
        <b-form @submit="onSubmit">
            <div class="modal fade" id="delete-restaurant-modal" tabindex="-1" role="dialog"
                 aria-labelledby="modalLabel"
                 aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="modalLabel">Delete Restaurant</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <div class="alert alert-danger" role="alert" v-if="otherErrorValidation">
                                {{ form.otherError }}
                            </div>
                            <p>Are you sure you want to delete restaurant
                                <strong>{{ this.form.restaurant.name }}</strong> ?</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <input type="submit" value="Delete" class="btn btn-primary">
                        </div>
                    </div>
                </div>
            </div>
        </b-form>
    </div>
</template>

<script>
  import {RestaurantDeletedEvent} from '../Events';
  import {RestaurantDeletedEvent} from '../Events';

  export default {
    name: 'delete-restaurant',
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
        form: this.createFormInstance({}),
      };
    },
    methods: {
      async onSubmit(evt) {
        evt.preventDefault();
        await this.deleteRestaurant();
      },
      async deleteRestaurant() {
        try {
          await this.lunchClient.deleteRestaurant(this.form.restaurant.name);
          this.closeFormModal();
          this.sendEvent(this.form.restaurant, this.form.listIndex);
        } catch (e) {
          this.displayOtherError(e.msg);
        }
      },
      displayOtherError(msg) {
        this.form.otherError = msg;
      },
      createFormInstance(restaurant, listIndex = -1) {
        return {
          restaurant: restaurant,
          listIndex: listIndex,
          otherError: '',
        };
      },
      closeFormModal() {
        $('#delete-restaurant-modal').modal('hide');
      },
      showFormModal() {
        $('#delete-restaurant-modal').modal('show');
      },
      sendEvent(restaurant, listIndex) {
        this.eventBus.$emit('restaurant-deleted', new RestaurantDeletedEvent(restaurant, listIndex));
      },
    },
    mounted() {
      this.eventBus.$on('restaurant-deleting', event => {
        this.form = this.createFormInstance(event.restaurant, event.listIndex);
        this.showFormModal();
      });
    },
    computed: {
      otherErrorValidation() {
        return this.form.otherError !== '';
      },
    },
  };
</script>
