from App.database import db
from datetime import datetime, timezone

class AccoladeHistory(db.Model):
    __tablename__ = 'accolade_history'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity_history.id'), nullable=False)

    accolade_id = db.Column(db.Integer, db.ForeignKey('accolade.accolade_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=True)
    description = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __init__(self, accolade_id, student_id, staff_id, description):
        self.accolade_id = accolade_id
        self.student_id = student_id
        self.staff_id = staff_id
        self.description = description

    def __repr__(self):
        return (
            f'<AccoladeHistory ID: {self.id} | '
            f'Accolade ID: {self.accolade_id} | '
            f'Student ID: {self.student_id} | '
            f'Staff ID: {self.staff_id} | '
            f'Description: {self.description} | '
            f'Date Awarded: {self.timestamp}>')


    def get_json(self):
        return {
            'id': self.id,
            'accolade_id': self.accolade_id,
            'student_id': self.student_id,
            'staff_id': self.staff_id,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }