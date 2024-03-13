from flask import render_template, flash, jsonify, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
#from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ToDoForm
from app.models import User, ToDo


@app.route('/')
@app.route('/index')
#@login_required
def index():
    if "User" in session :
        user = User.query.filter_by(user_id = session["User"]).first()
        todo = ToDo.query.filter_by(user_id = session["User"])
        return render_template('index.html', title='Home', todo=todo, user=user.username)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.password_hash == form.password.data:
            flash('Ungültiger Benutzername oder Passwort')
            return redirect(url_for('login'))
        session["User"] = user.user_id
        return redirect(url_for('index'))
        #login_user(user, remember=form.remember_me.data)
        #next_page = request.args.get('next')
        #if not next_page or url_parse(next_page).netloc != '':
            #next_page = url_for('index')
        #return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    session.pop("User", None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Herzlichen Glückwunsch {user.username}, Sie sind jetzt ein registrierter Benutzer!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/neuesToDo', methods=['GET', 'POST'])
def neuesToDo():
    form = ToDoForm()
    if "User" in session :
        user = User.query.filter_by(user_id = session["User"]).first()
        if form.validate_on_submit():
            todo = ToDo(titel=form.titel.data, description=form.description.data, status=form.status.data, todountil=form.todountil.data, user_id=session["User"])
            db.session.add(todo)
            db.session.commit()
            flash(f'Gratuliere {user.username}, Sie haben eine nue Aufgabe erstellt!')
            return redirect(url_for('login'))
        #form = ToDoForm()
        return render_template('neues_to_do.html', form=form, user=user.username)
    return redirect(url_for('login'))

@app.route('/todoSchliessen/<id>')
def todoSchliessen(id):
    if "User" in session :
        todo = ToDo.query.filter_by(ToDo_id = id).first()
        todo.status = "Erledigt"
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/todoProgress/<id>')
def todoProgress(id):
    if "User" in session :
        todo = ToDo.query.filter_by(ToDo_id = id).first()
        todo.status = "In Arbeit"
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/todoLoeschen/<id>')
def todoLoeschen(id):
    if "User" in session :
        todo = ToDo.query.filter_by(ToDo_id = id).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/api/getToDo/<userid>')
def api_getToDo(userid):
    todo = ToDo.query.filter_by(user_id = userid)
    return jsonify([s.toDict() for s in todo])

@app.route('/api/getallusers')
def api_getallusers():
    user = User.query.all()
    return jsonify([s.toDict() for s in user])