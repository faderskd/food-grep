<template>
    <div>
        <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#modal">Add new</button>

        <b-form @submit="onSubmit">
            <div class="modal fade" id="modal" tabindex="-1" role="dialog" aria-labelledby="modalLabel"
                 aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="modalLabel">Create Restaurant</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
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
                                        id="ur;"
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
                            <input type="submit" value="Create" class="btn btn-primary">
                        </div>
                    </div>
                </div>
            </div>
        </b-form>
    </div>
</template>

<script>
  import {Restaurant} from './model';
  import {ApiValidationError} from './lunch-client';

  export default {
    name: 'add-restaurant',
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
        form: {
          name: '',
          nameError: '',

          url: '',
          urlError: '',

          lunchRegex: '',
          lunchRegexError: '',

          imageUrlRegex: '',
          imageUrlRegexError: '',

          time: '',
          timeError: '',
        },
      };
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault();
        this.createRestaurant();
      },
      createRestaurant() {
        let restaurant = new Restaurant(this.form.name, this.form.url, this.form.lunchRegex, this.form.imageUrlRegex, this.form.time);
        try {
          this.lunchClient.createRestaurant(restaurant);
        } catch (e) {
          if (e instanceof ApiValidationError) {
            this.assignErrorsToFields(e.errors);
          } else {
            this.displayError(e.msg);
          }
        }
      },
      assignErrorsToFields(errors) {
        console.log(errors);
      },
      displayError(msg) {
        console.log(msg);
      },
    },
    computed: {
      nameValidation() {
        return this.form.nameError;
      },
      urlValidation() {
        return this.form.urlError;
      },
      lunchRegexValidation() {
        return this.form.lunchRegexError;
      },
      imageUrlRegexValidation() {
        return this.form.imageUrlRegexError;
      },
      timeValidation() {
        return this.form.timeError;
      },

    },
  };
</script>
