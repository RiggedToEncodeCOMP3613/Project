from .command import Command
from ..staff import Staff
from ..accolade import Accolade


class CreateAccoladeCommand(Command):

    def __init__(self, staff: Staff, description: str):
        self.staff = staff
        self.description = description
        self.log = None  # Will hold the created Accolade after execute()

    def execute(self):
        if not self.staff:
            raise ValueError("Staff member not set for CreateAccoladeCommand")
        if not self.description:
            raise ValueError("Description required to create accolade")
        
        self.log = self.staff.create_accolade(self.description)
        return self.log

    def get_log(self):
        if self.log:
            return f"create_accolade: staff={self.staff.staff_id} accolade_id={self.log.id} description='{self.log.description}'"
        return f"create_accolade: staff={self.staff.staff_id} description='{self.description}' (not yet executed)"
