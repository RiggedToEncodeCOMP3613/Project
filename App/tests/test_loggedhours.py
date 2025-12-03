import logging
import unittest

import pytest

from datetime import datetime, timezone

from App.main import create_app
from App.database import db, create_db
from App.models import Student, LoggedHoursHistory, MilestoneHistory
from App.controllers.student_controller import register_student
from App.controllers.staff_controller import register_staff
from App.controllers.loggedHoursHistory_controller import (
    create_logged_hours,
    delete_logged_hours,
    delete_all_logged_hours,
)
from App.controllers.milestone_controller import create_milestone
from App.controllers.leaderboard_controller import generate_leaderboard

LOGGER = logging.getLogger(__name__)

@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


class LoggedHoursUnitTests(unittest.TestCase):

    def test_init_loggedhours(self):
        Testlogged = LoggedHoursHistory(student_id=1, staff_id=2, service="volunteer", hours=20, before=0.0, after=20.0, date_completed="2025-01-01")
        self.assertEqual(Testlogged.student_id, 1)
        self.assertEqual(Testlogged.staff_id, 2)
        self.assertEqual(Testlogged.hours, 20)

    def test_repr_loggedhours(self):
        Testlogged = LoggedHoursHistory(student_id=1, staff_id=2, service="volunteer", hours=20, before=0.0, after=20.0, date_completed="2025-01-01")
        rep = repr(Testlogged)
        # Check all parts of the string representation
        self.assertIn("LoggedHoursHistory ID:", rep)
        self.assertIn("Student ID:", rep)
        self.assertIn("Staff ID:", rep)
        self.assertIn("Hours:", rep)
        self.assertIn("1", rep)
        self.assertIn("2", rep)
        self.assertIn("20", rep)

    def test_create_logged_hours(self):
        # Create a student for testing
        student = Student("Test Student", email="test@student.com", password="password")
        db.session.add(student)
        db.session.commit()
        student_id = student.student_id

        # Create logged hours
        logged_hour = create_logged_hours(student_id=student_id, staff_id=1, hours=5, service="Tutoring", date_completed="2024-01-01")

        self.assertIsNotNone(logged_hour)
        self.assertEqual(logged_hour.student_id, student_id)
        self.assertEqual(logged_hour.hours, 5.0)
        self.assertEqual(logged_hour.service, "Tutoring")
        self.assertEqual(logged_hour.date_completed.strftime("%Y-%m-%d"), "2024-01-01")

    def test_delete_logged_hours(self):
        # Create a student
        student = Student("Test Student", email="test@student.com", password="password")
        db.session.add(student)
        db.session.commit()
        student_id = student.student_id

        # Create a logged hours entry to delete
        logged_hour = create_logged_hours(student_id=student_id, staff_id=1, hours=5, service="Tutoring", date_completed="2024-01-01")
        log_id = logged_hour.id

        # Delete the logged hours entry
        result = delete_logged_hours(log_id)
        self.assertTrue(result)

        # Verify deletion
        deleted_log = LoggedHoursHistory.query.get(log_id)
        self.assertIsNone(deleted_log)

    def test_delete_all_logged_hours(self):
        # Create students
        student1 = Student("Test Student1", email="test1@student.com", password="password")
        db.session.add(student1)
        db.session.commit()
        student2 = Student("Test Student2", email="test2@student.com", password="password")
        db.session.add(student2)
        db.session.commit()

        # Create multiple logged hours entries
        create_logged_hours(student_id=student1.student_id, staff_id=1, hours=5, service="Tutoring", date_completed="2024-01-01")
        create_logged_hours(student_id=student2.student_id, staff_id=1, hours=3, service="Counseling", date_completed="2024-01-02")

        # Delete all logged hours entries
        num_deleted = delete_all_logged_hours()
        self.assertEqual(num_deleted, 2)

        # Verify deletion
        remaining_logs = LoggedHoursHistory.query.all()
        self.assertEqual(len(remaining_logs), 0)


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
        milestone_history = MilestoneHistory.query.filter_by(
            student_id=student.student_id,
            milestone_id=milestone.id
        ).first()
        assert milestone_history is not None
        assert milestone_history.hours == 10

    def test_logged_hours_updates_rank(self):
        # Register multiple students
        student1 = register_student("rank_student1", "rank1@test.com", "password123")
        student2 = register_student("rank_student2", "rank2@test.com", "password123")
        student3 = register_student("rank_student3", "rank3@test.com", "password123")
        assert student1 is not None
        assert student2 is not None
        assert student3 is not None

        # Register staff
        staff = register_staff("rank_staff", "rank_staff@test.com", "password123")
        assert staff is not None

        # Log different hours for each student
        current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Student1: 5 hours
        create_logged_hours(
            student_id=student1.student_id,
            staff_id=staff.staff_id,
            hours=5.0,
            service="volunteer_work",
            date_completed=current_date
        )

        # Student2: 10 hours
        create_logged_hours(
            student_id=student2.student_id,
            staff_id=staff.staff_id,
            hours=10.0,
            service="volunteer_work",
            date_completed=current_date
        )

        # Student3: 3 hours
        create_logged_hours(
            student_id=student3.student_id,
            staff_id=staff.staff_id,
            hours=3.0,
            service="volunteer_work",
            date_completed=current_date
        )

        # Update ranks for all students after logging hours
        student1.calculate_rank()
        student2.calculate_rank()
        student3.calculate_rank()

        # Generate leaderboard and verify ranks
        leaderboard = generate_leaderboard()

        # Find positions in leaderboard
        student1_entry = next(entry for entry in leaderboard if entry['student_id'] == student1.student_id)
        student2_entry = next(entry for entry in leaderboard if entry['student_id'] == student2.student_id)
        student3_entry = next(entry for entry in leaderboard if entry['student_id'] == student3.student_id)

        # Verify hours are correct
        assert student1_entry['hours'] == 5.0
        assert student2_entry['hours'] == 10.0
        assert student3_entry['hours'] == 3.0

        # Verify ranking: student2 (10h) > student1 (5h) > student3 (3h)
        student2_index = leaderboard.index(student2_entry)
        student1_index = leaderboard.index(student1_entry)
        student3_index = leaderboard.index(student3_entry)

        assert student2_index < student1_index < student3_index

        # Verify student ranks are updated correctly
        student1_refreshed = Student.query.get(student1.student_id)
        student2_refreshed = Student.query.get(student2.student_id)
        student3_refreshed = Student.query.get(student3.student_id)

        assert student2_refreshed.rank == 1  # 10 hours
        assert student1_refreshed.rank == 2  # 5 hours
        assert student3_refreshed.rank == 3  # 3 hours