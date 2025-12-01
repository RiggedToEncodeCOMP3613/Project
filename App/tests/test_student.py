import pytest
from App.main import create_app
from App.database import db
from App.controllers.student_controller import register_student
from App.models import Student

@pytest.fixture(autouse=True)
def app_context():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_register_student():
    student = register_student("Alice", "alice@email.com", "pass123")
    assert student.username == "Alice"
    assert student.student_id is not None
    assert str(student.student_id).startswith("8160")