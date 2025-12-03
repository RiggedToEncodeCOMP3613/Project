from .command import Command
from ..staff import Staff
from ..requestHistory import RequestHistory
from ..loggedHoursHistory import LoggedHoursHistory

class ApproveHoursCommand(Command):
    def __init__(self, staff: Staff):
        self.staff = staff
        self.log: LoggedHoursHistory = None

    def execute(self, request_id: str = None):
        if not self.staff:
            raise ValueError("Staff member not set for ApproveHoursCommand")
        
        if request_id is None:
            # CLI mode
            pending = self.staff.get_pending_requests()
            print("Pending Requests:")
            for req in pending:
                print(req) #will use the repr method of requestHistory class
            
            request_id = input("This is a list of your pending requests. Please enter the ID of the request you wish to log hours for: ")
        
        request = RequestHistory.query.get(request_id)
        if not request:
            raise ValueError("Invalid ID. Request not found")
        
        self.log = self.staff.approve_request(request)
        if request_id is not None:  # Web mode
            return self.log
        else:  # CLI mode
            print(f'Request ID {request_id} by Student {request.student_id} has been approved.')
            return self.log

    def get_log(self) -> LoggedHoursHistory:
        if not self.log:
            raise ValueError("No request has been approved yet")
        return self.log