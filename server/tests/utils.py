import unittest

from testcontainers.redis import RedisContainer

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

    def tearDown(self):
        self.database.remove_all()

    @classmethod
    def tearDownClass(cls):
        cls.container.stop()
