"""
forms.py -> Online-Formulare
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import datetime


class LoginForm(FlaskForm):

    """Login-Formular
    
    Attributes:
        password (StringField): Password-Feld
        submit (PasswordField): Submit-Feld
        username (SubmitField): Eingabe-Feld
    """
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class StockSelect(FlaskForm):

    """Formular zum Auswählen von Aktien
    
    Attributes:
        stock (StringField): Eingabe-Feld
        submit (SubmitField): Submit-Feld
    """
    
    stock = StringField('Ticker', validators=[DataRequired()])
    submit = SubmitField('Submit')
