import pytest
import requests
from tests.conftest import BASE_URL

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json().get("status") == "healthy"


def test_register_user(create_user, register_user):
    assert register_user.status_code == 201

    assert register_user.json().get("user").get("is_admin") == False

    assert register_user.json().get("user").get("username") == create_user.get("username")


def test_login_user(login_user):
    assert login_user.status_code == 200

    assert login_user.json().get("access_token") is not None


def test_create_event(create_event):
    # assert: check valid response
    assert create_event.status_code == 201

    # assert: check event title matches input
    assert create_event.json().get("title") == "Python Meetup"


def test_rsvp_event(create_event):
    # arrange: rsvp to event
    event_data = create_event.json()
    event_id = event_data.get("id")
    new_rspv = {
        "attending": True
    }

    # act: rsvp to event
    response = requests.post(f"{BASE_URL}/rsvps/event/{event_id}", json=new_rspv) # rsvp to public event - no auth

    # assert: check valid response
    assert response.status_code == 201

    # assert: check rsvp matches correct event
    assert response.json().get("event_id") == event_id


def test_duplicate_username_registration(create_user,register_user):
    assert register_user.status_code == 201

    # attempt to register same username again
    response = requests.post(f"{BASE_URL}/auth/register", json=create_user)

    assert response.status_code == 400


def test_create_event_without_auth():
    new_event = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }
    response = requests.post(f"{BASE_URL}/events", json=new_event)

    assert response.status_code == 401

    assert response.json().get("msg") == "Missing Authorization Header"


def test_create_event_missing_fields(auth_token):
    new_event = {
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/events", json=new_event, headers=headers)

    assert response.status_code == 400

    assert response.json().get("error") == "Title is required"