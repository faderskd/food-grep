<template>
    <div>
        <b-form @submit="onSubmit">
            <div class="modal fade" id="edit-restaurant-modal" tabindex="-1" role="dialog" aria-labelledby="modalLabel"
                 aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="modalLabel">Edit Restaurant</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <div class="alert alert-danger" role="alert" v-if="otherErrorValidation">
                                {{ form.otherError }}
                            </div>
                            <b-form-group
                                    label="Name"
                                    label-for="name">
                                <b-form-input
                                        id="name"
                                        v-model="form.name"
                                        required
                                        placeholder="Restaurant name"></b-form-input>
                                <b-form-invalid-feedback :state="nameValidation">
                                    {{form.nameError}}
                                </b-form-invalid-feedback>
                            </b-form-group>

                            <b-form-group
                                    label="Url"
                                    label-for="url">
                                <b-form-input
                                        id="url"
                                        v-model="form.url"
                                        required
                                        placeholder="Url to scrape"></b-form-input>
                                <b-form-invalid-feedback :state="urlValidation">
                                    {{form.urlError}}
                                </b-form-invalid-feedback>
                            </b-form-group>

                            <b-form-group
                                    label="Lunch regex"
                                    label-for="lunchRegex">
                                <b-form-input
                                        id="lunchRegex"
                                        v-model="form.lunchRegex"
                                        placeholder="Lunch regex required to classify text as lunch"
                                ></b-form-input>
                                <b-form-invalid-feedback :state="lunchRegexValidation">
                                    {{form.lunchRegexError}}
                                </b-form-invalid-feedback>
                            </b-form-group>

                            <b-form-group
                                    label="Image url regex"
                                    label-for="imageUrlRegex">
                                <b-form-input
                                        id="imageUrlRegex"
                                        v-model="form.imageUrlRegex"
                                        placeholder="Image url regex required to classify image as lunch"
                                ></b-form-input>
                                <b-form-invalid-feedback :state="imageUrlRegexValidation">
                                    {{form.imageUrlRegexError}}
                                </b-form-invalid-feedback>
                            </b-form-group>

                            <b-form-group
                                    label="Time"
                                    label-for="time">
                                <b-form-input
                                        id="time"
                                        v-model="form.time"
                                        placeholder="Time of lunch post publication"
                                ></b-form-input>
                                <b-form-invalid-feedback :state="timeValidation">
                                    {{form.timeError}}
                                </b-form-invalid-feedback>
                            </b-form-group>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <input type="submit" value="Edit" class="btn btn-primary">
                        </div>
                    </div>
                </div>
            </div>
        </b-form>
    </div>
</template>

<script>
  import {Restaurant} from './model';
  import {RestaurantFieldsValidationError} from './lunch-client';
  import {RestaurantEditedEvent} from '../Events';

  export default {
    name: 'edit-restaurant',
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
        await this.editRestaurant();
      },
      async editRestaurant() {
        let restaurant = new Restaurant(this.form.name, this.form.url, this.form.lunchRegex, this.form.imageUrlRegex, this.form.time);
        try {
          await this.lunchClient.editRestaurant(restaurant);
          this.closeFormModal();
          this.sendEvent(restaurant);
        } catch (e) {
          if (e instanceof RestaurantFieldsValidationError) {
            this.assignErrorsToFields(e.errors);
          } else {
            this.displayOtherError(e.msg);
          }
        }
      },
      assignErrorsToFields(errors) {
        if (errors['name']) {
          this.form.nameError = errors['name'];
        }
        if (errors['url']) {
          this.form.urlError = errors['url'];
        }
        if (errors['requirements'] && typeof errors['requirements'] === 'string') {
          this.form.otherError = errors['requirements'];
        } else if (errors['requirements']) {
          Object.keys(errors['requirements']).forEach((field) => {
            this.form[field + 'Error'] = errors['requirements'][field];
          });
        }
      },
      displayOtherError(msg) {
        this.form.otherError = msg;
      },
      createFormInstance(restaurant) {
        return {
          name: restaurant.name,
          nameError: '',

          url: restaurant.url,
          urlError: '',

          lunchRegex: restaurant.lunchRegex,
          lunchRegexError: '',

          imageUrlRegex: restaurant.imageURL,
          imageUrlRegexError: '',

          time: restaurant.time,
          timeError: '',

          otherError: '',
        };
      },
      closeFormModal() {
        $('#edit-restaurant-modal').modal('hide');
      },
      showFormModal() {
        $('#edit-restaurant-modal').modal('show');
      },
      sendEvent(restaurant) {
        this.eventBus.$emit('restaurant-edited', new RestaurantEditedEvent(restaurant));
      },
    },
    computed: {
      nameValidation() {
        return this.form.nameError === '';
      },
      urlValidation() {
        return this.form.urlError === '';
      },
      lunchRegexValidation() {
        return this.form.lunchRegexError === '';
      },
      imageUrlRegexValidation() {
        return this.form.imageUrlRegexError === '';
      },
      timeValidation() {
        return this.form.timeError === '';
      },
      otherErrorValidation() {
        return this.form.otherError !== '';
      },
    },
    mounted() {
      this.eventBus.$on('restaurant-editing', event => {
        this.form = this.createFormInstance(event.restaurant);
        this.showFormModal();
      });
    },
  };
</script>
