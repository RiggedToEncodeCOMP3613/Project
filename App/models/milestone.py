from App.database import db

# Association table for Student <-> Milestone many-to-many relationship
student_milestone = db.Table(
    'student_milestone',
    db.Column('student_id', db.Integer, db.ForeignKey('student.student_id'), primary_key=True),
    db.Column('milestone_id', db.Integer, db.ForeignKey('milestone.id'), primary_key=True)
)

class Milestone(db.Model):
    
    __tablename__ = 'milestone'
    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Integer, nullable=False, unique=True)
    #description = db.Column(db.String(255), nullable=True)
    
    # Many-to-many relationship with students
    students = db.relationship('Student', secondary=student_milestone, backref=db.backref('achieved_milestones', lazy=True), lazy=True)

    #def __init__(self, milestone, description=None):
    def __init__(self, hours):
        self.hours = hours
        #self.description = description

    def __repr__(self):
        #return f"<Milestone(id={self.id}, milestone={self.milestone}, description='{self.description}')>"
        return f"<Milestone(id={self.id}, hours={self.hours})>"
    
    def get_json(self):
        return {
            'id': self.id,
            'hours': self.hours
            #,'description': self.description
        }
    # Add a student to this milestone
    def add_student(self, student_id):
        from App.models import Student
        student = Student.query.get(student_id)
        if student and self not in student.achieved_milestones:
            student.achieved_milestones.append(self)
            db.session.commit()
        return student
