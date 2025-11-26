from .command import Command
from ..student import Student
from ..milestoneHistory import MilestoneHistory
from typing import List, Optional

class ReachedMilestoneCommand(Command):
    def __init__(self, student: Student):
        self.student = student
        self.log: Optional[List[MilestoneHistory]] = None

    def execute(self):
        if not self.student:
            raise ValueError("Student not set for ReachedMilestoneCommand")
        
        try:
            milestones = self.student.calculate_new_milestones() 
            if not milestones:
                print("No new milestone/s reached.")
                return None
            else:
                print("New milestone/s reached:")
                for m in milestones:
                    print(m.milestone)

                self.log = milestones
                print("Milestone was reached.")
                return self.log

        except Exception:
            print("Error calculating milestones. No milestones reached.")
            return None

    def get_log(self) -> Optional[List[MilestoneHistory]]:
        if self.log is None:
            raise ValueError("No milestones have been reached yet")
        return self.log