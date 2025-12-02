import unittest
from App.models import LoggedHoursHistory, ActivityHistory
from App.database import db
from App.models import Student
import pytest

# CLI COMMAND FUNCTIONS

def create_logged_hours(student_id, staff_id, hours, service, date_completed):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found")

    # Get or create activity history for the student
    activity = ActivityHistory.query.filter_by(student_id=student_id).first()
    if not activity:
        activity = ActivityHistory(student_id=student_id)
        db.session.add(activity)
        db.session.flush()

    before = student.total_hours if student else 0.0
    after = before + float(hours)
    logged_hour = LoggedHoursHistory(student_id, staff_id, service, float(hours), before, after, date_completed=date_completed)
    logged_hour.activity_id = activity.id
    db.session.add(logged_hour)
    db.session.commit()

    # Update student's total hours
    student.calculate_total_hours()

    return logged_hour


def search_logged_hours(query, search_type):
    if search_type == 'student':
        return search_logged_hours_by_student(query)
    elif search_type == 'staff':
        return search_logged_hours_by_staff(query)
    elif search_type == 'service':
        return search_logged_hours_by_service(query)
    elif search_type == 'date':
        return search_logged_hours_by_date(query)
    elif search_type == 'date_range':
        if isinstance(query, tuple) and len(query) == 2:
            start_date, end_date = query
            return search_logged_hours_by_date_range(start_date, end_date)
        else:
            raise ValueError("For date_range, query must be a tuple of (start_date, end_date).")
    else:
        raise ValueError("Invalid search type. Use 'student', 'staff', 'service', 'date', or 'date_range'.")


def delete_logged_hours(log_id):
    log = LoggedHoursHistory.query.get(log_id)
    if not log:
        raise ValueError(f"LoggedHoursHistory entry with id {log_id} not found.")
    db.session.delete(log)
    db.session.commit()
    return True


def delete_all_logged_hours():
    num_deleted = LoggedHoursHistory.query.delete()
    db.session.commit()
    return num_deleted


def update_logged_hours(log_id, student_id=None, staff_id=None, hours=None, status=None):
    log = LoggedHoursHistory.query.get(log_id)
    if not log:
        return None, f"LoggedHoursHistory entry with id {log_id} not found."

    if student_id is not None:
        student = Student.query.get(student_id)
        if not student:
            return None, f"Student with ID {student_id} not found."
        log.student_id = student_id

    if staff_id is not None:
        from App.models import Staff
        staff = Staff.query.get(staff_id)
        if not staff:
            return None, f"Staff with ID {staff_id} not found."
        log.staff_id = staff_id

    if hours is not None:
        try:
            log.hours = float(hours)
        except ValueError:
            return None, "Hours must be a valid number."

    if status is not None:
        log.status = status

    try:
        db.session.commit()
        # Update student's total hours if student_id or hours changed
        if student_id is not None or hours is not None:
            student = Student.query.get(log.student_id)
            if student:
                student.calculate_total_hours()
        return log, None
    except Exception as e:
        db.session.rollback()
        return None, f"Error updating logged hours: {str(e)}"


# HELPER FUNCTIONS

# Search logged hours history by student ID.
def search_logged_hours_by_student(student_id):
    return LoggedHoursHistory.query.filter_by(student_id=student_id).all()


# Search logged hours history by staff ID.
def search_logged_hours_by_staff(staff_id):
    return LoggedHoursHistory.query.filter_by(staff_id=staff_id).all()


# Search logged hours history by service.
def search_logged_hours_by_service(service):
    return LoggedHoursHistory.query.filter_by(service=service).all()


# Search logged hours history by date completed.
def search_logged_hours_by_date(date_completed):
    return LoggedHoursHistory.query.filter_by(date_completed=date_completed).all()


# Search logged hours history within a date range.
def search_logged_hours_by_date_range(start_date, end_date):
    return LoggedHoursHistory.query.filter(
        LoggedHoursHistory.date_completed >= start_date,
        LoggedHoursHistory.date_completed <= end_date
    ).all()

class TestLoggedHoursHistoryController(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, app, db):
        # Setup before each test
        with app.app_context():
            db.create_all()
            yield
            # Teardown after each test
            db.session.remove()
            db.drop_all()
    
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
        # Create a logged hours entry to delete
        logged_hour = create_logged_hours(student_id=1, staff_id=1, hours=5, service="Tutoring", date_completed="2024-01-01")
        log_id = logged_hour.id

        # Delete the logged hours entry
        result = delete_logged_hours(log_id)
        self.assertTrue(result)

        # Verify deletion
        deleted_log = LoggedHoursHistory.query.get(log_id)
        self.assertIsNone(deleted_log)
        
    def test_delete_all_logged_hours(self):
        # Create multiple logged hours entries
        create_logged_hours(student_id=1, staff_id=1, hours=5, service="Tutoring", date_completed="2024-01-01")
        create_logged_hours(student_id=2, staff_id=1, hours=3, service="Counseling", date_completed="2024-01-02")

        # Delete all logged hours entries
        num_deleted = delete_all_logged_hours()
        self.assertEqual(num_deleted, 2)

        # Verify deletion
        remaining_logs = LoggedHoursHistory.query.all()
        self.assertEqual(len(remaining_logs), 0)