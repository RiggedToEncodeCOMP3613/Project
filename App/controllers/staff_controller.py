from App.database import db
from App.models import User, Staff, Student, RequestHistory, Accolade

__all__ = ['register_staff', 'update_staff', 'fetch_all_requests', 'process_request_approval', 'process_request_denial', 'get_all_staff_json']

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

