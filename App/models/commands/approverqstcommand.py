from .command import Command
from ..staff import Staff

class ApproveRqstCommand(Command):
    def __init__(self, staff: Staff, request):
        self.staff = staff
        self.request = request

    def execute(self):
        from ..loggedhours import LoggedHours
        import datetime
        # Create a new LoggedHours object
        logged_hours = LoggedHours(
            student_id=self.request.student_id,
            staff_id=self.staff.id,
            hours=self.request.hours,
            status="approved",
            timestamp=datetime.datetime.now()
        )
        # Optionally update request status
        self.request.status = "approved"
        # Add to staff's loggedhours (if applicable)
        if hasattr(self.staff, 'loggedhours'):
            self.staff.loggedhours.append(logged_hours)
        return logged_hours