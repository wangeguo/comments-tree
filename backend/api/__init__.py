import os

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from api.exceptions import Error


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__,
                instance_relative_config=True,
                template_folder='../../frontend/dist',
                static_folder='../../frontend/dist/static'
                )
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "comments-tree.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CORS(app)

    @app.get('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>', methods=('GET', 'POST'))
    def index(path):
        return render_template('index.html')

    # register the database commands
    from . import db

    db.init_app(app)

    # apply the blueprints to the app
    from . import auth, post

    app.register_blueprint(auth.bp)
    app.register_blueprint(post.bp)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({"message": e.description}), e.code

    @app.errorhandler(Error)
    def handle_business_exception(e):
        return jsonify(e.to_dict()), e.status_code

    return app
