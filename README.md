# Stimline IDEX Software API Wrapper for Python

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

The `stimline-idex` package is an abstraction layer developed for interacting with the Stimline IDEX Collaboration software API.

It is based on available API documentation for the Aker BP IDEX environment publicly available [here](https://akerbp.idexcloud.net/idexapi/swagger/index.html).

The Wrapper currently supports API version 1.0.

## Getting started

Usage is fairly simple. You can authenticate using an `X-API-KEY` or using a JWT auth flow that requests a bearer token from the authentication endpoint.

```python
from stimline_idex import ApiKeyAuth, IDEXClient, JWTAuth

api_auth = ApiKeyAuth(
    base_url = "https://<env>.idexcloud.net/idexapi/1.0/",
    x_api_key = "00000000-0000-0000-0000-000000000000"
)

client_api = IDEXClient(auth=api_auth)

jwt_auth = JWTAuth(
    base_url = "https://<env>.idexcloud.net/idexapi/1.0/",
    username = "foo",
    password = "bar"
)

client_jwt = IDEXClient(auth=jwt_auth)
```

The different modules are available for interaction:

```python
wellbores = client_api.wellbores.get(top=3)
```
