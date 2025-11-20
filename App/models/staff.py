from App.database import db
from .user import User
from App.models import RequestHistory
from App.models import Accolade
from App.models import AccoladeHistory
from App.models import LoggedHoursHistory

class Staff(User):
    __tablename__ = "staff"
    staff_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), primary_key=True)
    
    # Relationships (match required names)
    loggedhours = db.relationship('LoggedHoursHistory', backref='staff', lazy=True, cascade="all, delete-orphan")
    accolades_created = db.relationship('Accolade', back_populates='staff', lazy=True, cascade="all, delete-orphan")
    accolades_awarded = db.relationship('AccoladeHistory', backref='awarded_by', lazy=True, cascade="all, delete-orphan")
    requests = db.relationship('RequestHistory', backref='staff', lazy=True, cascade="all, delete-orphan")

    # Inheritance setup
    __mapper_args__ = {
        "polymorphic_identity": "staff"
    }

    def __init__(self, username, email, password):
        super().__init__(username, email, password, role="staff")

    def __repr__(self):
        return f"[Staff ID= {str(self.staff_id)} Name= {self.username} Email= {self.email}]"
    
    def get_json(self):
        return {
            'staff_id': self.staff_id,
            'username': self.username,
            'email': self.email
        }
    
    @staticmethod
    def create_staff(username, email, password):
        newstaff = Staff(username=username, email=email, password=password)
        db.session.add(newstaff)
        db.session.commit()
        return newstaff
    
    def log_hours(self, student_id, hours):
        # need LoggedHoursHistory entry
        pass
    
    def get_pending_requests(self):
        pending = RequestHistory.query.filter_by(status='pending').all()
        return pending
    

######## Need History classes implemented to complete below methods #######
    def approve_request(self, requestHistory):
        if requestHistory.status != 'pending':
            return None
        requestHistory.status = 'approved'
        requestHistory.reviewed_by_id = self.staff_id
        
        # Create a LoggedHoursHistory entry
        logged = LoggedHoursHistory(
            student_id=requestHistory.student_id, 
            staff_id=self.staff_id, 
            hours=requestHistory.hours, 
            status='approved'
        )
        db.session.add(logged)
        db.session.commit()
        return logged
    
    def deny_request(self, request):
        if request.status != 'pending':
            return False
        request.status = 'denied'
        request.reviewed_by_id = self.staff_id
        db.session.commit()
        return True
    
    def create_accolade(self, description):
        accolade = Accolade(staff_id=self.staff_id, description=description)
        db.session.add(accolade)
        db.session.commit()
        return accolade
    
    def award_accolade(self, student_id, accolade_id):
        # student > accolade > accoladehistory
        pass


