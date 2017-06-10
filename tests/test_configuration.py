import mock
import pytest

from pyramid_oidc.configuration import (
    client_from_settings,
    validate_config)
from pyramid_oidc.exceptions import MissingConfigurationException


@pytest.fixture
def mock_client_cls(monkeypatch):
    client_cls = mock.Mock(spec=[])
    client_cls.return_value = mock.Mock(spec=['client_secret', 'provider_config'])
    monkeypatch.setattr('pyramid_oidc.configuration.Client', client_cls)
    return client_cls


def test_client_from_settings(mock_client_cls):
    settings = {
        'oidc.client_id': 'unit_test',
        'oidc.client_secret': 'deadbeef-dead-beef-dead-deadbeefdead',
        'oidc.provider_config_url': 'http://example.org/'}

    client = client_from_settings(settings)

    assert client == mock_client_cls.return_value


def test_valid_config():
    settings = {
        'oidc.client_id': '',
        'oidc.client_secret': '',
        'oidc.provider_config_url': ''}

    validate_config(settings)


def test_invalid_config():
    with pytest.raises(MissingConfigurationException):
        validate_config({})
