from datetime import datetime
from app import db, login
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def toDict(self):
       return dict(user_id = self.user_id, username = self.username, email = self.email)
    def __repr__(self):
        return '<User {}>'.format(self.username)


    def get_id(self):
        return (self.user_id)

class ToDo(db.Model):
    ToDo_id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    status = db.Column(db.String(15))
    todountil = db.Column(db.Date, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        return '<ToDo {}>'.format(self.titel)
    
    def toDict(self):
       return dict(ToDo_id = self.ToDo_id, titel = self.titel, description = self.description, status=self.status, todountil=self.todountil)
