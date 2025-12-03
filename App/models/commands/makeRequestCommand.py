from .command import Command
from ..student import Student
from ..requestHistory import RequestHistory

class MakeRequestCommand(Command):
    def __init__(self, student: Student):
        self.student = student
        self.log: RequestHistory = None

    def execute(self, service: str = None, staff_id: int = None, hours: float = None, date_completed: str = None):
        if not self.student:
            raise ValueError("Student not set for MakeRequestCommand")
        
        try:
            # If no parameters provided, use CLI mode
            if service is None or staff_id is None or hours is None or date_completed is None:
                print("Please provide the following details in order to make a request:")
                service = input("Service Description: ")
                staff_id = int(input("Staff ID: "))
                hours = float(input("Number of Hours: "))
                date_completed = input("Date Completed (YYYY-MM-DD): ")

            request = self.student.make_request(service, staff_id, hours, date_completed)
            self.log = request
            
            # Only print success message in CLI mode
            if service is not None and staff_id is not None and hours is not None and date_completed is not None:
                # This was CLI mode (all params were originally None)
                print("Request made successfully.")
            
            return self.log

        except Exception:
            print("Error in the details inputted.")
            return None

    def get_log(self) -> RequestHistory:
        if not self.log:
            raise ValueError("No request has been made yet")
        return self.log