from collections import defaultdict

from flask import Blueprint, g, jsonify, request
from werkzeug.exceptions import abort

from api.auth import login_required
from api.db import get_db
from api.exceptions import PostNotExistError, CreatePostValidateError, UpdatePostValidateError, ReplyPostValidateError, \
    AuthorRequiredError, PostNotFoundError
from api.form.post import CreatePostForm, UpdatePostForm, ReplyPostForm

bp = Blueprint("post", __name__, url_prefix='/api/posts')


@bp.get("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, p.parent_id, p.content, p.created, p.author_id, u.username as author"
        " FROM posts AS p JOIN users AS u ON p.author_id = u.id"
        " ORDER BY p.created DESC"
    ).fetchall()

    return jsonify(tree([dict(post) for post in posts]))


def tree(posts):
    parents = defaultdict(list)
    for post in posts:
        parents[post['parent_id']].append(post)
    for post in posts:
        post['children'] = parents[post['id']]

    return parents[None]


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
            .execute(
            "SELECT p.id, p.parent_id, p.content, p.created, p.author_id, u.username AS author"
            " FROM posts AS p JOIN users AS u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        ).fetchone()
    )

    if post is None:
        raise PostNotExistError

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.post("/")
@login_required
def create():
    """Create a new post for the current user."""
    form = CreatePostForm(request.form)
    if form.validate() is False:
        raise CreatePostValidateError(form.errors)

    db = get_db()
    content = form.content.data
    db.execute(
        "INSERT INTO posts (content, author_id) VALUES (?, ?)",
        (content, g.user["id"]),
    )
    db.commit()
    return "", 201


@bp.get("/<int:id>")
def get(id):
    """Fetch a single post detail."""
    return jsonify(dict(get_post(id)))


@bp.post("/<int:id>")
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)
    if post is None:
        raise PostNotFoundError

    if post['author_id'] != g.user['id']:
        raise AuthorRequiredError

    form = UpdatePostForm(request.form)
    if form.validate() is False:
        raise UpdatePostValidateError(form.errors)

    db = get_db()
    content = form.content.data
    db.execute(
        "UPDATE posts SET content = ? WHERE id = ?", (content, id)
    )
    db.commit()
    return "", 200


@bp.delete("/<int:id>")
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    post = get_post(id)
    if post is None:
        raise PostNotFoundError

    if post['author_id'] != g.user['id']:
        raise AuthorRequiredError

    db = get_db()
    db.execute("DELETE FROM posts WHERE id = ?", (id,))
    db.commit()
    return "", 200


@bp.post("/<int:parent_id>/replies/")
@login_required
def reply(parent_id):
    """Reply a post for the current user."""

    form = ReplyPostForm(request.form)
    if form.validate() is False:
        raise ReplyPostValidateError(form.errors)

    db = get_db()
    content = form.content.data
    db.execute(
        "INSERT INTO posts (parent_id, content, author_id) VALUES (?, ?, ?)",
        (parent_id, content, g.user["id"]),
    )
    db.commit()
    return "", 201
