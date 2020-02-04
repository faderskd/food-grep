import re
import logging

from flask import Flask, jsonify

from server.config import APP_PORT, APP_HOST
from server.database import get_cached_lunches
from server.lunches import get_restaurants

app = Flask(__name__)

COMMON_LUNCH_PHRASES = 'lunch,obiad'
DEFAULT_LUNCH_PATTERN = re.compile('|'.join(COMMON_LUNCH_PHRASES.split(',')))

logger = logging.getLogger(__name__)

restaurant_list = get_restaurants()


@app.route('/api/lunches-today')
def fetch_lunches():
    return jsonify(
        convert_lunches_to_dict(
            get_cached_lunches(restaurant_list)))


def convert_lunches_to_dict(lunches):
    return [dict(l._asdict()) for l in lunches]


if __name__ == '__main__':
    app.run(APP_HOST, APP_PORT)
