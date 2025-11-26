from App.database import db
from App.models import Milestone

def create_milestone(milestone_value):
    new_milestone = Milestone(milestone=milestone_value)
    db.session.add(new_milestone)
    db.session.commit()
    return new_milestone
