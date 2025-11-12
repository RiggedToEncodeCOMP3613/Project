from database import db
from datetime import datetime
from abc import ABC, abstractmethod

#This command serves as an interface for all concrete commands
class Command(ABC, db.Model):
    cmd = db.Column(db.String(200), primary_key=True)

    @abstractmethod
    def execute(self):
        pass
    
# No actual code is done in this class, it is just a template for future commands