from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
import pytest

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    role= db.Column(db.String(256),nullable=False, default="user")  #Create role column to distinguish user types

    __mapper_args__ = {
        "polymorphic_on": role,
        "polymorphic_identity": "user"
    }

    def __init__(self, username, email,password,role):
        self.username = username
        self.role=role
        self.set_password(password)
        self.email= email

    def get_json(self):
        return{
            'id': self.user_id,
            'username': self.username,
            'email': self.email
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
class testUser:
    @pytest.fixture
    def user(self):
        return User(username="testuser", email="testuser@example.com", password="password", role="user")
    def test_check_password(self, user):
        user.set_password("newpassword")
        assert user.check_password("newpassword") is True
        assert user.check_password("wrongpassword") is False
    def test_hashed_password(self, user):
        user.set_password("something")
        assert user.password != "something"


# from werkzeug.security import check_password_hash, generate_password_hash
# from App.database import db

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username =  db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(256), nullable=False)

#     def __init__(self, username, password):
#         self.username = username
#         self.set_password(password)

    
#     def get_json(self):
#         return{
#             'id': self.id,
#             'username': self.username
#         }

#     def set_password(self, password):
#         """Create hashed password."""
#         self.password = generate_password_hash(password)
    
#     def check_password(self, password):
#         """Check hashed password."""
#         return check_password_hash(self.password, password)

