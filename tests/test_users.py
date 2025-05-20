import pytest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from extensions import db as _db
from models.user_model import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret'

    with app.app_context():
        _db.create_all()
        yield app.test_client()
        _db.drop_all()

def create_user(username, is_admin=False):
    user = User(username=username, email=f"{username}@example.com", password="password123")
    _db.session.add(user)
    _db.session.commit()
    token = create_access_token(identity=username, additional_claims={"is_admin": is_admin})
    return token



# def test_get_all_users_as_admin(client):
#     token = create_user("Test User5", is_admin=True)

#     response = client.get('/users/all', headers={
#         "Authorization": f"Bearer {token}"
#     })

#     assert response.status_code == 200
#     assert "users" in response.get_json()




def test_get_all_users_as_non_admin(client):
    token = create_user("regularuser", is_admin=False)

    response = client.get('/users/all', headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    assert response.get_json()["Message"] == "Not an  admin member"





def test_get_all_users_unauthorized(client):
    response = client.get('/users/all')
    assert response.status_code == 401
