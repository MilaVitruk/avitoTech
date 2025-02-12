import pytest
import requests

from api.client import get_item_by_id, item_id, host
from jsonschema import validate


def test_can_get_item_by_valid_id(item_id):
    """Тест 1.1 создает объявление, получает id созданного объявления, запрашивает объявление по id"""
    assert get_item_by_id(item_id).status_code == 200


def test_equals_request_id_and_response_id(item_id):
    """Тест 1.2 создает объявление, получает id созданного объявления, запрашивает объявление по id, сравнивает id
    переданный в запрос с id, полученным в ответе"""
    data = get_item_by_id(item_id).json()[0]
    assert data['id'] == item_id


def test_validation_get_item_by_id_json(item_id):
    """Тест 1.3 создает объявление, получает id созданного объявления,
    запрашивает объявление по id,
    проводит валидацию JSON-схемы"""
    schema = {"type": "array",
              "minItems": 1,
              "items": {
                  "type": "object",
                  "required": ["id", "name", "price", "sellerId", "statistics"],
                  "properties": {
                      "id": {"type": "string"},
                      "name": {"type": "string"},
                      "price": {"type": "number"},
                      "sellerId": {"type": "number"},
                      "statistics": {"type": "object",
                                     "required": ["contacts", "likes", "viewCount"],
                                     "properties": {"contacts": {"type": "number"},
                                                    "likes": {"type": "number"},
                                                    "viewCount": {"type": "number"}

                                                    }},
                  }
              }}
    data = get_item_by_id(item_id).json()
    validate(data, schema)


@pytest.mark.parametrize("not_valid_id", ['teststringinput', None, '', 1234, "@#$%", -10])
def test_cant_get_item_by_not_valid_id(not_valid_id):
    """Тест 1.4 подставляет невалидные значения id в запрос"""
    assert get_item_by_id(not_valid_id).status_code == 400


def test_cant_get_item_by_not_existing_id(item_id):
    """Тест 1.5 подставляет несуществующий id в запрос"""
    split_id = item_id.split('-')
    split_id[1] = "0000"
    not_existing_id = '-'.join(split_id)
    assert get_item_by_id(not_existing_id).status_code == 404


def test_validation_not_existing_id_json(item_id):
    """Тест 1.6 Валидация JSON-схемы ошибки 404"""
    split_id = item_id.split('-')
    split_id[1] = "0000"
    not_existing_id = '-'.join(split_id)
    schema = {
        "type": "object",
        "required": ["result", "status"],
        "properties": {
            "result": {"type": "object",
                       "properties": {"message": {"type": "string"},
                                      "messages": {"type": "null", "properties": {}}},
                       "status": {"type": "string"}}},
        "status": {"type": "string"},
    }
    data = get_item_by_id(not_existing_id).json()
    validate(data, schema)

# Поначалу невалидные значения id провоцировали ошибку 500, в данный момент не получается ее вызвать
# def test_validation_not_existing_id_json(item_id):
#     """Тест 1.6 Валидация JSON-схемы ошибки 500"""
#     schema = {
#         "type": "object",
#         # "required": {"result", "status"},
#         "properties": {
#             "result": {"type": "object",
#                        "properties": {"message": {"type": "string"},
#                                       "messages": {"type": "null", "properties": {}}},
#                        "status": {"type": "string"}}},
#             "status": {"type": "string"},
#         }
#     data = get_item_by_id(item_id="teststringinput").json()
#     print(data)
#     validate(data, schema)


def test_cant_delete_item(item_id):
    """Тест 1.7 Вызов запроса с некорректным методом (DELETE)"""
    endpoint = f'api/1/item/{item_id}'
    response = requests.delete(url=f'{host}{endpoint}')
    assert response.status_code == 405


def test_cant_post_item(item_id):
    """Тест 1.8 Вызов запроса с некорректным методом (POST)"""
    endpoint = f'api/1/item/{item_id}'
    response = requests.post(url=f'{host}{endpoint}')
    assert response.status_code == 405
