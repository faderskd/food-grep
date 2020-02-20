import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './app.vue';
import './vendor';

Vue.use(VueRouter);

import router from './router';

new Vue({
  router,
  template: '<App/>',
  components: {App},
}).$mount('#app');
