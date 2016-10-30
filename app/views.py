from flask import session, render_template, redirect, url_for, request
from flask.ext.login import LoginManager, current_user, login_user, logout_user
from app import app, db, models
from app.oauth import OAuthSignIn
from app.stravaauth import StravaAuthSignIn
from stravalib.client import Client

from .models import User

lm = LoginManager(app)
lm.login_view = 'index'

StravaClient = Client()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
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

@app.route('/auth')
def auth():
    stravaauth = StravaAuthSignIn.get_provider('Strava')
    return stravaauth.authorize()

@app.route("/oauth_return")
def oauth_return():
    stravaauth = StravaAuthSignIn.get_provider('Strava')
    athlete = stravaauth.callback()
    # code = request.args.get("code")
    # print code
    # access_token = StravaClient.exchange_code_for_token(client_id=6572, client_secret='e5cfacb508546897eb2eab193a29698db29b15df', code=code)
    # print access_token
    # # session['access_token'] = access_token
    # # print 'fin qui va bene'
    #
    # social_id = 'facebook$10205370554636727'
    # # print social_id
    # user = User.query.filter_by(social_id=social_id).first()
    # print user
    # user.stravatoken = access_token
    # db.session.commit()
    # StravaClient.access_token = access_token
    # athlete = StravaClient.get_athlete()
    return "{id} {lastname}".format(id=athlete.firstname, lastname=athlete.lastname)
