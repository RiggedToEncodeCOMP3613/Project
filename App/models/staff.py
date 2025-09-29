from App.database import db

class Staff(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    #relationaship to LoggedHours
    loggedhours = db.relationship('LoggedHours', backref='staff', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"[Staff ID= {self.id:<3} Name= {self.name:<15} Email= {self.email}]"
    
    # Method to create a new staff member
    def create_staff(name, email):
        newstaff = Staff(name=name, email=email)
        db.session.add(newstaff)
        db.session.commit()
        return newstaff
    
    # Method for staff to approve or deny requests
    def approve_request(self, request):
        from App.models import LoggedHours
        if request.status != 'pending':
            return None
        # Mark request as approved
        request.status = 'approved'
        # Create a LoggedHours entry
        logged = LoggedHours(student_id=request.student_id, staff_id=self.id, hours=request.hours, status='approved')
        db.session.add(logged)
        db.session.commit()
        return logged
    
    #Method to deny a request
    def deny_request(self, request):
        if request.status != 'pending':
            return False
        request.status = 'denied'
        db.session.commit()
        return True
    
    