from App.database import db
from App.models import User,Staff,Student,RequestHistory
from datetime import datetime, timezone

def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)