import pytest
import requests
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def create_user():
    current_time = int(datetime.now().timestamp())
    new_user = {
        "username": f"user123_{current_time}",
        "password": "password123"
    }
    return new_user


@pytest.fixture
def register_user(create_user):
    response = requests.post(f"{BASE_URL}/auth/register", json=create_user)
    return response


@pytest.fixture
def login_user(create_user, register_user):
    response = requests.post(f"{BASE_URL}/auth/login", json=create_user)
    return response


@pytest.fixture
def auth_token(register_user, login_user):
    token = login_user.json().get("access_token")
    return token

@pytest.fixture
def create_event(auth_token):
    new_event = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/events", json=new_event, headers=headers)
    return response