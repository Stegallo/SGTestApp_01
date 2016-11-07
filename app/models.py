from app import db
# from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, current_user
from flask.ext.login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    notes = db.Column(db.String(64), nullable=True)
    movestoken = db.Column(db.String(256), nullable=True)
    stravatoken = db.Column(db.String(256), nullable=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.id'))
    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Athlete(db.Model):
    __tablename__ = 'athletes'
    id = db.Column(db.Integer, primary_key=True)
    stravatoken = db.Column(db.String(256), nullable=True)
    firstname = db.Column(db.String(256), nullable=True)
    lastname = db.Column(db.String(256), nullable=True)
    users = db.relationship('User', backref='athlete', lazy='dynamic')

    def __repr__(self):
        return '<Athlete %r>' % (self.id)
