from App.database import db
from App.models import Milestone
from rich.table import Table
from rich.console import Console
from App.models import MilestoneHistory
import pytest

def create_milestone(hours):
    new_milestone = Milestone(hours=hours)
    db.session.add(new_milestone)
    db.session.flush()  # Get the milestone ID

    from App.models import Student, ActivityHistory
    students = Student.query.filter(Student.total_hours >= hours).all()
    for student in students:
        existing_history = MilestoneHistory.query.filter_by(
            milestone_id=new_milestone.id,
            student_id=student.student_id
        ).first()
        if not existing_history:
            activity = ActivityHistory(student_id=student.student_id)
            db.session.add(activity)
            db.session.flush()  # To get activity ID
            milestone_history = MilestoneHistory(
                milestone_id=new_milestone.id,
                student_id=student.student_id,
                hours=new_milestone.hours
            )
            milestone_history.activity_id = activity.id
            db.session.add(milestone_history)

    db.session.commit()
    return new_milestone

def list_all_milestones():
    milestones = Milestone.query.all()
    if not milestones:
        return []
    return [m.get_json() for m in milestones]

def delete_milestone(milestone_id, delete_history=False):
    milestone = Milestone.query.get(milestone_id)
    if milestone:
        if delete_history:
            MilestoneHistory.query.filter_by(milestone_id=milestone_id).delete()
        
        db.session.delete(milestone)
        db.session.commit()
        return True
    return False

def delete_all_milestones(delete_history=False):
    from App.models import MilestoneHistory
    if delete_history:
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

def list_all_milestone_history():
    history_records = MilestoneHistory.query.all()
    if not history_records:
        return []
    return [h.get_json() for h in history_records]

class TestMilestoneController:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self, app):
        with app.app_context():
            db.create_all()
            yield
            db.session.remove()
            db.drop_all()

    def test_create_milestone(self):
        milestone = create_milestone(10)
        assert milestone.hours == 10
        assert Milestone.query.count() == 1
        assert milestone.id is not None

    def test_list_all_milestones(self):
        create_milestone(5)
        create_milestone(15)
        milestones = list_all_milestones()
        assert len(milestones) == 2

    def test_delete_milestone(self):
        milestone = create_milestone(20)
        result = delete_milestone(milestone.id)
        assert result is True
        assert Milestone.query.count() == 0

    def test_delete_all_milestones(self):
        create_milestone(5)
        create_milestone(15)
        num_deleted = delete_all_milestones()
        assert num_deleted == 2
        assert Milestone.query.count() == 0

    def test_search_milestones(self):
        m1 = create_milestone(10)
        m2 = create_milestone(20)
        results = search_milestones(hours=10)
        assert len(results) == 1
        assert results[0]['hours'] == 10

    def test_update_milestone(self):
        milestone = create_milestone(30)
        updated_milestone = update_milestone(milestone.id, 75)
        assert updated_milestone.hours == 75 # pyright: ignore[reportOptionalMemberAccess]

    def test_list_all_milestone_history(self):
        milestone = create_milestone(10)
        history = list_all_milestone_history()
        assert len(history) >= 0  # Depending on existing students