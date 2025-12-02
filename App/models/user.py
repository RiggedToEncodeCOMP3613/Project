import pytest
from App.models import User


@pytest.fixture
def user():
    return User(username="testuser", email="testuser@example.com", password="password", role="user")


class TestUser:

    def test_check_password(self):
        test_user = User("David Goggins", "goggs@gmail.com", "goggs123", "student")
        assert test_user.check_password("goggs123")

    def test_set_password(self):
        password = "passtest"
        new_password = "passtest"
        test_user = User("bob", "bob@email.com", password, "user")
        test_user.set_password(new_password)
        assert test_user.check_password(new_password)

    def test_check_password_with_fixture(self, user):
        user.set_password("newpassword")
        assert user.check_password("newpassword")
        assert not user.check_password("wrongpassword")

    def test_password_is_hashed(self, user):
        user.set_password("something")
        assert user.password != "something"