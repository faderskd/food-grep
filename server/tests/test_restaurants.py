from server.tests.utils import BaseIntegrationTest


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
        self.assertEqual(self.test_client.get('/api/restaurants').get_json(),
                         [
                             {'name': 'test_restaurant', 'url': 'http://folkgospoda.pl',
                              'requirements': {'lunchRegex': '*lunch*', 'imageUrlRegex': '', 'time': ''}}
                         ])

    def test_should_edit_restaurant(self):
        # given
        self.test_client.post('/api/restaurants', json=self.restaurant_data)

        # when
        self.restaurant_data.update({'requirements': {'lunchRegex': '*lunch today*', 'time': '09:00'}})
        self.test_client.put('/api/restaurants', json=self.restaurant_data)

        # then
        self.assertEqual(self.test_client.get('/api/restaurants').get_json(),
                         [
                             {'name': 'test_restaurant', 'url': 'http://folkgospoda.pl',
                              'requirements': {'lunchRegex': '*lunch today*', 'imageUrlRegex': '', 'time': '09:00'}}
                         ])

    def test_should_throw_error_when_restaurant_already_exists(self):
        # given
        self.test_client.post('/api/restaurants', json=self.restaurant_data)

        # when
        response = self.test_client.post('/api/restaurants', json=self.restaurant_data)

        # then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(),
                         {'error': 'Restaurant test_restaurant already exists', 'code': 'RESTAURANT_ALREADY_EXISTS'})

    def test_should_throw_error_when_restaurant_does_not_exists(self):
        # when
        response = self.test_client.put('/api/restaurants', json=self.restaurant_data)

        # then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(),
                         {'error': 'Restaurant test_restaurant does not exist', 'code': 'RESTAURANT_DOES_NOT_EXIST'})

    def test_should_throw_validation_error_when_given_bad_data_during_restaurant_creation(self):
        # given
        data = {'requirements': {}}

        # when
        response = self.test_client.post('/api/restaurants', json=data)

        # then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(),
                         {'code': 'RESTAURANT_VALIDATION_ERROR',
                          'errors': {'name': 'Name is required', 'url': 'Url is required',
                                     'requirements': 'At least one of the fields [lunchRegex, imageUrlRegex, time] is required'}})

        # when
        data = {}
        response = self.test_client.post('/api/restaurants', json=data)

        # then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(),
                         {'code': 'RESTAURANT_VALIDATION_ERROR',
                          'errors': {'name': 'Name is required',
                                     'url': 'Url is required',
                                     'requirements': 'Requirements are required'}})


        def test_should_throw_validation_error_when_given_bad_data_during_restaurant_edition(self):
            # given
            data = {'requirements': {}}

            # when
            response = self.test_client.post('/api/restaurants', json=data)

            # then
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json(),
                             {'code': 'RESTAURANT_VALIDATION_ERROR',
                              'errors': {'name': 'Name is required', 'url': 'Url is required',
                                         'requirements': 'At least one of the fields [lunchRegex, imageUrlRegex, time] is required'}})

            # when
            data = {}
            response = self.test_client.post('/api/restaurants', json=data)

            # then
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.get_json(),
                             {'code': 'RESTAURANT_VALIDATION_ERROR',
                              'errors': {'name': 'Name is required',
                                         'url': 'Url is required',
                                         'requirements': 'Requirements are required'}})
