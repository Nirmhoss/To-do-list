"""
Модуль утиліт аутентифікації для Todo API.

Цей модуль містить допоміжні функції та декоратори для
автентифікації і авторизації користувачів через JWT токени.
"""

import os
from functools import wraps
from typing import Callable, Any, Dict, Tuple, Optional

import jwt
from flask import request, jsonify, g, current_app

from app.models.user import User


def token_required(f: Callable) -> Callable:
    """
    Декоратор для захисту API-маршрутів.

    Цей декоратор перевіряє наявність і дійсність JWT токена в заголовку запиту.
    Якщо токен дійсний, він додає об'єкт користувача в g.current_user
    і передає його функції маршруту.

    Args:
        f: Функція-обробник маршруту, яку потрібно захистити

    Returns:
        Callable: Обгорнута функція з перевіркою токена

    Raises:
        401: Якщо токен відсутній, недійсний або прострочений
        404: Якщо користувач не знайдений
    """
    @wraps(f)
    def decorated(*args: Any, **kwargs: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        token = None

        # Перевірка наявності токена в заголовку
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Format: "Bearer <token>"
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Декодування токена
            jwt_secret = current_app.config.get('JWT_SECRET_KEY', os.environ.get('JWT_SECRET_KEY', 'default-jwt-secret-key'))
            data = jwt.decode(
                token,
                jwt_secret,
                algorithms=['HS256']
            )
            current_user = User.query.filter_by(id=data['user_id']).first()

            if not current_user:
                return jsonify({'message': 'User not found'}), 404

            # Збереження користувача в контексті запиту
            g.current_user = current_user

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        # Передача поточного користувача в маршрут
        return f(current_user, *args, **kwargs)

    return decorated