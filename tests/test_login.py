import pytest
from blacklist.application import app  
from flask import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_to_blacklist(client):
    data = {'email': 'test@example.com'}
    response = client.post('/blacklists', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert response.json['message'] == 'Email added to blacklist'

def test_get_blacklist(client):
    response = client.get('/blacklists/test@example.com')
    assert response.status_code == 200
    assert response.json['email'] == 'test@example.com'

def test_remove_from_blacklist(client):
    response = client.delete('/blacklists/test@example.com')
    assert response.status_code == 200
    assert response.json['message'] == 'Email removed from blacklist'
