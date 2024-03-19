from flask import render_template, flash, jsonify, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, ToDoForm
from app.models import User, ToDo


@app.route('/')
@app.route('/index')


def index():
    # Überprüft, ob ein Benutzer in der Sitzung angemeldet ist
    if "User" in session :
        # Holt den Benutzer und seine To-Do-Einträge aus der Datenbank
        user = User.query.filter_by(user_id = session["User"]).first()
        todo = ToDo.query.filter_by(user_id = session["User"])
        # Gibt die Startseite mit Benutzerinformationen und To-Do-Liste zurück
        return render_template('index.html', title='Home', todo=todo, user=user.username)
    # Leitet den Benutzer zur Login-Seite weiter, wenn nicht angemeldet
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])

def login():
    # Leitet authentifizierte Benutzer zur Startseite weiter
    if current_user.is_authenticated:
        return redirect(url_for('index')) 
    form = LoginForm() # Erstellt ein Anmeldeformular für nicht authentifizierte Benutzer
    if form.validate_on_submit():
        # Überprüft die Benutzeranmeldeinformationen
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.password_hash == form.password.data:
            flash('Ungültiger Benutzername oder Passwort')
            return redirect(url_for('login'))
        session["User"] = user.user_id
        return redirect(url_for('index')) # Authentifiziert und leitet den Benutzer zur Startseite weiter
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    session.pop("User", None) # Beendet die Benutzersitzung
    return redirect(url_for('index')) # Leitet den Benutzer zur Startseite weiter


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Leitet bereits authentifizierte Benutzer zur Startseite weiter
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm() # Erstellt ein Registrierungsformular
    if form.validate_on_submit():
        # Registriert einen neuen Benutzer
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Herzlichen Glückwunsch {user.username}, Sie sind jetzt ein registrierter Benutzer!')
        return redirect(url_for('login')) # Weiterleitung zur Anmeldeseite
    return render_template('register.html', title='Register', form=form) 

@app.route('/neuesToDo', methods=['GET', 'POST'])
def neuesToDo():
    form = ToDoForm()
    if "User" in session :
        user = User.query.filter_by(user_id = session["User"]).first()
        if form.validate_on_submit():
            # Erstellt ein neues To-Do und fügt es der Datenbank hinzu
            todo = ToDo(titel=form.titel.data, description=form.description.data, status=form.status.data, todountil=form.todountil.data, user_id=session["User"])
            db.session.add(todo)
            db.session.commit()
            flash(f'Gratuliere {user.username}, Sie haben eine neue Aufgabe erstellt!')
            return redirect(url_for('login')) # Weiterleitung zur Anmeldeseite
        return render_template('neues_to_do.html', form=form, user=user.username)
    return redirect(url_for('login'))

@app.route('/todoSchliessen/<id>')
def todoSchliessen(id):
    if "User" in session :
         # To-Do-Eintrag abschliessen und Änderungen speichern
        todo = ToDo.query.filter_by(ToDo_id = id).first()
        todo.status = "Erledigt"
        db.session.commit()
        return redirect(url_for('index')) # Weiterleitung zur Startseite
    return redirect(url_for('login')) # Weiterleitung zur Anmeldeseite

@app.route('/todoProgress/<id>')
def todoProgress(id):
    if "User" in session :
        # To-Do-Eintrag als "In Arbeit" markieren und Änderungen speichern
        todo = ToDo.query.filter_by(ToDo_id = id).first()
        todo.status = "In Arbeit"
        db.session.commit()
        return redirect(url_for('index')) # Weiterleitung zur Startseite
    return redirect(url_for('login')) # Weiterleitung zur Anmeldeseite

@app.route('/todoLoeschen/<id>')
def todoLoeschen(id):
    if "User" in session :
        # To-Do-Eintrag löschen und Änderungen speichern
        todo = ToDo.query.filter_by(ToDo_id = id).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('index')) # Weiterleitung zur Startseite
    return redirect(url_for('login')) # Weiterleitung zur Anmeldeseite



@app.route('/api/getToDo/<userid>')
def api_getToDo(userid):
    # To-Do-Einträge eines Benutzers im JSON-Format abrufen
    todo = ToDo.query.filter_by(user_id = userid)
    return jsonify([s.toDict() for s in todo])

@app.route('/api/getallusers')
def api_getallusers():
     # Alle Benutzer im JSON-Format abrufen
    user = User.query.all()
    return jsonify([s.toDict() for s in user])
