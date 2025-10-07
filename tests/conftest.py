import pytest
import os
from simplechat import create_app, db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Set environment variables for testing
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database

    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
