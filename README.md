# Stimline IDEX Software API Wrapper for Python

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

The `stimline-idex` package is an abstraction layer developed for interacting with the Stimline IDEX Collaboration software API.

It is based on available API documentation for the Aker BP IDEX environment publicly available [here](https://akerbp.idexcloud.net/idexapi/swagger/index.html).

The Wrapper currently supports API version 1.0.

## Getting started

Usage is fairly simple. You can authenticate using an `X-API-KEY` or using a JWT auth flow that requests a bearer token from the authentication endpoint.

```python
from stimline_idex.v1 import ApiKeyAuth, IDEXClient, JwtAuth
from stimline_idex.v1 import data_schemas as IDEXSchemas

api_auth = ApiKeyAuth(
    base_url = "https://<env>.idexcloud.net/idexapi/1.0/",
    x_api_key = "00000000-0000-0000-0000-000000000000"
)

client = IDEXClient(auth=api_auth)

jwt_auth = JWTAuth(
    base_url = "https://<env>.idexcloud.net/idexapi/1.0/",
    username = "foo",
    password = "bar"
)

client_jwt = IDEXClient(auth=jwt_auth)
```

The different modules are available for interaction, to get top 3 recently created wellbores:

```python
wellbores = client.wellbores.get(top=3, order_by="createdDate desc")
```

By default, some API endpoints return soft deleted records. However, the wrapper by default excludes deleted records in the query to the API. You can override this by using a kwarg: `include_soft_delete=True`. 

```python
wellbores = client.wellbores.get(include_soft_delete=True)
```

To make it easier to use the different attributes returned by the API, the wrapper uses Pydantic to validate that the return payload is according to the API specifications, the types are correctly parsed (e.g. as `datetime` objects instead of strings) and also provides a dot notation interface to work with the objects:

```python
wellbores = client.wellbores.get(top=3)

for wellbore in wellbores:
    print(wellbore.name)
```

Some of the endpoints allow for OData filtering. The filter string is passed as submitted to the function, it is up to the end user to ensure that this is in a correct format. The column names used in the filtering expression must be according to the API specification (i.e. not snake_cased). See the [official Odata documentation](https://docs.oasis-open.org/odata/odata/v4.0/errata03/os/complete/part2-url-conventions/odata-v4.0-errata03-os-part2-url-conventions-complete.html#_Toc453752357) for filtering inspiration..

> Note: Filtering on the `deletedDate` attribute *and* not having `include_soft_delete=True` will emit a warning log.

```python
from datetime import datetime, timezone

cutoff_date = datetime(2024, 1, 1, tzinfo=timezone.utc)

wellbores = client.wellbores.get(filter=f"createdDate gt {cutoff_date.isoformat()}")
```

You can also select a subset of columns instead of having the API return all columns. This can be useful for reducing the response time for use-cases where the full response is not required.

> Note: Currently the API modifies the response JSON when a `$select` clause is passed. 
> 
>The current behavior ( from 0.3.0) is to disregard the select clause when sending a request to the API, to avoid validation errors. Warning logs are emitted to reflect this.

```python
from datetime import datetime, timezone

cutoff_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
filter_str = f"createdDate gt {cutoff_date.isoformat()}"
colummns = ["name","modifiedDate"]

client.wellbores.get(filter=filter_str, select=columns)
```

For endpoints that require hierarchical context (e.g. retrieving all wellbores for a given well), you can pass either the parent object returned by the wrapper, or the appropriate id as a string. It is left as an exercise to the user to create further functions to loop over an iterable to retrieve children for multiple parents if that is required. 

```python
# By arbitrary `Well` object from API
well = client.wells.get(top=1)[0]
wellbores = client.wellbores.get(well=well)
```

```python
# By specific `Well` by id
well_id = "abc"
wellbores = client.wellbores.get(well_id=well_id)
```

For endpoints that support retrieval of a given object by id, pass this as a string:

```python
wellbore_id = "abc"
wellbore = client.wellbores.get(id=wellbore_id)
```