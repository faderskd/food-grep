import logging

from flask import Flask, jsonify

from server.app.database import get_cached_lunches
from server.app.lunches import get_restaurants
from server.app.scheduler import scrape_lunches_in_background
from server.config.config import APP_PORT, APP_HOST

app = Flask(__name__)

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
