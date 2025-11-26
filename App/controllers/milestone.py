from App.database import db
from App.models import Milestone
from rich.table import Table
from rich.console import Console
from App.models import MilestoneHistory

def create_milestone(hours):
    new_milestone = Milestone(hours=hours)
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
        MilestoneHistory.query.filter_by(milestone_id=milestone_id).delete()
        db.session.delete(milestone)
        db.session.commit()
        return True
    return False

def delete_all_milestones():
    from App.models import MilestoneHistory
    MilestoneHistory.query.delete()  # Delete all milestone history records
    num_deleted = db.session.query(Milestone).delete()
    db.session.commit()
    return num_deleted

def search_milestones(milestone_id=None, hours=None):
    query = Milestone.query
    if milestone_id is not None:
        query = query.filter_by(id=milestone_id)
    if hours is not None:
        query = query.filter_by(hours=hours)
    
    milestones = query.all()
    return [m.get_json() for m in milestones]

def update_milestone(milestone_id, new_hours):
    milestone = Milestone.query.get(milestone_id)
    if milestone:
        milestone.hours = new_hours
        db.session.commit()
        return milestone
    return None
