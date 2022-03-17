import json

import pytest
from flask import g
from flask import session

from api.db import get_db


def test_register(client, app):
    # test that successful registration
    response = client.post("/api/auth/register", data={"username": "aaaaaaaa", "email": "aaaaaaaa@example.com", "password": "aaaaaaaa"})
    assert response.status_code == 200

    # test that the user was inserted into the database
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM users WHERE username = 'aaaaaaaa'").fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("field", "username", "email", "password", "message"),
    (
        ("username", "", "", "", "Field must be between 5 and 20 characters long."),
        ("password", "aaaaaaaa", "a@example.com", "", "Field must be between 8 and 20 characters long."),
        ("email", "testtest", "test@example", "testtest", "Invalid email address."),
    ),
)
def test_register_validate_input(client, field, username, email, password, message):
    response = client.post(
        "/api/auth/register", data={"username": username, "email": email, "password": password}
    )
    data = json.loads(response.data.decode())
    assert message in data['errors'][field]


def test_login(client, auth):
    # test that successful login
    response = auth.login()

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "testtest"


@pytest.mark.parametrize(
    ("field", "username", "password", "message"),
    (
        ("username", "", "", "Field must be between 5 and 20 characters long."),
        ("password", "aaaaaaaa", "", "Field must be between 8 and 20 characters long.")
    )
)
def test_login_validate_input(auth, field, username, password, message):
    response = auth.login(username, password)
    data = json.loads(response.data.decode())
    assert message in data['errors'][field]


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
