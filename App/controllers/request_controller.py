from App.database import db
from App.models import RequestHistory, ActivityHistory, Student


def delete_request_entry(request_id): #Deletes a specific service request and its associated activity history.

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
    

def update_request_entry(request_id, student_id=None, service=None, hours=None, status=None):
    """
    Updates specific fields of a RequestHistory entry.
    Only updates fields that are provided.
    """
    request = RequestHistory.query.get(request_id)
    
    if not request:
        return None, f"Request with ID {request_id} not found."
    
    if student_id is not None:
        student = Student.query.get(student_id)
        if not student:
            return None, f"Student with ID {student_id} not found. Cannot update request."
        request.student_id = student_id

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


def search_requests(student_id=None, service=None, date=None):
    """
    Search requests by student_id, service description, or date_completed.
    
    """
    from datetime import datetime, timedelta
    
    try:
        query = RequestHistory.query
        
        if student_id is not None:
            student = Student.query.get(student_id)
            if not student:
                return None, f"Student with ID {student_id} not found."
            query = query.filter_by(student_id=student_id)
        
        # Filter by service (partial match, case-insensitive)
        if service is not None:
            query = query.filter(RequestHistory.service.ilike(f'%{service}%'))
        
        # Filter by date_completed (full day match)
        if date is not None:
            try:
                search_date = datetime.strptime(date, "%Y-%m-%d").date()
                query = query.filter(
                    RequestHistory.date_completed >= search_date,
                    RequestHistory.date_completed < (search_date + timedelta(days=1))
                )
            except ValueError:
                return None, "Invalid date format. Use YYYY-MM-DD"
        
        requests = query.all()
        
        if not requests:
            return [], None
        
        return requests, None
        
    except Exception as e:
        return None, f"Error searching requests: {str(e)}"