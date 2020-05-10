import logging
import re
from collections import namedtuple
from datetime import datetime

from crontab import CronTab
from facebook_scraper import get_posts

from server.app.utils import ignore_seconds
from server.app.model import Lunch
from server.config.config import FACEBOOK_SCRAPE_SLEEP, FACEBOOK_PAGES, FACEBOOK_URL, DEFAULT_LUNCH_PATTERN

logger = logging.getLogger(__name__)

Post = namedtuple('Post', ['text', 'time', 'image'])


def get_lunches_from_facebook(restaurant_list):
    for rest in restaurant_list:
        try:
            facebook_name = get_restaurant_name_from_facebook_url(rest.url)
            for post in fetch_facebook_restaurant_posts(facebook_name):
                if is_lunch(post, rest):
                    yield Lunch(rest.name, post.text, post.image, post.time)
                    break
        except Exception as e:
            logger.exception('Failed to search lunch for restaurant %s...' % str(rest), e)


def is_facebook(restaurant):
    return restaurant.url.startswith(FACEBOOK_URL)


def get_restaurant_name_from_facebook_url(url):
    return url[len(FACEBOOK_URL):].replace('/', '')


def fetch_facebook_restaurant_posts(restaurant_id):
    for post in list(get_posts(restaurant_id, pages=FACEBOOK_PAGES, sleep=FACEBOOK_SCRAPE_SLEEP)):
        yield Post(post['text'], post['time'], post['image'])


def is_lunch(post, restaurant):
    if restaurant.requirements.lunch_regex:
        return re.match(restaurant.requirements.lunch_regex, post.text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    if restaurant.requirements.time:
        return matches_time(post.time, restaurant.requirements.time)
    return DEFAULT_LUNCH_PATTERN.match(post.text)


def matches_time(time, expected_time):
    time = datetime.strptime(time, '%m/%d/%Y %H:%M:%S')
    return CronTab(expected_time).test(ignore_seconds(time))
