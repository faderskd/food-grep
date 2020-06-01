import unittest
from unittest.mock import patch, MagicMock

from server.app import facebook_source
from server.app.model import Restaurant, RestaurantRequirements, Lunch


class TestFacebookSource(unittest.TestCase):
    def setUp(self):
        self.return_data = [
            {'text': 'Description with lunch word inside', 'time': '04/14/2020 15:16:18', 'image': ''},
            {'text': 'Description', 'time': '05/10/2020 15:30:25', 'image': ''}
        ]

    @patch('server.app.facebook_source.get_posts')
    def test_should_get_lunches_from_facebook_based_on_lunch_regex(self, mock: MagicMock):
        # given
        mock.return_value = self.return_data

        # when
        lunches = list(facebook_source.get_lunches_from_facebook(
            [Restaurant('testRestaurant', 'http://facebook.com/testRestaurant',
                        RestaurantRequirements('.*lunch.*', None, None))]))

        # then
        self.assertEqual(lunches,
                         [Lunch('testRestaurant', 'Description with lunch word inside', '', '04/14/2020 15:16:18')])

    @patch('server.app.facebook_source.get_posts')
    def test_should_get_lunches_from_facebook_based_on_time(self, mock: MagicMock):
        # given
        mock.return_value = self.return_data

        # when
        lunches = list(facebook_source.get_lunches_from_facebook(
            [Restaurant('testRestaurant', 'http://facebook.com/testRestaurant',
                        RestaurantRequirements(None, None, '30 15 * * *'))]))

        # then
        self.assertEqual(lunches,
                         [Lunch('testRestaurant', 'Description', '', '05/10/2020 15:30:25')])
