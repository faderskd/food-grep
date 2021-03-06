from celery import Celery

from server.app.facebook_source import get_lunches_from_facebook, is_facebook
from server.app.html_source import get_lunches_from_html
from server.config.config import FACEBOOK_SCRAPE_INTERVAL_SECONDS, APP_NAME, CELERY_RESULT_BACKEND, CELERY_BROKER_URL
from . import app_factory

celery_beat_schedule = {
    'add-every-' + str(FACEBOOK_SCRAPE_INTERVAL_SECONDS) + '-seconds': {
        'task': 'server.app.scheduler.scrape_lunches_in_background',
        'schedule': FACEBOOK_SCRAPE_INTERVAL_SECONDS,
    }
}

celery = Celery(APP_NAME)
celery.conf.update(
    result_backend=CELERY_RESULT_BACKEND,
    broker_url=CELERY_BROKER_URL,
    timezone='Europe/Warsaw',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    beat_schedule=celery_beat_schedule)

_, database = app_factory.create_app_with_dependencies(__name__)


def scrape_lunches(restaurant_list):
    facebook_lunches = filter(is_facebook, restaurant_list)
    html_lunches = filter(lambda k: not is_facebook(k), restaurant_list)
    yield from get_lunches_from_facebook(facebook_lunches)
    yield from get_lunches_from_html(html_lunches)


@celery.task
def scrape_lunches_in_background():
    restaurant_list = database.get_saved_restaurants()
    for l in scrape_lunches(restaurant_list):
        database.save_lunch(l)
