
from App.models.commands.command import Command
from App.models.user import User
import copy

class Controller:
    def __init__(self, user: User = None, cmd: Command = None):
        self.user = user
        self.cmd = cmd
        self.history = []  # List of Command objects

    def setCommand(self, cmd: Command):
        self.cmd = cmd

    def setUser(self, user: User):
        self.user = user

    def executeButton(self):
        if not self.cmd:
            raise ValueError("No command set for execution")
        result = self.cmd.execute()
        self.history.append(copy.copy(self.cmd))  # store a copy
        return result

    def get_history(self):
        return self.history