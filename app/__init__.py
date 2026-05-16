from flask import Flask


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Register routes
    with app.app_context():
        from . import routes  # noqa: F401

    return app
