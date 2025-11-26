from App.database import db
from datetime import datetime, timezone

def parse_date(date_str: str) -> datetime:
    if isinstance(date_str, datetime):
        return date_str
    return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)

class LoggedHoursHistory(db.Model):
    __tablename__ = 'loggedhours_history'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity_history.id'), nullable=False)

    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=True)
    service = db.Column(db.String(100), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    before = db.Column(db.Float, nullable=False)
    after = db.Column(db.Float, nullable=False)
    date_completed = db.Column(db.DateTime, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __init__(self, student_id, staff_id, service, hours, before, after, date_completed):
        self.student_id = student_id
        self.staff_id = staff_id
        self.service = service
        self.hours = hours
        # Import Student locally to avoid circular imports
        from App.models.student import Student
        student = Student.query.get(self.student_id)
        self.before = student.total_hours if student else 0.0
        self.after = (student.total_hours if student else 0.0) + after
        self.date_completed = parse_date(date_completed)
        #self.date_completed = date_completed

    def __repr__(self):
        return (
            f'<LoggedHoursHistory ID: {self.id} | '
            f'Student ID: {self.student_id} | '
            f'Staff ID: {self.staff_id} | '
            f'Service: {self.service} | '
            f'Hours: {self.hours} | '
            f'Hours Before: {self.before} | '
            f'Hours After: {self.after} | '
            f'Date Completed: {self.date_completed} | '
            f'Date Hours Logged: {self.timestamp}>')


    def get_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'staff_id': self.staff_id,
            'service': self.service,
            'hours': self.hours,
            'before': self.before,
            'after': self.after,
            'date_completed': self.date_completed.isoformat(),
            'timestamp': self.timestamp.isoformat()
        }
    