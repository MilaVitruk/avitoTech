import requests
import pytest

host = 'https://qa-internship.avito.com/'


@pytest.fixture
def item_id():
    """Создает объявление, возвращает id созданного объявления"""
    payload = {
        "name": "Телефон",
        "price": 85566,
        "sellerId": 345212,
        "statistics": {
            "contacts": 32,
            "like": 35,
            "viewCount": 14
        }
    }
    endpoint = 'api/1/item'
    response = requests.post(url=f'{host}{endpoint}', json=payload)
    get_id = response.json()['status'].split()[3]
    return get_id


def create_item(payload):
    """Создает объявление, возвращает response созданного объявления"""
    endpoint = 'api/1/item'
    response = requests.post(url=f'{host}{endpoint}', json=payload)
    return response


def get_item_by_id(item_id):
    """Запрашивает объявление по id"""
    endpoint = f'api/1/item/{item_id}'
    response = requests.get(url=f'{host}{endpoint}')
    return response


def get_statistics_by_id(item_id):
    """Запрашивает статистику по id"""
    endpoint = f'/api/1/statistic/{item_id}'
    response = requests.get(url=f'{host}{endpoint}')
    return response


def get_items_by_seller_id(seller_id):
    """Запрашивает список объявлений по sellerId"""
    endpoint = f'api/1/{seller_id}/item'
    response = requests.get(url=f'{host}{endpoint}')
    return response
