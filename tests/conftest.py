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
    yield client