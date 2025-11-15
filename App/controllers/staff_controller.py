from App.database import db
from App.models import User,Staff,Student,Request

def register_staff(name,email,password): #registers a new staff member
    new_staff = Staff.create_staff(name, email, password)
    return new_staff

def fetch_all_requests(): #fetches all pending requests for staff to review
    pending_requests = Request.query.filter_by(status='pending').all()
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
    
    request = Request.query.get(request_id)
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
    
    request = Request.query.get(request_id)
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

def staff_query_router(string): # The user will enter a string, and this function will determine if it's an email, an ID, or a name and call the appropriate function
    if "@" in string and "." in string:
        return get_staff_by_email(string)
    elif string.isdigit():
        return get_staff_by_id(int(string))
    else:
        return get_staff_by_name(string)

def get_staff_by_id(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")
    return staff

def get_staff_by_email(email):
    staff = Staff.query.filter_by(email=email).first()
    if not staff:
        raise ValueError(f"Staff with email {email} not found.")
    return staff

def get_staff_by_name(name):
    staff = Staff.query.filter_by(username=name).first()
    if not staff:
        raise ValueError(f"Staff with name {name} not found.")
    return staff

def delete_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff member with id {staff_id} not found.")
    db.session.delete(staff)
    db.session.commit()
    return True

