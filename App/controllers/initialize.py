from App.database import db
from App.controllers.student_controller import register_student
from App.controllers.staff_controller import register_staff
from App.controllers.request_controller import create_request, process_request_approval, process_request_denial
from App.controllers.loggedHoursHistory_controller import create_logged_hours
from App.controllers.accolade_controller import create_accolade, assign_accolade_to_student
from App.controllers.milestone_controller import create_milestone


# Initialize the database and seed sample data.
# Args: drop_first (bool): if True, drop all tables before creating them.
# Returns a dict with lists of created record IDs.
def initialize(drop_first=True):
    # Import models here to avoid circular imports
    from App.models import Student, Staff, RequestHistory, LoggedHoursHistory, ActivityHistory, Accolade, AccoladeHistory, Milestone, MilestoneHistory
    from datetime import datetime, timezone
    import random
    
    if Student.query.filter_by(username='teststudent').first():
        return {}

    if drop_first:
        db.drop_all()
    db.create_all()

    # Random name generation
    first_names = ["Aliyah", "Bob", "Bobart", "Bobrick", "Bobson", "Deen", "Adam", "Michel", 
                   "Isabella", "Joe", "Kate", "Lily", "Ivy", "Rose", "Mia", "April", "May", 
                   "June", "Summer", "August", "Subaru", "Rem", "Emilia", "Rudeus", "Itachi", "Ryan", 
                   "Aaron", "Thanos", "Ching", "Shichellssichells", "Mandoes", "Joe"]
    last_names = ["Ali", "Maraj", "Maharaj", "Singh", "Maharajsingh", "King", "Queen", "Sanchez", 
                  "Mohammed", "Amoroso-Centeno", "White", "Black", "Smith", "Dickinson", "Harris", 
                  "Alwahree", "Wednesday", "Martini", "Gosling", "Chong", "Kent", "Rodriguez", 
                  "Walker", "Runner", "Sitter", "Uzimaki", "Natsuki", "Uchiha", "Bidehschischore", "Mendez", "Who"]
    services = ["Computer Lab", "Cleanup", "Classroom Setup", "Tax Fraud"]
    accolade_description = ["Outstanding Service", "Leadership", "Community Impact", "Excellence", "Dedication", 
                            "Teamwork", "Commitment", "Tax Fraud"]

    # Add test student
    students_data = [('teststudent', 'test@student.com', 'password')]

    # Generate 9 random students (since we added 1 test)
    used_names = {'teststudent'}
    for i in range(10):
        while True:
            first = random.choice(first_names)
            last = random.choice(last_names)
            username = first.lower()
            if username not in used_names:
                used_names.add(username)
                email = f"{first.lower()}.{last.lower()}@{random.choice(['gmail.com', 'outlook.com'])}"
                password = f"password{i+1}"
                students_data.append((username, email, password))
                break

    # Add test staff
    staff_data = [('teststaff', 'test@staff.com', 'password')]

    # Generate 9 random staff (since we added 1 test)
    used_names = {'teststaff'}
    for i in range(10):
        while True:
            first = random.choice(first_names)
            last = random.choice(last_names)
            prefix = random.choice(["Mr_", "Mrs_", "Dr_"])
            username = prefix + first.lower()
            if username not in used_names:
                used_names.add(username)
                email = f"{prefix}{first.lower()}.{last.lower()}@{random.choice(['gmail.com', 'outlook.com'])}"
                password = f"staffpass{i+1}"
                staff_data.append((username, email, password))
                break

    students = []
    for username, email, pwd in students_data:
        s = register_student(username, email, pwd)
        students.append(s)

    staff_members = []
    for username, email, pwd in staff_data:
        st = register_staff(username, email, pwd)
        staff_members.append(st)

    # Create 100 requests for random students and staff
    requests = []
    request_date = datetime.now(timezone.utc)

    for i in range(100):
        student = random.choice(students)
        staff_member = random.choice(staff_members)
        hours = round(random.uniform(1, 12))

        req, msg = create_request(student.user_id, random.choice(services), staff_member.user_id, hours, request_date)
        if req:
            requests.append(req)

    # Approve 60 requests, deny 20, leave 20 pending
    for req in requests[:60]:
        process_request_approval(req.staff_id, req.id)

    for req in requests[60:80]:
        process_request_denial(req.staff_id, req.id)

    # Update student hours after approved requests
    for student in students:
        student.calculate_total_hours()

    # Add 10 more logged hours entries for various students
    for i in range(10):
        student = random.choice(students)
        staff_member = random.choice(staff_members)
        hours = round(random.uniform(1, 12))

        create_logged_hours(student.user_id, staff_member.user_id, hours, random.choice(services), request_date)

    # Create accolades based on accolade_description list
    accolades = []
    for description in accolade_description:
        staff_member = random.choice(staff_members)
        accolade, err = create_accolade(staff_member.user_id, description)
        if accolade:
            accolades.append(accolade)

    # Assign accolades to 50 random students (controller handles duplicate prevention)
    for i in range(50):
        accolade = random.choice(accolades)
        student = random.choice(students)
        staff_member = random.choice(staff_members)

        assign_accolade_to_student(accolade.id, student.user_id, staff_member.user_id)

    # Create 10 milestones
    milestones = []
    milestone_hours = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for hours in milestone_hours:
        milestone = create_milestone(hours)
        milestones.append(milestone)


    # Update student hours and ranks
    for student in students:
        student.calculate_total_hours()

    # Return ids for reference
    result = {
        'students': [s.user_id for s in students],
        'staff': [st.user_id for st in staff_members],
        'requests': [r.id for r in RequestHistory.query.order_by(RequestHistory.id).all()],
        'logged_hours': [l.id for l in LoggedHoursHistory.query.order_by(LoggedHoursHistory.id).all()],
        'accolades': [a.id for a in Accolade.query.order_by(Accolade.id).all()],
        'accolade_histories': [ah.id for ah in AccoladeHistory.query.order_by(AccoladeHistory.id).all()],
        'milestones': [m.id for m in Milestone.query.order_by(Milestone.id).all()],
        'milestone_histories': [mh.id for mh in MilestoneHistory.query.order_by(MilestoneHistory.id).all()],
        'activity_histories': [ah.id for ah in ActivityHistory.query.order_by(ActivityHistory.id).all()]
    }

    return result
    