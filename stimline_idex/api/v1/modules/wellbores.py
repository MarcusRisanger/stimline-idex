from typing import Any, Optional, Union, overload
from ..api import IDEXApi
from ....data_schemas.v1.assets import Wellbore


class Wellbores:
    def __init__(self, api: IDEXApi) -> None:
        self._api = api

    @overload
    def get(self, *, id: str) -> Wellbore: ...

    @overload
    def get(
        self,
        *,
        filter: Optional[str] = None,
        select: Optional[list[str]] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        order_by: Optional[str] = None,
    ) -> list[Wellbore]: ...

    @overload
    def get(self, *, well_id: str) -> list[Wellbore]: ...

    def get(
        self,
        *,
        id: Optional[str] = None,
        well_id: Optional[str] = None,
        filter: Optional[str] = None,
        select: Optional[list[str]] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        order_by: Optional[str] = None,
    ) -> Union[Wellbore, list[Wellbore]]:
        if isinstance(id, str):
            # Get singular well
            data = self._api.get(url=f"Wellbores/{id}")
            return Wellbore.model_validate(data.json())

        if isinstance(well_id, str):
            # Get Wellbores for singular well
            data = self._api.get(url=f"Wells/{well_id}/Wellbores")
        else:
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

            data = self._api.get(url="Wellbores", params=params)

        return [Wellbore.model_validate(row) for row in data.json()]

    def _check_select(self, select: list[str]) -> list[str]:
        important_fields = ["id"]
        for field in important_fields:
            if field not in select:
                select.append(field)
        return select
