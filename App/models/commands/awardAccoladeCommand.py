from .command import Command
from ..staff import Staff
from ..accoladeHistory import AccoladeHistory


class AwardAccoladeCommand(Command):

    def __init__(self, staff: Staff):
        self.staff = staff
        self.log: AccoladeHistory = None

    def execute(self, student_id: int, accolade_id: int):
        if not self.staff:
            raise ValueError("Staff member not set for AwardAccoladeCommand")
        if not self.student_id:
            raise ValueError("Student ID required to award accolade")
        if not self.accolade_id:
            raise ValueError("Accolade ID required to award accolade")
        
        self.log = self.staff.award_accolade(student_id, accolade_id)
        return self.log

    def get_log(self) -> AccoladeHistory:
        return self.log