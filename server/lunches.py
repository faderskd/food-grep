import json
from collections import namedtuple

from server.config import RESTAURANT_FILE


Lunch = namedtuple('Lunch', ['name', 'description', 'image', 'time'])

Restaurant = namedtuple('Restaurant', ['name', 'url', 'lunch_regex'])


def get_restaurants():
    with open(RESTAURANT_FILE) as f:
        return [Restaurant(r['name'], r['url'], r['lunch_regex'] if 'lunch_regex' in r else None)
                for r in json.load(f)['restaurants']]
