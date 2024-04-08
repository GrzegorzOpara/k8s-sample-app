# Third party modules
import pytest

# First party modules
from app import create_app, db
from app.models import User

@pytest.fixture
def client():
    app = create_app(config='test')

    app.config["TESTING"] = True
    app.testing = True

    client = app.test_client()

    with app.app_context():
        db.create_all()
        user1 = User(name="adam", email="januszek@domain.com")
        user2 = User(name="ala", email="ala@domain.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
    yield client