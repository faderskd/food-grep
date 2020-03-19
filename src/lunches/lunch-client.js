import LunchInfo from './lunch-info';
import {Restaurant} from './model';

const fetch = require('node-fetch');


class LunchClient {
  constructor(serverUrl) {
    this.serverUrl = serverUrl;
  }

  async fetchLunchesToday() {
    const response = await fetch(this.serverUrl + '/api/lunches-today');
    const json = await response.json();
    // eslint-disable-next-line max-len
    return json.map((info) => new LunchInfo(info.image, info.description, info.name));
  }

  async createRestaurant(restaurant) {
    await sendData(this.serverUrl + '/api/restaurants', restaurant.toDict());
  }

  async editRestaurant(restaurant) {
    // eslint-disable-next-line max-len
    await sendData(this.serverUrl + '/api/restaurants', restaurant.toDict(), 'PUT');
  }

  async getRestaurants() {
    return await getData(this.serverUrl + '/api/restaurants');
  }
}

async function sendData(url, data = {}, method = 'POST') {
  const options = {
    method: method,
    headers: {'Content-Type': 'application/json'},
  };
  if (data) {
    options['body'] = JSON.stringify(data);
  }
  const response = await fetch(url, options);

  if (response.status === 400) {
    const errorData = await response.json();
    throw new ApiValidationError(errorData['errors']);
  } else if (!response.status.ok) {
    throw new ApiUnknownError('Sorry, unknown error :(');
  }
  return response;
}

async function getData(url) {
  const options = {
    method: 'GET',
    headers: {'Content-Type': 'application/json'},
  };
  const response = await fetch(url, options);
  const json = await response.json();

  if (!response.ok) {
    throw new ApiUnknownError('Sorry unknown error :(');
  }
  return json.map(
    data => new Restaurant(
      data.name,
      data.url,
      data.requirements.lunch_regex,
      data.requirements.image_url_regex,
      data.requirements.time,
    ),
  );
}

class ApiUnknownError {
  constructor(msg) {
    this.msg = msg;
  }
}

class ApiValidationError {
  constructor(errors) {
    this.errors = errors;
  }
}

export {LunchClient, ApiValidationError, ApiUnknownError}