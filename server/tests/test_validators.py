import unittest
from server.app import validators
from server.app.validators import RestaurantValidationErrorException


class RestaurantValidatorTest(unittest.TestCase):
    def setUp(self):
        self.data = {'name': 'test', 'url': 'http://www.testdomain.com',
                     'requirements': {'lunchRegex': '*lunch*', 'time': '*/2 * * * *'}}

    def test_should_throw_no_errors_when_restaurant_data_is_valid(self):
        # expect no exception
        validators.validate_restaurant(self.data)

    def test_should_throw_error_when_no_name_is_given(self): \
            # given
        self.data.pop('name')

        # expect
        with self.assertRaises(RestaurantValidationErrorException) as e:
            validators.validate_restaurant(self.data)

        self.assertEqual(e.exception.errors, {'name': 'Name is required'})

    def test_should_throw_error_when_no_url_is_given(self):
        # given
        self.data.pop('url')

        # expect
        with self.assertRaises(RestaurantValidationErrorException) as e:
            validators.validate_restaurant(self.data)

        self.assertEqual(e.exception.errors, {'url': 'Url is required'})

    def test_should_throw_error_when_no_requirements_is_given(self):
        # given
        self.data.pop('requirements')

        # expect
        with self.assertRaises(RestaurantValidationErrorException) as e:
            validators.validate_restaurant(self.data)

        self.assertEqual(e.exception.errors,
                         {'requirements': 'Requirements are required'})

    def test_should_throw_error_when_no_requirements_are_empty(self):
        # given
        self.data['requirements'] = {}

        # expect
        with self.assertRaises(RestaurantValidationErrorException) as e:
            validators.validate_restaurant(self.data)

        self.assertEqual(e.exception.errors,
                         {'requirements': 'At least one of the fields [lunchRegex, imageUrlRegex, time] is required'})

    def test_should_throw_error_when_url_is_invalid(self):
        # given
        self.data['url'] = 'invalid url'

        # expect
        with self.assertRaises(RestaurantValidationErrorException) as e:
            validators.validate_restaurant(self.data)

        self.assertEqual(e.exception.errors, {'url': 'Invalid url'})

    def test_should_throw_error_when_time_is_invalid_cron(self):
        # given
        self.data['requirements']['time'] = '* * * *'

        # expect
        with self.assertRaises(RestaurantValidationErrorException) as e:
            validators.validate_restaurant(self.data)

        self.assertEqual(e.exception.errors,
                         {'time': 'improper number of cron entries specified; got 4 need 5 to 7'})
