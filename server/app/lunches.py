import json
import pathlib
from collections import namedtuple

from server.config.config import RESTAURANT_FILE

Lunch = namedtuple('Lunch', ['name', 'description', 'image', 'time'])

Restaurant = namedtuple('Restaurant', ['name', 'url', 'lunch_regex'])


def get_restaurants():
    main_path = pathlib.Path(__file__).parent.parent.absolute()
    file_path = f'{main_path}/config/{RESTAURANT_FILE}'
    with open(file_path) as f:
        return [Restaurant(r['name'], r['url'], r['lunch_regex'] if 'lunch_regex' in r else None)
                for r in json.load(f)['restaurants']]
