from datetime import datetime


class Lunch:
    def __init__(self, name, description, image, time):
        self.name = name
        self.description = description
        self.image = image
        self.time = time

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'time': self.time.strftime('%m/%d/%Y %H:%M:%S')
        }

    @staticmethod
    def from_dict(data):
        name = data['name']
        description = data['description']
        image = data['image']
        time = data['time']
        return Lunch(name, description, image, time)

class RestaurantRequirements:
    def __init__(self, lunch_regex, image_url_regex, time):
        self.lunch_regex = lunch_regex
        self.image_url_regex = image_url_regex
        self.time = time

    def to_dict(self):
        return {
            'lunch_regex': self.lunch_regex,
            'image_url_regex': self.image_url_regex,
            'time': self.time_requirement_to_str()
        }

    def time_requirement_to_str(self):
        return "%s:%s" % (self.time.hour, self.time.second)

    @staticmethod
    def from_dict(data):
        lunch_regex = data.get('lunch_regex', None)
        image_url_regex = data.get('image_url_regex', None)
        time = data.get('time', None)
        if time:
            time = RestaurantRequirements.parse_time_requirement(time)
        return RestaurantRequirements(lunch_regex, image_url_regex, time)

    @staticmethod
    def parse_time_requirement(time):
        now_date_as_str = datetime.now().strftime('%m/%d/%Y')
        date_str = "%s %s" % (now_date_as_str, time)
        return datetime.strptime(date_str, '%m/%d/%Y %H:%M')


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
        name = data['name']
        url = data['url']
        requirements = RestaurantRequirements.from_dict(data['requirements'])
        return Restaurant(name, url, requirements)


def parse_restaurants(data):
    return [Restaurant.from_dict(d) for d in data]
