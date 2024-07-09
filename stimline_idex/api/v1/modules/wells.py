from typing import Any, Optional, Union, overload

from stimline_idex.data_schemas import IdType

from ....data_schemas.v1.assets import Well
from ..api import IDEXApi


class Wells:
    def __init__(self, api: IDEXApi) -> None:
        self._api = api

    @overload
    def get(self, *, id: IdType) -> Well: ...

    @overload
    def get(
        self,
        *,
        filter: Optional[str] = None,
        select: Optional[list[str]] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        order_by: Optional[str] = None,
    ) -> list[Well]: ...

    def get(
        self,
        *,
        id: Optional[IdType] = None,
        filter: Optional[str] = None,
        select: Optional[list[str]] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        order_by: Optional[str] = None,
    ) -> Union[Well, list[Well]]:
        if id is not None and any(v is not None for v in [filter, select, top, skip, order_by]):
            raise ValueError("You can only submit either an ID or parameters, not both.")

        if id is not None:
            # Get singular well
            data = self._api.get(url=f"Wells/{id}")
            return Well.model_validate(data.json())

        params: dict[str, Any] = {}
        if filter is not None:
            params["$filter"] = filter
        if select is not None:
            select = self._check_select(select)
            params["$select"] = ",".join(select)
        if top is not None:
            params["$top"] = top
        if skip is not None:
            params["$skip"] = skip
        if order_by is not None:
            params["$orderby"] = order_by

        data = self._api.get(url="Wells", params=params)

        if data.status_code == 204:
            return []

        return [Well.model_validate(row) for row in data.json()]

    def _check_select(self, select: list[str]) -> list[str]:
        important_fields = ["id"]
        for field in important_fields:
            if field not in select:
                select.append(field)
        return select
