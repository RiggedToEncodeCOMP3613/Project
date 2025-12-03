from App.database import db
from App.models import User, Staff, Student, RequestHistory


# CLI COMMAND FUNCTIONS (in order of CLI usage)

def register_student(username, email, password):
    new_student = Student.create_student(username, email, password)
    return new_student


def query_router(string):
    # email check
    if "@" in string and "." in string:
        return get_student_by_email(string)

    # ID check using new constraints
    if string.isdigit() and len(string) == 9 and string.startswith("8160"):
        return get_student_by_id(int(string))

    # rank check — but be careful, rank is NOT guaranteed to be unique
    if string.isdigit():
        return get_student_by_rank(int(string))

    # fallback: treat as name
    return get_student_by_name(string)


def update_student_info(student_id, username=None, email=None, password=None):
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    if username:
        student.username = username
    if email:
        student.email = email
    if password:
        student.set_password(password)

    db.session.commit()
    return student


def get_hours(student_id):  # returns the total hours for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    return (student.username, student.total_hours)


def delete_student(student_id):  # deletes a student by id
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    db.session.delete(student)
    db.session.commit()
    return True




# HELPER FUNCTIONS

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


def create_hours_request(student_id, hours):  # creates a new hours request for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    req = student.request_hours_confirmation(hours)
    return req


def fetch_requests(student_id):  # fetch requests for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    return student.requests


def fetch_accolades(student_id):  # fetch accolades for a student
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with id {student_id} not found.")

    accolades = student.accolades()
    return accolades


def get_all_students_json():
    students = Student.query.all()
    return [student.get_json() for student in students]


def delete_all_students():
    num_deleted = Student.query.delete()
    db.session.commit()
    return num_deleted
