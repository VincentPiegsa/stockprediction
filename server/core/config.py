'''
config.py -> Konfiguration des Servers

Attributes:
    SECRET_KEY (str): Secret Key für Formulare
    SQLALCHEMY_DATABASE_URI (str): Datenbank Speicheraddresse
'''

from secrets import token_hex

SECRET_KEY = token_hex(32)
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

