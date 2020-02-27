import json
import pathlib
from datetime import datetime

from server.app.model import RestaurantRequirements, Restaurant
from server.config.config import RESTAURANT_FILE

NOW_DATE_AS_STR = datetime.now().strftime('%m/%d/%Y')


def get_restaurants():
    main_path = pathlib.Path(__file__).parent.parent.absolute()
    file_path = f'{main_path}/config/{RESTAURANT_FILE}'
    restaurants = []
    with open(file_path) as f:
        for r in json.load(f)['restaurants']:
            requirements = RestaurantRequirements(
                lunch_regex=r['lunch_regex'] if 'lunch_regex' in r else None,
                image_url_regex=r['image_url_regex'] if 'image_url_regex' in r else None,
                time=get_restaurant_time_requirement(r))
            restaurants.append(Restaurant(r['name'], r['url'], requirements))
    return restaurants


def get_restaurant_time_requirement(r):
    if 'time' in r:
        date_str = "%s %s" % (NOW_DATE_AS_STR, r['time'])
        return datetime.strptime(date_str, '%m/%d/%Y %H:%M')
