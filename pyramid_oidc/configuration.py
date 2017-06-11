import logging

from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD

from pyramid_oidc.exceptions import MissingConfigurationException


log = logging.getLogger(__name__)


def client_from_settings(settings):
    """
    Return a oic client from a configuration dictionary.
    """
    validate_config(settings)

    client_id = settings['oidc.client_id']
    client_secret = settings['oidc.client_secret']
    provider_config_url = settings['oidc.provider_config_url']

    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    client.store_registration_info(
        {'client_id': client_id,
        'client_secret': client_secret})

    try:
        client.provider_config(provider_config_url)
    except Exception as exc:
        log.error(
            "Unable to load config from the provider at '{}'"
            .format(provider_config_url))
        raise

    return client


def validate_config(settings):
    missing_options = [
        option
        for option in ('oidc.provider_config_url', 'oidc.client_id', 'oidc.client_secret')
        if option not in settings]
    if missing_options:
        raise MissingConfigurationException(missing_options)
