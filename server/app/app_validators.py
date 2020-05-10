import re
from collections import defaultdict
from crontab import CronTab
import validators


def validate_restaurant(data):
    errors = {}
    if 'name' not in data or not data['name']:
        errors['name'] = 'Name is required'

    if 'url' not in data or not data['url']:
        errors['url'] = 'Url is required'
    elif not validators.url(data['url']):
        errors['url'] = 'Invalid url'

    if 'requirements' not in data or not isinstance(data['requirements'], dict):
        errors['requirements'] = 'Requirements are required'
    else:
        errors.update(validate_requirements(data['requirements']))
    if errors:
        raise RestaurantValidationErrorException(errors)


def validate_requirements(data):
    errors = defaultdict(dict)
    lunch_regex = data.get('lunchRegex')
    image_url_regex = data.get('imageUrlRegex')
    time = data.get('time')

    if not lunch_regex and not image_url_regex and not time:
        errors['requirements'] = 'At least one of the fields [lunchRegex, imageUrlRegex, time] is required'

    try:
        if lunch_regex:
            re.compile(lunch_regex)
    except Exception as e:
        errors['requirements']['lunchRegex'] = 'Invalid regex'

    try:
        if image_url_regex:
            re.compile(image_url_regex)
    except Exception as e:
        errors['requirements']['imageUrlRegex'] = 'Invalid regex'

    try:
        if time:
            CronTab(time)
    except Exception as e:
        errors['requirements']['time'] = str(e)

    return errors


class RestaurantValidationErrorException(Exception):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors

    def __str__(self):
        return 'RestaurantValidationErrorException(errors=%s)' % self.errors
