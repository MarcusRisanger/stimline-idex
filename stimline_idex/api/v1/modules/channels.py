import logging
from typing import Optional, overload

from ....data_schemas.v1.assets import Channel, Log
from ....data_schemas.v1.events import Run
from ..api import IDEXApi
from .text_utils import url_encode_id


class Channels:
    def __init__(self, api: IDEXApi) -> None:
        self._api = api

    @overload
    def get(self, *, log: Log, include_soft_delete: Optional[bool] = False) -> list[Channel]: ...
    @overload
    def get(self, *, log_id: str, include_soft_delete: Optional[bool] = False) -> list[Channel]: ...
    @overload
    def get(self, *, run: Run, include_soft_delete: Optional[bool] = False) -> list[Channel]: ...
    @overload
    def get(self, *, run_id: str, include_soft_delete: Optional[bool] = False) -> list[Channel]: ...

    def get(
        self,
        *,
        log: Optional[Log] = None,
        log_id: Optional[str] = None,
        run: Optional[Run] = None,
        run_id: Optional[str] = None,
        include_soft_delete: Optional[bool] = False,
    ) -> list[Channel]:
        """
        Get `Channel` object(s).

        Parameters
        ----------
        log : Optional[Log]
            Log object to get Channel for.
        log_id : Optional[str]
            Log ID to get Channel for.
        run : Optional[Run]
            Run object to get Channel for.
        run_id : Optional[str]
            Run ID to get Channel for.
        include_soft_delete : Optional[bool] = False
            Include soft deleted records.

        Returns
        -------
        list[Channel]
            The `Channel` object(s).

        """
        if log is not None or log_id is not None:
            id = log_id if log is None else log.id
            assert id is not None
            logging.debug(f"Getting Channels for Log with ID: {id}")
            id = url_encode_id(id)
            data = self._api.get(url=f"Logs/{id}/Channels")

        elif run is not None or run_id is not None:
            id = run_id if run is None else run.id
            assert id is not None
            logging.debug(f"Getting Channels for Run with ID: {id}")
            id = url_encode_id(id)
            data = self._api.get(url=f"Runs/{id}/Channels")

        else:
            raise TypeError("Either `log`, `log_id`, `run` or `run_id` must be provided.")

        if data.status_code == 204:
            return []

        records = [Channel.model_validate(row) for row in data.json()]

        if include_soft_delete:
            return records

        return [rec for rec in records if rec.deleted_date is None]
