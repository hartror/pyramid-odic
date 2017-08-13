from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.httpexceptions import HTTPForbidden, HTTPFound
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory
from pyramid.security import Allow, Authenticated, Everyone, NO_PERMISSION_REQUIRED, forget


COOKIE_SECRET = '494e9b40dc6a9350b877d1e1788a9f37'


def session_authn_callback(userid, request):
    return userid, Authenticated


class Protected(object):

    __acl__ = [
        (Allow, Authenticated, 'view')
    ]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    """
    Setup a Pyramid WSGI application
    """
    config = Configurator(
        settings=dict(global_config.items() + settings.items()),
    )

    # Insecure session factory
    config.set_session_factory(SignedCookieSessionFactory(COOKIE_SECRET))

    config.set_authentication_policy(SessionAuthenticationPolicy(
        callback=session_authn_callback))
    config.set_authorization_policy(ACLAuthorizationPolicy())

    config.add_route('index', '/')
    config.add_route('logout', '/logout')
    config.add_route('private', '/private', factory=Protected)
    config.add_view(index, route_name='index', permission=NO_PERMISSION_REQUIRED)
    config.add_view(logout, route_name='logout', permission=NO_PERMISSION_REQUIRED)
    config.add_view(private, route_name='private', permission='view')

    config.add_forbidden_view(forbidden)

    return config.make_wsgi_app()


def index(request):
    return Response('<a href="/private">Private</a>')


def private(request):
    return Response('Hello')

def logout(request):
    forget(request)
    return HTTPFound('/')


def forbidden(request):
    if request.authenticated_userid:
        return Response('forbidden')
    else:
        return HTTPFound(location=request.route_url('oidc_authn'))
