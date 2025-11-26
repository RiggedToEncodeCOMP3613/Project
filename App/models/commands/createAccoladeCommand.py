from .command import Command
from ..staff import Staff
from ..accolade import Accolade


class CreateAccoladeCommand(Command):

    def __init__(self, staff: Staff):
        self.staff = staff
        self.log: Accolade = None

    #def execute(self, description: str):
    def execute(self):
        if not self.staff:
            raise ValueError("Staff member not set for CreateAccoladeCommand")
        #if not self.description:
        #    raise ValueError("Description required to create accolade")
        
        description = input("Please enter a description for the accolade: ")

        self.log = self.staff.create_accolade(description)
        print("Accolade created with description:", description)
        return self.log

    def get_log(self) -> Accolade:
        if not self.log:
            raise ValueError("No accolade has been created yet")
        return self.log
