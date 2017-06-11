import mock

from pyramid_oidc.views import oidc_authn


def test_missing_query_params():
    mock_req = mock.Mock(spec=['GET'])
    mock_req.GET = {}

    resp = oidc_authn(mock_req)

    assert resp.code == 400
