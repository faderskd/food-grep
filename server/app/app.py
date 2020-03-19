import logging

from flask import Flask, jsonify, request, make_response

from server.app.database import get_cached_lunches, get_saved_restaurants, create_restaurant, edit_restaurant, \
    RestaurantAlreadyExistsException, RestaurantDoesNotExist
from server.app.model import parse_restaurant, RestaurantValidationErrorException
from server.config.config import APP_PORT, APP_HOST

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route('/api/lunches-today')
def fetch_lunches():
    return jsonify(
        convert_elements_to_dict(
            get_cached_lunches(get_saved_restaurants())))


@app.route('/api/restaurants', methods=['GET', 'PUT', 'POST'])
def restaurants():
    if request.method == 'GET':
        return jsonify(
            convert_elements_to_dict(
                get_saved_restaurants()))
    else:
        try:
            return create_or_edit_restaurant()
        except (RestaurantAlreadyExistsException, RestaurantDoesNotExist, RestaurantValidationErrorException) as e:
            logger.exception(e)
            return convert_exception_to_response(e)


def create_or_edit_restaurant():
    restaurant_json = request.get_json()
    restaurant = parse_restaurant(restaurant_json)
    if request.method == 'POST':
        create_restaurant(restaurant)
    else:
        edit_restaurant(restaurant)
    return make_response()


def convert_elements_to_dict(element_list):
    return [l.to_dict() for l in element_list]


def convert_exception_to_response(ex):
    if isinstance(ex, (RestaurantDoesNotExist, RestaurantAlreadyExistsException)):
        return jsonify({'error': ex.msg}), 400
    if isinstance(ex, RestaurantValidationErrorException):
        return jsonify({'errors': ex.errors}), 400
    return make_response(500)


if __name__ == '__main__':
    app.run(APP_HOST, APP_PORT)
