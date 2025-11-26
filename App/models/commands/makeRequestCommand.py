from .command import Command
from ..student import Student
from ..requestHistory import RequestHistory

class MakeRequestCommand(Command):
    def __init__(self, student: Student):
        self.student = student
        self.log: RequestHistory = None

    def execute(self):
        if not self.student:
            raise ValueError("Student not set for MakeRequestCommand")
        
        try:
            print("Please provide the following details in order to make a request:")

            service = input("Service Description: ")
            staff_id = int(input("Staff ID: "))
            hours = float(input("Number of Hours: "))
            date_completed = input("Date Completed (YYYY-MM-DD): ")

            request = self.student.make_request(service, staff_id, hours, date_completed)
            self.log = request
            print("Request made successfully.")
            return self.log

        except Exception:
            print("Error in the details inputted.")
            return None

    def get_log(self) -> RequestHistory:
        if not self.log:
            raise ValueError("No request has been made yet")
        return self.log