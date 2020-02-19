import re

FACEBOOK_URL = 'https://www.facebook.com'
FACEBOOK_PAGES = 2
FACEBOOK_SCRAPE_SLEEP = 1
FACEBOOK_SCRAPE_INTERVAL_SECONDS = 100

RESTAURANT_FILE = 'restaurants.json'

REDIS_PORT = 6379
REDIS_HOST = 'localhost'

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

APP_PORT = '8000'
APP_HOST = '0.0.0.0'
APP_NAME = 'food_grep'

COMMON_LUNCH_PHRASES = 'lunch,obiad'
DEFAULT_LUNCH_PATTERN = re.compile('|'.join(COMMON_LUNCH_PHRASES.split(',')))