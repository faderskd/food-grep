import json
import logging

from server.app.model import Lunch, Restaurant, parse_restaurants

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def get_cached_lunches(self, restaurant_list):
        for rest in restaurant_list:
            try:
                cached_lunch = self.lunch_or_none_when_not_exist(rest)
                if cached_lunch:
                    yield cached_lunch
            except Exception as e:
                logger.exception('Failed to get lunch from redis for restaurant %s...' % str(rest), e)

    def lunch_or_none_when_not_exist(self, rest):
        rest_data = self.redis_client.get(rest.name)
        data = json.loads(rest_data) if rest_data else None
        if data:
            return Lunch.from_dict(data)

    def save_lunch(self, lunch: Lunch):
        self.redis_client.set(lunch.restaurant_name, json.dumps(lunch.to_dict()))

    def create_restaurant(self, restaurant: Restaurant):
        existing_list = self.get_saved_restaurants()
        if restaurant in existing_list:
            raise RestaurantAlreadyExistsException("Restaurant %s already exists" % restaurant.name)

        existing_list.append(restaurant)
        to_save = [r.to_dict() for r in existing_list]
        self.redis_client.set('restaurants', json.dumps(to_save))

    def edit_restaurant(self, restaurant: Restaurant):
        existing_list = self.get_saved_restaurants()
        if restaurant not in existing_list:
            raise RestaurantDoesNotExist("Restaurant %s does not exist" % restaurant.name)

        replace_in_list(restaurant, existing_list)
        to_save = [r.to_dict() for r in existing_list]
        self.redis_client.set('restaurants', json.dumps(to_save))

    def get_saved_restaurants(self):
        restaurants_data = self.redis_client.get('restaurants')
        restaurants = json.loads(restaurants_data) if restaurants_data else []
        return parse_restaurants(restaurants)


def replace_in_list(restaurant, restaurant_list):
    index = restaurant_list.index(restaurant)
    restaurant_list[index] = restaurant


class RestaurantAlreadyExistsException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class RestaurantDoesNotExist(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg
