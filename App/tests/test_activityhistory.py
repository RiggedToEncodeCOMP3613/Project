import logging
import unittest

import pytest

from datetime import datetime, timezone

from App.main import create_app
from App.database import db, create_db
from App.models import Student, RequestHistory, Staff, ActivityHistory, LoggedHoursHistory, AccoladeHistory, MilestoneHistory
from App.controllers.student_controller import register_student
from App.controllers.staff_controller import register_staff
from App.controllers.request_controller import create_request
from App.controllers.loggedHoursHistory_controller import create_logged_hours
from App.controllers.accolade_controller import create_accolade, assign_accolade_to_student
from App.controllers.milestone_controller import create_milestone

LOGGER = logging.getLogger(__name__)

# This fixture creates an empty database for the test and deletes it after the test
@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class ActivityHistoryIntegrationTests(unittest.TestCase):

    def test_activity_history_request_tracking(self):
  
        # Register a student
        student = register_student("test_student_request", "test_request@example.com", "testpass")
        assert student is not None
        assert student.username == "test_student_request"

        # Register a staff member
        staff = register_staff("test_staff_request", "staff_request@example.com", "staffpass")
        assert staff is not None
        assert staff.username == "test_staff_request"

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

    def test_activity_history_logged_hours_tracking(self):
    
        # Register a student
        student = register_student("test_student_hours", "test_hours@example.com", "testpass")
        assert student is not None
        assert student.username == "test_student_hours"

        # Register a staff member
        staff = register_staff("test_staff_hours", "staff_hours@example.com", "staffpass")
        assert staff is not None
        assert staff.username == "test_staff_hours"

        # Create logged hours using the student and staff
        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        logged_hours = create_logged_hours(
            student_id=student.student_id,
            staff_id=staff.staff_id,
            hours=3.5,
            service="community_service",
            date_completed=current_date
        )

        # Verify logged hours was created successfully
        assert logged_hours is not None
        assert logged_hours.student_id == student.student_id
        assert logged_hours.staff_id == staff.staff_id
        assert logged_hours.hours == 3.5
        assert logged_hours.service == "community_service"

        # Verify ActivityHistory was created and linked
        assert logged_hours.activity_id is not None

        # Fetch the ActivityHistory from the database
        activity_history = ActivityHistory.query.get(logged_hours.activity_id)
        assert activity_history is not None
        assert activity_history.student_id == student.student_id

        # Verify the logged hours is properly linked to the activity history
        assert logged_hours in activity_history.loggedhours

        # Verify the activity history is properly linked to the student
        assert activity_history in student.activity_history

        # Verify the activity history contains the logged hours entry
        assert len(activity_history.loggedhours) == 1
        assert activity_history.loggedhours[0].id == logged_hours.id

        LOGGER.info("ActivityHistory logged hours tracking test passed successfully!")

    def test_activity_history_accolade_tracking(self):
  
        # Register a student
        student = register_student("test_student_accolade", "test_accolade@example.com", "testpass")
        assert student is not None
        assert student.username == "test_student_accolade"

        # Register a staff member
        staff = register_staff("test_staff_accolade", "staff_accolade@example.com", "staffpass")
        assert staff is not None
        assert staff.username == "test_staff_accolade"

        # Create an accolade using the staff member
        accolade, message = create_accolade(staff.staff_id, "Test Accolade for Achievement")
        assert accolade is not None
        assert message is None
        assert accolade.staff_id == staff.staff_id
        assert accolade.description == "Test Accolade for Achievement"

        # Assign the accolade to the student
        result, error = assign_accolade_to_student(
            accolade_id=accolade.id,
            student_id=student.student_id,
            staff_id=staff.staff_id
        )

        # Verify the assignment was successful
        assert result is not None
        assert error is None
        assert 'accolade' in result
        assert 'student' in result
        assert 'history' in result

        # Extract the history record from the result
        history_record = result['history']
        assert history_record is not None
        assert history_record.accolade_id == accolade.id
        assert history_record.student_id == student.student_id
        assert history_record.staff_id == staff.staff_id
        assert history_record.description == accolade.description

        # Verify ActivityHistory was created and linked
        assert history_record.activity_id is not None

        # Fetch the ActivityHistory from the database
        activity_history = ActivityHistory.query.get(history_record.activity_id)
        assert activity_history is not None
        assert activity_history.student_id == student.student_id

        # Verify the accolade history is properly linked to the activity history
        assert history_record in activity_history.accolades

        # Verify the activity history is properly linked to the student
        assert activity_history in student.activity_history

        # Verify the activity history contains the accolade history entry
        assert len(activity_history.accolades) == 1
        assert activity_history.accolades[0].id == history_record.id

        LOGGER.info("ActivityHistory accolade tracking test passed successfully!")

    def test_activity_history_milestone_tracking(self):

        # Register a student
        student = register_student("test_student_milestone", "test_milestone@example.com", "testpass")
        assert student is not None
        assert student.username == "test_student_milestone"

        # Create a milestone with 10 hours requirement
        milestone = create_milestone(10)
        assert milestone is not None
        assert milestone.hours == 10

        # Create logged hours to make student reach the milestone
        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        logged_hours = create_logged_hours(
            student_id=student.student_id,
            staff_id=None,  # No staff needed for this test
            hours=10.0,
            service="volunteer",
            date_completed=current_date
        )

        # Verify logged hours was created successfully
        assert logged_hours is not None
        assert logged_hours.student_id == student.student_id
        assert logged_hours.hours == 10.0

        # Update student's total hours to trigger milestone calculation
        student.calculate_total_hours()

        # Verify student has reached the milestone
        assert student.total_hours >= milestone.hours

        # Check if milestone history was created
        milestone_history = MilestoneHistory.query.filter_by(
            milestone_id=milestone.id,
            student_id=student.student_id
        ).first()

        assert milestone_history is not None
        assert milestone_history.milestone_id == milestone.id
        assert milestone_history.student_id == student.student_id
        assert milestone_history.hours == milestone.hours

        # Verify ActivityHistory was created and linked
        assert milestone_history.activity_id is not None

        # Fetch the ActivityHistory from the database
        activity_history = ActivityHistory.query.get(milestone_history.activity_id)
        assert activity_history is not None
        assert activity_history.student_id == student.student_id

        # Verify the milestone history is properly linked to the activity history
        assert milestone_history in activity_history.milestones

        # Verify the activity history is properly linked to the student
        assert activity_history in student.activity_history

        # Verify the activity history contains the milestone history entry
        assert len(activity_history.milestones) == 1
        assert activity_history.milestones[0].id == milestone_history.id

        LOGGER.info("ActivityHistory milestone tracking test passed successfully!")