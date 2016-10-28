
 #Flask, Response, redirect, request, url_for
from flask import session, render_template, redirect, url_for
from flask.ext.login import LoginManager, current_user, login_user, logout_user
from app import app, db, models
from app.oauth import OAuthSignIn

from .models import User

lm = LoginManager(app)
lm.login_view = 'index'

client_id='OQbN3bqMBUbNfBsl9C6oI3SLNn8uGioP'
client_secret='0kT7T8y92jyTzEriVwBXjqimc0Plh4s747mnRd_JzjQNbwE7afuvxnO0q34CILpI'

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
    print 'inizio'
    # social_id = 'facebook$10205370554636727' # local for development

    if current_user.is_authenticated:
        print 'esiste un current user'

    print 'andiamo ad index'


    return render_template('index.html')

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    print 'qui'
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    session['social_id'] = social_id
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
