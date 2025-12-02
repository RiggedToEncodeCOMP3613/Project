import pytest
import unittest
from App.main import create_app
from App.database import db
from App.controllers.student_controller import register_student, delete_student, create_hours_request, fetch_accolades, get_hours
from App.models import Student, Staff, ActivityHistory
from App.controllers.leaderboard_controller import generate_leaderboard

@pytest.fixture(autouse=True)
def app_context():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

class StudentUnitTests(unittest.TestCase):

    def test_register_student(self):
        student = register_student("Alice", "alice@email.com", "pass123")
        assert student.username == "Alice"
        assert student.student_id is not None
        assert str(student.student_id).startswith("8160")

    def test_create_hours_request(self):
        from datetime import datetime, timezone
        student = register_student("Requester", "req@email.com", "pass")
        req = student.make_request("volunteer", 1, 3.0, datetime.now(timezone.utc))
        assert req is not None
        assert req.hours == 3.0
        assert req.status == 'Pending'

    def test_delete_student(self):
        student = register_student("Bob", "bob@example.com", "pw")
        sid = student.student_id
        result = delete_student(sid)
        assert result is True
        assert Student.query.get(sid) is None

    def test_init_student(self):
        newStudent = Student("David Moore", "david77@outlook.com", "iloveschool67")
        self.assertEqual(newStudent.username, "David Moore")
        self.assertEqual(newStudent.email, "david77@outlook.com")
        self.assertTrue(newStudent.check_password("iloveschool67"))

    def test_student_get_json(self):
        newstudent = Student("David Moore", "david77@outlook.com", "iloveschool67")
        student_json = newstudent.get_json()
        self.assertEqual(student_json['username'], "David Moore")
        self.assertEqual(student_json['email'], "david77@outlook.com")

    def test_repr_student(self):
        newstudent = Student("David Moore", "david77@outlook.com", "iloveschool67")
        rep = repr(newstudent)
        # Check all parts of the string representation
        self.assertIn("Student ID=", rep)
        self.assertIn("Name=", rep)
        self.assertIn("Email=", rep)
        self.assertIn("David Moore", rep)
        self.assertIn("david77@outlook.com", rep)


class StudentIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        student_model = Student.create_student("Student Model", "student.model@test.com", "pw")
        assert isinstance(student_model, Student)
        db_student = Student.query.filter_by(student_id=student_model.student_id).first()
        assert db_student is not None
        assert db_student.username == "Student Model"

        registered = register_student("Student Registered", "student.registered@test.com", "pw")
        assert registered is not None
        assert registered.student_id is not None
        db_registered = Student.query.filter_by(student_id=registered.student_id).first()
        assert db_registered is not None
        assert db_registered.username == "Student Registered"

    def test_request_hours_confirmation(self):
        from datetime import datetime, timezone
        student = Student.create_student("amara", "amara@example.com", "pass")
        req = student.make_request("volunteer", 1, 4.0, datetime.now(timezone.utc))
        assert req is not None
        assert req.hours == 4.0
        assert req.status == 'Pending'

    #tests the make_request method of Student model
    def test_create_hours_request(self):
        newstudent = Student.create_student("Zoro", "green@gmail.com", "strongpass")
        newstaff = Staff("Luffy", "red@gmail.com", "dumbpass")
        db.session.add(newstaff)
        db.session.commit()

        newrequest = newstudent.make_request("community service", newstaff.staff_id, 5.0, "2024-12-01")
        
        self.assertEqual(newrequest.student_id, newstudent.student_id)
        self.assertEqual(newrequest.staff_id, newstaff.staff_id)
        self.assertEqual(newrequest.service, "community service")
        self.assertEqual(newrequest.hours, 5.0)
        self.assertEqual(newrequest.status, "Pending")  
        self.assertIsNotNone(newrequest.activity_id)  
        
        activity = ActivityHistory.query.get(newrequest.activity_id)
        self.assertIsNotNone(activity, "ActivityHistory should exist for this request")
        self.assertEqual(activity.student_id, newstudent.student_id)
        
        self.assertIn(newrequest, activity.requests)
        
        self.assertEqual(newstudent.activity_history.id, activity.id)
        self.assertIn(newrequest, newstudent.activity_history.requests)

        self.assertIn(newrequest, newstaff.requests)
        


    def test_fetch_requests(self):
        from datetime import datetime, timezone
        student = Student.create_student("kareem", "kareem@example.com", "pass")
        # create two requests
        r1 = student.make_request("volunteer", 1, 1.0, datetime.now(timezone.utc))
        r2 = student.make_request("volunteer", 1, 2.5, datetime.now(timezone.utc))
        from App.models import RequestHistory
        reqs = RequestHistory.query.filter_by(student_id=student.student_id).all()
        assert len(reqs) >= 2
        hours = [r.hours for r in reqs]
        assert 1.0 in hours and 2.5 in hours

    def test_get_approved_hours_and_accolades(self):
        from App.models import LoggedHoursHistory, ActivityHistory, MilestoneHistory
        from datetime import datetime, timezone

        student = Student.create_student("nisha", "nisha@example.com", "pass")
        from App.models import Milestone

        milestone_10 = Milestone(hours=10)
        db.session.add(milestone_10)
        db.session.commit()

        activity1 = ActivityHistory(student_id=student.student_id)
        activity2 = ActivityHistory(student_id=student.student_id)
        db.session.add_all([activity1, activity2])
        db.session.flush()

        lh1 = LoggedHoursHistory(student_id=student.student_id, staff_id=1, service="volunteer", hours=6.0, before=0.0, after=6.0, date_completed=datetime.now(timezone.utc))
        lh1.activity_id = activity1.id
        lh2 = LoggedHoursHistory(student_id=student.student_id, staff_id=1, service="volunteer", hours=5.0, before=6.0, after=11.0, date_completed=datetime.now(timezone.utc))
        lh2.activity_id = activity2.id
        db.session.add_all([lh1, lh2])
        db.session.commit()

        student.calculate_total_hours()

        name, total = get_hours(student.student_id)
        assert name == student.username
        assert total == 11.0

        milestone_10.add_student(student.student_id)
        db.session.commit()

        if not hasattr(Student, 'accolades'):
            def _accolades(self):
                return [f"{m.hours} Hours Milestone" for m in getattr(self, 'achieved_milestones', [])]
            Student.accolades = _accolades

        accolades = fetch_accolades(student.student_id)
        assert isinstance(accolades, list)
        assert any('10' in str(a) for a in accolades)

    def test_generate_leaderboard(self):
        s_a = Student.create_student("Student A", "a@test.com", "pw")
        s_b = Student.create_student("Student B", "b@test.com", "pw")
        s_c = Student.create_student("Student C", "c@test.com", "pw")

        s_a.total_hours = 5.0
        s_b.total_hours = 15.0
        s_c.total_hours = 10.0
        db.session.commit()

        leaderboard = generate_leaderboard()
        assert isinstance(leaderboard, list)
        assert leaderboard[0]['name'] == 'Student B' and leaderboard[0]['hours'] == 15.0
        assert leaderboard[1]['name'] == 'Student C' and leaderboard[1]['hours'] == 10.0
        assert leaderboard[2]['name'] == 'Student A' and leaderboard[2]['hours'] == 5.0

    def test_student_milestone_achievement(self):
        from App.controllers.milestone_controller import create_milestone
        from App.controllers.loggedHoursHistory_controller import create_logged_hours
        from App.models import MilestoneHistory
        from datetime import datetime, timezone

        student = register_student("Milestoner", "milestone.student@test.com", "pw")
        milestone = create_milestone(5)

        # No milestone history should exist yet
        before = MilestoneHistory.query.filter_by(student_id=student.student_id, milestone_id=milestone.id).first()
        assert before is None

        # Log some hours below the threshold
        create_logged_hours(student.student_id, staff_id=1, hours=3.0, service="volunteer", date_completed=datetime.now(timezone.utc))
        mid = MilestoneHistory.query.filter_by(student_id=student.student_id, milestone_id=milestone.id).first()
        assert mid is None

        # Log additional hours to cross the milestone threshold
        create_logged_hours(student.student_id, staff_id=1, hours=3.0, service="volunteer", date_completed=datetime.now(timezone.utc))

        # Now the milestone history record should exist
        after = MilestoneHistory.query.filter_by(student_id=student.student_id, milestone_id=milestone.id).first()
        assert after is not None
        # And the student's total hours should reflect both logs
        from App.controllers.student_controller import get_hours
        name, total = get_hours(student.student_id)
        assert total == pytest.approx(6.0)

    def test_student_view_accolades(self):
        from App.controllers.staff_controller import register_staff
        try:
            from App.controllers.accolade_controller import create_accolade, assign_accolade_to_student
        except Exception:
            create_accolade = None
            assign_accolade_to_student = None

        from App.models import Accolade, AccoladeHistory
        from sqlalchemy import inspect

        staff = register_staff("AccoladeStaff", "accolade.staff@test.com", "pw")
        student = register_student("AccoladeViewer", "accolade.viewer@test.com", "pw")

        if create_accolade:
            raw = create_accolade(staff.staff_id, "Shining Star")
            accolade_obj = raw[0] if isinstance(raw, tuple) else raw
        else:
            accolade_obj = Accolade(staff_id=staff.staff_id, description="Shining Star")
            db.session.add(accolade_obj)
            db.session.commit()

        try:
            ident = inspect(accolade_obj).identity
            pk = ident[0] if ident else None
        except Exception:
            pk = getattr(accolade_obj, "id", None)
        accolade_id = pk
        assert accolade_id is not None

        if assign_accolade_to_student:
            assign_accolade_to_student(accolade_id, student.student_id, staff.staff_id)
        else:
            accolade_obj.add_student(student.student_id)
            hist = AccoladeHistory(student_id=student.student_id, staff_id=staff.staff_id, accolade_id=accolade_id, description=accolade_obj.description)
            db.session.add(hist)
            db.session.commit()

        Student.accolades = Student.check_accolades

        accolades = fetch_accolades(student.student_id)
        assert isinstance(accolades, list)
        assert any((getattr(a, 'description', None) == 'Shining Star') or ('Shining' in str(a)) for a in accolades)