from .configuration import includeme


def session_authn_callback(user_id, request):
    if user_id == request.session.get('oidc', {}).get('user_id'):
        return []
