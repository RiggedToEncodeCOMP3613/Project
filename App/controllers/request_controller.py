from App.database import db
from App.models import RequestHistory, ActivityHistory, Student, Staff


# CLI COMMAND FUNCTIONS (in order of CLI usage)

def create_request(student_id, service, staff_id, hours, date_completed):
    student = Student.query.get(student_id)
    if not student:
        return None, f"Student with ID {student_id} not found."

    staff = Staff.query.get(staff_id)
    if not staff:
        return None, f"Staff with ID {staff_id} not found."

    try:
        request = student.make_request(
            service=service,
            staff_id=staff_id,
            hours=float(hours),
            date_completed=date_completed,
        )
        return request, "Request created successfully."
    except ValueError as e:
        return None, f"Date error: {str(e)}"
    except Exception as e:
        return None, f"Error creating request: {str(e)}"


def search_requests(student_id=None, service=None, date=None, staff_id=None, status=None):
    from datetime import datetime, timedelta

    try:
        query = RequestHistory.query

        if student_id is not None:
            student = Student.query.get(student_id)
            if not student:
                return None, f"Student with ID {student_id} not found."
            query = query.filter_by(student_id=student_id)

        # Filter by staff_id
        if staff_id is not None:
            staff = Staff.query.get(staff_id)
            if not staff:
                return None, f"Staff with ID {staff_id} not found."
            query = query.filter_by(staff_id=staff_id)

        # Filter by status (case-insensitive)
        if status is not None:
            valid_statuses = ["pending", "approved", "denied"]
            status_lower = status.lower()
            if status_lower not in valid_statuses:
                return None, f"Invalid status '{status}'. Must be one of: Pending, Approved, Denied."
            query = query.filter(RequestHistory.status.ilike(status_lower))

        # Filter by service (partial match, case-insensitive)
        if service is not None:
            query = query.filter(RequestHistory.service.ilike(f'%{service}%'))

        # Filter by date_completed (full day match)
        if date is not None:
            try:
                search_date = datetime.strptime(date, "%Y-%m-%d").date()
                query = query.filter(
                    RequestHistory.date_completed >= search_date,
                    RequestHistory.date_completed < (search_date + timedelta(days=1)),
                )
            except ValueError:
                return None, "Invalid date format. Use YYYY-MM-DD"

        requests = query.all()

        if not requests:
            return [], None

        return requests, None

    except Exception as e:
        return None, f"Error searching requests: {str(e)}"


def update_request_entry(request_id, student_id=None, service=None, hours=None, status=None, staff_id=None):
    request = RequestHistory.query.get(request_id)

    if not request:
        return None, f"Request with ID {request_id} not found."

    if student_id is not None:
        student = Student.query.get(student_id)
        if not student:
            return None, f"Student with ID {student_id} not found. Cannot update request."
        request.student_id = student_id

    if staff_id is not None:
        from App.models import Staff
        staff = Staff.query.get(staff_id)
        if not staff:
            return None, f"Staff with ID {staff_id} not found. Cannot update request."
        request.staff_id = staff_id

    if service is not None:
        request.service = service

    if hours is not None:
        try:
            request.hours = float(hours)
        except ValueError:
            return None, "Hours must be a valid number."

    if status is not None:
        valid_statuses = ["Pending", "Approved", "Denied", "pending", "approved", "denied"]
        if status not in valid_statuses:
            return None, f"Invalid status '{status}'. Must be one of: Pending, Approved, Denied."
        request.status = status.lower()

    try:
        db.session.add(request)
        db.session.commit()
        return request, "Request updated successfully."
    except Exception as e:
        db.session.rollback()
        return None, f"Error updating request: {str(e)}"


def process_request_approval(staff_id, request_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")

    request = RequestHistory.query.get(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")

    student = Student.query.get(request.student_id)
    name = student.username if student else "Unknown"
    logged = staff.approve_request(request)

    return {
        'request': request,
        'student_name': name,
        'staff_name': staff.username,
        'logged_hours': logged,
    }


def process_request_denial(staff_id, request_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")

    request = RequestHistory.query.get(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")

    student = Student.query.get(request.student_id)
    name = student.username if student else "Unknown"
    success = staff.deny_request(request)

    return {
        'request': request,
        'student_name': name,
        'staff_name': staff.username,
        'denial_successful': success,
    }


def delete_request_entry(request_id):  # Deletes a specific service request and its associated activity history.

    request = RequestHistory.query.get(request_id)

    if not request:
        return False, f"Request with ID {request_id} not found."

    activity_id = request.activity_id

    try:
        db.session.delete(request)

        if activity_id:
            activity = ActivityHistory.query.get(activity_id)
            if activity:
                db.session.delete(activity)

        db.session.commit()
        return True, f"Request {request_id} and associated activity deleted successfully."

    except Exception as e:
        db.session.rollback()
        return False, f"Error deleting request: {str(e)}"


def drop_request_table():  # Deletes all entries in the RequestHistory table.

    try:
        request_count = RequestHistory.query.count()
        RequestHistory.query.delete()

        db.session.commit()

        return {
            'requests_deleted': request_count
        }, None

    except Exception as e:
        db.session.rollback()
        return None, f"Error dropping request table: {str(e)}"


# EXPORTED HELPER FUNCTIONS

# Fetches all pending requests for staff to review
def fetch_all_requests():
    pending_requests = RequestHistory.query.filter(RequestHistory.status.ilike('pending')).all()
    if not pending_requests:
        return []

    requests_data = []
    for req in pending_requests:
        student = Student.query.get(req.student_id)
        student_name = student.username if student else "Unknown"

        requests_data.append({
            'id': req.id,
            'student_name': student_name,
            'hours': req.hours,
            'status': req.status.lower() if isinstance(req.status, str) else req.status,
        })

    return requests_data
