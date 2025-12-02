import pytest
from App.main import create_app
from App.database import db
from App.controllers.request_controller import delete_request_entry, update_request_entry, drop_request_table
from App.controllers.student_controller import register_student
from App.models import RequestHistory, ActivityHistory

@pytest.fixture(autouse=True)
def app_context():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


# Unit Test
def test_delete_request_entry_unit():
    
    req = RequestHistory(
        student_id=1,
        staff_id=1,
        service="Test",
        hours=1.0,
        date_completed="2025-12-01"
    )
    req.activity_id = 1
    db.session.add(req)
    db.session.commit()
    request_id = req.id

    success, message = delete_request_entry(request_id)
    
    assert success is True
    assert "deleted successfully" in message.lower()
    
    deleted_req = RequestHistory.query.filter_by(id=request_id).first()
    assert deleted_req is None

def test_update_request_student_id():
    student1 = register_student("Student1", "student1@test.com", "pw1")
    student2 = register_student("Student2", "student2@test.com", "pw2")
    
    activity = ActivityHistory(student_id=student1.student_id)
    db.session.add(activity)
    db.session.commit()
    
    req = RequestHistory(
        student_id=student1.student_id,
        staff_id=1,
        service="Test Service",
        hours=2.0,
        date_completed="2025-12-01"
    )
    req.activity_id = activity.id
    db.session.add(req)
    db.session.commit()
    request_id = req.id

    updated_req, message = update_request_entry(request_id, student_id=student2.student_id)
    
    assert updated_req is not None
    assert "successfully" in message.lower()
    assert updated_req.student_id == student2.student_id
    
    db_req = RequestHistory.query.filter_by(id=request_id).first()
    assert db_req is not None
    assert db_req.student_id == student2.student_id

def test_update_request_service():
    student = register_student("ServiceStudent", "service@test.com", "pw")
    
    activity = ActivityHistory(student_id=student.student_id)
    db.session.add(activity)
    db.session.commit()
    
    req = RequestHistory(
        student_id=student.student_id,
        staff_id=1,
        service="Original Service",
        hours=2.0,
        date_completed="2025-12-01"
    )
    req.activity_id = activity.id
    db.session.add(req)
    db.session.commit()
    request_id = req.id

    updated_req, message = update_request_entry(request_id, service="New Service")
    
    assert updated_req is not None
    assert "successfully" in message.lower()
    assert updated_req.service == "New Service"
    
    db_req = RequestHistory.query.filter_by(id=request_id).first()
    assert db_req is not None
    assert db_req.service == "New Service"

def test_update_request_hours():
    student = register_student("HoursStudent", "hours@test.com", "pw")
    
    activity = ActivityHistory(student_id=student.student_id)
    db.session.add(activity)
    db.session.commit()
    
    req = RequestHistory(
        student_id=student.student_id,
        staff_id=1,
        service="Test Service",
        hours=5.0,
        date_completed="2025-12-01"
    )
    req.activity_id = activity.id
    db.session.add(req)
    db.session.commit()
    request_id = req.id

    updated_req, message = update_request_entry(request_id, hours=10.5)
    
    assert updated_req is not None
    assert "successfully" in message.lower()
    assert updated_req.hours == 10.5
    
    db_req = RequestHistory.query.filter_by(id=request_id).first()
    assert db_req is not None
    assert db_req.hours == 10.5

def test_update_request_status():
    student = register_student("StatusStudent", "status@test.com", "pw")
    
    activity = ActivityHistory(student_id=student.student_id)
    db.session.add(activity)
    db.session.commit()
    
    req = RequestHistory(
        student_id=student.student_id,
        staff_id=1,
        service="Test Service",
        hours=3.0,
        date_completed="2025-12-01"
    )
    req.activity_id = activity.id
    db.session.add(req)
    db.session.commit()
    request_id = req.id

    updated_req, message = update_request_entry(request_id, status="Approved")
    
    assert updated_req is not None
    assert "successfully" in message.lower()
    assert updated_req.status.lower() == "approved"
    
    db_req = RequestHistory.query.filter_by(id=request_id).first()
    assert db_req is not None
    assert db_req.status.lower() == "approved"

def test_drop_request_table():
    student = register_student("DropStudent", "drop@test.com", "pw")
    
    activity = ActivityHistory(student_id=student.student_id)
    db.session.add(activity)
    db.session.commit()
    
    for i in range(3):
        req = RequestHistory(
            student_id=student.student_id,
            staff_id=1,
            service=f"Service {i}",
            hours=float(i + 1),
            date_completed="2025-12-01"
        )
        req.activity_id = activity.id
        db.session.add(req)
    db.session.commit()
    
    count_before = RequestHistory.query.count()
    assert count_before >= 3
    
    result, error = drop_request_table()
    
    assert isinstance(result, dict)
    assert result.get('requests_deleted') >= 0
    assert error is None
    
    count_after = RequestHistory.query.count()
    assert count_after == 0
