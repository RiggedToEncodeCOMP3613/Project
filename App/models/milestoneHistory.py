from App.database import db
from datetime import datetime, timezone

class MilestoneHistory(db.Model):
    __tablename__ = 'milestone_history'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity_history.id'), nullable=False)

    milestone_id = db.Column(db.Integer, db.ForeignKey('milestone.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __init__(self, milestone_id, student_id, value):
        self.milestone_id = milestone_id
        self.student_id = student_id
        self.value = value

    def __repr__(self):
        return (
            f'<MilestoneHistory ID: {self.id} | '
            f'Milestone ID: {self.milestone_id} | '
            f'Student ID: {self.student_id} | '
            f'Value: {self.value} | '
            f'Date Recorded: {self.timestamp}>')


    def get_json(self):
        return {
            'id': self.id,
            'milestone_id': self.milestone_id,
            'student_id': self.student_id,
            'value': self.value,
            'timestamp': self.timestamp.isoformat()
        }