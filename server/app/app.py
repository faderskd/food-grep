import logging

from flask import Flask, jsonify, request

from server.app.database import get_cached_lunches, get_saved_restaurants, save_restaurant
from server.app.model import parse_restaurant
from server.config.config import APP_PORT, APP_HOST

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route('/api/lunches-today')
def fetch_lunches():
    return jsonify(
        convert_elements_to_dict(
            get_cached_lunches(get_saved_restaurants())))


@app.route('/api/restaurants', methods=['GET', 'POST'])
def restaurants():
    if request.method == 'GET':
        return jsonify(
            convert_elements_to_dict(
                get_saved_restaurants()))
    else:
        restaurant_json = request.get_json()
        save_restaurant(parse_restaurant(restaurant_json))
        return jsonify()


def convert_elements_to_dict(element_list):
    return [l.to_dict() for l in element_list]


if __name__ == '__main__':
    app.run(APP_HOST, APP_PORT)
