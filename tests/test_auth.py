
import pytest


import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app  # Import the global app instance
from extensions import db as _db
from models.user_model import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        _db.create_all()
        yield app.test_client()
        _db.drop_all()

def test_register_user(client):
    response = client.post('/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "User created"

def test_register_existing_user(client):
    client.post('/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post('/register', json={
        "username": "testuser",
        "email": "test2@example.com",
        "password": "password123"
    })
    assert response.status_code == 403
    assert "user already exist" in response.get_json()["Error"]

def test_login_user_success(client):
    client.post('/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.post('/login', json={
        "username": "testuser",
        "password": "password123"
    })
    data = response.get_json()
    assert response.status_code == 200
    assert "access" in data["tokens"]

def test_login_user_failure(client):
    response = client.post('/login', json={
        "username": "nonexistent",
        "password": "wrongpass"
    })
    assert response.status_code == 400
    assert "Invalid username or password" in response.get_json()["error"]

def test_get_claim(client):
    client.post('/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    login_res = client.post('/login', json={
        "username": "testuser",
        "password": "password123"
    })
    token = login_res.get_json()["tokens"]["access"]

    response = client.get('/getclaim', headers={
        "Authorization": f"Bearer {token}"
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data["user_details"]["username"] == "testuser"
