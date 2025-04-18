"""
Модуль маршрутів для управління завданнями в Todo API.

Цей модуль визначає API-ендпоінти для операцій CRUD над завданнями,
включаючи створення, читання, оновлення та видалення завдань користувачів.
"""

from flask import Blueprint, jsonify, request
from typing import List, Dict, Any, Tuple, Optional

from app import db
from app.models.todo import Todo
from app.utils.auth import token_required


todos_bp = Blueprint('todos', __name__)


@todos_bp.route('', methods=['POST'])
@token_required
def create_todo(current_user) -> Tuple[Dict[str, Any], int]:
    """
    Створює нове завдання для поточного користувача.

    Ця функція обробляє POST-запити для створення нового завдання (todo).
    Вона приймає JSON-дані з деталями завдання, валідує їх та створює
    новий запис у базі даних.

    Args:
        current_user: Об'єкт поточного користувача, доданий декоратором token_required

    Returns:
        Tuple[Dict[str, Any], int]: JSON-відповідь з даними створеного завдання і код 201

    Raises:
        400: Якщо титул (title) завдання відсутній у запиті

    Request Body:
        {
            "title": "Зробити домашнє завдання",
            "description": "Виконати всі вправи з математики",
            "completed": false
        }

    Response:
        {
            "id": 1,
            "title": "Зробити домашнє завдання",
            "description": "Виконати всі вправи з математики",
            "completed": false,
            "user_id": 42,
            "created_at": "2025-04-18T10:30:00Z",
            "updated_at": "2025-04-18T10:30:00Z"
        }
    """
    data = request.get_json()

    # Перевірка наявності обов'язкових полів
    if 'title' not in data:
        return jsonify({'message': 'Title is required'}), 400

    # Створення нового завдання
    new_todo = Todo(
        title=data['title'],
        description=data.get('description', ''),
        completed=data.get('completed', False),
        user_id=current_user.id
    )

    # Додавання завдання до бази даних
    db.session.add(new_todo)
    db.session.commit()

    # Повернення створеного завдання у відповіді
    return jsonify(new_todo.to_dict()), 201