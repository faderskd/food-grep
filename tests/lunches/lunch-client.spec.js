import LunchInfo from '../../src/lunches/lunch-info';
import {Restaurant} from '../../src/lunches/model';
import {LunchClient} from '../../src/lunches/lunch-client';

const mockServer = require('mockttp').getLocal();
const chai = require('chai');

const {expect} = chai;

describe('async/await functions in js', () => {
  const lunchClient = new LunchClient('http://localhost:9005');

  beforeEach(async () => {
    await mockServer.start(9005);
  });
  afterEach(async () => await mockServer.stop());

  it('should fetch restaurants', async () => {
    // given
    const data = JSON.stringify([{
      'name': 'test_restaurant', 'url': 'http://folkgospoda.pl',
      'requirements': {
        'lunchRegex': '*lunch*',
        'imageUrlRegex': '',
        'time': '',
      },
    }]);

    // when
    await mockServer.get('/api/restaurants').thenReply(200, data);
    const restaurants = await lunchClient.getRestaurants();

    // then
    expect(restaurants[0]).to.deep.equal(new Restaurant('test_restaurant', 'http://folkgospoda.pl',
      '*lunch*', '', ''));
  });

  it('should create restaurant', async () => {
    // given
    const data = JSON.stringify({
      'name': 'test_restaurant',
      'url': 'http://folkgospoda.pl',
      'requirements':
        {
          'lunchRegex': '*lunch*',
          'imageUrlRegex': '',
          'time': '',
        },
    });

    await mockServer.post('/api/restaurants').withBody(data).thenReply(200);

    // when
    await lunchClient.createRestaurant(new Restaurant('test_restaurant',
      'http://folkgospoda.pl', '*lunch*', '', ''));
  });

  it('should fetch lunches', async () => {
    const data = JSON.stringify([
      {
        imageUrl: 'imageUrl1',
        description: 'Description lunch1',
        restaurantName: 'Munja',
        time: '04/14/2020 15:16:18',
      },
      {
        imageUrl: 'imageUrl2',
        description: 'Description lunch2',
        restaurantName: 'Zigi',
        time: '04/14/2020 15:16:18',
      },
    ]);

    await mockServer.get('/api/lunches-today').thenReply(200, data);
    const lunches = await lunchClient.fetchLunchesToday();
    expect(lunches[0]).to.deep.equal(new LunchInfo('imageUrl1', 'Description lunch1', 'Munja', '04/14/2020 15:16:18'));
    expect(lunches[1]).to.deep.equal(new LunchInfo('imageUrl2', 'Description lunch2', 'Zigi', '04/14/2020 15:16:18'));
  });
});
