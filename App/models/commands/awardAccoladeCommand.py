from .command import Command
from .createAccoladeCommand import CreateAccoladeCommand
from ..staff import Staff
from ..accoladeHistory import AccoladeHistory


class AwardAccoladeCommand(Command):

    def __init__(self, staff: Staff):
        self.staff = staff
        self.log: AccoladeHistory = None

    #def execute(self, student_id: int, accolade_id: int):
    def execute(self):
        if not self.staff:
            raise ValueError("Staff member not set for AwardAccoladeCommand")
        #if not self.student_id:
            #raise ValueError("Student ID required to award accolade")
        #if not self.accolade_id:
            #raise ValueError("Accolade ID required to award accolade")

        student_id = input("Please enter the ID of the student: ")

        flag = input("Is the accolade created? (y/n): ")
        if flag.lower() != 'y' and flag.lower() != 'n':
            raise ValueError("Invalid input. Please enter 'y' or 'n'.")
        elif flag.lower() == 'y':
            accolade_id = input("Please enter the ID of the accolade to award: ")
            self.log = self.staff.award_accolade(student_id, accolade_id)
        elif flag.lower() == 'n':
            print("You need to create an accolade first.")
            cmd = CreateAccoladeCommand(self.staff)
            accolade = cmd.execute()
            self.log = self.staff.award_accolade(student_id, accolade.id)

        print("Accolade awarded to student ID:", student_id)
        return self.log
        
        

    def get_log(self) -> AccoladeHistory:
        if not self.log:
            raise ValueError("No accolade has been awarded yet")
        return self.log