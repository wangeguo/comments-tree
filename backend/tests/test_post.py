import pytest
from flask import json

from api.db import get_db


def test_index(client, auth):
    response = client.get("/api/posts/")

    assert b"test" in response.data
    assert b"Mon, 01 Jan 2018 00:00:00 GMT" in response.data
    assert b'children' in response.data


@pytest.mark.parametrize("path", ("/api/posts/", "/api/posts/1"))
def test_login_required(client, path):
    response = client.post(path)
    assert response.status_code == 401


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute("UPDATE posts SET author_id = 2 WHERE id = 1")
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post("/api/posts/1").status_code == 403
    assert client.delete("/api/posts/1").status_code == 403


@pytest.mark.parametrize("path", ("/api/posts/2",))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    client.post("/api/posts/", data={"content": "created"})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM posts").fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    client.post("/api/posts/1", data={"content": "updated"})

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM posts WHERE id = 1").fetchone()
        assert post["content"] == "updated"


@pytest.mark.parametrize("path", ("/api/posts/", "/api/posts/1"))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"content": ""})

    data = json.loads(response.data.decode())
    assert 'Field must be between 3 and 200 characters long.' in data['errors']['content']


def test_delete(client, auth, app):
    auth.login()
    response = client.delete("/api/posts/1")
    assert response.status_code == 200

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM posts WHERE id = 1").fetchone()
        assert post is None
