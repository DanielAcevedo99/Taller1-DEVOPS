import pytest
from blacklist.application import app
from flask import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login(client):
    data = {'username': 'admin', 'password': 'password'}
    response = client.post('/login', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_protected_route_without_token(client):
    response = client.get('/protected-route')
    assert response.status_code == 401

def test_protected_route_with_token(client):
    login_data = {'username': 'admin', 'password': 'password'}
    login_response = client.post('/login', data=json.dumps(login_data), content_type='application/json')
    token = login_response.json['access_token']

    headers = {'Authorization': f'Bearer {token}'}
    response = client.get('/protected-route', headers=headers)
    assert response.status_code == 200
