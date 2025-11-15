from App.database import db
from App.models import User,Staff,Student,Request

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

def query_router(string): #The user will enter a string, and this function will determine if it's an email or an id or a name and call the appropriate function
    if "@" in string and "." in string:
        return get_student_by_email(string)
    elif string.isdigit():
        return get_student_by_id(int(string))
    else:
        return get_student_by_name(string)
