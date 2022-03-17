import functools

from flask import Blueprint, g, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from api.db import get_db
from api.exceptions import IncorrectUsernameError, IncorrectPasswordError, \
    UserAlreadyExistsError, LoginValidateError, RegisterValidateError, LoginRequiredError
from api.form.user import RegistrationForm, LoginForm

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            raise LoginRequiredError

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        )


@bp.post("/register")
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    form = RegistrationForm(request.form)
    if form.validate() is False:
        raise RegisterValidateError(form.errors)

    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (form.username.data, form.email.data, generate_password_hash(form.password.data)),
        )
        db.commit()
    except db.IntegrityError:
        # The username was already taken, which caused the
        # commit to fail. Show a validation error.
        raise UserAlreadyExistsError

    return {"user": {"username": form.username.data}, "token": "xxx"}


@bp.post("/login")
def login():
    """Log in a registered user by adding the user id to the session."""

    form = LoginForm(request.form)
    if form.validate() is False:
        raise LoginValidateError(form.errors)

    db = get_db()
    username = form.username.data
    password = form.password.data

    user = db.execute(
        "SELECT * FROM users WHERE username = ? or email = ?", (username, username,)
    ).fetchone()

    if user is None:
        raise IncorrectUsernameError
    elif not check_password_hash(user["password"], password):
        raise IncorrectPasswordError

    # store the user id in a new session
    session.clear()
    session["user_id"] = user["id"]

    return {"user": {"username": form.username.data}, "token": "xxx"}


@bp.post("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return "", 200
