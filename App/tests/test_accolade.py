from App.main import create_app
from App.database import db
import pytest

from App.controllers.staff_controller import register_staff
from App.controllers.student_controller import register_student
try:
    from App.controllers.accolade_controller import create_accolade, assign_accolade_to_student, delete_accolade
except Exception:
    create_accolade = None
    assign_accolade_to_student = None
    delete_accolade = None

@pytest.fixture(autouse=True)
def app_context():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


def test_delete_accolade_with_history():
    from App.models import Accolade, AccoladeHistory, ActivityHistory
    from sqlalchemy import inspect
    from datetime import datetime, timezone

    staff = register_staff("DelStaff", "del.staff@test.com", "pw")
    student = register_student("DelStudent", "del.student@test.com", "pw")

    
    raw = create_accolade(staff.staff_id, "Temporary Honor")
    accolade_obj = raw[0] if isinstance(raw, tuple) else raw
   
    try:
        ident = inspect(accolade_obj).identity
        accolade_id = ident[0] if ident else getattr(accolade_obj, 'id', None)
    except Exception:
        accolade_id = getattr(accolade_obj, 'id', None)

    assert accolade_id is not None

    assign_accolade_to_student(accolade_id, student.student_id, staff.staff_id)
    hist_record = AccoladeHistory.query.filter_by(student_id=student.student_id, accolade_id=accolade_id).first()
    assert hist_record is not None

    act = ActivityHistory.query.filter_by(student_id=student.student_id).first()
    assert act is not None

    delete_accolade(accolade_id, delete_history=True)
    
    assert Accolade.query.get(accolade_id) is None
    assert AccoladeHistory.query.filter_by(accolade_id=accolade_id).first() is None
    assert ActivityHistory.query.filter_by(student_id=student.student_id).first() is None


def test_remove_student_from_accolade():
    from App.models import Accolade, AccoladeHistory
    from sqlalchemy import inspect
    from App.controllers.accolade_controller import remove_accolade_from_student
    

    staff = register_staff("RemStaff", "rem.staff@test.com", "pw")
    student = register_student("RemStudent", "rem.student@test.com", "pw")
    raw = create_accolade(staff.staff_id, "Transient Award")
    accolade_obj = raw[0] if isinstance(raw, tuple) else raw
    ident = inspect(accolade_obj).identity
    accolade_id = ident[0] if ident else getattr(accolade_obj, 'id', None)
    assert accolade_id is not None

    assign_accolade_to_student(accolade_id, student.student_id, staff.staff_id)
   
    # Reload accolade and verify relationship exists
    accolade = Accolade.query.get(accolade_id)
    db.session.refresh(accolade)
    assert any(s.student_id == student.student_id for s in accolade.students) or AccoladeHistory.query.filter_by(student_id=student.student_id, accolade_id=accolade_id).first() is not None

    remove_accolade_from_student(accolade_id, student.student_id, delete_history=True)
    
    # Verify student is removed from accolade
    accolade_after = Accolade.query.get(accolade_id)
    db.session.refresh(accolade_after)
    assert not any(s.student_id == student.student_id for s in accolade_after.students)
    assert AccoladeHistory.query.filter_by(student_id=student.student_id, accolade_id=accolade_id).first() is None
