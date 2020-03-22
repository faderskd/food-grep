import unittest

from testcontainers.redis import RedisContainer

from server.app.model import Restaurant, RestaurantRequirements
from ..config import config
from server.app import app_factory


class BaseIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.container = RedisContainer()
        cls.container.start()
        config.REDIS_PORT = cls.container.get_exposed_port(6379)

    def setUp(self):
        app, database = app_factory.create_app_with_dependencies(app_config=config)
        self.database = database
        self.test_client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.container.stop()


class RestaurantsTest(BaseIntegrationTest):
    def setUp(self):
        super().setUp()
        self.restaurant_data = {'name': 'test_restaurant', 'url': 'http://folkgospoda.pl',
                                'requirements': {'lunchRegex': '*lunch*'}}

    def test_should_create_restaurant(self):
        # when
        response = self.test_client.post('/api/restaurants', json=self.restaurant_data)

        # then
        self.assertEqual(response.status_code, 200)

        # and
        self.assertEqual(self.database.get_saved_restaurants(),
                         [
                             Restaurant('test_restaurant', 'http://folkgospoda.pl',
                                        RestaurantRequirements('*lunch*', '', ''))
                         ])
