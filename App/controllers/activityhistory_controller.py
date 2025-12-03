from App.database import db
from App.models import Student, ActivityHistory


def _get_student_activity_history(student_id):
    student = Student.query.get(student_id)
    if not student:
        return None, f"Student with id {student_id} not found."

    activity_histories = student.activity_history  # now a list
    return student, activity_histories


def list_all_activity_history(student_id):
    student, activity_histories = _get_student_activity_history(student_id)
    if not student:
        return None, activity_histories  # error

    all_history = []
    for ah in activity_histories:
        all_history.extend(ah.requests)
        all_history.extend(ah.loggedhours)
        all_history.extend(ah.accolades)
        all_history.extend(ah.milestones)

    # Sort by timestamp descending
    all_history.sort(key=lambda x: x.timestamp, reverse=True)
    return [item.get_json() for item in all_history], None

def list_all_student_requests_history(student_id):
    student, activity_histories = _get_student_activity_history(student_id)
    if not student:
        return None, activity_histories

    all_requests = []
    for ah in activity_histories:
        for request in ah.requests:
            data = request.get_json()
            data['activity_id'] = request.activity_id
            all_requests.append(data)
    all_requests.sort(key=lambda x: x['timestamp'], reverse=False)
    return all_requests, None

def list_all_student_logged_hours_history(student_id):
    student, activity_histories = _get_student_activity_history(student_id)
    if not student:
        return None, activity_histories

    all_logged = []
    for ah in activity_histories:
        for logged_hour in ah.loggedhours:
            data = logged_hour.get_json()
            data['activity_id'] = logged_hour.activity_id
            all_logged.append(data)
    all_logged.sort(key=lambda x: x['timestamp'], reverse=False)
    return all_logged, None

def list_all_student_accolades_history(student_id):
    student, activity_histories = _get_student_activity_history(student_id)
    if not student:
        return None, activity_histories

    all_accolades = []
    for ah in activity_histories:
        for accolade in ah.accolades:
            data = accolade.get_json()
            data['activity_id'] = accolade.activity_id
            all_accolades.append(data)
    all_accolades.sort(key=lambda x: x['timestamp'], reverse=False)
    return all_accolades, None

def list_all_student_milestones_history(student_id):
    student, activity_histories = _get_student_activity_history(student_id)
    if not student:
        return None, activity_histories

    all_milestones = []
    for ah in activity_histories:
        for milestone in ah.milestones:
            data = milestone.get_json()
            data['activity_id'] = milestone.activity_id
            all_milestones.append(data)
    all_milestones.sort(key=lambda x: x['timestamp'], reverse=False)
    return all_milestones, None

def search_history_by_student(student_id):
    return list_all_activity_history(student_id)

def search_history_by_activity(activity_id):
    activity = ActivityHistory.query.get(activity_id)
    if not activity:
        return None, f"ActivityHistory with id {activity_id} not found."

    all_history = activity.requests + activity.loggedhours + activity.accolades + activity.milestones
    all_history.sort(key=lambda x: x.timestamp, reverse=True)
    return [item.get_json() for item in all_history], None

def search_history_by_request(student_id, request_id):
    student, activity_histories = _get_student_activity_history(student_id)
    if not student:
        return None, activity_histories

    for ah in activity_histories:
        request = next((req for req in ah.requests if req.id == request_id), None)
        if request:
            return request.get_json(), None
    return None, None

def search_history_by_logged_hours(student_id, logged_hours_id):
    student, activity_histories = _get_student_activity_history(student_id)
    if not student:
        return None, activity_histories

    for ah in activity_histories:
        logged_hour = next((lh for lh in ah.loggedhours if lh.id == logged_hours_id), None)
        if logged_hour:
            return logged_hour.get_json(), None
    return None, None

def search_history_by_accolade(student_id, accolade_id):
    student, activity_histories = _get_student_activity_history(student_id)
    if not student:
        return None, activity_histories

    for ah in activity_histories:
        accolade = next((ac for ac in ah.accolades if ac.id == accolade_id), None)
        if accolade:
            return accolade.get_json(), None
    return None, None

def search_history_by_milestone(student_id, milestone_id):
    student, activity_histories = _get_student_activity_history(student_id)
    if not student:
        return None, activity_histories

    for ah in activity_histories:
        milestone = next((ms for ms in ah.milestones if ms.id == milestone_id), None)
        if milestone:
            return milestone.get_json(), None
    return None, None


# Global list functions (all students)
def list_all_requests():
    from App.models import RequestHistory
    requests = RequestHistory.query.all()
    result = []
    for req in requests:
        data = req.get_json()
        data['activity_id'] = req.activity_id
        result.append(data)
    return result, None

def list_all_logged_hours():
    from App.models import LoggedHoursHistory
    logs = LoggedHoursHistory.query.all()
    result = []
    for log in logs:
        data = log.get_json()
        data['activity_id'] = log.activity_id
        result.append(data)
    return result, None

def list_all_accolades():
    from App.models import AccoladeHistory
    accolades = AccoladeHistory.query.all()
    result = []
    for acc in accolades:
        data = acc.get_json()
        data['activity_id'] = acc.activity_id
        result.append(data)
    return result, None

def list_all_milestones():
    from App.models import MilestoneHistory
    milestones = MilestoneHistory.query.all()
    result = []
    for ms in milestones:
        data = ms.get_json()
        data['activity_id'] = ms.activity_id
        result.append(data)
    return result, None


# Global list all activity history (combined)
def list_all_activity_history_global():
    all_history = []

    # Get all requests
    requests, _ = list_all_requests()
    for req in requests:
        req['type'] = 'Request'
        req['summary'] = f"{req.get('service', 'N/A')} - {req.get('hours', 'N/A')}h - {req.get('status', 'N/A')}"
        all_history.append(req)

    # Get all logged hours
    logged, _ = list_all_logged_hours()
    for log in logged:
        log['type'] = 'Logged Hours'
        log['summary'] = f"{log.get('service', 'N/A')} - {log.get('hours', 'N/A')}h"
        all_history.append(log)

    # Get all accolades
    accolades, _ = list_all_accolades()
    for acc in accolades:
        acc['type'] = 'Accolade'
        acc['summary'] = acc.get('description', 'N/A')
        all_history.append(acc)

    # Get all milestones
    milestones, _ = list_all_milestones()
    for ms in milestones:
        ms['type'] = 'Milestone'
        ms['summary'] = f"Milestone {ms.get('milestone_id', 'N/A')} - {ms.get('hours', 'N/A')}h"
        all_history.append(ms)

    # Sort by timestamp if available, else by id (ascending)
    all_history.sort(key=lambda x: (x.get('timestamp') or x.get('date_completed') or x.get('id', 0)), reverse=False)

    return all_history, None



