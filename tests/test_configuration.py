import mock
import pytest

from pyramid_oidc.configuration import (
    oidc_client,
    validate_config)
from pyramid_oidc.exceptions import MissingConfigurationException


SETTINGS = {
    'oidc.client_id': 'unit_test',
    'oidc.client_secret': 'deadbeef-dead-beef-dead-beefdeadbeef',
    'oidc.provider_config_url': 'http://example.org/'}


@pytest.fixture
def mock_request():
    request = mock.Mock(spec=['registry', 'route_url'])
    request.registry.settings = SETTINGS
    return request


@pytest.fixture
def mock_client_cls(monkeypatch):
    client_cls = mock.Mock(spec=[])
    client_cls.return_value = mock.Mock(spec=['store_registration_info', 'provider_config'])
    monkeypatch.setattr('pyramid_oidc.configuration.Client', client_cls)
    return client_cls


def test_oidc_client(mock_request, mock_client_cls):
    client = oidc_client(mock_request)

    assert client == mock_client_cls.return_value


def test_dead_provider(mock_request, mock_client_cls):
    exc = Exception('Tis but a scratch')
    mock_client_cls.return_value.provider_config.side_effect = exc

    with pytest.raises(Exception) as excinfo:
        client = oidc_client(mock_request)

    assert excinfo.value == exc


def test_valid_config():
    validate_config(SETTINGS)


def test_invalid_config():
    with pytest.raises(MissingConfigurationException):
        validate_config({})
