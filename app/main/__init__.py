from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from app.main.config import configurations

# Initialize SQLAlchemy database
db = SQLAlchemy()

# Initialzie Bcrypt
bcrypt = Bcrypt()


def create_app(config):
    # Check if configuration is valid
    if config not in configurations:
        raise ValueError(f'{config} is not a valid configuration.')

    # Create Flask application and initialize Bcrypt and SQLAlchemy with the application instance
    app = Flask(__name__)
    app.config.from_object(configurations[config])

    db.app = app
    db.init_app(app)

    bcrypt.init_app(app)

    @app.teardown_request
    def shutdown_session(response_or_exc):
        if app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']:
            if response_or_exc is None:
                db.session.commit()

        db.session.remove()
        return response_or_exc

    return app
