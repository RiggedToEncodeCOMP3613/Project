from App.database import db
from App.models import User, Staff, Student, RequestHistory, Accolade, AccoladeHistory, ActivityHistory


#Search accolades based on various criteria
def search_accolades(accolade_id=None, staff_id=None, description=None, student_id=None):

    from App.models import Student
    
    try:
        query = Accolade.query
        
        if accolade_id is not None:
            query = query.filter_by(id=accolade_id)
        
        if staff_id is not None:
            staff = Staff.query.get(staff_id)
            if not staff:
                return None, f"Staff with ID {staff_id} not found"
            query = query.filter_by(staff_id=staff_id)
        
        if description is not None:
            query = query.filter(Accolade.description.ilike(f'%{description}%'))
        
        if student_id is not None:
            student = Student.query.get(student_id)
            if not student:
                return None, f"Student with ID {student_id} not found"
            # Join with student_accolade table to filter by student
            query = query.join(Accolade.students).filter(Student.student_id == student_id)
        
        accolades = query.all()
        
        return accolades, None
        
    except Exception as e:
        return None, f"Error searching accolades: {str(e)}"
    
    
# Drop accolade table (accolade records and accolade-student associations)
def drop_accolade_table():

    try:
        accolade_count = Accolade.query.count()
        Accolade.query.delete()
        
        db.session.commit()
        
        return {
            'accolades_deleted': accolade_count
        }, None
        
    except Exception as e:
        db.session.rollback()
        return None, f"Error dropping accolade table: {str(e)}"