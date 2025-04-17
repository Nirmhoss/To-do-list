import sys
import os
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.todo import Todo

def seed_database():
    """
    Seed the database with sample data
    
    This function creates sample users and todos for testing purposes
    """
    app = create_app()
    
    with app.app_context():
        print("Starting database seed...")
        
        # Clear existing data
        db.session.query(Todo).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Create sample users
        users = [
            User(username='user1', email='user1@example.com', password='password123'),
            User(username='user2', email='user2@example.com', password='password123')
        ]
        
        db.session.add_all(users)
        db.session.commit()
        
        # Create sample todos
        todos = [
            Todo(title='Complete project', description='Finish the TODO API project', user_id=1),
            Todo(title='Learn Flask', description='Study Flask framework in depth', user_id=1),
            Todo(title='Exercise', description='Go for a 30-minute run', completed=True, user_id=1),
            Todo(title='Read book', description='Read chapter 5 of Python cookbook', user_id=2),
            Todo(title='Buy groceries', description='Milk, eggs, bread, and vegetables', user_id=2)
        ]
        
        db.session.add_all(todos)
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()