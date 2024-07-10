"""Some helpers for authentication purposes."""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional, Protocol
from urllib.parse import urljoin

import requests

from ...data_schemas.v1.auth import (
    AuthenticateRequest,
    AuthenticateResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
)


class IDEXAuth(Protocol):
    # Add post-init for parsing base url

    @property
    def base_url(self) -> str: ...

    def get_auth_header(self, **kwargs: Any) -> dict[str, str]: ...


@dataclass
class JwtAuth:
    base_url: str
    username: str
    password: str
    auth: Optional[AuthenticateResponse] = field(default=None, init=False, repr=False)

    @property
    def auth_request_payload(self) -> str:
        return AuthenticateRequest(
            username=self.username,
            password=self.password,
        ).model_dump_json()

    @property
    def refresh_request_payload(self) -> str:
        assert self.auth is not None
        return RefreshTokenRequest(
            refresh_token=self.auth.refresh_token,
        ).model_dump_json()

    def _acquire_token(self, base_url: str) -> AuthenticateResponse:
        """For acquiring a new token."""
        response = requests.post(
            url=urljoin(base_url, "Access/Authenticate"),
            headers={"Content-Type": "application/json"},
            data=self.auth_request_payload,
        )
        response.raise_for_status()
        logging.info("Received new token.")
        return AuthenticateResponse.model_validate_json(response.text)

    def _refresh_token(self, base_url: str) -> RefreshTokenResponse:
        """For refreshing token."""
        response = requests.post(
            url=urljoin(base_url, "Access/RefreshToken"),
            headers={"Content-Type": "application/json"},
            data=self.refresh_request_payload,
        )
        response.raise_for_status()
        logging.info("Refreshed token.")
        return RefreshTokenResponse.model_validate_json(response.text)

    def get_auth_header(self, **kwargs: Any) -> dict[str, str]:
        try:
            base_url = kwargs["base_url"]
        except KeyError:
            raise ValueError("The `base_url` keyword must be provided.")

        if self.auth is None:
            self.auth = self._acquire_token(base_url=base_url)

        elif self.auth.refresh_token_expire <= datetime.now(tz=timezone.utc):
            self.auth = self._acquire_token(base_url=base_url)

        elif self.auth.token_expire <= datetime.now(tz=timezone.utc):
            resp = self._refresh_token(base_url=base_url)
            self.auth.token = resp.token
            self.auth.token_expire = resp.token_expire

        return {"Authorization": self.auth.token}


@dataclass(frozen=True)
class ApiKeyAuth:
    base_url: str
    x_api_key: str

    def get_auth_header(self, **kwargs: Any) -> dict[str, str]:
        return {"X-API-KEY": self.x_api_key}
