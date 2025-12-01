import pytest
from App.main import create_app
from App.database import db
from App.controllers.request_controller import delete_request_entry
from App.models import RequestHistory

@pytest.fixture(autouse=True)
def app_context():
    app = create_app()
    app.config.update({"TESTING": True})
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


# Unit Test
def test_delete_request_entry_unit():
    
    req = RequestHistory(
        student_id=1,
        staff_id=1,
        service="Test",
        hours=1.0,
        date_completed="2025-12-01"
    )
    req.activity_id = 1
    db.session.add(req)
    db.session.commit()
    request_id = req.id

    success, message = delete_request_entry(request_id)
    
    assert success is True
    assert "deleted successfully" in message.lower()
    
    deleted_req = RequestHistory.query.filter_by(id=request_id).first()
    assert deleted_req is None
