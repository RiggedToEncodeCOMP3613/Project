from App.models import User
from App.database import db

def create_user(username, password, email):
    newuser = User(username=username, password=password, email=email)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None


def get_all_requests_json():
    from App.models.requestHistory import RequestHistory
    
    requests = RequestHistory.query.all()
    if not requests:
        return []
    requests = [req.get_json() for req in requests]
    return requests

def get_all_logged_hours_json():
    from App.models.loggedHoursHistory import LoggedHoursHistory
    
    logs = LoggedHoursHistory.query.all()
    if not logs:
        return []
    logs = [log.get_json() for log in logs]
    return logs
