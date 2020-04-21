import sys
import requests
from PIL import Image
from io import BytesIO
from .scale_handler import get_scale


def get_image_url(toponym_to_find, default):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        return default

    json_response = response.json()
    toponyms = json_response["response"]["GeoObjectCollection"]["featureMember"]

    if not toponyms:
        return default

    toponym = toponyms[0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": get_scale(json_response),
        "l": "sat",
        "pt": toponym_coodrinates.replace(' ', ',') + ",flag"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"

    return requests.Request("GET", map_api_server, params=map_params).prepare().url
