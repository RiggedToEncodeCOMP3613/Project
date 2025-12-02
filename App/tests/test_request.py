import pytest
from App.main import create_app
from App.database import db, create_db
from App.models import Student, Staff, RequestHistory, ActivityHistory
from App.controllers.request_controller import create_request, update_request_entry, delete_request_entry, drop_request_table, process_request_approval, process_request_denial
from App.controllers.student_controller import register_student


@pytest.fixture(autouse=True)
def app_context():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

class TestRequestIntegration:

    def test_update_pending_request(self):
        # Create a student and staff
        student = Student.create_student("testuser", "test@example.com", "testpass")
        staff = Staff("staffuser", "staff@example.com", "staffpass")
        db.session.add(staff)
        db.session.commit()

        # Create a request
        request, message = create_request(student.student_id, "volunteer", staff.staff_id, 5.0, "2023-10-01")
        assert request is not None
        assert request.status == 'Pending'

        # Update the request (change hours and service)
        updated_request, update_message = update_request_entry(request.id, hours=7.5, service="community service")
        assert updated_request is not None
        assert update_message == "Request updated successfully."

        # Fetch the updated request from database
        fetched_request = RequestHistory.query.get(request.id)
        assert fetched_request.hours == 7.5
        assert fetched_request.service == "community service"
        assert fetched_request.status == 'Pending'  # Assuming status not changed

        # Ensure user record has correct values
        fetched_student = Student.query.get(student.student_id)
        assert fetched_student.username == "testuser"
        assert fetched_student.email == "test@example.com"
        assert fetched_student.check_password("testpass")

    def test_create_student(self):
        # Create a student using register_student
        student = register_student("newstudent", "new@example.com", "newpass")
        assert student.username == "newstudent"
        assert student.email == "new@example.com"
        assert student.check_password("newpass")

        # Create a staff
        staff = Staff("staffuser2", "staff2@example.com", "staffpass2")
        db.session.add(staff)
        db.session.commit()

        # Create a pending request
        request, message = create_request(student.student_id, "volunteer", staff.staff_id, 3.0, "2023-10-02")
        assert request is not None
        assert request.status == 'Pending'

        # Update service and hours
        updated_request, update_message = update_request_entry(request.id, service="updated service", hours=5.0)
        assert updated_request is not None
        assert update_message == "Request updated successfully."

        # Verify changes persist
        fetched_request = RequestHistory.query.get(request.id)
        assert fetched_request.service == "updated service"
        assert fetched_request.hours == 5.0
        assert fetched_request.status == 'Pending'

    def test_delete_request_with_activity(self):
        # Create a student and staff
        student = Student.create_student("deletestudent", "delete@example.com", "deletepass")
        staff = Staff("deletestaff", "deletestaff@example.com", "deletestaffpass")
        db.session.add(staff)
        db.session.commit()

        # Create a request (which also creates an ActivityHistory)
        request, message = create_request(student.student_id, "volunteer", staff.staff_id, 4.0, "2023-10-03")
        assert request is not None
        activity_id = request.activity_id
        assert activity_id is not None

        # Verify activity exists
        activity = ActivityHistory.query.get(activity_id)
        assert activity is not None

        # Delete the request
        success, delete_message = delete_request_entry(request.id)
        assert success is True
        assert "deleted successfully" in delete_message

        # Verify request is deleted
        deleted_request = RequestHistory.query.get(request.id)
        assert deleted_request is None

        # Verify activity is also deleted
        deleted_activity = ActivityHistory.query.get(activity_id)
        assert deleted_activity is None


class TestRequestUnit:

    def test_create_request(self):
        student = register_student("testuser", "test@example.com", "testpass")
        staff = Staff("staffuser", "staff@example.com", "staffpass")
        db.session.add(staff)
        db.session.commit()
        request, message = create_request(student.student_id, "volunteer", staff.staff_id, 5.0, "2023-10-01")
        assert request is not None
        assert message == "Request created successfully."
        assert request.status == 'Pending'

    def test_process_request_approval(self):
        student = register_student("testuser", "test@example.com", "testpass")
        staff = Staff("staffuser", "staff@example.com", "staffpass")
        db.session.add(staff)
        db.session.commit()
        request, _ = create_request(student.student_id, "volunteer", staff.staff_id, 5.0, "2023-10-01")
        result = process_request_approval(staff.staff_id, request.id)
        assert result['request'].status == 'Approved'
        assert result['student_name'] == "testuser"
        assert result['staff_name'] == "staffuser"
        assert 'logged_hours' in result

    def test_process_request_denial(self):
        student = register_student("testuser2", "test2@example.com", "testpass")
        staff = Staff("staffuser2", "staff2@example.com", "staffpass")
        db.session.add(staff)
        db.session.commit()
        request, _ = create_request(student.student_id, "volunteer", staff.staff_id, 5.0, "2023-10-01")
        result = process_request_denial(staff.staff_id, request.id)
        assert result['request'].status == 'Denied'
        assert result['student_name'] == "testuser2"
        assert result['staff_name'] == "staffuser2"
        assert result['denial_successful'] is True

    def test_delete_request_entry(self):
        
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

    def test_update_request_student_id(self):
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

    def test_update_request_service(self):
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

    def test_update_request_hours(self):
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

    def test_update_request_status(self):
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

    def test_drop_request_table(self):
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
    
