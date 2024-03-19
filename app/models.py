from datetime import datetime
from app import db, login
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

# Definiert eine Datenbanktabelle für Benutzer mit Benutzer-ID, Benutzername, E-Mail und Passwort
class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True) # Eindeutige Benutzer-ID
    username = db.Column(db.String(50), index=True, unique=True) # Eindeutiger Benutzername
    email = db.Column(db.String(120), index=True, unique=True) # Eindeutige E-Mail-Adresse
    password_hash = db.Column(db.String(128)) # Passwort

    #Gibt die Attribute des Benutzerobjekts
    def toDict(self):
       return dict(user_id = self.user_id, username = self.username, email = self.email)
    
    #Gibt den Benutzernamen zurück
    def __repr__(self):
        return '<User {}>'.format(self.username)

     #Gibt die Benutzer-ID zurück
    def get_id(self):
        return (self.user_id)


#Definiert eine Datenbanktabelle für To-Do-Einträge, die einen Titel, eine Beschreibung, einen Status, ein Fälligkeitsdatum und die ID des zugehörigen Benutzers speichert.
class ToDo(db.Model):
    ToDo_id = db.Column(db.Integer, primary_key=True) # Eindeutige To-Do-ID
    titel = db.Column(db.String(100)) # Titel des To-Do
    description = db.Column(db.String(1000)) # Beschreibung des To-Do
    status = db.Column(db.String(15)) # Status des To-Do
    todountil = db.Column(db.Date, index=True) # Fälligkeitsdatum des To-Do
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id')) # Verknüpfung mit Benutzer-ID

    #Gibt eine kurze Beschreibung des To-Do-Eintrags zurück, die nur den Titel enthält.
    def __repr__(self):
        return '<ToDo {}>'.format(self.titel)
    #Gibt To-Do-ID, den Titel, die Beschreibung, den Status und das Fälligkeitsdatum des To-Do-Eintrags zurück
    def toDict(self):
       return dict(ToDo_id = self.ToDo_id, titel = self.titel, description = self.description, status=self.status, todountil=self.todountil)
