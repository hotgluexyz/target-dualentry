
from hotglue_singer_sdk.target_sdk.auth import Authenticator


class DualentryAuthenticator(Authenticator):
    """API Authenticator for OAuth 2.0 flows."""

    def __init__(self, target, state):
        super().__init__(target, state)
        self._config_file_path = getattr(target, '_config_file_path', None)
    
    @property
    def auth_headers(self) -> dict:
        result = {}
        result["X-API-KEY"] = self._config.get('api_key')
        return result