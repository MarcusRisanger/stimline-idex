import logging
from typing import Optional, Union, overload

from ....data_schemas.v1.assets import Log, Unit
from ..api import IDEXApi


class Logs:
    def __init__(self, api: IDEXApi) -> None:
        self._api = api

    @overload
    def get(self, *, id: str) -> Log: ...
    @overload
    def get(self, *, unit: Unit) -> list[Log]: ...
    @overload
    def get(self, *, unit_id: str) -> list[Log]: ...

    def get(
        self,
        *,
        id: Optional[str] = None,
        unit: Optional[Unit] = None,
        unit_id: Optional[str] = None,
    ) -> Union[Log, list[Log]]:
        """
        Get `Log` object(s).

        Parameters
        ----------
        id : Optional[str]
            Log to retrieve.
        unit : Optional[Unit]
            Unit object to get Logs for.
        unit_id : Optional[str]
            Unit ID to get Logs for.

        Returns
        -------
        Union[Log, list[Log]]
            The `Log` object(s).

        """
        if id is not None:
            logging.debug(f"Getting Wellbore with ID: {id}")
            data = self._api.get(url=f"Logs/{id}")
            return Log.model_validate(data.json())

        if unit is not None:
            logging.debug(f"Getting Logs for Unit with ID: {unit.id}")
            data = self._api.get(url=f"Units/{unit.id}/Logs")
        elif unit_id is not None:
            logging.debug(f"Getting Logs for Unit with ID: {unit_id}")
            data = self._api.get(url=f"Units/{unit_id}/Logs")
        else:
            raise ValueError("Either `unit` or `unit_id` must be provided.")

        if data.status_code == 204:
            return []

        return [Log.model_validate(row) for row in data.json()]
