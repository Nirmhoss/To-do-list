"""
Модуль, що визначає моделі користувачів системи Todo API.

Цей модуль містить основну модель User, яка представляє користувачів
в системі та забезпечує функціональність аутентифікації, шифрування паролів
та управління даними користувачів.
"""

from __future__ import annotations
from datetime import datetime
from typing import Dict, Any, Optional

from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(db.Model):
    """
    Модель користувача системи.

    Ця модель представляє зареєстрованого користувача в системі управління завданнями
    та зберігає основну інформацію про нього, включаючи захищений пароль.

    Attributes:
        id (int): Унікальний ідентифікатор користувача
        username (str): Унікальне ім'я користувача для входу
        email (str): Електронна адреса користувача (унікальна)
        password_hash (str): Хеш паролю користувача (не зберігає сам пароль)
        created_at (datetime): Дата та час створення облікового запису
        updated_at (datetime): Дата та час останнього оновлення облікового запису
        todos (List[Todo]): Зв'язок із завданнями, які належать користувачу
    """
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email: str = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash: str = db.Column(db.String(128))
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with todos - if user is deleted, their todos are also deleted
    todos = db.relationship('Todo', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, username: str, email: str, password: str) -> None:
        """
        Ініціалізація нового користувача.

        Args:
            username: Унікальне ім'я користувача
            email: Електронна адреса користувача
            password: Пароль користувача (буде захешовано)
        """
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password: str) -> None:
        """
        Встановлює хеш пароля для користувача.

        Перетворює відкритий пароль у захищений хеш, який зберігається в базі даних.

        Args:
            password: Відкритий пароль у вигляді рядка
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Перевіряє відповідність відкритого пароля збереженому хешу.

        Args:
            password: Відкритий пароль для перевірки

        Returns:
            bool: True, якщо пароль правильний, False - інакше
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> Dict[str, Any]:
        """
        Конвертує об'єкт користувача в словник для відповідей API.

        Returns:
            Dict[str, Any]: Словник з даними користувача
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self) -> str:
        """
        Представлення об'єкта у вигляді рядка для відлагодження.

        Returns:
            str: Рядкове представлення користувача
        """
        return f'<User {self.username}>'