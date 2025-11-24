import models.loggedHoursHistory
from App.database import db

def search_logged_hours_by_student(student_id):
    """Search logged hours history by student ID."""
    return models.loggedHoursHistory.LoggedHoursHistory.query.filter_by(student_id=student_id).all()

def search_logged_hours_by_staff(staff_id):
    """Search logged hours history by staff ID."""
    return models.loggedHoursHistory.LoggedHoursHistory.query.filter_by(staff_id=staff_id).all()

def search_logged_hours_by_service(service):
    """Search logged hours history by service."""
    return models.loggedHoursHistory.LoggedHoursHistory.query.filter_by(service=service).all()

def search_logged_hours_by_date_range(start_date, end_date):
    """Search logged hours history within a date range."""
    return models.loggedHoursHistory.LoggedHoursHistory.query.filter(
        models.loggedHoursHistory.LoggedHoursHistory.date_completed >= start_date,
        models.loggedHoursHistory.LoggedHoursHistory.date_completed <= end_date
    ).all()
    
def search_logged_hours (query, search_type):
    """General search function for logged hours history."""
    if search_type == 'student':
        return search_logged_hours_by_student(query)
    elif search_type == 'staff':
        return search_logged_hours_by_staff(query)
    elif search_type == 'service':
        return search_logged_hours_by_service(query)
    elif search_type == 'date_range':
        start_date, end_date = query
        return search_logged_hours_by_date_range(start_date, end_date) # ! This is not fully correct, needs tuple unpacking
    else:
        raise ValueError("Invalid search type. Use 'student', 'staff', 'service', or 'date_range'.")    
