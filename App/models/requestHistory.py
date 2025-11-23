from App.database import db
from App.controllers.date_controller import parse_date
from datetime import datetime, timezone

class RequestHistory(db.Model):
    __tablename__ = 'request_history'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity_history.id'), nullable=False)

    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    date_completed = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    date_responded = db.Column(db.DateTime)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __init__(self, student_id, staff_id, service, hours, date_completed):
        self.student_id = student_id
        self.staff_id = staff_id
        self.service = service
        self.hours = hours
        self.date_completed = parse_date(date_completed)
        self.date_responded = None

    
    def __repr__(self):
        return f'<Request ID: {self.id} | Student ID: {self.student_id} |  Staff ID: {self.staff_id} | Service: {self.service} | Hours: {self.duration} |  Date Completed: {self.date_completed} | Status: {self.status} | Date Resolved: {self.date_responded} |  Date Request Was Made: {self.timestamp}>'
       
    
    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'staff_id': self.staff_id,
            'service': self.service,
            'hours': self.hours,
            'date_completed': self.date_completed.isoformat(),
            'status': self.status,
            'date_responded': self.date_responded.isoformat() if self.date_responded else None,
            'timestamp': self.timestamp.isoformat()
        }


