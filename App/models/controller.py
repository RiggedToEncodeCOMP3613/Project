from app.database import db
from datetime import datetime
from app.models.command import Command

class Controller(db.Model):
    #The user takes an existing user from the database
    user = db.Column(db.String(50), db.ForeignKey('user.username'), primary_key=True)
    cmd = db.Column(db.String(200), db.ForeignKey('command.cmd'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)
    
    def set_command(self, C: Command):
        # store the command identifier string for the foreign key
        self.cmd = C.cmd
    def set_user(self, U):
        # store the user identifier string for the foreign key
        self.user = U.username
    def execute_command(self):
        # retrieve the command object from the database using the cmd identifier
        command = Command.query.filter_by(cmd=self.cmd).first()
        if command:
            return command.execute()
        else:
            raise ValueError("Command not found in database")
        
    def __repr__(self):
        return f"<Controller User: {self.user}, Command: {self.cmd}, Timestamp: {self.timestamp}>"