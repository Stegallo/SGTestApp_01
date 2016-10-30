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

    def __repr__(self):
        return '<User %r>' % (self.nickname)
