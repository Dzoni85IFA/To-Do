from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

#Definiert ein Anmeldeformular mit Feldern für Benutzername, Passwort und "Remember Me"
class LoginForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Anmeldung')

# Definiert ein Registrierungsformular mit Feldern für Benutzername, E-Mail, Passwort und Passwortbestätigung
class RegistrationForm(FlaskForm):
    username = StringField('Benutzername', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    password2 = PasswordField(
        'Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrieren')
    
    # Überprüft, ob der Benutzername bereits verwendet wird
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Bitte verwenden Sie einen anderen Benutzernamen!')
    
    # Überprüft, ob die E-Mail-Adresse bereits verwendet wird
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Bitte verwenden Sie eine andere E-Mail Adresse!')

# Definiert ein Formular für das Erstellen eines To-Do-Eintrags mit Titel, Beschreibung, Status und Fälligkeitsdatum Feldern
class ToDoForm(FlaskForm):
    titel = StringField('Titel', validators=[DataRequired()])
    description = TextAreaField('Beschreibung', validators=[DataRequired()])
    status_choices = [('Neu'), ('In Arbeit')]
    status = SelectField('Status', choices=status_choices, validators=[DataRequired()])
    todountil = DateField('Fälligkeitsdatum', validators=[DataRequired()])
    submit = SubmitField('Speichern')
