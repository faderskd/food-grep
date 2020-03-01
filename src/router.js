import VueRouter from 'vue-router';
import LunchListComponent from './lunches/lunch-list';
import EditLunchesComponent from './lunches/restaurants';
import Config from './config';

const router = new VueRouter({
  base: __dirname,
  routes: [
    {
      path: '/lunches',
      name: 'LunchList',
      component: LunchListComponent,
      props: {
        lunchClient: Config.lunchClient,
      },
    },
    {
      path: '/restaurants',
      name: 'EditLunches',
      component: EditLunchesComponent,
      props: {
        lunchClient: Config.lunchClient,
      },
    },
    {
      path: '*',
      name: 'Default',
      component: LunchListComponent,
      props: {
        lunchClient: Config.lunchClient,
      },
    },
  ],
});

export default router;
