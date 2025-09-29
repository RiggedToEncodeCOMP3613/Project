from App.database import db

class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    #relationship to LoggedHours and Request both One-to-Many
    loggedhours = db.relationship('LoggedHours', backref='student', lazy=True, cascade="all, delete-orphan")
    requests = db.relationship('Request', backref='student', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"[Student ID= {self.id:<3}  Name= {self.name:<15} Email= {self.email}]"
    
    
    # Method to create a new student
    def create_student(name, email):
        newstudent = Student(name=name, email=email)
        db.session.add(newstudent)
        db.session.commit()
        return newstudent
    
    # Method for student to request hours
    def request_hours_confirmation(self, hours):
        from App.models import Request
        request = Request(student_id=self.id, hours=hours, status='pending')
        db.session.add(request)
        db.session.commit()
        return request
    
    # Method to calculate total approved hours and accolades
    def accolades(self):
        # Only count approved logged hours
        total_hours = sum(lh.hours for lh in self.loggedhours if lh.status == 'approved')
        accolades = []
        if total_hours >= 10:
            accolades.append('10 Hours Milestone')
        if total_hours >= 25:
            accolades.append('25 Hours Milestone')
        if total_hours >= 50:
            accolades.append('50 Hours Milestone')
        return accolades
    
    