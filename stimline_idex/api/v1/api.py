"""Lazy abstraction for HTTP client."""

from typing import Any
from urllib.parse import urljoin

from requests import Response, Session

from .auth import IDEXAuth


class IDEXApi:
    def __init__(
        self,
        *,
        auth: IDEXAuth,
        session: Session,
    ):
        self.auth = auth
        self.session = session

    @property
    def base_url(self):
        return self.auth.base_url

    def _authenticate(self) -> None:
        new_auth = self.auth.get_auth_header(base_url=self.base_url)
        self.session.headers.update(new_auth)

    def _send_request(self, *, method: str, url: str, **kwargs: Any) -> Response:
        self._authenticate()
        request_url = urljoin(self.base_url, url)
        rsp = self.session.request(method=method, url=request_url, **kwargs)
        rsp.raise_for_status()
        return rsp

    def get(self, *, url: str, **kwargs: Any) -> Response:
        return self._send_request(method="GET", url=url, **kwargs)

    def post(self, *, url: str, **kwargs: Any) -> Response:
        return self._send_request(method="POST", url=url, **kwargs)
