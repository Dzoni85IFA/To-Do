from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config




app = Flask(__name__) # Flask-App initialisieren
app.config.from_object(Config) # Konfiguration der App aus der Config-Klasse laden

# SQLAlchemy-Datenbankobjekt und Flask-Migrate initialisieren
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app) # Flask-Login für Benutzerauthentifizierung initialisieren
login.login_view = 'login'  # Ansicht für den Login festlegen

from app import routes, models # Routen und Modelle importieren

# Benutzer laden, der mit der übergebenen user_id verknüpft ist
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
