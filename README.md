# Todo List API

A simple RESTful API for managing a todo list with user authentication using JWT tokens.

## Features

- User registration and authentication
- JWT token-based authentication
- Todo list management (create, read, update, delete)
- SQLite database with migrations
- Database seeding for testing

## Technology Stack

- **Framework**: Flask - A lightweight web framework for Python
- **ORM**: SQLAlchemy - Python SQL toolkit and Object-Relational Mapping system
- **Database**: SQLite - Lightweight disk-based database
- **Migrations**: Flask-Migrate - Database migration handling based on Alembic
- **Authentication**: PyJWT - JSON Web Token implementation in Python

## Project Structure

```
todo_api/
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── README.md               # Documentation
├── requirements.txt        # Project dependencies
├── config.py               # Configuration settings
├── app/
│   ├── __init__.py         # Application initialization
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   ├── user.py         # User model
│   │   └── todo.py         # Todo model
│   ├── routes/             # API routes
│   │   ├── __init__.py
│   │   ├── auth.py         # Authentication routes
│   │   └── todos.py        # Todo CRUD routes
│   └── utils/              # Utility functions
│       ├── __init__.py
│       └── auth.py         # JWT token utilities
├── migrations/             # Database migrations folder
├── seeds/                  # Database seed data
│   ├── __init__.py
│   └── seed.py             # Seed script
└── run.py                  # Application entry point
```

## Project Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd todo_api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env` (or create a new `.env` file)
   - Update the values in the `.env` file if necessary

5. Initialize the database with migrations:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. (Optional) Seed the database with sample data:
```bash
python -m seeds.seed
```

### Running the Application

```bash
python run.py
```

The API will be available at http://localhost:5000

## API Documentation

### Authentication Endpoints

#### Register a new user
- **URL**: `/api/auth/register`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "user1",
    "email": "user1@example.com",
    "password": "password123"
  }
  ```
- **Success Response**: `201 Created`

#### Login
- **URL**: `/api/auth/login`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "user1@example.com",
    "password": "password123"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Login successful",
    "token": "jwt_token_here",
    "user": {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
  }
  ```

#### Get Current User Profile
- **URL**: `/api/auth/me`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Success Response**: `200 OK`

### Todo Endpoints

All todo endpoints require authentication with JWT token in the Authorization header:
`Authorization: Bearer <token>`

#### Get All Todos
- **URL**: `/api/todos`
- **Method**: `GET`
- **Success Response**: `200 OK`
  ```json
  [
    {
      "id": 1,
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "user_id": 1,
      "created_at": "timestamp",
      "updated_at": "timestamp"
    },
    ...
  ]
  ```

#### Get a Todo by ID
- **URL**: `/api/todos/<id>`
- **Method**: `GET`
- **Success Response**: `200 OK`
- **Error Response**: `404 Not Found`

#### Create a Todo
- **URL**: `/api/todos`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "title": "Task title",
    "description": "Task description",
    "completed": false
  }
  ```
- **Success Response**: `201 Created`

#### Update a Todo
- **URL**: `/api/todos/<id>`
- **Method**: `PUT`
- **Request Body**:
  ```json
  {
    "title": "Updated title",
    "description": "Updated description",
    "completed": true
  }
  ```
- **Success Response**: `200 OK`
- **Error Response**: `404 Not Found`

#### Delete a Todo
- **URL**: `/api/todos/<id>`
- **Method**: `DELETE`
- **Success Response**: `200 OK`
- **Error Response**: `404 Not Found`

## Development

### Creating Database Migrations

When you need to make changes to the database schema:

```bash
flask db migrate -m "Description of the changes"
flask db upgrade
```

### Running the Seed Script

To reset the database and populate it with sample data:

```bash
python -m seeds.seed
```

## License

MIT
