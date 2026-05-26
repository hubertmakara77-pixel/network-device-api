import pytest
from app import create_app
from app.database import db

@pytest.fixture
def client():
    app = create_app()
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all() 
            yield client    
            db.drop_all()  

def test_get_devices_empty(client):
    response = client.get('/api/devices')
    
    assert response.status_code == 200
    assert response.json == []

def test_add_device(client):
    
    new_device = {
        "hostname": "Nokia-Test-Router",
        "ip_address": "10.0.0.1",
        "snmp_community": "public"
    }
    response = client.post('/api/devices', json=new_device)
    
    assert response.status_code == 201
    assert response.json['message'] == 'Device added!'
    
    verify_response = client.get('/api/devices')
    assert len(verify_response.json) == 1
    assert verify_response.json[0]['hostname'] == "Nokia-Test-Router"