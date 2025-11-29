from App.models import LoggedHoursHistory
from App.database import db

def search_logged_hours_by_student(student_id):
    """Search logged hours history by student ID."""
    return LoggedHoursHistory.query.filter_by(student_id=student_id).all()

def search_logged_hours_by_staff(staff_id):
    """Search logged hours history by staff ID."""
    return LoggedHoursHistory.query.filter_by(staff_id=staff_id).all()

def search_logged_hours_by_service(service):
    """Search logged hours history by service."""
    return LoggedHoursHistory.query.filter_by(service=service).all()

def search_logged_hours_by_date(date_completed):
    """Search logged hours history by date completed."""
    return LoggedHoursHistory.query.filter_by(date_completed=date_completed).all()

def search_logged_hours_by_date_range(start_date, end_date):
    """Search logged hours history within a date range."""
    return LoggedHoursHistory.query.filter(
        LoggedHoursHistory.date_completed >= start_date,
        LoggedHoursHistory.date_completed <= end_date
    ).all()
    
def search_logged_hours (query, search_type):
    """General search function for logged hours history."""
    if search_type == 'student':
        return search_logged_hours_by_student(query)
    elif search_type == 'staff':
        return search_logged_hours_by_staff(query)
    elif search_type == 'service':
        return search_logged_hours_by_service(query)
    elif search_type == 'date':
        return search_logged_hours_by_date(query)
    elif search_type == 'date_range':
        start_date, end_date = query
        return search_logged_hours_by_date_range(start_date, end_date) # ! This is not fully correct, needs tuple unpacking
    else:
        raise ValueError("Invalid search type. Use 'student', 'staff', 'service', or 'date_range'.")    
