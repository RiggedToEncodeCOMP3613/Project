import pytest
from App.main import create_app
from App.database import db
from App.controllers.student_controller import register_student, delete_student
from App.models import Student
from App.controllers.leaderboard_controller import generate_leaderboard

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


def test_generate_leaderboard():
    s_a = Student.create_student("Student A", "a@test.com", "pw")
    s_b = Student.create_student("Student B", "b@test.com", "pw")
    s_c = Student.create_student("Student C", "c@test.com", "pw")

    s_a.total_hours = 5.0
    s_b.total_hours = 15.0
    s_c.total_hours = 10.0
    db.session.commit()

    leaderboard = generate_leaderboard()
    assert isinstance(leaderboard, list)
    assert leaderboard[0]['name'] == 'Student B' and leaderboard[0]['hours'] == 15.0
    assert leaderboard[1]['name'] == 'Student C' and leaderboard[1]['hours'] == 10.0
    assert leaderboard[2]['name'] == 'Student A' and leaderboard[2]['hours'] == 5.0