from App.database import db
from App.models import Student, ActivityHistory


def list_all_acivity_history(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activity_history = student.activity_history
    if not activity_history:
        return []

    return activity_history.sorted_history()

def list_all_student_requests_history(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activity_history = student.activity_history
    if not activity_history:
        return []

    return [request.get_json() for request in activity_history.requests]

def list_all_student_logged_hours_history(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activity_history = student.activity_history
    if not activity_history:
        return []

    return [logged_hour.get_json() for logged_hour in activity_history.loggedhours]

def list_all_student_accolades_history(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activity_history = student.activity_history
    if not activity_history:
        return []

    return [accolade.get_json() for accolade in activity_history.accolades]

def list_all_student_milestones_history(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activity_history = student.activity_history
    if not activity_history:
        return []

    return [milestone.get_json() for milestone in activity_history.milestones]

def search_history_by_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activity_history = student.activity_history
    if not activity_history:
        return []

    return activity_history.sorted_history()

def search_history_by_activity(activity_id):
    '''Returns a sorted history list (with combined history objects) for a specific ActivityHistory ID'''
    activity = ActivityHistory.query.get(activity_id)
    if not activity:
        raise ValueError(f"ActivityHistory with id {activity_id} not found.")

    return activity.sorted_history()

def search_history_by_request(student_id, request_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activity_history = student.activity_history
    if not activity_history:
        return None

    request = next((req for req in activity_history.requests if req.id == request_id), None)
    return request.get_json() if request else None

def search_history_by_logged_hours(student_id, logged_hours_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activity_history = student.activity_history
    if not activity_history:
        return None

    logged_hour = next((lh for lh in activity_history.loggedhours if lh.id == logged_hours_id), None)
    return logged_hour.get_json() if logged_hour else None

def search_history_by_accolade(student_id, accolade_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activity_history = student.activity_history
    if not activity_history:
        return None

    accolade = next((ac for ac in activity_history.accolades if ac.id == accolade_id), None)
    return accolade.get_json() if accolade else None

def search_history_by_milestone(student_id, milestone_id):  
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    activity_history = student.activity_history
    if not activity_history:
        return None

    milestone = next((ms for ms in activity_history.milestones if ms.id == milestone_id), None)
    return milestone.get_json() if milestone else None






