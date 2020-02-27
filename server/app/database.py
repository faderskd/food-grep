import json
import logging
from typing import List

import redis

from server.app.model import Lunch, Restaurant, parse_restaurants
from server.config.config import REDIS_HOST, REDIS_PORT

logger = logging.getLogger(__name__)

redis_client = redis.Redis(REDIS_HOST, REDIS_PORT, charset='utf-8', decode_responses=True)
redis_client.mset({'minute': 0, 'second': 0})


def get_cached_lunches(restaurant_list):
    for rest in restaurant_list:
        try:
            cached_lunch = lunch_or_none_when_not_exist(rest)
            if cached_lunch:
                yield cached_lunch
        except Exception as e:
            logger.exception('Failed to get lunch from redis for restaurant %s...' % str(rest), e)


def lunch_or_none_when_not_exist(rest):
    data = json.loads(redis_client.get(rest.name))
    if data:
        return Lunch.from_dict(data)


def save_lunch(lunch: Lunch):
    redis_client.set(lunch.name, json.dumps(lunch.to_dict()))


def save_restaurants(restaurants: List[Restaurant]):
    restaurants_list = [r.to_dict() for r in restaurants]
    redis_client.set('restaurants', json.dumps(restaurants_list))


def get_saved_restaurants():
    restaurants_data = json.loads(redis_client.get('restaurants'))
    return parse_restaurants(restaurants_data)
