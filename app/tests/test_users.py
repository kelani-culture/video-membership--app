import pytest
from ..users.model import User
from app import db

@pytest.fixture(scope='module')
def setup():
    session = db.get_session()
    yield session
    q = User.objects.filter(email='test@gmail.com')
    if q.count() == 0:
        q.delete()
    session.shutdown()


def test_create_user(setup):
    User.create_user(email='test@test.com', password='abc123')

def test_create_duplicate_user(setup):
    with pytest.raises(Exception):  
        User.create_user(email='test@test.com', password='abc123')