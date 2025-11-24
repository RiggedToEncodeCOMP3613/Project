from .command import Command
from ..staff import Staff
from ..accolade import Accolade


class CreateAccoladeCommand(Command):

    def __init__(self, staff: Staff):
        self.staff = staff
        self.log: Accolade = None

    def execute(self, description: str):
        if not self.staff:
            raise ValueError("Staff member not set for CreateAccoladeCommand")
        if not self.description:
            raise ValueError("Description required to create accolade")
        
        self.log = self.staff.create_accolade(description)
        return self.log

    def get_log(self) -> Accolade:
        return self.log
