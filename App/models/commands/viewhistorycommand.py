from . import command
from ..student import Student

class ViewHistoryCommand(command.Command):
    def __init__(self, student: Student):
        self.student = student

    def execute(self):
        print(self.student.history)