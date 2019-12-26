'''
__init__.py -> Server Definierung

Attributes:
    bcrypt Modul für Verschlüsselung
    db: Datenbank Objeckt
    logger: Logger 
    login_manager: Modul für Login
    server: Server Objekt
'''


from flask import Flask

from flask_login import LoginManager
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy

from core.packages.logger import init_logger

logger = init_logger()

server = Flask(__name__)
server.config.from_pyfile('config.py')

db = SQLAlchemy(server)

bcrypt = Bcrypt(server)

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'main.login'

from core.main.views import main

server.register_blueprint(main)


logger.debug('Starting server')
