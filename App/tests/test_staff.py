import pytest
from App.main import create_app
from App.database import db
from App.controllers.staff_controller import register_staff
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