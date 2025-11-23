from App.database import db
from datetime import datetime

class ActivityHistory(db.Model): 
    __tablename__ = 'activity_history'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    
    requests = db.relationship('RequestHistory', backref='activity', lazy=True, cascade="all, delete-orphan")
    loggedhours = db.relationship('LoggedHoursHistory', backref='activity', lazy=True, cascade="all, delete-orphan")
    accolades = db.relationship('AccoladeHistory', backref='activity', lazy=True, cascade="all, delete-orphan")
    milestones = db.relationship('MilestoneHistory', backref='activity', lazy=True, cascade="all, delete-orphan")


    def __init__(self, student_id):
        self.student_id = student_id
        
    def __repr__(self):
        return (
            f'<ActivityHistory ID: {self.id} | '
            f'Student ID: {self.student_id}>')
    
    def sorted_history(self):
        history = self.requests + self.loggedhours + self.accolades + self.milestones
        return {
            'history': sorted([item.get_json() for item in history],
                          key=lambda x: x['timestamp'],
                          reverse=True)
        }