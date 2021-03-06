import LunchInfo from './lunch-info';
import {Restaurant} from './model';

const fetch = require('node-fetch');


class LunchClient {
  constructor(serverUrl) {
    this.serverUrl = serverUrl;
    this.restaurantsPath = '/api/restaurants';
  }

  async fetchLunchesToday() {
    let json = await getData(this.serverUrl + '/api/lunches-today');
    return json.map(
      info => new LunchInfo(
        info.imageUrl,
        info.description,
        info.restaurantName,
        info.time),
    );
  }

  async createRestaurant(restaurant) {
    await sendData(this.serverUrl + this.restaurantsPath, restaurant.toDict());
  }

  async editRestaurant(restaurant) {
    // eslint-disable-next-line max-len
    await sendData(this.serverUrl + this.restaurantsPath, restaurant.toDict(), 'PUT');
  }

  async deleteRestaurant(restaurantName) {
    await sendData(this.serverUrl + this.restaurantsPath + '/' + restaurantName, {}, 'DELETE');
  }

  async getRestaurants() {
    let json = await getData(this.serverUrl + this.restaurantsPath);
    return json.map(
      data => new Restaurant(
        data.name,
        data.url,
        data.requirements.lunchRegex,
        data.requirements.imageUrlRegex,
        data.requirements.time,
      ),
    );
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
    throw buildProperException(errorData);
  } else if (!response.ok) {
    console.warn('Response status : ' + response.status);
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
  return json;
}

class ApiUnknownError {
  constructor(msg) {
    this.msg = msg;
  }
}

class RestaurantValidationError {
  constructor(msg) {
    this.msg = msg;
  }
}

class RestaurantFieldsValidationError {
  constructor(errors) {
    this.errors = errors;
  }

}

function buildProperException(data) {
  if (data['code'] === 'RESTAURANT_VALIDATION_ERROR') {
    return new RestaurantFieldsValidationError(data['errors']);
  } else {
    return new RestaurantValidationError(data['error']);
  }
}

export {
  LunchClient,
  RestaurantValidationError,
  RestaurantFieldsValidationError,
  ApiUnknownError,
};