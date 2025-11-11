from .command import Command
from .staff import Staff

class DenyRqstCommand(Command):
    def __init__(self, staff: Staff, request):
        self.staff = staff
        self.request = request

    def execute(self):
        # Forget everything (no action needed)
        self.request.status = "denied"
        return "DENIED!"