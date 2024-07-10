import logging
from typing import Any, Optional, overload

from ....data_schemas.v1.assets import Unit, Wellbore
from ....data_schemas.v1.events.events import Run
from ..api import IDEXApi
from .text_utils import url_encode_id


class Runs:
    def __init__(self, api: IDEXApi) -> None:
        self._api = api

    @overload
    def get(self, *, unit: Unit) -> list[Run]: ...
    @overload
    def get(self, *, wellbore: Wellbore) -> list[Run]: ...
    @overload
    def get(self, *, unit_id: str) -> list[Run]: ...
    @overload
    def get(self, *, wellbore_id: str) -> list[Run]: ...
    @overload
    def get(self, *, filter: str, select: list[str], top: int, skip: int, order_by: str) -> list[Run]: ...

    def get(
        self,
        unit: Optional[Unit] = None,
        unit_id: Optional[str] = None,
        wellbore: Optional[Wellbore] = None,
        wellbore_id: Optional[str] = None,
        filter: Optional[str] = None,
        select: Optional[list[str]] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        order_by: Optional[str] = None,
    ) -> list[Run]:
        """
        Get `Run` objects.

        Parameters
        ----------
        unit : Optional[Unit]
            Unit object to get Runs for.
        unit_id : Optional[str]
            Unit ID to get Runs for.
        wellbore : Optional[Wellbore]
            Wellbore object to get Runs for.
        wellbore_id : Optional[str]
            Wellbore ID to get Runs for.
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

        Returns
        -------
        list[Run]
            The `Run` objects.

        """
        if unit is not None or unit_id is not None:
            id = unit_id if unit is None else unit.id
            assert id is not None
            logging.debug(f"Getting Runs for Unit with ID: {id}")
            id = url_encode_id(id)
            data = self._api.get(url=f"Units/{id}/Runs")

        elif wellbore is not None or wellbore_id is not None:
            id = wellbore_id if wellbore is None else wellbore.id
            assert id is not None
            logging.debug(f"Getting Runs for Wellbore with ID: {id}")
            id = url_encode_id(id)
            data = self._api.get(url=f"Wellbores/{id}/Runs")

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

            data = self._api.get(url="Runs", params=params)

        if data.status_code == 204:
            logging.debug("No Runs found.")
            return []

        return [Run.model_validate(row) for row in data.json()]

    def _check_select(self, select: list[str]) -> list[str]:
        important_fields = ["id"]
        for field in important_fields:
            if field not in select:
                select.append(field)
        return select
