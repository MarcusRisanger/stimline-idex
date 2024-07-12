import logging
from typing import Any, Optional, Union, overload

from ....v1.data_schemas import Well, Wellbore
from ..api import IDEXApi


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
        include_soft_delete: Optional[bool] = False,
    ) -> list[Wellbore]: ...

    @overload
    def get(self, *, well: Well, include_soft_delete: Optional[bool] = False) -> list[Wellbore]: ...
    @overload
    def get(self, *, well_id: str, include_soft_delete: Optional[bool] = False) -> list[Wellbore]: ...

    def get(
        self,
        *,
        id: Optional[str] = None,
        well: Optional[Well] = None,
        well_id: Optional[str] = None,
        filter: Optional[str] = None,
        select: Optional[list[str]] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        order_by: Optional[str] = None,
        include_soft_delete: Optional[bool] = False,
    ) -> Union[Wellbore, list[Wellbore]]:
        """
        Get `Wellbore` object(s).

        Parameters
        ----------
        id : Optional[str]
            Well to retrieve.
        well : Optional[Well]
            Well object to get Wellbores for.
        well_id : Optional[str]
            Well ID to get Wellbores for.
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
        Union[Wellbore, list[Wellbore]]
            The `Wellbore` object(s).

        """
        if id is not None:
            # Get singular well
            logging.debug("Getting Wellbore with ID: {id}")
            data = self._api.get(url=f"Wellbores/{id}")
            return Wellbore.model_validate(data.json())

        elif well is not None:
            logging.debug(f"Getting Wellbores for Well with ID: {well.id}")
            # Get Wellbores for singular well
            data = self._api.get(url=f"Wells/{well.id}/Wellbores")

        elif well_id is not None:
            # Get Wellbores for singular well
            logging.debug(f"Getting Wellbores for Well with ID: {well_id}")
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

        if data.status_code == 204:
            return []

        wellbores = [Wellbore.model_validate(row) for row in data.json()]

        if include_soft_delete:
            return wellbores

        return [wb for wb in wellbores if wb.deleted_date is None]

    def _check_select(self, select: list[str]) -> list[str]:
        important_fields = ["id"]
        for field in important_fields:
            if field not in select:
                select.append(field)
        return select
