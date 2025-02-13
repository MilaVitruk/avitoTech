import random

import pytest
from jsonschema.validators import validate

# import requests
from api.client import get_item_by_id, host, create_item
from api.utils import schemas

sellerID = random.randint(1111, 9999)

payload_without_statistics = {
    "name": 'Телефон',
    "price": 10,
    "sellerId": 999999
}

payload_with_statistics = {
    "name": 'Телефон',
    "price": 10,
    "sellerId": 999999,
    "statistics": {
        "contacts": 32,
        "likes": 35,
        "viewCount": 14
    }
}


def test_validation_json_post_item():
    """Тест 4.1 проверка структуры JSON ответа, возвращаемого при успешном post запросе"""
    response = create_item(payload_without_statistics)
    schema = schemas['post_OK']
    validate(response.json(), schema)


def test_can_post_item():
    """Тест 4.2, что объявление с опубликованным id существует"""
    response = create_item(payload_without_statistics).json()
    id_posted_item = response['status'].split()[3]
    get_response = get_item_by_id(id_posted_item)
    assert get_response.status_code == 200


def test_create_item_name_correct():
    """Тест 4.3, проверка, что имя создаваемого объявления соответствует имени опубликованного"""
    response = create_item(payload_without_statistics).json()
    id_posted_item = response['status'].split()[3]
    get_response = get_item_by_id(id_posted_item)
    assert get_response.json()[0]['name'] == payload_without_statistics['name']


def test_create_item_price_correct():
    """Тест 4.4, проверка, что стоимость создаваемого объявления соответствует стоимости опубликованного"""
    response = create_item(payload_without_statistics).json()
    id_posted_item = response['status'].split()[3]
    get_response = get_item_by_id(id_posted_item)
    assert get_response.json()[0]['price'] == payload_without_statistics['price']


def test_create_item_sellerId_correct():
    """Тест 4.5, проверка, что ID продавца создаваемого объявления соответсвтует ID опубликованного"""
    response = create_item(payload_without_statistics).json()
    id_posted_item = response['status'].split()[3]
    get_response = get_item_by_id(id_posted_item)
    assert get_response.json()[0]['sellerId'] == payload_without_statistics['sellerId']


def test_posted_statistics_is_null():
    """Тест 4.6, проверка, что в случае добавления "статистики" в публикуемое объявление, значения будут нулевые"""
    # Не считаю хорошей идеей возможность публиковать статистику
    response = create_item(payload_with_statistics).json()
    id_posted_item = response['status'].split()[3]
    get_response = get_item_by_id(id_posted_item)
    schema = schemas['post_statistic']
    assert type(get_response.json()[0]['statistics']) == dict
    validate(get_response.json()[0]['statistics'], schema)


@pytest.mark.parametrize("name_not_valid", [123, None, True, -10])
def test_cant_create_item_name_not_valid(name_not_valid):
    """Тест 4.7, проверка возможности публикации объявления с невалидным именем"""
    payload_test = {
        "name": name_not_valid,
        "price": 10,
        "sellerId": 56788
    }
    assert create_item(payload_test).status_code == 400


@pytest.mark.parametrize("price_not_valid", [-1000, 0, None, True, "1234"])
def test_cant_create_item_price_not_valid(price_not_valid):
    """Тест 4.8, проверка возможности публикации объявления с невалидной ценой"""
    payload_test = {
        "name": "Some Valid Name",
        "price": price_not_valid,
        "sellerId": 56788
    }
    assert create_item(payload_test).status_code == 400


@pytest.mark.parametrize("sellerId_not_valid",
                         [-1000, 0, random.randint(0, 111111),
                          random.randint(999999, 9999999), True, "123456"])
def test_cant_create_item_sellerId_not_valid(sellerId_not_valid):
    """Тест 4.9, проверка возможности публикации объявления с невалидным id продавца"""
    payload_test = {
        "name": "Some Valid Name",
        "price": 10000,
        "sellerId": sellerId_not_valid
    }
    assert create_item(payload_test).status_code == 400


def test_validation_bad_request_json():
    """Тест 4.10 Валидация JSON-схемы некорректного запроса публикации"""
    payload_test_BAD = {
        "name": "Some Valid Name",
        "price": 'Not valid price',
        "sellerId": 45678,
        "statistics": {
            "contacts": 32,
            "likes": 35,
            "viewCount": 14
        }
    }

    schema = schemas['post_BAD']

    data = create_item(payload_test_BAD).json()
    validate(data, schema)
