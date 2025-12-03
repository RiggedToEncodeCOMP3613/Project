from App.database import db
from .user import User
from App.models.requestHistory import RequestHistory
from App.models.accolade import Accolade
from App.models.accoladeHistory import AccoladeHistory
from App.models.loggedHoursHistory import LoggedHoursHistory
from datetime import datetime, timezone
from App.models.student import Student
from App.models.ActivityHistory import ActivityHistory
from sqlalchemy import func

class Staff(User):
    __tablename__ = "staff"
    staff_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True, autoincrement=False)

    # Class variable for next suffix
    _next_suffix = 10000

    # Relationships (match required names)
    loggedhours = db.relationship('LoggedHoursHistory', backref='staff', lazy=True, cascade="all, delete-orphan")
    accolades_created = db.relationship('Accolade', back_populates='staff', lazy=True, cascade="all, delete-orphan")
    accolades_awarded = db.relationship('AccoladeHistory', backref='awarded_by', lazy=True, cascade="all, delete-orphan")
    requests = db.relationship('RequestHistory', backref='staff', lazy=True, cascade="all, delete-orphan")

    # Inheritance setup
    __mapper_args__ = {
        "polymorphic_identity": "staff"
    }

    def __init__(self, username, email, password):
        prefix = 300
        # Get the next suffix by finding the max existing staff_id
        max_staff = db.session.query(func.max(Staff.staff_id)).scalar()
        if max_staff is None:
            suffix = 10000
        else:
            suffix = (max_staff % 100000) + 1  # Extract suffix and increment
        self.staff_id = int(f"{prefix}{suffix:05d}")
        self.user_id = self.staff_id
        super().__init__(username, email, password, role="staff")

    def __repr__(self):
        return f"[Staff ID= {str(self.staff_id)} Name= {self.username} Email= {self.email}]"
    
    def get_json(self):
        return {
            'staff_id': self.staff_id,
            'username': self.username,
            'email': self.email
        }
    
    @staticmethod
    def create_staff(username, email, password):
        newstaff = Staff(username=username, email=email, password=password)
        db.session.add(newstaff)
        db.session.commit()
        return newstaff
    
    # Create a LoggedHoursHistory entry for hours worked by a student
    def log_hours(self, service, student_id, hours, date_completed):
        # Create activity history record
        activity = ActivityHistory(student_id=student_id)
        db.session.add(activity)
        db.session.flush()  # Flush to get the activity ID without committing
        
        logged = LoggedHoursHistory(
            student_id=student_id,
            staff_id=self.staff_id,
            service=service,
            hours=hours,
            before=0,  
            after=hours,
            date_completed=date_completed
        )
        logged.activity_id = activity.id
        db.session.add(logged)
        db.session.commit()
        
        # Update student's total hours
        student = Student.query.get(student_id)
        if student:
            student.calculate_total_hours()
        
        return logged
    
    # Get all pending requests awaiting staff approval
    def get_pending_requests(self):
        pending = RequestHistory.query.filter_by(staff_id=self.staff_id, status='pending').all()
        return pending
    
    # Approve a pending request and create a LoggedHoursHistory entry
    def approve_request(self, request):
        if request.status != 'Pending':
            return None
        
        # Update request status
        request.status = 'Approved'
        request.date_responded = datetime.now(timezone.utc)
        db.session.commit()
        
        # Create a LoggedHoursHistory entry from the approved request
        logged = self.log_hours(
            service=request.service,
            student_id=request.student_id,
            hours=request.hours,
            date_completed=request.date_completed
        )
        
        return logged
    
    # Deny a pending request
    def deny_request(self, request):
        if request.status != 'Pending':
            return False
        request.status = 'Denied'
        request.date_responded = datetime.now(timezone.utc)
        db.session.commit()
        return True
    
    def create_accolade(self, description):
        accolade = Accolade(staff_id=self.staff_id, description=description)
        db.session.add(accolade)
        db.session.commit()
        return accolade
    
    # Award an accolade to a student, creating an AccoladeHistory entry
    def award_accolade(self, student_id, accolade_id):
        accolade = Accolade.query.get(accolade_id)
        if not accolade:
            raise ValueError("Invalid ID. Accolade not found")
            #return None
        
        # Create activity history record
        activity = ActivityHistory(student_id=student_id)
        db.session.add(activity)
        db.session.flush()  # Flush to get the activity ID without committing
        
        # Add student to accolade's students relationship
        student = Student.query.get(student_id)
        if student and student not in accolade.students:
            accolade.students.append(student)
        
        # Create AccoladeHistory entry
        accolade_history = AccoladeHistory(
            accolade_id=accolade_id,
            student_id=student_id,
            staff_id=self.staff_id,
            description=accolade.description
        )
        accolade_history.activity_id = activity.id
        db.session.add(accolade_history)
        db.session.commit()
        
        return accolade_history