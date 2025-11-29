from App.database import db


# Initialize the database and seed sample data.
# Args: drop_first (bool): if True, drop all tables before creating them.
# Returns a dict with lists of created record IDs.
def initialize_db(drop_first=True):
    # Import models here to avoid circular imports
    from App.models import Student, Staff, RequestHistory, LoggedHoursHistory, ActivityHistory
    from datetime import datetime, timezone
    
    if drop_first:
        db.drop_all()
    db.create_all()

    # Sample students (username, email, password)
    students_data = [
        ("alice", "alice.smith@gmail.com", "password1"),
        ("bob", "bob.jones@hotmail.com", "password2"),
        ("charlie", "charlie.brown@gmail.com", "password3"),
        ("diana", "diana.lee@hotmail.com", "password4"),
        ("eve", "eve.patel@gmail.com", "password5"),
    ]

    # Sample staff (username, email, password)
    staff_data = [
        ("msmith", "mr.smith@gmail.com", "staffpass1"),
        ("mjohnson", "ms.johnson@hotmail.com", "staffpass2"),
        ("mlee", "mr.lee@gmail.com", "staffpass3"),
    ]

    students = []
    for username, email, pwd in students_data:
        s = Student(username=username, email=email, password=pwd)
        students.append(s)
        db.session.add(s)

    staff_members = []
    for username, email, pwd in staff_data:
        st = Staff(username=username, email=email, password=pwd)
        staff_members.append(st)
        db.session.add(st)

    db.session.commit()

    # Create 4 requests for first 4 students
    import random
    requests = []
    request_date = datetime.now(timezone.utc)
    
    for i in range(4):
        student = students[i]
        staff_member = staff_members[i % len(staff_members)]
        hours = random.choice([5, 10, 12.5, 8])
        
        # Create activity history record
        activity = ActivityHistory(student_id=student.user_id)
        db.session.add(activity)
        db.session.flush()  # Get the activity ID
        
        # Create request linked to activity
        req = RequestHistory(
            student_id=student.user_id,
            staff_id=staff_member.user_id,
            service="volunteer",
            hours=hours,
            date_completed=request_date
        )
        req.activity_id = activity.id
        requests.append(req)
        db.session.add(req)

    db.session.commit()

    # Approve first two requests and create logged hours entries
    for i, req in enumerate(requests[:2]):
        req.status = 'approved'
        staff_member = staff_members[i % len(staff_members)]
        
        # Create activity history for logged hours
        activity = ActivityHistory(student_id=req.student_id)
        db.session.add(activity)
        db.session.flush()
        
        log = LoggedHoursHistory(
            student_id=req.student_id,
            staff_id=staff_member.user_id,
            service="volunteer",
            hours=req.hours,
            before=0.0,
            after=req.hours,
            date_completed=request_date
        )
        log.activity_id = activity.id
        db.session.add(log)

    # Deny the third request (if present)
    if len(requests) >= 3:
        requests[2].status = 'denied'

    # Leave the fourth request pending

    db.session.commit()

    # Add 3 extra logged hours entries
    for idx, (student_id, staff_id, hours_val, status) in enumerate([
        (students[0].user_id, staff_members[0].user_id, 3.5, 'approved'),
        (students[1].user_id, staff_members[1].user_id, 7.0, 'approved'),
        (students[2].user_id, staff_members[2].user_id, 4.0, 'approved'),
    ]):
        activity = ActivityHistory(student_id=student_id)
        db.session.add(activity)
        db.session.flush()
        
        log = LoggedHoursHistory(
            student_id=student_id,
            staff_id=staff_id,
            service="volunteer",
            hours=hours_val,
            before=0.0,
            after=hours_val,
            date_completed=request_date
        )
        log.activity_id = activity.id
        db.session.add(log)

    db.session.commit()

    # Return ids for reference
    result = {
        'students': [s.user_id for s in students],
        'staff': [st.user_id for st in staff_members],
        'requests': [r.id for r in RequestHistory.query.order_by(RequestHistory.id).all()],
        'logged_hours': [l.id for l in LoggedHoursHistory.query.order_by(LoggedHoursHistory.id).all()]
    }

    return result


# Compatibility wrapper used by CLI (keeps previous name `initialize`).
def initialize(drop_first=True):
    return initialize_db(drop_first=drop_first)

#from App.models import User,Student, Staff, Request
#from App.database import db


# def initialize():


#     db.drop_all()
#     db.create_all()
#     #create_user('bob', 'bobpass')

#     # Add sample students

#     students = [
#         Student(name='Alice', email='alice.smith@gmail.com'),
#         Student(name='Bob', email='bob.jones@hotmail.com'),
#         Student(name='Charlie', email='charlie.brown@gmail.com'),
#         Student(name='Diana', email='diana.lee@hotmail.com'),
#         Student(name='Eve', email='eve.patel@gmail.com'),
#         Student(name='Frank', email='frank.miller@gmail.com'),
#         Student(name='Grace', email='grace.wilson@hotmail.com'),
#     ]
#     db.session.add_all(students)
#     db.session.commit()

#     # Add sample staff members
#     staff_members = [
#         Staff(name='Mr. Smith', email='mr.smith@gmail.com'),
#         Staff(name='Ms. Johnson', email='ms.johnson@hotmail.com'),
#         Staff(name='Mr. Lee', email='mr.lee@gmail.com'),
        
#     ]
#     for staff_member in staff_members:
#         db.session.add(staff_member)
#     db.session.commit()

#     # Add sample requests for students
#     all_students = Student.query.order_by(Student.id).all()
#     requests = []
#     import random
#     for i, student in enumerate(all_students):
#         hours = random.randint(10, 60)
#         req = Request(student_id=student.id, hours=hours, status='pending')
#         requests.append(req)
#     db.session.add_all(requests)
#     db.session.commit()

#     # Add sample logged hours (approve first 2 requests by first 3 staff)
#     from App.models import LoggedHours
#     all_staff = Staff.query.order_by(Staff.id).all()
#     for i, req in enumerate(requests[:3]):
#         staff_member = all_staff[i % len(all_staff)]
#         if i < 2:
#             req.status = 'approved'
#             log = LoggedHours(student_id=req.student_id, staff_id=staff_member.id, hours=req.hours, status='approved')
#             db.session.add(log)
#         else:
#             req.status = 'denied'
#     db.session.commit()

    
    