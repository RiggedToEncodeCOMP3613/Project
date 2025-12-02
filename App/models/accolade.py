from App.database import db

# Association table for Student <-> Accolade many-to-many relationship
student_accolade = db.Table(
    'student_accolade',
    db.Column('student_id', db.Integer, db.ForeignKey('student.student_id'), primary_key=True),
    db.Column('accolade_id', db.Integer, db.ForeignKey('accolade.id'), primary_key=True)
)

class Accolade(db.Model):

    __tablename__ = 'accolade'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    # Many-to-many relationship with students (one-sided)
    students = db.relationship(
        'Student',
        secondary=student_accolade,
        lazy=True
    )

    # Relationship to Staff who created the accolade
    staff = db.relationship('Staff', back_populates='accolades_created')

    def __init__(self, staff_id, description):
        self.staff_id = staff_id
        self.description = description

    def __repr__(self):
        return f"<Accolade(id={self.id}, staff_id={self.staff_id}, description='{self.description}')>"

    def get_json(self):
        return {
            'id': self.id,
            'staff_id': self.staff_id,
            'description': self.description
        }

    def add_student(self, student_id):
        from App.models import Student
        student = Student.query.get(student_id)
        if student and student not in self.students:
            try:
                self.students.append(student)
                db.session.commit()
            except Exception:
                # ignore failures to append
                pass
        return student