import LunchClient from '../../src/lunches/lunch-client';
import LunchInfo from '../../src/lunches/lunch-info';

const mockServer = require('mockttp').getLocal();
const chai = require('chai');

const {expect} = chai;

describe('async/await functions in js', () => {
  const lunchClient = new LunchClient('http://localhost:9000');

  beforeEach(async () => {
    await mockServer.start(9000);
  });
  afterEach(async () => await mockServer.stop());

  it('should fetch tasks to do', async () => {
    // eslint-disable-next-line max-len
    const data = JSON.stringify({
      lunches: [
        {
          imageUrl: 'imageUrl1',
          description: 'Description lunch1',
          name: 'Munja',
        },
        {
          imageUrl: 'imageUrl2',
          description: 'Description lunch2',
          name: 'Zigi',
        }],
    });

    await mockServer.get('/lunches-today').thenReply(200, data);
    const lunches = await lunchClient.fetchLunchesToday();
    expect(lunches[0]).to.deep.equal(new LunchInfo('imageUrl1', 'Description lunch1', 'Munja'));
    expect(lunches[1]).to.deep.equal(new LunchInfo('imageUrl2', 'Description lunch2', 'Zigi'));
  });
});
