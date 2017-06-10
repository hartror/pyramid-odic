import mock
import pytest

from pyramid_oidc.configuration import (
    client_from_settings,
    validate_config)
from pyramid_oidc.exceptions import MissingConfigurationException


SETTINGS = {
    'oidc.client_id': 'unit_test',
    'oidc.client_secret': 'deadbeef-dead-beef-dead-beefdeadbeef',
    'oidc.provider_config_url': 'http://example.org/'}


@pytest.fixture
def mock_client_cls(monkeypatch):
    client_cls = mock.Mock(spec=[])
    client_cls.return_value = mock.Mock(spec=['client_secret', 'provider_config'])
    monkeypatch.setattr('pyramid_oidc.configuration.Client', client_cls)
    return client_cls


def test_client_from_settings(mock_client_cls):
    client = client_from_settings(SETTINGS)

    assert client == mock_client_cls.return_value


def test_dead_provider(mock_client_cls):
    exc = Exception('Tis but a scratch')
    mock_client_cls.return_value.provider_config.side_effect = exc

    with pytest.raises(Exception) as excinfo:
        client = client_from_settings(SETTINGS)

    assert excinfo.value == exc



def test_valid_config():
    validate_config(SETTINGS)


def test_invalid_config():
    with pytest.raises(MissingConfigurationException):
        validate_config({})
