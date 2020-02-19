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
}
