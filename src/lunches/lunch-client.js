import LunchInfo from './lunch-info';

const fetch = require('node-fetch');


export default class LunchClient {
  constructor(serverUrl) {
    this.serverUrl = serverUrl;
  }

  async fetchLunchesToday() {
    let response = await fetch(this.serverUrl + '/api/lunches-today');
    let json = await response.json();
    return json.map(info => new LunchInfo(info.image, info.description, info.name));
  }

  async createRestaurant(restaurant) {
    await sendData(this.serverUrl + '/api/restaurants', restaurant.toDict());
  }

  async editRestaurant(restaurant) {
    await sendData(this.serverUrl + '/api/restaurants', restaurant.toDict(), 'PUT');
  }
}

async function sendData(url, data = {}, method = 'POST') {
  let options = {
    method: method,
    headers: {'Content-Type': 'application/json'},
  };
  if (data) {
    options['body'] = JSON.stringify(data);
  }
  let response = await fetch(url, options);

  if (response.status === 400) {
    let errorData = await response.json();
    throw new ApiError(errorData['error']);
  } else if (!response.status.ok) {
    throw new ApiError('Sorry, unknown error :(');
  }
  return response;
}

class ApiError {
  constructor(msg) {
    this.msg = msg;
  }

}
