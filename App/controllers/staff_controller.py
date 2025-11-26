from App.database import db
from App.models import User, Staff, Student, RequestHistory, Accolade


def register_staff(name,email,password): #registers a new staff member
    new_staff = Staff.create_staff(name, email, password)
    return new_staff

def update_staff(staff_id, username=None, email=None, password=None):
    """
    Updates a staff member's attributes by their ID.
    Finds the staff member, updates the provided fields,
    and commits the changes to the database.
    """
    staff = Staff.query.get(staff_id)
    
    if not staff:
        return None
    
    # Update attributes only if they are provided
    if username:
        staff.username = username
    
    if email:
        if "@" not in email:
            raise ValueError("Invalid email address.")
        staff.email = email
    
    if password:
        staff.set_password(password)
    
    db.session.add(staff)
    db.session.commit()
    
    return staff


def create_accolade(staff_id, description): #creates a new accolade
    
    staff = Staff.query.get(staff_id)
    if not staff:
        return None, f"Staff with ID {staff_id} not found"
    
    existing_accolade = Accolade.query.filter_by(description=description).first()
    if existing_accolade:
        return None, f"Accolade with description '{description}' already exists (ID: {existing_accolade.id})"
    
    try:
        accolade = Accolade(staff_id=staff_id, description=description)
        db.session.add(accolade)
        db.session.commit()
        
        return accolade, None
        
    except Exception as e:
        db.session.rollback()
        return None, f"Error creating accolade: {str(e)}"
    

def update_accolade(accolade_id, staff_id=None, description=None): #Updates an accolade's attributes

    accolade = Accolade.query.get(accolade_id)
    if not accolade:
        return None, f"Accolade with ID {accolade_id} not found"
    
    if staff_id is None and description is None:
        return None, "No fields to update. Provide at least one of: staff_id, description"
    
    try:
        updated_fields = []
        
        if staff_id is not None:
            staff = Staff.query.get(staff_id)
            if not staff:
                return None, f"Staff with ID {staff_id} not found"
            accolade.staff_id = staff_id
            updated_fields.append(f"staff_id: {staff_id}")
        
        if description is not None:
            existing = Accolade.query.filter(
                Accolade.description == description,
                Accolade.id != accolade_id
            ).first()
            if existing:
                return None, f"Another accolade already has description '{description}' (ID: {existing.id})"
            accolade.description = description
            updated_fields.append(f"description: '{description}'")
        
        db.session.commit()
        
        return {
            'accolade': accolade,
            'updated_fields': updated_fields
        }, None
        
    except Exception as e:
        db.session.rollback()
        return None, f"Error updating accolade: {str(e)}"


def delete_accolade(accolade_id, delete_history=False):
    """
    Deletes an accolade by ID.
    delete_history: If True, also deletes associated AccoladeHistory records
    
    """
    
    accolade = Accolade.query.get(accolade_id)
    if not accolade:
        return False, f"Accolade with ID {accolade_id} not found"
    
    try:
        description = accolade.description
        history_count = 0
        activity_count = 0
        
        if delete_history:
            from App.models import AccoladeHistory, ActivityHistory
            history_records = AccoladeHistory.query.filter_by(accolade_id=accolade_id).all()
            history_count = len(history_records)
            
            # Track activity IDs that might need cleanup
            activity_ids = set()
            
            for record in history_records:
                activity_ids.add(record.activity_id)
                db.session.delete(record)
            
            # Check if any ActivityHistory records are now empty and delete them
            for activity_id in activity_ids:
                activity = ActivityHistory.query.get(activity_id)
                if activity:
                    # Check if this activity has any remaining history
                    has_history = (
                        len(activity.requests) > 0 or
                        len(activity.loggedhours) > 0 or
                        len(activity.accolades) > 0 or
                        len(activity.milestones) > 0
                    )
                    if not has_history:
                        db.session.delete(activity)
                        activity_count += 1
        
        db.session.delete(accolade)
        db.session.commit()
        
        return True, {
            'description': description,
            'history_deleted': history_count,
            'empty_activities_deleted': activity_count
        }
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error deleting accolade: {str(e)}"


def fetch_all_requests(): #fetches all pending requests for staff to review
    pending_requests = RequestHistory.query.filter_by(status='pending').all()
    if not pending_requests:
        return []
    
    requests_data=[]
    for req in pending_requests:
        student = Student.query.get(req.student_id)
        student_name = student.username if student else "Unknown"
        
        requests_data.append({
            'id': req.id,
            'student_name': student_name,
            'hours': req.hours,
            'status':req.status
        })
    
    return requests_data

def process_request_approval(staff_id, request_id): #staff approves a student's hours request
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")
    
    request = RequestHistory.query.get(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")
    
    student = Student.query.get(request.student_id)
    name = student.username if student else "Unknown" # should always find student if data integrity is maintained
    logged = staff.approve_request(request)

    return {
        'request': request,
        'student_name': name,
        'staff_name': staff.username,
        'logged_hours': logged
    }

def process_request_denial(staff_id, request_id): #staff denies a student's hours request
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")
    
    request = RequestHistory.query.get(request_id)
    if not request:
        raise ValueError(f"Request with id {request_id} not found.")
    
    student = Student.query.get(request.student_id)
    name = student.username if student else "Unknown"
    denied = staff.deny_request(request)
    
    return {
        'request': request,
        'student_name': name,
        'staff_name': staff.username,
        'denial_successful': denied
    }
    
def get_all_staff_json(): #returns all staff members in JSON format
    staff_members = Staff.query.all()
    return [staff.get_json() for staff in staff_members]

