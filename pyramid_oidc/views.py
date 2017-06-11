import logging

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.response import Response
from pyramid.view import view_config


log = logging.getLogger(__name__)


@view_config(name='oidc_authn', permission=NO_PERMISSION_REQUIRED)
def oidc_authn(request):
    """
    Accepts OIDC authentication response, obtains a access token and finally
    authenticates the user.

    This is configured as the OIDC client redirect_uri.
    """
    missing_qp = [
        q
        for q in ('state', 'nonce')
        if q not in request.GET]
    if missing_qp:
        msg = (
            "Query params {} missing from request."
            .format(', '.join(missing_qp)))
        log.warn(msg)
        return HTTPBadRequest(detail=msg)
