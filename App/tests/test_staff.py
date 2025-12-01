import pytest
from App.main import create_app
from App.database import db
from App.controllers.staff_controller import register_staff, update_staff, delete_staff
from App.models import Staff

@pytest.fixture(autouse=True)
def app_context():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_register_staff():
    staff = register_staff("Dr. Smith", "smith@email.com", "pass123")
    assert staff.username == "Dr. Smith"
    assert staff.staff_id is not None
    assert str(staff.staff_id).startswith("3000")

def test_update_staff_username():
    staff = register_staff("Dr. Who", "who@email.com", "tardis")
    updated = update_staff(staff.staff_id, username="New Name")
    assert updated is not None
    assert updated.username == "New Name"

def test_update_staff_email():
    staff = register_staff("Dr. House", "house@hospital.com", "vicodin")
    updated = update_staff(staff.staff_id, email="house.new@hospital.com")
    assert updated is not None
    assert updated.email == "house.new@hospital.com"

def test_update_staff_password():
    staff = register_staff("Dr. Banner", "banner@avengers.com", "gamma")
    updated = update_staff(staff.staff_id, password="newpass")
    assert updated is not None
    assert updated.check_password("newpass") is True
    assert updated.check_password("gamma") is False

def test_delete_staff():
    staff = register_staff("Dr. Palmer", "palmer@hospital.com", "healing")
    result = delete_staff(staff.staff_id)
    assert result is True
    db_staff = Staff.query.filter_by(staff_id=staff.staff_id).first()
    assert db_staff is None
