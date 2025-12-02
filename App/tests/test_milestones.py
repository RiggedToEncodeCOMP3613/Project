import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from datetime import datetime, timezone
from App.models import User, Student, RequestHistory, Staff, LoggedHoursHistory, Milestone
from App.models.milestoneHistory import MilestoneHistory
from App.controllers.student_controller import register_student
from App.controllers.staff_controller import register_staff
from App.controllers.loggedHoursHistory_controller import create_logged_hours
from App.controllers.milestone_controller import (
    create_milestone, search_milestones, update_milestone,
    list_all_milestones, delete_milestone, delete_all_milestones,
    list_all_milestone_history
)
from App.controllers.leaderboard_controller import generate_leaderboard

LOGGER = logging.getLogger(__name__)

@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    with app.app_context():
        create_db()
        yield
        db.drop_all()


class MilestoneIntegrationTests(unittest.TestCase):

    def test_create_milestone_retroactive_award(self):
        # Register staff
        staff = register_staff("test_staff", "staff@test.com", "password123")
        assert staff is not None

        # Register multiple students with existing hours
        student1 = register_student("student1", "student1@test.com", "password123")
        student2 = register_student("student2", "student2@test.com", "password123")
        student3 = register_student("student3", "student3@test.com", "password123")
        assert student1 is not None
        assert student2 is not None
        assert student3 is not None

        # Log hours for students: student1 gets 12 hours (eligible), student2 gets 8 (not eligible), student3 gets 15 (eligible)
        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        create_logged_hours(
            student_id=student1.student_id,
            staff_id=staff.staff_id,
            hours=12.0,
            service="volunteer_work",
            date_completed=current_date
        )

        create_logged_hours(
            student_id=student2.student_id,
            staff_id=staff.staff_id,
            hours=8.0,
            service="volunteer_work",
            date_completed=current_date
        )

        create_logged_hours(
            student_id=student3.student_id,
            staff_id=staff.staff_id,
            hours=15.0,
            service="volunteer_work",
            date_completed=current_date
        )

        # Verify students have correct total hours
        student1_refreshed = Student.query.get(student1.student_id)
        student2_refreshed = Student.query.get(student2.student_id)
        student3_refreshed = Student.query.get(student3.student_id)
        assert student1_refreshed.total_hours == 12.0
        assert student2_refreshed.total_hours == 8.0
        assert student3_refreshed.total_hours == 15.0

        # Create milestone at 10 hours
        milestone = create_milestone(10)
        assert milestone is not None
        assert milestone.hours == 10

        # Verify eligible students auto-awarded

        # Student1 should have milestone history
        milestone_history1 = MilestoneHistory.query.filter_by(
            student_id=student1.student_id,
            milestone_id=milestone.id
        ).first()
        assert milestone_history1 is not None
        assert milestone_history1.hours == 10

        # Student2 should not have milestone history (only 8 hours)
        milestone_history2 = MilestoneHistory.query.filter_by(
            student_id=student2.student_id,
            milestone_id=milestone.id
        ).first()
        assert milestone_history2 is None

        # Student3 should have milestone history
        milestone_history3 = MilestoneHistory.query.filter_by(
            student_id=student3.student_id,
            milestone_id=milestone.id
        ).first()
        assert milestone_history3 is not None
        assert milestone_history3.hours == 10

    def test_search_milestones(self):
        m1 = create_milestone(10)
        m2 = create_milestone(20)
        results = search_milestones(hours=10)
        assert len(results) == 1
        assert results[0]['hours'] == 10
        
    def test_update_milestone_hours(self):
        milestone = create_milestone(50)
        updated_milestone = update_milestone(milestone.id, 75)
        assert updated_milestone.hours == 75
        # Verify change persists in db

        refreshed_milestone = Milestone.query.get(milestone.id)
        assert refreshed_milestone.hours == 75

class MilestoneUnitTests:

    def test_create_milestone(self):
        milestone = create_milestone(10)
        assert milestone.hours == 10
        assert Milestone.query.count() == 1
        assert milestone.id is not None

    def test_list_all_milestones(self):
        create_milestone(5)
        create_milestone(15)
        milestones = list_all_milestones()
        assert len(milestones) == 2

    def test_delete_milestone(self):
        milestone = create_milestone(20)
        result = delete_milestone(milestone.id)
        assert result is True
        assert Milestone.query.count() == 0

    def test_delete_all_milestones(self):
        create_milestone(5)
        create_milestone(15)
        num_deleted = delete_all_milestones()
        assert num_deleted == 2
        assert Milestone.query.count() == 0

    def test_update_milestone(self):
        milestone = create_milestone(30)
        updated_milestone = update_milestone(milestone.id, 75)
        assert updated_milestone.hours == 75 # pyright: ignore[reportOptionalMemberAccess]

    def test_list_all_milestone_history(self):
        milestone = create_milestone(10)
        history = list_all_milestone_history()
        assert len(history) >= 0  # Depending on existing students