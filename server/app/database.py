import logging

import redis

from server.app.lunches import Lunch
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
    lunch = redis_client.hmget(rest.name, 'description', 'image', 'time')
    if any(lunch):
        return Lunch(rest.name, lunch[0], lunch[1], lunch[2])
