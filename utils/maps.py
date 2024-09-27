# utils/maps.py
import requests
from config import YANDEX_MAPS_API_KEY

def get_museum_map():
    latitude = 56.838011  # Координаты музея
    longitude = 60.597465
    map_params = {
        "ll": f"{longitude},{latitude}",
        "z": "16",
        "l": "map",
        "size": "450,450",
        "pt": f"{longitude},{latitude},pm2dgl",
        "apikey": YANDEX_MAPS_API_KEY
    }
    response = requests.get(
        "https://static-maps.yandex.ru/1.x/",
        params=map_params
    )
    if response.status_code == 200:
        return response.content
    else:
        return None

def get_route_map(place_name):
    museum_coords = "60.597465,56.838011"
    places_coords = {
        'Храм-на-Крови': "60.610873,56.838500",
        'Плотинка': "60.603358,56.838984",
        'Исторический сквер': "60.605829,56.839671"
    }
    destination_coords = places_coords.get(place_name)
    if not destination_coords:
        return None

    map_params = {
        "rtt": "mt",
        "ll": museum_coords,
        "z": "14",
        "l": "map",
        "pl": f"{museum_coords},{destination_coords}",
        "size": "450,450",
        "pt": f"{museum_coords},pm2dgl~{destination_coords},pm2rdl",
        "apikey": YANDEX_MAPS_API_KEY
    }
    response = requests.get(
        "https://static-maps.yandex.ru/1.x/",
        params=map_params
    )
    if response.status_code == 200:
        return response.content
    else:
        return None