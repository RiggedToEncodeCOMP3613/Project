from App.database import db
from App.models import User, Staff, Student, RequestHistory

def register_student(name,email,password):
    new_student=Student.create_student(name,email,password)
    return new_student

def delete_student(student_id): #deletes a student by id
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    db.session.delete(student)
    db.session.commit()
    return True

def get_approved_hours(student_id): #calculates and returns the total approved hours for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    total_hours = sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')
    return (student.username,total_hours)

def create_hours_request(student_id,hours): #creates a new hours request for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    req = student.request_hours_confirmation(hours)
    return req

def create_request(student_id, service, staff_id, hours, date_completed):
    """
    Creates a new service request for a student.
    """
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
            date_completed=date_completed
        )
        return request, "Request created successfully."
    except ValueError as e:
        return None, f"Date error: {str(e)}"
    except Exception as e:
        return None, f"Error creating request: {str(e)}"

def fetch_requests(student_id): #fetch requests for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    return student.requests

def fetch_accolades(student_id): #fetch accolades for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    accolades = student.accolades()
    return accolades

def generate_leaderboard():
    students = Student.query.all()
    leaderboard = []
    for student in students:
        total_hours=sum(lh.hours for lh in student.loggedhours if lh.status == 'approved')

        leaderboard.append({
            'name': student.username,
            'hours': total_hours
        })

    leaderboard.sort(key=lambda item: item['hours'], reverse=True)

    return leaderboard

def get_all_students_json():
    students = Student.query.all()
    return [student.get_json() for student in students]

def get_student_by_id(student_id):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    return student

def get_student_by_email(email):
    student = Student.query.filter_by(email=email).first()
    if not student:
        raise ValueError(f"Student with email {email} not found.")
    return student

def get_student_by_name(name):
    student = Student.query.filter_by(username=name).first()
    if not student:
        raise ValueError(f"Student with name {name} not found.")
    return student

def get_student_by_rank(rank):
    student = Student.query.filter_by(rank=rank).first()
    if not student:
        raise ValueError(f"Student with rank {rank} not found.")
    return student

def query_router(string):
    # email check
    if "@" in string and "." in string:
        return get_student_by_email(string)

    # ID check using new constraints
    if string.isdigit() and len(string) == 9 and string.startswith("8160"): # assuming student IDs follow this pattern with the future update to ID system (9 digits starting with 8160) this does NOT work at the time of writing
        return get_student_by_id(int(string))

    # rank check — but be careful, rank is NOT guaranteed to be unique
    if string.isdigit():
        return get_student_by_rank(int(string))

    # fallback: treat as name
    return get_student_by_name(string)

    
def update_student_info(student_id, name=None, email=None, password=None):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")
    
    if name:
        student.username = name
    if email:
        student.email = email
    if password:
        student.set_password(password)
    
    db.session.commit()
    return student
