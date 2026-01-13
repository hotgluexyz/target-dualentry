"""Dualentry target sink class, which handles writing streams."""

from __future__ import annotations

import backoff
import requests
from hotglue_singer_sdk.exceptions import FatalAPIError, RetriableAPIError

from hotglue_singer_sdk.target_sdk.client import HotglueSink


from target_dualentry.auth import DualentryAuthenticator


class DualentrySink(HotglueSink):
    """Dualentry target sink class."""

    @property
    def base_url(self) -> str:
        base_url = "https://api.dualentry.com/public/v1"
        return base_url

    @property
    def authenticator(self):
        return DualentryAuthenticator(self._target, dict())