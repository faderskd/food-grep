import re
import json
import logging
from collections import namedtuple

import redis
from celery import Celery
from flask import Flask
from facebook_scraper import get_posts

app = Flask(__name__)

# @app.route('api/lunches-today')
# def fetch_lunches():
#     pass

COMMON_LUNCH_PHRASES = 'lunch,obiad'
DEFAULT_LUNCH_PATTERN = re.compile('|'.join(COMMON_LUNCH_PHRASES.split(',')))

FACEBOOK_URL = 'FACEBOOK_URL'
FACEBOOK_PAGES = 'FACEBOOK_PAGES'
FACEBOOK_SCRAPE_SLEEP = 'FACEBOOK_SCRAPE_SLEEP'
REDIS_PORT = 'REDIS_PORT'
REDIS_HOST = 'REDIS_HOST'
CELERY_BROKER_URL = 'CELERY_BROKER_URL'
CELERY_RESULT_BACKEND = 'CELERY_RESULT_BACKEND'

app.config[FACEBOOK_URL] = 'https://www.facebook.com'
app.config[FACEBOOK_PAGES] = 2
app.config[FACEBOOK_SCRAPE_SLEEP] = 1
app.config[REDIS_PORT] = 6379
app.config[REDIS_HOST] = 'localhost'
app.config[CELERY_BROKER_URL] = 'redis://localhost:6379/0'
app.config[CELERY_RESULT_BACKEND] = 'redis://localhost:6379/0'

database = redis.Redis(app.config[REDIS_HOST], app.config[REDIS_PORT], charset='utf-8', decode_responses=True)
database.mset({'minute': 0, 'second': 0})

celery_beat_schedule = {
    'add-every-5-seconds': {
        'task': 'app.fetch_lunches_in_background',
        # Run every hour
        'schedule': 5.0,
    }
}

celery = Celery(app.name)
celery.conf.update(
    result_backend=app.config[CELERY_RESULT_BACKEND],
    broker_url=app.config[CELERY_BROKER_URL],
    timezone='Europe/Warsaw',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    beat_schedule=celery_beat_schedule,
)

Post = namedtuple('Post', ['text', 'time', 'image'])

Lunch = namedtuple('Lunch', ['name', 'description', 'image', 'time'])

Restaurant = namedtuple('Restaurant', ['name', 'url', 'lunch_regex'])

logger = logging.getLogger(__name__)


def fetch_lunches():
    with open('restaurants.json') as f:
        restaurants = [Restaurant(r['name'], r['url'], r['lunch_regex'] if 'lunch_regex' in r else None)
                       for r in json.load(f)['restaurants']]
        for rest in restaurants:
            try:
                if is_facebook(rest):
                    yield from get_lunch_from_facebook(rest)
            except Exception as e:
                print(rest)
                logger.exception('Failed to search lunches for restaurant %s...' % str(rest), e)


def get_lunch_from_facebook(res):
    facebook_name = get_restaurant_name_from_facebook_url(res.url)
    for post in fetch_facebook_restaurant_posts(facebook_name):
        if is_lunch(post, res):
            yield Lunch(res.name, post.text, post.image, post.time)


def is_facebook(restaurant):
    return restaurant.url.startswith(app.config[FACEBOOK_URL])


def get_restaurant_name_from_facebook_url(url):
    return url[len(app.config[FACEBOOK_URL]):].replace('/', '')


def fetch_facebook_restaurant_posts(restaurant_id):
    for post in get_posts(restaurant_id, pages=app.config[FACEBOOK_PAGES], sleep=app.config[FACEBOOK_SCRAPE_SLEEP]):
        yield Post(post['text'], post['time'], post['image'])


def is_lunch(post, restaurant):
    if restaurant.lunch_regex:
        return re.match(restaurant.lunch_regex, post.text)
    return DEFAULT_LUNCH_PATTERN.match(post.text)

@celery.task
def fetch_lunches_in_background():
    for l in fetch_lunches():
        database.hmset(l.name,
                       {'image': l.image, 'description': l.description, 'time': l.time.strftime('%m/%d/%Y, %H:%M:%S')})
