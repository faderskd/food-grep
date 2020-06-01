from datetime import datetime
from . import app_validators

CONSTANT_DATETIME = datetime.fromtimestamp(0)


class Lunch:
    def __init__(self, restaurant_name, description, image, time):
        self.restaurant_name = restaurant_name
        self.description = description
        self.image = image
        self.time = time

    def to_dict(self):
        return {
            'restaurant_name': self.restaurant_name,
            'description': self.description,
            'image': self.image,
            'time': self.time.strftime('%m/%d/%Y %H:%M:%S')
        }

    @staticmethod
    def from_dict(data):
        restaurant_name = data['restaurant_name']
        description = data['description']
        image = data['image']
        time = datetime.strptime(data['time'], '%m/%d/%Y %H:%M:%S')
        return Lunch(restaurant_name, description, image, time)

    def __eq__(self, other):
        return self.restaurant_name == other.restaurant_name and \
               self.description == other.description and \
               self.image == other.image and \
               self.time == other.time


class RestaurantRequirements:
    def __init__(self, lunch_regex, image_url_regex, time):
        self.lunch_regex = lunch_regex
        self.image_url_regex = image_url_regex
        self.time = time

    def to_dict(self):
        return {
            'lunchRegex': self.lunch_regex,
            'imageUrlRegex': self.image_url_regex,
            'time': self.time
        }

    @staticmethod
    def from_dict(data):
        lunch_regex = data.get('lunchRegex', '')
        image_url_regex = data.get('imageUrlRegex', '')
        time = data.get('time', '')
        return RestaurantRequirements(lunch_regex, image_url_regex, time)

    def __repr__(self):
        return str(self.to_dict())


class Restaurant:
    def __init__(self, name, url, requirements):
        self.name = name
        self.url = url
        self.requirements = requirements

    def to_dict(self):
        return {
            'name': self.name,
            'url': self.url,
            'requirements': self.requirements.to_dict()
        }

    @staticmethod
    def from_dict(data):
        app_validators.validate_restaurant(data)
        name = data['name']
        url = data['url']
        requirements = RestaurantRequirements.from_dict(data['requirements'])
        return Restaurant(name, url, requirements)

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return str(self.to_dict())


def parse_restaurant(data):
    return Restaurant.from_dict(data)


def parse_restaurants(data):
    restaurants = {}
    if not data:
        return restaurants
    for d in data:
        r = parse_restaurant(d)
        restaurants[d['name']] = r
    return restaurants
