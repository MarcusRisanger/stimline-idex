import logging
from typing import Optional, overload

from ....data_schemas.v1.assets import Unit, Wellbore
from ....data_schemas.v1.events import WellboreHistory
from ..api import IDEXApi
from .text_utils import url_encode_id


class WellboreHistories:
    def __init__(self, api: IDEXApi) -> None:
        self._api = api

    @overload
    def get(self, *, unit: Unit, include_soft_delete: Optional[bool] = False) -> list[WellboreHistory]: ...
    @overload
    def get(self, *, unit_id: str, include_soft_delete: Optional[bool] = False) -> list[WellboreHistory]: ...
    @overload
    def get(self, *, wellbore: Wellbore, include_soft_delete: Optional[bool] = False) -> list[WellboreHistory]: ...
    @overload
    def get(self, *, wellbore_id: str, include_soft_delete: Optional[bool] = False) -> list[WellboreHistory]: ...

    def get(
        self,
        *,
        unit: Optional[Unit] = None,
        unit_id: Optional[str] = None,
        wellbore: Optional[Wellbore] = None,
        wellbore_id: Optional[str] = None,
        include_soft_delete: Optional[bool] = False,
    ) -> list[WellboreHistory]:
        """
        Get `WellboreHistory` object(s).

        Parameters
        ----------
        unit : Optional[Unit]
            Unit object to get WellboreHistory for.
        unit_id : Optional[str]
            Unit ID to get WellboreHistory for.
        wellbore : Optional[Wellbore]
            Wellbore object to get WellboreHistory for.
        wellbore_id : Optional[str]
            Wellbore ID to get WellboreHistory for.
        include_soft_delete : Optional[bool] = False
            Include soft deleted records.

        Returns
        -------
        list[WellboreHistory]
            The `WellboreHistory` object(s).

        """
        if unit is not None or unit_id is not None:
            id = unit_id if unit is None else unit.id
            assert id is not None
            logging.debug(f"Getting WellboreHistory for Unit with ID: {id}")
            id = url_encode_id(id)
            data = self._api.get(url=f"unit/{id}/UnitWellboreHistory")

        elif wellbore is not None or wellbore_id is not None:
            id = wellbore_id if wellbore is None else wellbore.id
            assert id is not None
            logging.debug(f"Getting WellboreHistory for Wellbore with ID: {id}")
            id = url_encode_id(id)
            data = self._api.get(url=f"Wellbores/{id}/UnitWellboreHistory")

        else:
            raise TypeError("Either `unit`, `unit_id`, `wellbore` or `wellbore_id` must be provided.")

        if data.status_code == 204:
            return []

        records = [WellboreHistory.model_validate(row) for row in data.json()]

        if include_soft_delete:
            return records

        return [rec for rec in records if rec.deleted_date is None]
