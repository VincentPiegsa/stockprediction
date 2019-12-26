'''
models.py -> Datenbank Objekte 
'''

from flask_login import UserMixin
from core import db, login_manager  

@login_manager.user_loader
def load_user(user_id):
    """Gibt Benutzer mit ID aus
    
    Args:
        user_id (int): Benutzer-ID
    
    Returns:
        User: Benutzer
    """
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    """Benutzer
    
    Attributes:
        id (db.Column): automatisch generierte ID
        password (db.Column): verschlüsseltes Password
        status (db.Column): Status
        username (db.Column): Benutzername
    """
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    status = db.Column(db.String(20), default='standard')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        """Ausgeben des Benutzers
        
        Returns:
            str: Benutzerdaten
        """
        return '<User|{}> #{}: {}'.format(self.status, self.id, self.username)
