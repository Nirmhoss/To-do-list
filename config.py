"""
Configuration settings for the Todo API.

This module defines configuration parameters for the application, including
database connection, JWT settings, and other environment-specific settings.
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///todo.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "default-jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 3600))
    )
