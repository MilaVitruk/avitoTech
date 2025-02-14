import pytest
import requests

from api.client import get_statistics_by_id, item_id, get_item_by_id, host
from jsonschema import validate
from utils.schemas import schemas

def test_can_get_statistic_by_id(item_id):
    """Тест 3.1 создает объявление, получает id созданного объявления, запрашивает статистику по id"""
    assert get_statistics_by_id(item_id).status_code == 200


def test_can_get_statistic_values(item_id):
    """Тест 3.2 создает объявление, получает id созданного объявления,
     запрашивает статистику по id, запрашивает объявление по id, сравнивает результат"""
    item_statistics = get_item_by_id(item_id).json()[0]["statistics"]
    assert get_statistics_by_id(item_id).json()[0] == item_statistics


@pytest.mark.parametrize("id_not_valid", ['teststringinput', None, '', 1234, "@#$%", -10])
def test_cant_get_statistic_it_not_valid(id_not_valid):
    """Тест 3.3 запрашивает статистику по невалидному id"""
    assert get_statistics_by_id(item_id).status_code == 400


def test_validation_get_statistic_OK(item_id):
    """Тест 3.4 запрашивает статистику id, проверяет схему полученного ответа"""
    data = get_statistics_by_id(item_id).json()
    schema = schemas['get_statistics_by_id_OK']
    validate(data, schema)


def test_cant_get_statistic_id_not_exist(item_id):
    """Тест 3.5 запрашивает статистику по несуществующему id, проверяет статус-код"""
    split_id = item_id.split('-')
    split_id[1] = "0000"
    not_existing_id = '-'.join(split_id)
    assert get_statistics_by_id(not_existing_id).status_code == 404


def test_validate_statistics_not_exist(item_id):
    """Тест 3.6 запрашивает статистику по несуществующему id, проверяет схему полученного ответа"""
    split_id = item_id.split('-')
    split_id[1] = "0000"
    not_existing_id = '-'.join(split_id)
    schema = schemas['get_statistics_by_id_BAD']
    data = get_statistics_by_id(not_existing_id).json()
    validate(data, schema)


def test_cant_delete_item(item_id):
    """Тест 3.7 Вызов запроса с некорректным методом (DELETE)"""
    endpoint = f'/api/1/statistic/{item_id}'
    response = requests.delete(url=f'{host}{endpoint}')
    assert response.status_code == 405


