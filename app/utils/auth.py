"""
Authentication utilities for the Todo API.

This module provides helper functions and decorators for handling JWT-based
authentication and protecting API routes.
"""
import os
from functools import wraps

import jwt
from flask import jsonify, request

from app.models.user import User


def token_required(f):
    """
    Decorator for protecting API routes

    This decorator checks if a valid JWT token is present in the request header.
    If it is, it decodes the token and passes the user to the route function.
    If not, it returns an error response.

    Usage:
        @token_required
        def protected_route(current_user):
            # Access to current_user object
            pass
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if token is in the header
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]  # Format: "Bearer <token>"
            except IndexError:
                return jsonify({"message": "Invalid token format"}), 401

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            # Decode the token
            data = jwt.decode(
                token,
                os.environ.get("JWT_SECRET_KEY", "default-jwt-secret-key"),
                algorithms=["HS256"],
            )
            current_user = User.query.filter_by(id=data["user_id"]).first()

            if not current_user:
                return jsonify({"message": "User not found"}), 404

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        # Pass the current user to the route
        return f(current_user, *args, **kwargs)

    return decorated
