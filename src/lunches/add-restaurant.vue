<template>
    <b-form @submit="onSubmit">
        <h4> Add new restaurant </h4>
        <b-form-group
                label="Name"
                label-for="name">
            <b-form-input
                    id="name"
                    v-model="form.name"
                    required
                    placeholder="Restaurant name"></b-form-input>
            <b-form-invalid-feedback :state="nameValidation">
                {{nameError}}
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
                {{lunchRegexError}}
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
                {{imageUrlRegexError}}
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
                {{timeError}}
            </b-form-invalid-feedback>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
    </b-form>
</template>

<script>
  export default {
    name: 'add-restaurant',
    props: {
      restaurantList: {
        required: true,
        type: Array
      },
      lunchClient: {
        required: true,
        type: Object
      }
    },
    data() {
      return {
        form: {
          name: '',
          nameError: '',

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
      },
      createRestaurant() {
        this.validate();
        let restaurant = new Restaurant(this.form.name, this.form.lunchRegex, this.form.imageUrlRegex, this.form.time);
        this.lunchClient.createRestaurant(restaurant);
        this.restaurantList.push(restaurant);
      },
      validate() {

      }
    },
    computed: {
      nameValidation() {
        return this.nameError;
      },
      lunchRegexValidation() {
        return this.lunchRegexError;
      },
      imageUrlRegexValidation() {
        return this.imageUrlRegexError;
      },
      timeValidation() {
        return this.timeError;
      },

    },
  };
</script>
