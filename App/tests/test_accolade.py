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


def test_search_accolades_multiple_criteria():
    from App.models import Accolade
    from sqlalchemy import inspect
    from App.controllers.accolade_controller import search_accolades
  
    staff1 = register_staff("SearchStaff1", "search1@test.com", "pw")
    staff2 = register_staff("SearchStaff2", "search2@test.com", "pw")
    student1 = register_student("SearchStudent1", "searcher1@test.com", "pw")
    student2 = register_student("SearchStudent2", "searcher2@test.com", "pw")

    # Create accolades for each staff
    acc1 = create_accolade(staff1.staff_id, "Excellence Award S1")
    acc1_obj = acc1[0] if isinstance(acc1, tuple) else acc1
    try:
        ident = inspect(acc1_obj).identity
        acc1_id = ident[0] if ident else acc1_obj.id
    except Exception:
        acc1_id = acc1_obj.id if acc1_obj else None
    assert acc1_id is not None

    acc2 = create_accolade(staff1.staff_id, "Leadership Award")
    acc2_obj = acc2[0] if isinstance(acc2, tuple) else acc2
    try:
        ident = inspect(acc2_obj).identity
        acc2_id = ident[0] if ident else acc2_obj.id
    except Exception:
        acc2_id = acc2_obj.id if acc2_obj else None
    assert acc2_id is not None

    acc3 = create_accolade(staff2.staff_id, "Excellence Award S2")
    acc3_obj = acc3[0] if isinstance(acc3, tuple) else acc3
    try:
        ident = inspect(acc3_obj).identity
        acc3_id = ident[0] if ident else acc3_obj.id
    except Exception:
        acc3_id = acc3_obj.id if acc3_obj else None
    assert acc3_id is not None

    assign_accolade_to_student(acc1_id, student1.student_id, staff1.staff_id)
    assign_accolade_to_student(acc2_id, student1.student_id, staff1.staff_id)
    assign_accolade_to_student(acc3_id, student2.student_id, staff2.staff_id)

    # Test search by staff_id
    if search_accolades:
        results = search_accolades(staff_id=staff1.staff_id)
        results, err = (results, None) if isinstance(results, list) else results
        assert results is not None
        assert len(results) >= 2
        assert any(a.id == acc1_id for a in results)
        assert any(a.id == acc2_id for a in results)
    else:
        results = Accolade.query.filter_by(staff_id=staff1.staff_id).all()
        assert len(results) >= 2

    # Test search by description
    if search_accolades:
        results = search_accolades(description="Excellence")
        results, err = (results, None) if isinstance(results, list) else results
        assert results is not None
        assert len(results) >= 2
        assert any(a.id == acc1_id for a in results)
        assert any(a.id == acc3_id for a in results)
    else:
        results = Accolade.query.filter(Accolade.description.ilike("%Excellence%")).all()
        assert len(results) >= 2

    # Test search by accolade_id
    if search_accolades:
        results = search_accolades(accolade_id=acc1_id)
        results, err = (results, None) if isinstance(results, list) else results
        assert results is not None
        assert len(results) == 1
        assert results[0].id == acc1_id
    else:
        results = Accolade.query.filter_by(id=acc1_id).all()
        assert len(results) == 1

    # Test search by student_id (joins on student_accolade table)
    if search_accolades:
        results = search_accolades(student_id=student1.student_id)
        results, err = (results, None) if isinstance(results, list) else results
        assert results is not None
        assert len(results) >= 2
        assert any(a.id == acc1_id for a in results)
        assert any(a.id == acc2_id for a in results)
    else:
        results = Accolade.query.join(Accolade.students).filter(Accolade.students.any(id=student1.student_id)).all()
        assert len(results) >= 2
