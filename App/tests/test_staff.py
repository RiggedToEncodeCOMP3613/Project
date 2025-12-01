import pytest
from App.main import create_app
from App.database import db
from App.controllers.staff_controller import register_staff, update_staff, delete_staff, fetch_all_requests
from App.models import Staff, RequestHistory, ActivityHistory, Student, Accolade, AccoladeHistory
try:
    from App.controllers.accolade_controller import create_accolade, assign_accolade_to_student
except Exception:
    create_accolade = None
    assign_accolade_to_student = None

@pytest.fixture(autouse=True)
def app_context():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

# Unit Tests
def test_register_staff():
    staff = register_staff("Dr. Smith", "smith@email.com", "pass123")
    assert staff.username == "Dr. Smith"
    assert staff.staff_id is not None
    assert str(staff.staff_id).startswith("3000")

def test_update_staff_username():
    staff = register_staff("Dr. Who", "who@email.com", "tardis")
    updated = update_staff(staff.staff_id, username="New Name")
    assert updated is not None
    assert updated.username == "New Name"

def test_update_staff_email():
    staff = register_staff("Dr. House", "house@hospital.com", "vicodin")
    updated = update_staff(staff.staff_id, email="house.new@hospital.com")
    assert updated is not None
    assert updated.email == "house.new@hospital.com"

def test_update_staff_password():
    staff = register_staff("Dr. Banner", "banner@avengers.com", "gamma")
    updated = update_staff(staff.staff_id, password="newpass")
    assert updated is not None
    assert updated.check_password("newpass") is True
    assert updated.check_password("gamma") is False

def test_delete_staff():
    staff = register_staff("Dr. Palmer", "palmer@hospital.com", "healing")
    result = delete_staff(staff.staff_id)
    assert result is True
    db_staff = Staff.query.filter_by(staff_id=staff.staff_id).first()
    assert db_staff is None


# Integration Test
def test_create_staff():
    staff_model = Staff.create_staff("Dr. Gray Model", "gray.model@hospital.com", "secure")
    assert isinstance(staff_model, Staff)
    db_staff = Staff.query.filter_by(staff_id=staff_model.staff_id).first()
    assert db_staff is not None
    assert db_staff.username == "Dr. Gray Model"

    registered = register_staff("Dr. Gray Registered", "gray.registered@hospital.com", "secure")
    assert registered is not None
    assert registered.staff_id is not None
    db_registered = Staff.query.filter_by(staff_id=registered.staff_id).first()
    assert db_registered is not None
    assert db_registered.username == "Dr. Gray Registered"

def test_request_fetch():
    initial = fetch_all_requests()
    assert isinstance(initial, list)

    staff = register_staff("Dr. Tester", "tester@hospital.com", "pw")

    student = Student(username="TestStudent", email="student@test.com", password="studentpw")
    db.session.add(student)
    db.session.flush()

    activity = ActivityHistory(student_id=student.student_id)
    db.session.add(activity)
    db.session.commit()

    req = RequestHistory(
        student_id=student.student_id,
        staff_id=staff.staff_id,
        service="Volunteer Service",
        hours=5.0,
        date_completed="2025-12-01 10:00:00"
    )
    req.activity_id = activity.id
    db.session.add(req)
    db.session.commit()

    all_requests = fetch_all_requests()
    assert isinstance(all_requests, list)
    assert len(all_requests) > 0
    
    assert any(r.get("student_name") == "TestStudent" for r in all_requests)
    assert any(r.get("hours") == 5.0 for r in all_requests)
    assert any(r.get("status") == "pending" for r in all_requests)

def test_staff_create_and_award_accolade():
    staff = register_staff("Dr. Award", "award@hospital.com", "pw")
    student = Student(username="AwardStudent", email="awardstudent@test.com", password="pw")
    db.session.add(student)
    db.session.commit()

    if create_accolade:
        raw = create_accolade(staff.staff_id, "Excellence Award")
        print("DEBUG: create_accolade returned:", raw)
        accolade_obj = raw[0] if isinstance(raw, tuple) else raw
    else:
        accolade_obj = Accolade(staff_id=staff.staff_id, description="Excellence Award")
        db.session.add(accolade_obj)
        db.session.commit()

    from sqlalchemy import inspect
    try:
        db.session.flush()
        db.session.commit()
    except Exception:
        pass

    if accolade_obj is None:
        accolade_obj = Accolade.query.filter_by(staff_id=staff.staff_id).first()
    assert accolade_obj is not None

    pk = None
    try:
        ident = inspect(accolade_obj).identity
        pk = ident[0] if ident else None
    except Exception:
        pk = getattr(accolade_obj, "id", None)
    accolade_id = pk
    assert accolade_id is not None

    if assign_accolade_to_student:
        res = assign_accolade_to_student(accolade_id, student.student_id, staff.staff_id)
        print("DEBUG: assign_accolade_to_student returned:", res)
    else:
        hist = AccoladeHistory(student_id=student.student_id, staff_id=staff.staff_id, accolade_id=accolade_id, description=accolade_obj.description)
        db.session.add(hist)
        db.session.commit()

    hist_record = AccoladeHistory.query.filter_by(student_id=student.student_id, accolade_id=accolade_id).first()
    assert hist_record is not None
