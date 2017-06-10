import pytest

from pyramid_oidc.configuration import validate_config
from pyramid_oidc.exceptions import MissingConfigurationException


def test_valid_config():
    settings = {
        'oidc.client_id': '',
        'oidc.client_secret': '',
        'oidc.provider_uri': ''}

    validate_config(settings)


def test_invalid_config():
    with pytest.raises(MissingConfigurationException):
        validate_config({})
