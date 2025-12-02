import unittest, pytest
from App.main import create_app
from App.database import db, create_db
from App.models import Student, Staff, RequestHistory, ActivityHistory
from App.controllers.request_controller import create_request, update_request_entry, delete_request_entry
from App.controllers.student_controller import register_student

@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class RequestIntegrationTests(unittest.TestCase):

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

    