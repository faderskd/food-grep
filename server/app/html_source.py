import logging

import re
import requests
from bs4 import BeautifulSoup
from urllib import parse

from server.app.model import Lunch
from server.app.utils import get_time

logger = logging.getLogger(__name__)

HEADER_PATTERN = re.compile('^h[1-6]$')


def get_lunches_from_html(restaurant_list):
    for rest in restaurant_list:
        try:
            html = requests.get(rest.url).text
            lunch = find_lunch_in_html(html, rest)
            if lunch:
                yield lunch
        except Exception as e:
            logger.exception('Failed to search lunch for restaurant %s...' % str(rest), e)


def find_lunch_in_html(html, rest):
    soup = BeautifulSoup(html, 'html.parser')
    return find_lunch_image(soup, rest)


def find_lunch_image(soup, rest):
    if rest.requirements.image_url_regex:
        regex = re.compile(rest.requirements.image_url_regex)
        lunch_images = soup.find_all('img', attrs={
            'src': regex
        })
        if lunch_images:
            return Lunch(rest.name, None, get_image_url(lunch_images[0], rest), get_time())


def get_image_url(soup_image, rest):
    image_url = soup_image.attrs['src']
    rest_url_data = parse.urlparse(rest.url)
    url_data = parse.urlparse(image_url)
    if not url_data.netloc:
        image_path_without_leading_slash = url_data.path.lstrip('/')
        return f'{rest_url_data.scheme}://{rest_url_data.netloc}/{image_path_without_leading_slash}'
    return image_url
