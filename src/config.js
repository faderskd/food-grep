import Vue from 'vue';

import {LunchClient} from './lunches/lunch-client';

const EventBus = new Vue();


export default {
  lunchClient: new LunchClient('http://localhost:8001/http://localhost:8000'),
  eventBus: EventBus
};
