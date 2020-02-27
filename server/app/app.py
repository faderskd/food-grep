import logging

from flask import Flask, jsonify, request

from server.app.database import get_cached_lunches, save_restaurants, get_saved_restaurants
from server.app.lunches import get_restaurants
from server.app.model import parse_restaurants
from server.config.config import APP_PORT, APP_HOST

app = Flask(__name__)

logger = logging.getLogger(__name__)

restaurant_list = get_restaurants()


@app.route('/api/lunches-today')
def fetch_lunches():
    return jsonify(
        convert_elements_to_dict(
            get_cached_lunches(restaurant_list)))


@app.route('/api/restaurants', methods=['GET', 'POST'])
def restaurants():
    if request.method == 'GET':
        return jsonify(
            convert_elements_to_dict(
                get_saved_restaurants()))
    else:
        save_restaurants(parse_restaurants(request.get_json()))


def convert_elements_to_dict(element_list):
    return [l.to_dict() for l in element_list]


if __name__ == '__main__':
    app.run(APP_HOST, APP_PORT)
