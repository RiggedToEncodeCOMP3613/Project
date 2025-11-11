from database import db
from datetime import datetime

class ActivityHistory(db.Model): #The purpose of this class is to log activities performed by students.
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(255), nullable=False) #simple description of the activity