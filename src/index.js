import Vue from 'vue';
import VueRouter from 'vue-router';
import {BootstrapVue} from 'bootstrap-vue';
import App from './app.vue';
import './vendor';

Vue.use(VueRouter);
Vue.use(BootstrapVue);

import router from './router';

new Vue({
  router,
  template: '<App/>',
  components: {App},
}).$mount('#app');
