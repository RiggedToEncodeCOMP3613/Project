from .command import Command
from ..staff import Staff
from ..loggedHoursHistory import LoggedHoursHistory

class LogHoursCommand(Command):
    def __init__(self, staff: Staff):
        self.staff = staff
        self.log: LoggedHoursHistory = None

    def execute(self):
        if not self.staff:
            raise ValueError("Staff member not set for LogHoursCommand")

        try:
            print("Please provide the following details in order to log hours for a student:")

            service = input("Service Description: ")
            student_id = int(input("Student ID: "))
            hours = float(input("Number of Hours: "))
            date_completed = input("Date Completed (YYYY-MM-DD): ")

            logged_hours = self.staff.log_hours(service, student_id, hours, date_completed)
            self.log = logged_hours
            print(f'Hours logged successfully for Student ID {student_id}.')
            return self.log

        except Exception:
            print("Error in the details inputted.")
            return None
    
    def get_log(self) -> LoggedHoursHistory:
        if not self.log:
            raise ValueError("No hours have been logged yet")
        return self.log