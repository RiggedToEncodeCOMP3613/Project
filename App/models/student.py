from App.database import db
from App.models.milestoneHistory import MilestoneHistory
from .user import User
from App.models.milestone import Milestone
from App.models.accolade import Accolade
from App.models.requestHistory import RequestHistory
from App.models.loggedHoursHistory import LoggedHoursHistory
from App.models.ActivityHistory import ActivityHistory
from sqlalchemy import func

class Student(User):

    __tablename__ = "student"
    student_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True, autoincrement=False)
    total_hours = db.Column(db.Float, default=0.0, nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    
    # Relationships
    activity_history = db.relationship('ActivityHistory', backref='student', lazy=True, cascade="all, delete-orphan", uselist=True)

    # Inheritance setup
    __mapper_args__ = {
        "polymorphic_identity": "student"
    }

    def __init__(self, username, email, password):
        prefix = 8160
        max_id = db.session.query(func.max(User.user_id)).filter(User.role == 'student', User.user_id.between(prefix*10**5, (prefix+1)*10**5-1)).scalar()
        if max_id:
            suffix = int(str(max_id)[4:]) + 1
        else:
            suffix = 10000
        self.student_id = int(f"{prefix}{suffix:05d}")
        self.user_id = self.student_id
        super().__init__(username, email, password, role="student")
        self.total_hours = 0.0
        self.rank = 0

    def __repr__(self):
        return f"[Student ID= {str(self.student_id)}  Name= {self.username} Email= {self.email} Rank= {self.rank} Total Hours= {self.total_hours}]"
    
    def get_json(self):
        return {
            'student_id': self.student_id,
            'username': self.username,
            'email': self.email,
            'total_hours': self.total_hours,
            'rank': self.rank
        }
    
    @staticmethod
    def create_student(username, email, password):
        newstudent = Student(username=username, email=email, password=password)
        db.session.add(newstudent)
        db.session.commit()
        return newstudent
    
    # Create a request for hours to be logged
    def make_request(self, service, staff_id, hours, date_completed):

        # Create activity history record
        activity = ActivityHistory(student_id=self.student_id)
        db.session.add(activity)
        db.session.flush()  # Flush to get the activity ID without committing
        
        # Create request linked to activity
        request = RequestHistory(
            student_id=self.student_id,
            staff_id=staff_id,
            service=service,
            hours=hours,
            date_completed=date_completed
        )
        request.activity_id = activity.id
        #request.status = 'pending' #redudant
        db.session.add(request)
        db.session.commit()
        return request
    
    # Calculate total hours earned by the student from all logged hours history and update total_hours attribute
    def calculate_total_hours(self):
        total = 0.0
        logged_hours = LoggedHoursHistory.query.filter_by(student_id=self.student_id).all()
        for log in logged_hours:
            total += log.hours
        self.total_hours = total
        db.session.commit()
        self.calculate_rank()
        self.calculate_new_milestones()
        return self.total_hours
    
    # Calculate the student's rank based on total hours compared to all other students
    def calculate_rank(self):
        all_students = Student.query.order_by(Student.total_hours.desc()).all()
        for idx, student in enumerate(all_students, start=1):
            if student.student_id == self.student_id:
                self.rank = idx
                db.session.commit()
                return self.rank
        return None
    
    # Check if student has unlocked new milestones based on total hours
    def calculate_new_milestones(self):
        all_milestones = Milestone.query.order_by(Milestone.hours).all()
        m = []
        for milestone in all_milestones:
            if self.total_hours >= milestone.hours:
                existing = MilestoneHistory.query.filter_by(
                    milestone_id=milestone.id,
                    student_id=self.student_id
                ).first()
                
                # If milestone hasn't been recorded yet, create a history entry
                if not existing:
                    # Create activity history record
                    activity = ActivityHistory(student_id=self.student_id)
                    db.session.add(activity)
                    db.session.flush()  # Flush to get the activity ID
                    
                    # Create milestone history entry
                    milestone_history = MilestoneHistory(
                        milestone_id=milestone.id,
                        student_id=self.student_id,
                        hours=milestone.hours
                    )
                    milestone_history.activity_id = activity.id
                    db.session.add(milestone_history)
                    db.session.commit()
                    m.append(milestone_history)
        return m
    
    # Return a list of accolades that this student has earned
    def check_accolades(self):
        try:
            return Accolade.query.filter(Accolade.students.any(Student.student_id == self.student_id)).all()
        except Exception:
            # Fallback: manually filter accolades
            return [a for a in Accolade.query.all() if self in a.students]
    
    # Return a list of milestones that this student has earned
    def check_for_milestones(self):
        try:
            return Milestone.query.filter(Milestone.students.any(Student.student_id == self.student_id)).all()
        except Exception:
            # Fallback: manually filter milestones
            return [m for m in Milestone.query.all() if self in m.students]
    


