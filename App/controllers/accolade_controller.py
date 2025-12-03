from App.database import db
from App.models import Staff, Student, Accolade, AccoladeHistory, ActivityHistory

# COMMAND FUNCTIONS

def create_accolade(staff_id, description):
    staff = Staff.query.get(staff_id)
    if not staff:
        return None, f"Staff with ID {staff_id} not found"

    existing_accolade = Accolade.query.filter_by(description=description).first()
    if existing_accolade:
        return None, f"Accolade with description '{description}' already exists (ID: {existing_accolade.id})"

    try:
        accolade = Accolade(staff_id=staff_id, description=description)
        db.session.add(accolade)
        db.session.commit()

        return accolade, None

    except Exception as e:
        db.session.rollback()
        return None, f"Error creating accolade: {str(e)}"


def search_accolades(accolade_id=None, staff_id=None, description=None, student_id=None):

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


def update_accolade(accolade_id, staff_id=None, description=None):

    accolade = Accolade.query.get(accolade_id)
    if not accolade:
        return None, f"Accolade with ID {accolade_id} not found"

    if staff_id is None and description is None:
        return None, "No fields to update. Provide at least one of: staff_id, description"

    try:
        updated_fields = []

        if staff_id is not None:
            staff = Staff.query.get(staff_id)
            if not staff:
                return None, f"Staff with ID {staff_id} not found"
            accolade.staff_id = staff_id
            updated_fields.append(f"staff_id: {staff_id}")

        if description is not None:
            existing = Accolade.query.filter(
                Accolade.description == description,
                Accolade.id != accolade_id,
            ).first()
            if existing:
                return None, f"Another accolade already has description '{description}' (ID: {existing.id})"
            accolade.description = description
            updated_fields.append(f"description: '{description}'")

        db.session.commit()

        return {
            'accolade': accolade,
            'updated_fields': updated_fields,
        }, None

    except Exception as e:
        db.session.rollback()
        return None, f"Error updating accolade: {str(e)}"


def assign_accolade_to_student(accolade_id, student_id, staff_id):
    accolade = Accolade.query.get(accolade_id)
    if not accolade:
        return None, f"Accolade with ID {accolade_id} not found"

    staff = Staff.query.get(staff_id)
    if not staff:
        return None, f"Staff with ID {staff_id} not found"

    # Check if student was already assigned
    existing_history = AccoladeHistory.query.filter_by(
        accolade_id=accolade_id,
        student_id=student_id,
    ).first()

    if existing_history:
        return None, f"Student {student_id} is already assigned to this accolade"

    try:
        student = accolade.add_student(student_id)

        if not student:
            return None, f"Student with ID {student_id} not found"

        # Get or create ActivityHistory for this student
        activity = ActivityHistory.query.filter_by(student_id=student_id).first()
        if not activity:
            activity = ActivityHistory(student_id=student_id)
            db.session.add(activity)
            db.session.flush()

        # Create history record
        history = AccoladeHistory(
            accolade_id=accolade_id,
            student_id=student_id,
            staff_id=staff_id,
            description=accolade.description,
        )
        history.activity_id = activity.id
        db.session.add(history)
        db.session.commit()

        return {
            'accolade': accolade,
            'student': student,
            'history': history,
        }, None

    except Exception as e:
        db.session.rollback()
        return None, f"Error assigning student to accolade: {str(e)}"


def delete_accolade(accolade_id, delete_history=False):
    accolade = Accolade.query.get(accolade_id)
    if not accolade:
        return False, f"Accolade with ID {accolade_id} not found"
    
    try:
        description = accolade.description
        history_deleted = 0
        activities_deleted = 0
        
        # Delete associated history records if requested
        if delete_history:
            # Get all history records for this accolade
            history_records = AccoladeHistory.query.filter_by(accolade_id=accolade_id).all()
            activity_ids_to_check = set()
            
            for history_record in history_records:
                activity_ids_to_check.add(history_record.activity_id)
                history_deleted += 1
            
            # Delete the history records
            AccoladeHistory.query.filter_by(accolade_id=accolade_id).delete()
            
            # Check if any ActivityHistory records are now empty and delete them
            for activity_id in activity_ids_to_check:
                activity = ActivityHistory.query.get(activity_id)
                if activity:
                    has_history = (
                        len(activity.requests) > 0 or
                        len(activity.loggedhours) > 0 or
                        len(activity.accolades) > 0 or
                        len(activity.milestones) > 0
                    )
                    if not has_history:
                        db.session.delete(activity)
                        activities_deleted += 1
        
        # Delete the accolade
        db.session.delete(accolade)
        db.session.commit()
        
        return True, {
            'description': description,
            'history_deleted': history_deleted,
            'empty_activities_deleted': activities_deleted
        }
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error deleting accolade: {str(e)}"


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


# HELPER FUNCTIONS

# Removes a student from an accolade.
# If `delete_history` is True, also deletes the associated AccoladeHistory record.
def remove_accolade_from_student(accolade_id, student_id, delete_history=False):

    accolade = Accolade.query.get(accolade_id)
    if not accolade:
        return None, f"Accolade with ID {accolade_id} not found"

    student = Student.query.get(student_id)
    if not student:
        return None, f"Student with ID {student_id} not found"

    if student not in accolade.students:
        return None, f"Student {student_id} is not assigned to accolade {accolade_id}"

    try:
        accolade.students.remove(student)

        history_deleted = 0
        activity_deleted = False

        # Delete history record if requested
        if delete_history:
            history_record = AccoladeHistory.query.filter_by(
                accolade_id=accolade_id,
                student_id=student_id,
            ).first()

            if history_record:
                activity_id = history_record.activity_id
                db.session.delete(history_record)
                history_deleted = 1

                # Check if ActivityHistory is now empty
                activity = ActivityHistory.query.get(activity_id)
                if activity:
                    has_history = (
                        len(activity.requests) > 0 or
                        len(activity.loggedhours) > 0 or
                        len(activity.accolades) > 0 or
                        len(activity.milestones) > 0
                    )
                    if not has_history:
                        db.session.delete(activity)
                        activity_deleted = True

        db.session.commit()

        return {
            'accolade': accolade,
            'student': student,
            'history_deleted': history_deleted,
            'activity_deleted': activity_deleted,
        }, None

    except Exception as e:
        db.session.rollback()
        return None, f"Error removing student from accolade: {str(e)}"


# Removed unused `listAllAccolades`; use `search_accolades` or direct queries instead.