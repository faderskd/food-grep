import logging

import redis
from flask import Flask
from flask import jsonify, request, make_response

from server.app.database import Database, RestaurantAlreadyExistsException, RestaurantDoesNotExist
from server.app.validators import RestaurantValidationErrorException
from server.config import config
from server.app.model import parse_restaurant

logger = logging.getLogger(config.APP_NAME)


def create_app_with_dependencies(name=config.APP_NAME, app_config=config):
    redis_client = redis.Redis(app_config.REDIS_HOST, app_config.REDIS_PORT, charset='utf-8', decode_responses=True)
    database = Database(redis_client)
    app = Flask(name)

    @app.route('/api/lunches-today')
    def fetch_lunches():
        return jsonify(
            convert_elements_to_dict(
                database.get_cached_lunches(database.get_saved_restaurants())))

    @app.route('/api/restaurants', methods=['GET', 'PUT', 'POST'])
    def restaurants():
        if request.method == 'GET':
            return jsonify(
                convert_elements_to_dict(
                    database.get_saved_restaurants()))
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
            database.create_restaurant(restaurant)
        else:
            database.edit_restaurant(restaurant)
        return make_response()

    return app, database


def convert_elements_to_dict(element_list):
    return [l.to_dict() for l in element_list]


def convert_exception_to_response(ex):
    if isinstance(ex, RestaurantDoesNotExist):
        return jsonify({'error': ex.msg, 'code': 'RESTAURANT_DOES_NOT_EXIST'}), 400
    if isinstance(ex, RestaurantAlreadyExistsException):
        return jsonify({'error': ex.msg, 'code': 'RESTAURANT_ALREADY_EXISTS'}), 400
    if isinstance(ex, RestaurantValidationErrorException):
        return jsonify({'errors': ex.errors, 'code': 'RESTAURANT_VALIDATION_ERROR'}), 400
    return make_response(500)
