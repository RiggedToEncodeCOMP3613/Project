import datetime
from App.database import db
from App.models import User, Staff, Student, RequestHistory, LoggedHoursHistory
from App.models import User, Staff, Student, RequestHistory, Accolade

#Comamand to list all staff in the database
def printAllStaff():

    print("\n")
    staff = Staff.query.all()
    for member in staff:
        print(member)
    print("\n")
#Comamand to list all students in the database
def printAllStudents():

    print("\n")
    students = Student.query.all()
    for student in students:
        print(student)
    print("\n")

#Comamand to list all accolades in the database
def listAllAccolades():

    print("\n")
    accolades = Accolade.query.all()
    for accolade in accolades:
        print(accolade)
    print("\n")

#Comamand to list all requests in the database
def listAllRequests():

    print("\nAll Requests:")
    requests = RequestHistory.query.all()
    for request in requests:
        print(request)
    print("\n")


#Comamand to list all approved requests in the database
def listAllApprovedRequests():

    print("\nAll Approved Requests:")
    requests = RequestHistory.query.filter_by(status='approved').all()
    for request in requests:
        print(request)
    print("\n")

#Comamand to list all denied requests in the database
def listAllDeniedRequests():

    print("\nAll Denied Requests:")
    requests = RequestHistory.query.filter_by(status='denied').all()
    for request in requests:
        print(request)
    print("\n")

#Comamand to list all pending requests in the database
def listAllPendingRequests():
    print("\nAll Pending Requests:")
    requests = RequestHistory.query.filter_by(status='pending').all()
    for request in requests:
        print(request)
    print("\n")

#Comamand to list all logged hours in the database
def listAllloggedHours():
    print("\nAll Logged Hours:")
    from App.models import LoggedHoursHistory
    logged_hours = LoggedHoursHistory.query.all()
    for log in logged_hours:
        print(log)
    print("\n")

#Comamand to list all users in the database
def listAllUsers():
    print("\nAll Users:")
    users = User.query.all()
    for user in users:
        print(user)
    print("\n")

def create_logged_hours(student_id, staff_id, hours, timestamp, status='approved', service=None):
    logged_hour = LoggedHoursHistory(student_id, staff_id, hours, status, service, None, date_completed=timestamp) # ! This could be wrong, I am not sure about the parameters
    db.session.add(logged_hour)
    db.session.commit()
    return logged_hour

def delete_logged_hours(log_id):
    log = LoggedHoursHistory.query.get(log_id)
    if not log:
        raise ValueError(f"LoggedHoursHistory entry with id {log_id} not found.")
    db.session.delete(log)
    db.session.commit()
    return True

def delete_all_logged_hours():
    num_deleted = LoggedHoursHistory.query.delete()
    db.session.commit()
    return num_deleted