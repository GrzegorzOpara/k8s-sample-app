from app import create_app  # Assuming create_app function exists
from app.models import User
import pytest

@pytest.fixture
def client():
    with create_app('testing') as app:
        with app.test_client() as client:
            # Perform test setup (optional)
            yield client  # Yield the client fixture