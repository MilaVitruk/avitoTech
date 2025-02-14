import pytest
import requests

from api.client import get_items_by_seller_id, host
from jsonschema import validate
from utils.schemas import schemas

# Предусловия
sellers_id = 1234345231
not_valid_id = 'teststringinput'


def test_can_get_items_by_id():
    """Тест 2.1 запрашивает объявления по id продавца, получает статус-код, сверяет значение"""
    assert get_items_by_seller_id(sellers_id).status_code == 200


def test_equals_sellers_id():
    """Тест 2.2 запрашивает объявления по id продавца, сверяет id продавца в запросе с id продавца в ответе"""
    data = get_items_by_seller_id(sellers_id).json()
    for item in data:
        assert item['sellerId'] == sellers_id


def test_validation_get_items_by_sellersId_OK():
    """Тест 2.3 запрашивает объявления по id продавца, проверяет схему полученного ответа"""
    data = get_items_by_seller_id(sellers_id).json()
    schema = schemas['get_items_by_sellers_id_OK']
    validate(data, schema)


@pytest.mark.parametrize('not_valid_id', ['teststringinput', None, '', "{@#$%}", -10, 0])
def test_cant_get_items_by_not_valid_id(not_valid_id):
    """Тест 2.4 запрашивает объявления по id продавца, получает статус-код, сверяет значение"""
    assert get_items_by_seller_id(not_valid_id).status_code == 400


def test_validation_get_items_by_sellersId_BAD():
    """Тест 2.5 запрашивает объявления по id продавца, проверяет схему полученного ответа"""
    data = get_items_by_seller_id(not_valid_id).json()
    schema = schemas['get_items_by_sellers_id_BAD']
    validate(data, schema)

def test_cant_delete_item():
    """Тест 2.6 Вызов запроса с некорректным методом (DELETE)"""
    endpoint = f'api/1/item/{sellers_id}'
    response = requests.delete(url=f'{host}{endpoint}')
    assert response.status_code == 405