from celery import Celery

from server.app.database import redis_client
from server.app.facebook_source import get_lunches_from_facebook
from server.app.lunches import get_restaurants
from server.config.config import FACEBOOK_SCRAPE_INTERVAL_SECONDS, APP_NAME, CELERY_RESULT_BACKEND, CELERY_BROKER_URL

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
    beat_schedule=celery_beat_schedule,
)

def scrape_lunches(restaurant_list):
    yield from get_lunches_from_facebook(restaurant_list)

@celery.task
def scrape_lunches_in_background():
    restaurant_list = get_restaurants()
    for l in scrape_lunches(restaurant_list):
        redis_client.hmset(l.name,
                           {'image': l.image, 'description': l.description,
                            'time': l.time.strftime('%m/%d/%Y, %H:%M:%S')})


