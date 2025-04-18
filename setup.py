from setuptools import find_packages, setup

setup(
    name="todo_api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "Flask-SQLAlchemy",
        "Flask-Migrate",
        "Flask-Cors",
        "PyJWT",
        "python-dotenv",
        "werkzeug",
    ],
    python_requires=">=3.9",
)
