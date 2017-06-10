"""
Exceptions for the pyramid_oidc package.
"""

class BaseException(Exception):
    pass


class ConfigurationException(Exception):
    """Raised for an error during configuration"""

    pass


class MissingConfigurationException(Exception):
    """Raised for missing configuration options during configuration"""

    def __init__(self, options):
        self._options = options

    def __str__(self):
        return (
            "Missing configuration options: {}"
            .format(', '.join(self._options)))
