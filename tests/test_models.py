import pytest
from models import User

def test_password_hashing():
    user = User(username="user123")
    user.set_password("password123")
    assert user.check_password != "password123"
    assert user.check_password("password123") == True
    assert user.check_password("wrongpassword") == False