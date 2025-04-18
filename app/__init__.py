"""
Todo API application initialization.

This module creates and configures the Flask application, initializes extensions,
and registers blueprints for different API routes.
"""

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    """
    Factory function to create and configure the Flask application.

    Args:
        config_class: Configuration class to use for the application

    Returns:
        Configured Flask application
    """
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Enable CORS for all routes

    # Import blueprints here to avoid circular imports
    from app.routes.auth import auth_bp
    from app.routes.todos import todos_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(todos_bp, url_prefix="/api/todos")

    return app
