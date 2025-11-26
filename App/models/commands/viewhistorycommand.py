from .command import Command
from ..student import Student 
from typing import Optional, Any

class ViewHistoryCommand(Command):
    def __init__(self, student: Student):
        self.student = student
        self.log: Optional[list[Any]] = None

    def execute(self):
        if not self.student:
            raise ValueError("Student not set for ViewHistoryCommand")
        
        history = self.student.activity_history.sorted_history()

        if not history:
            raise ValueError("No activity history found.")
        
        print("Activity History:")
        for activity in history:
            print(activity) #will use the repr method of each respective history class
            
        self.log = history
        print("History viewed successfully.")
        return self.log

    def get_log(self) -> Optional[list[Any]]:
        if self.log is None:
            raise ValueError("History has not been viewed yet")
        return self.log