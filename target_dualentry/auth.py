import json
from datetime import datetime
from typing import Optional
from base64 import b64encode
from typing import Any, Dict, Optional

import logging
import requests
from target_hotglue.auth import Authenticator


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