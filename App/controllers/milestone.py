from App.database import db
from App.models import Milestone
from rich.table import Table
from rich.console import Console

def create_milestone(milestone_value):
    new_milestone = Milestone(milestone=milestone_value)
    db.session.add(new_milestone)
    db.session.commit()
    return new_milestone

def list_all_milestones():
    milestones = Milestone.query.all()
    if not milestones:
        return []
    return [m.get_json() for m in milestones]

def delete_milestone(milestone_id):
    milestone = Milestone.query.get(milestone_id)
    if milestone:
        db.session.delete(milestone)
        db.session.commit()
        return True
    return False

def delete_all_milestones():
    num_deleted = db.session.query(Milestone).delete()
    db.session.commit()
    return num_deleted
