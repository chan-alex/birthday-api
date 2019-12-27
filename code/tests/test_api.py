import pytest
import requests

url_prefix = "http://127.0.0.1:5000/"


def test_root():
    response = requests.get(url_prefix)
    assert response.status_code == 404


def test_get():
    url = url_prefix + 'hello/jimmy'
    response = requests.get(url)
    assert response.status_code == 200


def test_put():
    url = url_prefix + 'hello/jackey'
    headers = {"Content-Type": "application/json"}
    json = '{ "dateOfBirth": "1990-12-27" }'
    response = requests.put(url, headers=headers, data=json)

    assert response.status_code == 204
    assert response.content == b'' 


def test_put_invalid_name():
    url = url_prefix + 'hello/jackey123'
    headers = {"Content-Type": "application/json"}
    json = '{ "dateOfBirth": "1990-12-27" }'
    response = requests.put(url, headers=headers, data=json)

    assert response.status_code == 422
    assert response.content == b'{\n    "message": "User name should contain alphabets only"\n}\n'
