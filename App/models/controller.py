from app.database import db
from datetime import datetime
from app.models.command import Command
# ! Command not yet implemented this is a placeholder for future functionality

class Controller(db.Model):
    #The user takes an existing user from the database
    user = db.Column(db.String(50), db.ForeignKey('user.username'), primary_key=True)
    cmd = db.Column(db.String(200), db.ForeignKey('command.cmd'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)
    
    setCommand (Command C)