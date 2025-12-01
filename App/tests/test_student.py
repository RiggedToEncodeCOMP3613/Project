import pytest
from App.main import create_app
from App.database import db
from App.controllers.student_controller import register_student, delete_student
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

#Unit Tests
def test_register_student():
    student = register_student("Alice", "alice@email.com", "pass123")
    assert student.username == "Alice"
    assert student.student_id is not None
    assert str(student.student_id).startswith("8160")

def test_delete_student():
    student = register_student("Bob", "bob@example.com", "pw")
    sid = student.student_id
    result = delete_student(sid)
    assert result is True
    assert Student.query.get(sid) is None


#Integration Test
def test_create_student():
    student_model = Student.create_student("Student Model", "student.model@test.com", "pw")
    assert isinstance(student_model, Student)
    db_student = Student.query.filter_by(student_id=student_model.student_id).first()
    assert db_student is not None
    assert db_student.username == "Student Model"

    registered = register_student("Student Registered", "student.registered@test.com", "pw")
    assert registered is not None
    assert registered.student_id is not None
    db_registered = Student.query.filter_by(student_id=registered.student_id).first()
    assert db_registered is not None
    assert db_registered.username == "Student Registered"