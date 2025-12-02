import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, RequestHistory, Staff, LoggedHoursHistory
from App.controllers.student_controller import register_student
from App.controllers.staff_controller import register_staff
from App.controllers.loggedHoursHistory_controller import create_logged_hours
from App.controllers.milestone_controller import create_milestone

LOGGER = logging.getLogger(__name__)

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class LoggedHoursIntegrationTests(unittest.TestCase):

    def test_logged_hours_student_total_update(self):
        # Register student
        student = register_student("test_student", "student@test.com", "password123")
        assert student is not None
        assert student.total_hours == 0.0

        # Register staff
        staff = register_staff("test_staff", "staff@test.com", "password123")
        assert staff is not None

        # Log hours for the student
        from datetime import datetime, timezone
        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        logged_hours = create_logged_hours(
            student_id=student.student_id,
            staff_id=staff.staff_id,
            hours=5.0,
            service="volunteer_work",
            date_completed=current_date
        )
        assert logged_hours is not None
        assert logged_hours.hours == 5.0

        # Verify student's total_hours has been updated
        student_refreshed = Student.query.get(student.student_id)
        assert student_refreshed.total_hours == 5.0

    def test_logged_hours_triggers_milestone(self):
        # Create a milestone at 10 hours
        milestone = create_milestone(10)
        assert milestone is not None
        assert milestone.hours == 10

        # Register student
        student = register_student("milestone_student", "milestone@test.com", "password123")
        assert student is not None
        assert student.total_hours == 0.0

        # Register staff
        staff = register_staff("milestone_staff", "milestone_staff@test.com", "password123")
        assert staff is not None

        # Log 12 hours for the student (over the 10 hour milestone threshold)
        from datetime import datetime, timezone
        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        logged_hours = create_logged_hours(
            student_id=student.student_id,
            staff_id=staff.staff_id,
            hours=12.0,
            service="volunteer_work",
            date_completed=current_date
        )
        assert logged_hours is not None
        assert logged_hours.hours == 12.0

        # Verify student's total_hours has been updated
        student_refreshed = Student.query.get(student.student_id)
        assert student_refreshed.total_hours == 12.0

        # Verify milestone has been awarded
        from App.models.milestoneHistory import MilestoneHistory
        milestone_history = MilestoneHistory.query.filter_by(
            student_id=student.student_id,
            milestone_id=milestone.id
        ).first()
        assert milestone_history is not None
        assert milestone_history.hours == 10