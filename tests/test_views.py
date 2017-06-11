import mock
import pytest

from pyramid_oidc.views import oidc_authn
from webob.multidict import MultiDict


@pytest.fixture
def mock_req():
    mock_req = mock.Mock(spec=['GET'])
    mock_req.GET = MultiDict({
        'state': 'foo',
        'code': 'bar'})
    return mock_req


def test_missing_query_params(mock_req):
    mock_req.GET.clear()

    resp = oidc_authn(mock_req)

    assert resp.code == 400


def test_multiple_query_params(mock_req):
    mock_req.GET.add('code', 'foo')

    resp = oidc_authn(mock_req)

    assert resp.code == 400
