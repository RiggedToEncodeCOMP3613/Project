import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, RequestHistory, Staff, ActivityHistory
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)
from App.controllers.student_controller import (
    register_student,
    create_hours_request,
    fetch_requests,
    get_hours,
    fetch_accolades
)
from App.controllers.leaderboard_controller import generate_leaderboard
from App.controllers.staff_controller import (
    register_staff,
    fetch_all_requests,
    process_request_approval,
    process_request_denial
)
from App.controllers.request_controller import create_request

LOGGER = logging.getLogger(__name__)

# This fixture creates an empty database for the test and deletes it after the test
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class ActivityHistoryRequestTrackingTests(unittest.TestCase):

    def test_activity_history_request_tracking(self):
        """
        Test: test_activity_history_request_tracking()
        Dependencies: register_student(), create_request()
        Description: Create request, verify ActivityHistory created and linked
        """
        # Register a student
        student = register_student("test_student", "test@example.com", "testpass")
        assert student is not None
        assert student.username == "test_student"

        # Register a staff member
        staff = register_staff("test_staff", "staff@example.com", "staffpass")
        assert staff is not None
        assert staff.username == "test_staff"

        # Create a request using the student and staff
        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        request, message = create_request(
            student_id=student.student_id,
            service="volunteer",
            staff_id=staff.staff_id,
            hours=5.0,
            date_completed=current_date
        )

        # Verify request was created successfully
        assert request is not None
        assert message == "Request created successfully."
        assert request.student_id == student.student_id
        assert request.staff_id == staff.staff_id
        assert request.hours == 5.0
        assert request.service == "volunteer"

        # Verify ActivityHistory was created and linked
        assert request.activity_id is not None

        # Fetch the ActivityHistory from the database
        activity_history = ActivityHistory.query.get(request.activity_id)
        assert activity_history is not None
        assert activity_history.student_id == student.student_id

        # Verify the request is properly linked to the activity history
        assert request in activity_history.requests

        # Verify the activity history is properly linked to the student
        assert activity_history in student.activity_history

        # Verify the activity history contains the request
        assert len(activity_history.requests) == 1
        assert activity_history.requests[0].id == request.id

        LOGGER.info("ActivityHistory request tracking test passed successfully!")