from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.response import Response
from pyramid.view import view_config


@view_config(name='oidc_authn', permission=NO_PERMISSION_REQUIRED)
def oidc_authn(request):
    """
    Accepts OIDC authentication response, obtains a access token and finally
    authenticates the user.

    This is configured as the OIDC client redirect_uri
    """
    pass
