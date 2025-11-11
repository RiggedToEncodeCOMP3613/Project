from .command import Command
from .student import Student

class RequestHrsCommand(Command):
    def __init__(self, student: Student, hours: float):
        self.student = student
        self.hours = hours

    def execute(self):
        from .request import Request
        import datetime
        # Create a new Request object
        new_request = Request(
            student_id=self.student.id,
            hours=self.hours,
            status="pending",
            timestamp=datetime.datetime.now()
        )
        # Add to student's requests (if applicable)
        if hasattr(self.student, 'requests'):
            self.student.requests.append(new_request)
        return new_request