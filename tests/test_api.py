import os
import requests
import random
import string
import datetime

url_prefix = os.environ.get('TEST_URL_PREFIX',
                            'http://127.0.0.1:5000/')


def test_root():
    ''' Tests GET for / '''
    response = requests.get(url_prefix)

    # Should return at least a 404
    assert response.status_code == 404


def test_get():
    ''' Test GET for /hello/<name> '''
    url = url_prefix + 'hello/jimmy'
    response = requests.get(url)

    # Should return at least a 202
    assert response.status_code == 200


def test_put():
    ''' Test PUT for /hello/<name> '''
    url = url_prefix + 'hello/jackey'
    headers = {"Content-Type": "application/json"}
    json = '{ "dateOfBirth": "1990-12-27" }'
    response = requests.put(url, headers=headers, data=json)

    assert response.status_code == 204
    assert response.content == b''


def test_put_invalid_name():
    ''' Test PUT for /hello/<name> where name is in invalid format '''
    url = url_prefix + 'hello/jackey123'
    headers = {"Content-Type": "application/json"}
    json = '{ "dateOfBirth": "1990-12-27" }'
    response = requests.put(url, headers=headers, data=json)

    assert response.status_code == 422


def test_put_invalid_dateOfBirth_fieldname():
    ''' Test PUT for /hello/<name> where dateOfBirth field is wrong or missing '''
    url = url_prefix + 'hello/jackey'
    headers = {"Content-Type": "application/json"}
    json = '{ "dateOfBirthXXX": "1990-12-27" }'
    response = requests.put(url, headers=headers, data=json)

    assert response.status_code == 400


def test_put_invalid_json():
    ''' Test PUT for /hello/<name> where the json is invalid '''
    url = url_prefix + 'hello/jackey'
    headers = {"Content-Type": "application/json"}
    json = '"dateOfBirth": 1990-12-27'
    response = requests.put(url, headers=headers, data=json)

    assert response.status_code == 400


def test_put_invalid_dateOfBirth_date():
    ''' Test PUT for /hello/<name> where the birthday date is invalid '''
    url = url_prefix + 'hello/jackey'
    headers = {"Content-Type": "application/json"}
    json = '{ "dateOfBirth": "1990" }'
    response = requests.put(url, headers=headers, data=json)

    assert response.status_code == 400


def randomString(stringLength=10):
    ''' Generate a random string of fixed length '''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_test_dob(year=1990, delta=0):
    today = datetime.datetime.now()
    today = datetime.datetime(today.year, today.month, today.day)

    if delta < 0:
        dob = today - datetime.timedelta(days=abs(delta))
    elif delta == 0:
        dob = today
    elif delta > 0:
        dob = today + datetime.timedelta(days=abs(delta))

    dob = datetime.datetime(year, dob.month, dob.day)
    return dob.strftime("%Y-%m-%d")


def dob_test_helper(day_delta):
    username = randomString()
    test_dob = get_test_dob(delta=day_delta)
    url = url_prefix + 'hello/' + username
    headers = {"Content-Type": "application/json"}

    response = requests.put(url, headers=headers, json={'dateOfBirth': test_dob})
    assert response.status_code != 400

    response = requests.get(url)
    assert response.status_code == 200

    if day_delta > 0:
        assert str(day_delta) in response.json()['message']
    elif day_delta == 0:
        assert "Happy" in response.json()['message']
    elif day_delta < 0 and day_delta > -365:
        assert str(365 - abs(day_delta) + 1) in response.json()['message']


def test_get_dob():
    ''' This set of tests test the birthday calcuations '''
    dob_test_helper(5)
    dob_test_helper(0)
    dob_test_helper(-5)


def test_liveness_probe():
    ''' Tests the liveness probe '''
    url = url_prefix + 'hello/liveness'
    response = requests.get(url)
    assert response.status_code == 200


def test_readiness_probe():
    ''' Tests the readiness probe '''
    url = url_prefix + 'hello/readiness'
    response = requests.get(url)
    assert response.status_code == 200
