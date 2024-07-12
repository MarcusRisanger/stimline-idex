import logging
from typing import Any, Optional, Union, overload

from ....v1.data_schemas import Field
from ..api import IDEXApi


class Fields:
    def __init__(self, api: IDEXApi) -> None:
        self._api = api

    @overload
    def get(self, *, id: str) -> Field: ...
    @overload
    def get(
        self,
        *,
        filter: Optional[str] = None,
        select: Optional[list[str]] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        order_by: Optional[str] = None,
        include_soft_delete: Optional[bool] = False,
    ) -> list[Field]: ...

    def get(
        self,
        id: Optional[str] = None,
        filter: Optional[str] = None,
        select: Optional[list[str]] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        order_by: Optional[str] = None,
        include_soft_delete: Optional[bool] = False,
    ) -> Union[Field, list[Field]]:
        """
        Get `Field` object(s).

        Parameters
        ----------
        id : Optional[str]
            Field to retrieve.
        filter : Optional[str]
            OData filter string.
        select : list[str] | None
            Provide a list of columns to retrieve from output.
        top : Optional[int]
            Limit the number of results returned.
        skip : Optional[int]
            Skip the first N results.
        order_by : Optional[str]
            Order the results by columns.
        include_soft_delete : Optional[bool] = False
            Include soft deleted records.

        Returns
        -------
        Union[Field, list[Field]]
            The `Field` object(s).

        """
        if id is not None:
            logging.debug(f"Getting Field with ID: {id}")
            data = self._api.get(url=f"Fields/{id}")
            return Field.model_validate(data.json())

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

        data = self._api.get(url="Fields", params=params)

        if data.status_code == 204:
            return []

        fields = [Field.model_validate(row) for row in data.json()]

        if include_soft_delete:
            return fields

        return [field for field in fields if field.deleted_date is None]

    def _check_select(self, select: list[str]) -> list[str]:
        important_fields = ["id"]
        for field in important_fields:
            if field not in select:
                select.append(field)
        return select
