from functools import wraps
import logging

from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from pyramid.security import NO_PERMISSION_REQUIRED, remember
from pyramid.response import Response
from pyramid.view import view_config

from .configuration import (
    CONFIG_CLIENT_ID,
    CONFIG_CLIENT_SECRET,
    CONFIG_OP_AUTHZ_URI,
    CONFIG_OP_PUBLIC_KEY,
    CONFIG_OP_TOKEN_URI,
    CONFIG_OP_USERINFO_URI)
from .oidc import OidcSession


log = logging.getLogger(__name__)


@view_config(route_name='oidc_authn', permission=NO_PERMISSION_REQUIRED)
def oidc_authn(request):
    settings = request.registry.settings
    client_id = settings[CONFIG_CLIENT_ID]
    op_authz_uri = settings[CONFIG_OP_AUTHZ_URI]

    oidc = OidcSession(
        client_id=client_id,
        redirect_uri=request.route_url('oidc_callback'),
        scope=['openid'])
    url, state, nonce = oidc.authorization_url(op_authz_uri)

    request.session['oidc_state'] = state
    request.session['oidc_nonce'] = nonce

    return HTTPFound(url)


@view_config(route_name='oidc_callback', permission=NO_PERMISSION_REQUIRED)
def oidc_callback(request):
    """
    Accepts OIDC authentication response, obtains a access token and finally
    authenticates the user.

    This is configured as the OIDC client redirect_uri.
    """
    settings = request.registry.settings
    client_id = settings[CONFIG_CLIENT_ID]
    client_secret = settings[CONFIG_CLIENT_SECRET]
    op_public_key = settings[CONFIG_OP_PUBLIC_KEY]
    op_token_uri = settings[CONFIG_OP_TOKEN_URI]
    op_userinfo_uri = settings[CONFIG_OP_USERINFO_URI]

    try:
        state = request.GET.getone('state')
        code = request.GET.getone('code')
    except KeyError as exc:
        msg = (
            "Bad or missing query params {} in request."
            .format(request.GET))
        log.warn(msg)
        return HTTPBadRequest(detail=msg)

    # TODO check state against session
    # TODO check nonce exists in session
    nonce = request.session.get('oidc_nonce')

    oidc = OidcSession(
        client_id=client_id,
        public_key=op_public_key,
        state=state,
        redirect_uri=request.route_url('oidc_callback'))
    token = oidc.fetch_token(
        op_token_uri,
        nonce,
        client_secret=client_secret,
        authorization_response=request.url)

    print oidc.token

    #request.session['oidc_userinfo'] = oidc.fetch_userinfo(op_userinfo_uri)
    userinfo = oidc.fetch_userinfo(op_userinfo_uri)

    print userinfo
    remember(request, userinfo['preferred_username'])

    return Response(status_int=200)
