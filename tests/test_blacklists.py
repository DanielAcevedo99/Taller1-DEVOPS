import pytest
from blacklist.application import app
from flask import json
import uuid

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_header(client):
    login_data = {'username': 'admin', 'password': 'password'}
    login_response = client.post('/login', data=json.dumps(login_data), content_type='application/json')
    token = login_response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_add_to_blacklist(client, auth_header):
    unique_email = f"{uuid.uuid4()}@example.com"
    data = {
        'email': unique_email,
        'app_uuid': 'some-uuid',
        'blocked_reason': 'Motivo de prueba'
    }
    response = client.post('/blacklists', data=json.dumps(data), headers=auth_header, content_type='application/json')
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

def test_get_blacklist(client, auth_header):
    data = {
        'email': 'test@example.com',
        'app_uuid': 'some-uuid',
        'blocked_reason': 'Motivo de prueba'
    }
    client.post('/blacklists', data=json.dumps(data), headers=auth_header, content_type='application/json')

    response = client.get('/blacklists/test@example.com', headers=auth_header)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json['is_blacklisted'] == True
    assert response.json['reason'] == 'Motivo de prueba'
