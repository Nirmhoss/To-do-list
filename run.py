from app import create_app, db

# Create the application using the factory function
app = create_app()

# Create tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Run the application with debugging enabled
    app.run(debug=True, host='0.0.0.0', port=5000)