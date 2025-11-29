from App.database import db
from App.models import User, Staff, Student, RequestHistory, Accolade, AccoladeHistory, ActivityHistory

# Re-export some request-related helpers for tests/legacy imports
from App.controllers.request_controller import fetch_all_requests, process_request_approval, process_request_denial


# CLI COMMAND FUNCTIONS (in order of CLI usage)

def register_staff(name, email, password):  # registers a new staff member
    new_staff = Staff.create_staff(name, email, password)
    return new_staff


def staff_query_router(string):  # The user will enter a string to route to the appropriate lookup
    if "@" in string and "." in string:
        return get_staff_by_email(string)
    elif string.isdigit():
        return get_staff_by_id(int(string))
    else:
        return get_staff_by_name(string)


def update_staff_info(staff_id, name=None, email=None, password=None):
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff with id {staff_id} not found.")
    if name:
        staff.username = name
    if email:
        staff.email = email
    if password:
        staff.set_password(password)
    db.session.commit()
    return staff


def delete_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        raise ValueError(f"Staff member with id {staff_id} not found.")
    db.session.delete(staff)
    db.session.commit()
    return True


# HELPER FUNCTIONS

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


def get_all_staff_json():  # returns all staff members in JSON format
    staff_members = Staff.query.all()
    return [staff.get_json() for staff in staff_members]


def update_staff(staff_id, username=None, email=None, password=None):
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


def delete_all_staff():
    num_deleted = Staff.query.delete()
    db.session.commit()
    return num_deleted
