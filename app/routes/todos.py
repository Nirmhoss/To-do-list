from flask import Blueprint, request, jsonify

from app import db
from app.models.todo import Todo
from app.utils.auth import token_required

# Create blueprint
todos_bp = Blueprint('todos', __name__)

@todos_bp.route('', methods=['GET'])
@token_required
def get_todos(current_user):
    """
    Get all todos for the current user
    
    This route is protected by the token_required decorator
    
    Returns:
        200: List of todos
    """
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return jsonify([todo.to_dict() for todo in todos]), 200

@todos_bp.route('/<int:todo_id>', methods=['GET'])
@token_required
def get_todo(current_user, todo_id):
    """
    Get a specific todo by ID
    
    This route is protected by the token_required decorator
    
    Args:
        todo_id: The ID of the todo to retrieve
    
    Returns:
        200: Todo details
        404: Todo not found
    """
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
        
    return jsonify(todo.to_dict()), 200

@todos_bp.route('', methods=['POST'])
@token_required
def create_todo(current_user):
    """
    Create a new todo
    
    This route is protected by the token_required decorator
    
    Request body:
        {
            "title": "string",
            "description": "string" (optional),
            "completed": boolean (optional, defaults to false)
        }
    
    Returns:
        201: Created todo
        400: Title is required
    """
    data = request.get_json()
    
    # Check if required fields are provided
    if 'title' not in data:
        return jsonify({'message': 'Title is required'}), 400
    
    # Create new todo
    new_todo = Todo(
        title=data['title'],
        description=data.get('description', ''),
        completed=data.get('completed', False),
        user_id=current_user.id
    )
    
    # Add todo to database
    db.session.add(new_todo)
    db.session.commit()
    
    return jsonify(new_todo.to_dict()), 201

@todos_bp.route('/<int:todo_id>', methods=['PUT'])
@token_required
def update_todo(current_user, todo_id):
    """
    Update a todo
    
    This route is protected by the token_required decorator
    
    Args:
        todo_id: The ID of the todo to update
        
    Request body:
        {
            "title": "string" (optional),
            "description": "string" (optional),
            "completed": boolean (optional)
        }
    
    Returns:
        200: Updated todo
        404: Todo not found
    """
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    
    data = request.get_json()
    
    # Update todo fields if they are provided
    if 'title' in data:
        todo.title = data['title']
    if 'description' in data:
        todo.description = data['description']
    if 'completed' in data:
        todo.completed = data['completed']
    
    db.session.commit()
    
    return jsonify(todo.to_dict()), 200

@todos_bp.route('/<int:todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    """
    Delete a todo
    
    This route is protected by the token_required decorator
    
    Args:
        todo_id: The ID of the todo to delete
        
    Returns:
        200: Todo deleted successfully
        404: Todo not found
    """
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({'message': 'Todo deleted successfully'}), 200