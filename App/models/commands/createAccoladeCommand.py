from .command import Command
from ..staff import Staff
from ..accolade import Accolade


class CreateAccoladeCommand(Command):

    def __init__(self, staff: Staff):
        self.staff = staff
        self.log: Accolade = None

    def execute(self, description: str = None):
        if not self.staff:
            raise ValueError("Staff member not set for CreateAccoladeCommand")
        
        if description is None:
            # CLI mode
            description = input("Please enter a description for the accolade: ")

        self.log = self.staff.create_accolade(description)
        
        # Only print message in CLI mode
        if description is not None:
            # This was CLI mode (description was originally None)
            print("Accolade created with description:", description)
        
        return self.log

    def get_log(self) -> Accolade:
        if not self.log:
            raise ValueError("No accolade has been created yet")
        return self.log
