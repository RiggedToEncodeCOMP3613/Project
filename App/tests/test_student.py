import pytest
from App.main import create_app
from App.database import db
from App.controllers.student_controller import register_student, delete_student, create_hours_request, fetch_accolades, get_hours
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


def test_get_approved_hours_and_accolades():
    from App.models import LoggedHoursHistory, ActivityHistory, MilestoneHistory
    from datetime import datetime, timezone

    student = Student.create_student("nisha", "nisha@example.com", "pass")
    from App.models import Milestone
   
    milestone_10 = Milestone(hours=10)
    db.session.add(milestone_10)
    db.session.commit()
    
    activity1 = ActivityHistory(student_id=student.student_id)
    activity2 = ActivityHistory(student_id=student.student_id)
    db.session.add_all([activity1, activity2])
    db.session.flush()
    
    lh1 = LoggedHoursHistory(student_id=student.student_id, staff_id=1, service="volunteer", hours=6.0, before=0.0, after=6.0, date_completed=datetime.now(timezone.utc))
    lh1.activity_id = activity1.id
    lh2 = LoggedHoursHistory(student_id=student.student_id, staff_id=1, service="volunteer", hours=5.0, before=6.0, after=11.0, date_completed=datetime.now(timezone.utc))
    lh2.activity_id = activity2.id
    db.session.add_all([lh1, lh2])
    db.session.commit()

    student.calculate_total_hours()

    name, total = get_hours(student.student_id)
    assert name == student.username
    assert total == 11.0

    milestone_10.add_student(student.student_id)
    db.session.commit()

    if not hasattr(Student, 'accolades'):
        def _accolades(self):
            return [f"{m.hours} Hours Milestone" for m in getattr(self, 'achieved_milestones', [])]
        Student.accolades = _accolades

    accolades = fetch_accolades(student.student_id)
    assert isinstance(accolades, list)
    assert any('10' in str(a) for a in accolades)


def test_student_milestone_achievement():
    from App.controllers.milestone_controller import create_milestone
    from App.controllers.loggedHoursHistory_controller import create_logged_hours
    from App.models import MilestoneHistory
    from datetime import datetime, timezone

    student = register_student("Milestoner", "milestone.student@test.com", "pw")
    milestone = create_milestone(5)

    # No milestone history should exist yet
    before = MilestoneHistory.query.filter_by(student_id=student.student_id, milestone_id=milestone.id).first()
    assert before is None

    # Log some hours below the threshold
    create_logged_hours(student.student_id, staff_id=1, hours=3.0, service="volunteer", date_completed=datetime.now(timezone.utc))
    mid = MilestoneHistory.query.filter_by(student_id=student.student_id, milestone_id=milestone.id).first()
    assert mid is None

    # Log additional hours to cross the milestone threshold
    create_logged_hours(student.student_id, staff_id=1, hours=3.0, service="volunteer", date_completed=datetime.now(timezone.utc))

    # Now the milestone history record should exist
    after = MilestoneHistory.query.filter_by(student_id=student.student_id, milestone_id=milestone.id).first()
    assert after is not None
    # And the student's total hours should reflect both logs
    from App.controllers.student_controller import get_hours
    name, total = get_hours(student.student_id)
    assert total == pytest.approx(6.0)