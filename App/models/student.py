from App.database import db
from .user import User
from App.models.milestone import Milestone
from App.models.accolade import Accolade

class Student(User):

    __tablename__ = "student"
    student_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    total_hours = db.Column(db.Float, default=0.0, nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    
    # Relationships
    activity_history = db.relationship('ActivityHistory', backref='student', lazy=True, cascade="all, delete-orphan")

    # Inheritance setup
    __mapper_args__ = {
        "polymorphic_identity": "student"
    }

    def __init__(self, username, email, password):
        super().__init__(username, email, password, role="student")
        self.total_hours = 0.0
        self.rank = 0

    def __repr__(self):
        return f"[Student ID= {str(self.student_id)}  Name= {self.username} Email= {self.email}]"
    
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
    
    def calculate_total_hours(self):
        # Need LoggedHoursHistory model
        return self.total_hours
    
    def calculate_rank(self):
        self.calculate_total_hours()
        all_students = Student.query.order_by(Student.total_hours.desc()).all()
        for idx, student in enumerate(all_students, start=1):
            if student.student_id == self.student_id:
                self.rank = idx
                db.session.commit()
                return self.rank
        return None
    
    def check_accolades(self):
        try:
            return Accolade.query.filter(Accolade.students.any(student_id=self.student_id)).all()
        except Exception:
            return [a for a in Accolade.query.all() if any(getattr(s, 'student_id', None) == self.student_id for s in a.students)]
    
    def check_for_milestones(self):
        try:
            return Milestone.query.filter(Milestone.students.any(student_id=self.student_id)).all()
        except Exception:
            return [m for m in Milestone.query.all() if any(getattr(s, 'student_id', None) == self.student_id for s in m.students)]
    
    def make_request(self, hours):
        # need RequestHistory model
        pass


