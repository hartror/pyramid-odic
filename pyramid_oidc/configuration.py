from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD

from pyramid_oidc.exceptions import MissingConfigurationException


def client_from_settings(settings):
    """
    Create a oic client from a configuration dictionary.
    """
    validate_config(config)

    client_id = settings['oidc.client_id']
    client_secret = settings['oidc.client_secret']
    provider_uri = settings['oidc.provider_config_uri']

    client = Client(client_id=client_id)
    client.client_secret = client_secret

    client.provider_config(provider_uri)

    return client


def validate_config(settings):
    missing_options = [
        option
        for option in ('oidc.provider_uri', 'oidc.client_id', 'oidc.client_secret')
        if option not in settings]
    if missing_options:
        raise MissingConfigurationException(missing_options)
