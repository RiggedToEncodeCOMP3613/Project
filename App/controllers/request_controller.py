from App.database import db
from App.models import RequestHistory, ActivityHistory


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