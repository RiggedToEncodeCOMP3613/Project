import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, RequestHistory, Staff, LoggedHoursHistory
from App.models import User
from App.models import Staff
from App.models import Student
from App.models import RequestHistory
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)
from App.controllers.student_controller import (
    register_student,
    create_hours_request,
    fetch_requests,
    get_hours,
    fetch_accolades
)
from App.controllers.leaderboard_controller import generate_leaderboard
from App.controllers.staff_controller import (
    register_staff,
    fetch_all_requests,
    process_request_approval,
    process_request_denial
)

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_check_password(self):
        Testuser = User("David Goggins", "goggs@gmail.com", "goggs123", "student")
        self.assertTrue(Testuser.check_password("goggs123"))

    def test_set_password(self):
        password = "passtest"
        new_password = "passtest"
        Testuser = User("bob", "bob@email.com", password, "user")
        Testuser.set_password(new_password)
        assert Testuser.check_password(new_password)

class StaffUnitTests(unittest.TestCase):

    def test_init_staff(self):
        newstaff = Staff("Jacob Lester", "jacob55@gmail.com", "Jakey55")
        self.assertEqual(newstaff.username, "Jacob Lester")
        self.assertEqual(newstaff.email, "jacob55@gmail.com")
        self.assertTrue(newstaff.check_password("Jakey55"))

    def test_staff_get_json(self):
        Teststaff = Staff("Jacob Lester", "jacob55@gmail.com", "jakey55")
        staff_json = Teststaff.get_json()
        self.assertEqual(staff_json['username'], "Jacob Lester")
        self.assertEqual(staff_json['email'], "jacob55@gmail.com")

    def test_repr_staff(self):
        Teststaff = Staff("Jacob Lester", "jacob55@gmail.com", "jakey55")
        rep = repr(Teststaff)
        # Check all parts of the string representation
        self.assertIn("Staff ID=", rep)
        self.assertIn("Name=", rep)
        self.assertIn("Email=", rep)
        self.assertIn("Jacob Lester", rep)
        self.assertIn("jacob55@gmail.com", rep)

class StudentUnitTests(unittest.TestCase):

    def test_init_student(self):
        newStudent = Student("David Moore", "david77@outlook.com" , "iloveschool67")
        self.assertEqual(newStudent.username, "David Moore")
        self.assertEqual(newStudent.email, "david77@outlook.com")
        self.assertTrue(newStudent.check_password("iloveschool67"))

    def test_student_get_json(self):
        newstudent = Student("David Moore", "david77@outlook.com" , "iloveschool67")
        student_json = newstudent.get_json()
        self.assertEqual(student_json['username'], "David Moore")
        self.assertEqual(student_json['email'], "david77@outlook.com")

    def test_repr_student(self):
        newstudent = Student("David Moore", "david77@outlook.com" , "iloveschool67")
        rep = repr(newstudent)
        # Check all parts of the string representation
        self.assertIn("Student ID=", rep)
        self.assertIn("Name=", rep)
        self.assertIn("Email=", rep)
        self.assertIn("David Moore", rep)
        self.assertIn("david77@outlook.com", rep)

class RequestUnitTests(unittest.TestCase):

    def test_init_request(self):
        from App.models import RequestHistory
        from datetime import datetime, timezone
        Testrequest = RequestHistory(student_id=12, staff_id=1, service="volunteer", hours=30, date_completed=datetime.now(timezone.utc))
        self.assertEqual(Testrequest.student_id, 12)
        self.assertEqual(Testrequest.hours, 30)
        self.assertEqual(Testrequest.status, None)

    def test_repr_request(self):
        from App.models import RequestHistory
        from datetime import datetime, timezone
        Testrequest = RequestHistory(student_id=4, staff_id=1, service="volunteer", hours=40, date_completed=datetime.now(timezone.utc))
        Testrequest.status = 'denied'
        rep = repr(Testrequest)
        # Check all parts of the string representation
        self.assertIn("Request ID:", rep)
        self.assertIn("Student ID:", rep)
        self.assertIn("Hours:", rep)
        self.assertIn("Status:", rep)
        self.assertIn("4", rep)
        self.assertIn("40", rep)
        self.assertIn("denied", rep)

class LoggedHoursUnitTests(unittest.TestCase):

    def test_init_loggedhours(self):
        from App.models import LoggedHoursHistory
        Testlogged = LoggedHoursHistory(student_id=1, staff_id=2, service="volunteer", hours=20, before=0.0, after=20.0, date_completed="2025-01-01")
        self.assertEqual(Testlogged.student_id, 1)
        self.assertEqual(Testlogged.staff_id, 2)
        self.assertEqual(Testlogged.hours, 20)

    def test_repr_loggedhours(self):
        from App.models import LoggedHoursHistory
        Testlogged = LoggedHoursHistory(student_id=1, staff_id=2, service="volunteer", hours=20, before=0.0, after=20.0, date_completed="2025-01-01")
        rep = repr(Testlogged)
        # Check all parts of the string representation
        self.assertIn("LoggedHoursHistory ID:", rep)
        self.assertIn("Student ID:", rep)
        self.assertIn("Staff ID:", rep)
        self.assertIn("Hours:", rep)
        self.assertIn("1", rep)
        self.assertIn("2", rep)
        self.assertIn("20", rep)
        


    






# '''
#     Integration Tests
# '''
# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="function")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class StaffIntegrationTests(unittest.TestCase):

    def test_create_staff(self):
        staff = register_staff("marcus", "marcus@example.com", "pass123")
        assert staff.username == "marcus"
        # ensure staff persisted
        fetched = Staff.query.get(staff.staff_id)
        assert fetched is not None

    def test_request_fetch(self):
        # create a student and a pending request
        from App.models import RequestHistory, ActivityHistory
        from datetime import datetime, timezone
        student = Student.create_student("tariq", "tariq@example.com", "studpass")
        activity = ActivityHistory(student_id=student.student_id)
        db.session.add(activity)
        db.session.flush()
        req = RequestHistory(student_id=student.student_id, staff_id=1, service="volunteer", hours=3.5, date_completed=datetime.now(timezone.utc))
        req.activity_id = activity.id
        db.session.add(req)
        db.session.commit()

        requests = fetch_all_requests()
        # should include request with student name 'tariq'
        assert any(r['student_name'] == 'tariq' and r['hours'] == 3.5 for r in requests)

    def test_hours_approval(self):
        # prepare staff, student and request
        from App.models import RequestHistory, ActivityHistory
        from datetime import datetime, timezone
        staff = register_staff("carmichael", "carm@example.com", "staffpass")
        student = Student.create_student("niara", "niara@example.com", "studpass")
        activity = ActivityHistory(student_id=student.student_id)
        db.session.add(activity)
        db.session.flush()
        req = RequestHistory(student_id=student.student_id, staff_id=staff.staff_id, service="volunteer", hours=2.0, date_completed=datetime.now(timezone.utc))
        req.activity_id = activity.id
        db.session.add(req)
        db.session.commit()

        result = process_request_approval(staff.staff_id, req.id)
        # verify logged hours created and request status updated
        logged = result.get('logged_hours')
        assert logged is not None
        assert logged.hours == 2.0
        assert result['request'].status == 'Approved'

    def test_hours_denial(self):
        # prepare staff, student and request
        from App.models import RequestHistory, ActivityHistory
        from datetime import datetime, timezone
        staff = register_staff("maritza", "maritza@example.com", "staffpass")
        student = Student.create_student("jabari", "jabari@example.com", "studpass")
        activity = ActivityHistory(student_id=student.student_id)
        db.session.add(activity)
        db.session.flush()
        req = RequestHistory(student_id=student.student_id, staff_id=staff.staff_id, service="volunteer", hours=1.0, date_completed=datetime.now(timezone.utc))
        req.activity_id = activity.id
        db.session.add(req)
        db.session.commit()

        result = process_request_denial(staff.staff_id, req.id)
        assert result['denial_successful'] is True
        assert result['request'].status == 'Denied'


class StudentIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        student = register_student("junior", "junior@example.com", "studpass")
        assert student.username == "junior"
        fetched = Student.query.get(student.student_id)
        assert fetched is not None

    def test_request_hours_confirmation(self):
        from datetime import datetime, timezone
        student = Student.create_student("amara", "amara@example.com", "pass")
        req = student.make_request("volunteer", 1, 4.0, datetime.now(timezone.utc))
        assert req is not None
        assert req.hours == 4.0
        assert req.status == 'Pending'

    def test_fetch_requests(self):
        from datetime import datetime, timezone
        student = Student.create_student("kareem", "kareem@example.com", "pass")
        # create two requests
        r1 = student.make_request("volunteer", 1, 1.0, datetime.now(timezone.utc))
        r2 = student.make_request("volunteer", 1, 2.5, datetime.now(timezone.utc))
        reqs = RequestHistory.query.filter_by(student_id=student.student_id).all()
        assert len(reqs) >= 2
        hours = [r.hours for r in reqs]
        assert 1.0 in hours and 2.5 in hours

    def test_get_approved_hours_and_accolades(self):
        from App.models import LoggedHoursHistory, ActivityHistory
        from datetime import datetime, timezone
        from App.controllers.milestone_controller import create_milestone
        create_milestone(10)
        student = Student.create_student("nisha", "nisha@example.com", "pass")
        # Manually add logged approved hours
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

        from App.models.milestoneHistory import MilestoneHistory
        from App.models.milestone import Milestone
        milestone_histories = MilestoneHistory.query.filter_by(student_id=student.student_id).all()
        milestones = [Milestone.query.get(h.milestone_id) for h in milestone_histories]
        accolades = [f"{m.hours} Hours Milestone" for m in milestones]
        # 11 hours should give at least the 10 hours milestone
        assert '10 Hours Milestone' in accolades

    def test_generate_leaderboard(self):
        from App.models import LoggedHoursHistory, ActivityHistory
        from datetime import datetime, timezone
        # create three students with varying approved hours
        a = Student.create_student("zara", "zara@example.com", "p")
        b = Student.create_student("omar", "omar@example.com", "p")
        c = Student.create_student("leon", "leon@example.com", "p")
        activity_a = ActivityHistory(student_id=a.student_id)
        activity_b = ActivityHistory(student_id=b.student_id)
        activity_c = ActivityHistory(student_id=c.student_id)
        db.session.add_all([activity_a, activity_b, activity_c])
        db.session.flush()
        lh_a = LoggedHoursHistory(student_id=a.student_id, staff_id=1, service="volunteer", hours=10.0, before=0.0, after=10.0, date_completed=datetime.now(timezone.utc))
        lh_a.activity_id = activity_a.id
        lh_b = LoggedHoursHistory(student_id=b.student_id, staff_id=1, service="volunteer", hours=5.0, before=0.0, after=5.0, date_completed=datetime.now(timezone.utc))
        lh_b.activity_id = activity_b.id
        lh_c = LoggedHoursHistory(student_id=c.student_id, staff_id=1, service="volunteer", hours=1.0, before=0.0, after=1.0, date_completed=datetime.now(timezone.utc))
        lh_c.activity_id = activity_c.id
        db.session.add_all([lh_a, lh_b, lh_c])
        db.session.commit()

        leaderboard = generate_leaderboard()
        # leaderboard should be ordered desc by hours for the students we created
        names = [item['name'] for item in leaderboard]
        # ensure our students are present
        assert 'zara' in names and 'omar' in names and 'leon' in names
        # assert relative ordering: zara (10) > omar (5) > leon (1)
        assert names.index('zara') < names.index('omar') < names.index('leon')
