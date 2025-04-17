from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
import os

from app import db
from app.models.user import User
from app.utils.auth import token_required

# Create blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request body:
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }
    
    Returns:
        201: User registered successfully
        400: Missing required fields
        409: User already exists
    """
    data = request.get_json()
    
    # Check if required fields are provided
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User with this email already exists'}), 409
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already taken'}), 409
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    # Add user to database
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and generate JWT token
    
    Request body:
        {
            "email": "string",
            "password": "string"
        }
    
    Returns:
        200: Login successful with JWT token
        400: Missing email or password
        401: Invalid credentials
    """
    data = request.get_json()
    
    # Check if required fields are provided
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'message': 'Missing email or password'}), 400
    
    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    # Generate JWT token
    token = jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiration time
        },
        os.environ.get('JWT_SECRET_KEY', 'default-jwt-secret-key'),
        algorithm='HS256'
    )
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_user_profile(current_user):
    """
    Get the current user's profile
    
    This route is protected by the token_required decorator
    
    Returns:
        200: User profile
    """
    return jsonify(current_user.to_dict()), 200