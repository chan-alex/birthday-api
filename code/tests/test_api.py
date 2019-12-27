import pytest
import requests

url_prefix = "http://127.0.0.1:5000/"


def call_api(url):
    try:
        response = requests.get(url)
    except:
        pytest.fail("Error when calling api. Is the process running?")
        return False
    return response    


def test_root():
    response = requests.get(url_prefix)
    response = call_api(url_prefix)
    assert response.status_code == 404

