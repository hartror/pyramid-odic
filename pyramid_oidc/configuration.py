import logging
import os

from pyramid_oidc.exceptions import MissingConfiguration

log = logging.getLogger(__name__)


# Development mode no SSL
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


CONFIG_CLIENT_ID = 'oidc.client_id'
CONFIG_CLIENT_SECRET = 'oidc.client_secret'
CONFIG_OP_AUTHZ_URI = 'oidc.op_authz_uri'
CONFIG_OP_TOKEN_URI = 'oidc.op_token_uri'
CONFIG_OP_PUBLIC_KEY = 'oidc.op_public_key'
CONFIG_OP_USERINFO_URI = 'oidc.op_userinfo_uri'

REQUIRED_CONFIG = (
    CONFIG_CLIENT_ID,
    CONFIG_CLIENT_SECRET,
    CONFIG_OP_AUTHZ_URI,
    CONFIG_OP_PUBLIC_KEY,
    CONFIG_OP_TOKEN_URI,
    CONFIG_OP_USERINFO_URI)


def includeme(config):
    validate_config(config.registry.settings)

    config.add_route('oidc_authn', '/oidc_authn')
    config.add_route('oidc_callback', '/oidc_callback')

    config.scan('pyramid_oidc.views')


def validate_config(settings):
    missing_options = [
        option
        for option in REQUIRED_CONFIG
        if option not in settings]
    if missing_options:
        raise MissingConfiguration(missing_options)
