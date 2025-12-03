from App.database import db


# Initialize the database and seed sample data.
# Args: drop_first (bool): if True, drop all tables before creating them.
# Returns a dict with lists of created record IDs.
def initialize(drop_first=True):
    # Import models here to avoid circular imports
    from App.models import Student, Staff, RequestHistory, LoggedHoursHistory, ActivityHistory, Accolade, AccoladeHistory, Milestone, MilestoneHistory
    from datetime import datetime, timezone
    import random

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

    # Generate 10 random students
    students_data = []
    used_names = set()
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

    # Generate 10 random staff
    staff_data = []
    used_names = set()
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
        s = Student(username=username, email=email, password=pwd)
        students.append(s)
        db.session.add(s)

    staff_members = []
    for username, email, pwd in staff_data:
        st = Staff(username=username, email=email, password=pwd)
        staff_members.append(st)
        db.session.add(st)

    db.session.commit()

    # Create 10 requests for random students and staff
    requests = []
    request_date = datetime.now(timezone.utc)

    for i in range(50):
        student = random.choice(students)
        staff_member = random.choice(staff_members)
        hours = round(random.uniform(1, 12))

        # Create activity history record
        activity = ActivityHistory(student_id=student.user_id)
        db.session.add(activity)
        db.session.flush()  # Get the activity ID

        # Create request linked to activity
        req = RequestHistory(
            student_id=student.user_id,
            staff_id=staff_member.user_id,
            service=random.choice(services),
            hours=hours,
            date_completed=request_date
        )
        req.activity_id = activity.id
        requests.append(req)
        db.session.add(req)

    db.session.commit()

    # Approve 5 requests, deny 3, leave 2 pending
    for i, req in enumerate(requests[:30]):
        req.status = 'approved'
        staff_member = Staff.query.get(req.staff_id)

        # Create activity history for logged hours
        activity = ActivityHistory(student_id=req.student_id)
        db.session.add(activity)
        db.session.flush()

        log = LoggedHoursHistory(
            student_id=req.student_id,
            staff_id=staff_member.user_id,
            service=req.service,
            hours=req.hours,
            before=0.0,
            after=req.hours,
            date_completed=request_date
        )
        log.activity_id = activity.id
        db.session.add(log)

    for req in requests[30:40]:
        req.status = 'denied'

    # Leave requests[40:50] as pending

    db.session.commit()

    # Update student hours after approved requests
    for student in students:
        student.calculate_total_hours()

    # Add 10 more logged hours entries for various students
    for i in range(10):
        student = random.choice(students)
        staff_member = random.choice(staff_members)
        hours = round(random.uniform(1, 12))

        activity = ActivityHistory(student_id=student.user_id)
        db.session.add(activity)
        db.session.flush()

        log = LoggedHoursHistory(
            student_id=student.user_id,
            staff_id=staff_member.user_id,
            service=random.choice(services),
            hours=hours,
            before=0.0,
            after=hours,
            date_completed=request_date
        )
        log.activity_id = activity.id
        db.session.add(log)

    db.session.commit()

    # Create 10 accolades
    accolades = []
    for i in range(10):
        staff_member = random.choice(staff_members)
        description = f"Accolade {i+1}: {random.choice(accolade_description)}"
        accolade = Accolade(staff_id=staff_member.user_id, description=description)
        accolades.append(accolade)
        db.session.add(accolade)

    db.session.commit()

    # Assign 10 accolades to random students
    for i in range(10):
        accolade = random.choice(accolades)
        student = random.choice(students)
        staff_member = random.choice(staff_members)

        # Check if already assigned
        existing = AccoladeHistory.query.filter_by(accolade_id=accolade.id, student_id=student.user_id).first()
        if not existing:
            # Create activity history
            activity = ActivityHistory(student_id=student.user_id)
            db.session.add(activity)
            db.session.flush()

            # Create history
            history = AccoladeHistory(
                accolade_id=accolade.id,
                student_id=student.user_id,
                staff_id=staff_member.user_id,
                description=accolade.description
            )
            history.activity_id = activity.id
            db.session.add(history)

            # Add to accolade students
            accolade.add_student(student.user_id)

    db.session.commit()

    # Create 10 milestones
    milestones = []
    milestone_hours = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for hours in milestone_hours:
        milestone = Milestone(hours=hours)
        milestones.append(milestone)
        db.session.add(milestone)

    db.session.commit()


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
    