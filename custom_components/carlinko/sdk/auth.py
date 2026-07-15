"""
carlinko/auth.py

Authentication and request signing for the CarLinko API.

Refactored from the reverse-engineered J5 EV Dashboard project.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import socket
import time

import httpx

from .exceptions import AuthenticationError

#
# Force IPv4.
# The original dashboard does this because some ISPs prefer IPv6
# while CarLinko only answers correctly over IPv4.
#

_original_getaddrinfo = socket.getaddrinfo


def _getaddrinfo_ipv4(host, port, family=0, *args, **kwargs):
    return _original_getaddrinfo(
        host,
        port,
        socket.AF_INET,
        *args,
        **kwargs,
    ) or _original_getaddrinfo(
        host,
        port,
        family,
        *args,
        **kwargs,
    )


socket.getaddrinfo = _getaddrinfo_ipv4


class Authentication:

    DEFAULT_SIGN_KEY = "mYj3fzMpn77bir66"

    def __init__(
        self,
        account: str,
        password: str,
        region: str = "sea",
        *,
        sign_key: str | None = None,
        timeout: int = 20,
    ):

        self.account = account
        self.password = password

        self.region = region.lower()

        self.sign_key = (
            sign_key
            or self.DEFAULT_SIGN_KEY
        ).encode()

        self.client = httpx.Client(
            timeout=timeout
        )

        self.token: str | None = None

    @property
    def api_base(self) -> str:
        return (
            f"https://cqr-api-{self.region}.hzhjcl.com"
        )

    @staticmethod
    def now_ms() -> str:
        return str(int(time.time() * 1000))

    def sign(self, params: dict) -> str:

        payload = {
            key: "" if value is None else str(value)
            for key, value in params.items()
        }

        ordered = {
            key: payload[key]
            for key in sorted(payload.keys())
        }

        message = json.dumps(
            ordered,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()

        digest = hmac.new(
            self.sign_key,
            message,
            hashlib.sha256,
        ).digest()

        return base64.b64encode(digest).decode()

    def headers(
        self,
        params: dict,
        *,
        include_token: bool = True,
    ) -> dict:

        timestamp = self.now_ms()

        headers = {
            "timestamp": timestamp,
            "signature": self.sign(
                {
                    **params,
                    "timestamp": timestamp,
                }
            ),
            "user-agent": "Dart/3.10 (dart:io)",
            "language": "en",
            "content-type": "application/json",
        }

        if include_token and self.token:
            headers["token"] = self.token

        return headers

    def login(self) -> str:

        body = {
            "account": self.account,
            "password": self.password,
            "method": "PASSWORD",
            "appType": "APP",
            "osType": "ANDROID",
            "appName": "CarLinko",
            "appVersion": "1.12.0",
            "osVersion": "13",
            "language": "en",
            "timeZone": "Africa/Johannesburg",
            "phoneBrand": "Google",
            "phoneModel": "Pixel 7 Pro",
            "md5": "",
            "verifyCode": "",
            "dateTime": self.now_ms(),
        }

        response = self.client.post(
            self.api_base + "/user/login",
            json=body,
            headers=self.headers(
                body,
                include_token=False,
            ),
        )

        response.raise_for_status()

        payload = response.json()

        print(payload)  # Keep this while debugging

        if str(payload.get("code")) != "0000":
            raise AuthenticationError(
                f"Login failed: {payload}"
            )

        data = payload.get("data") or {}

        # The API sometimes returns the token directly as a string.
        if isinstance(data, dict):
            token = data.get("token")
        else:
            token = data

        if not token:
            raise AuthenticationError(
                f"Login succeeded but no token found: {payload}"
            )

        self.token = token

        return token
