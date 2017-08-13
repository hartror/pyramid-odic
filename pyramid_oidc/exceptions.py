"""
Exceptions for the pyramid_oidc package.
"""

import datetime


class Base(Exception):
    pass


class Configuration(Exception):
    """Raised for an error during configuration"""

    pass


class MissingConfiguration(Exception):
    """Raised for missing configuration options during configuration"""

    def __init__(self, options):
        self._options = options

    def __str__(self):
        return (
            "Missing configuration options: {}"
            .format(', '.join(self._options)))


class OidcSession(BaseException):
    """Raised by the OidcSession"""

    pass


class OdicSessionBadNonce(OidcSession):
    """Raised when the expected nonce doesn't match the ID token's nonce"""

    def __init__(self, nonce, expected_nonce):
        self.nonce = nonce
        self.expected_nonce = expected_nonce

    def __str__(self):
        return (
            "Possible attack, bad nonce recieved expected {} and got {}"
            .format(self.expected_nonce, self.nonce))


class OidcSessionExpiredToken(OidcSession):
    """Raised when the nonce"""

    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        return (
            "Expired ID token with expiry {}"
            .format(datetime.datetime.fromtimestamp(self.exp).isoformat()))
