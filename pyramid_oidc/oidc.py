import time

import jwt
from oauthlib.common import generate_nonce
from requests_oauthlib import OAuth2Session

from . import exceptions


class OidcSession(OAuth2Session):

    def __init__(self, public_key=None, **kwargs):
        self.public_key = public_key
        super(OidcSession, self).__init__(**kwargs)

    def authorization_url(self, url, state=None, nonce=None, **kwargs):
        nonce = nonce or generate_nonce()
        url, state = super(OidcSession, self).authorization_url(
            url, state=state, nonce=nonce, **kwargs)
        return url, state, nonce

    def fetch_token(self, url, nonce, **kwargs):
        # TODO handle fetch_token failure
        token = super(OidcSession, self).fetch_token(url, **kwargs)
        raw_id_token = token['id_token']

        # TODO: handle jwt decode failure
        id_token = jwt.decode(raw_id_token, self.public_key, audience=self.client_id)

        if id_token['nonce'] != nonce:
            raise exceptions.OidcSessionBadNonce(nonce, id_token['nonce'])

        # TODO: this is always failing?
        #if id_token['exp'] > time.time():
        #    raise exceptions.OidcSessionExpiredToken(id_token['exp'])

        # TODO: use iat to invalidate old tokens
        # TODO: validate iss (will need a new config setting)

        token['id_token'] = id_token
        token['_raw_id_token'] = raw_id_token

        self.token = token

        return token

    def fetch_userinfo(self, url):
        return self.get(url).json()

    def request(self, method, url, data=None, headers=None, **kwargs):
        """Intercept all requests and add the access token"""
        if self.token:
            headers = headers or {}
            headers['Authorization'] = 'Bearer {}'.format(self.token['access_token'])
            print headers
        return super(OidcSession, self).request(
            method, url, headers=headers, data=data, **kwargs)
