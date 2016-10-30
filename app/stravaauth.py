# from rauth import OAuth1Service, OAuth2Service
from flask import current_app, url_for, request, redirect, session
from stravalib.client import Client


class StravaAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['STRAVAAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_return',
                       _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class StrvaSignIn(StravaAuthSignIn):
    def __init__(self):
        super(StrvaSignIn, self).__init__('Strava')
        self.StravaClient = Client()


    def authorize(self):
        return redirect(self.StravaClient.authorization_url(
            client_id=self.consumer_id,
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:
            return None
        access_token = self.StravaClient.exchange_code_for_token(
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            code=request.args['code']
        )
        self.StravaClient.access_token = access_token
        return self.StravaClient.get_athlete()
