import logging
from typing import Any, Optional, Union, overload

from ....v1.data_schemas.assets import Customer
from ..api import IDEXApi


class Customers:
    def __init__(self, api: IDEXApi) -> None:
        self._api = api

    @overload
    def get(self, *, id: str) -> Customer: ...
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
    ) -> list[Customer]: ...

    def get(
        self,
        id: Optional[str] = None,
        filter: Optional[str] = None,
        select: Optional[list[str]] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        order_by: Optional[str] = None,
        include_soft_delete: Optional[bool] = False,
    ) -> Union[Customer, list[Customer]]:
        """
        Get `Customer` object(s).

        Parameters
        ----------
        id : Optional[str]
            Customer to retrieve.
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
        Union[Customer, list[Customer]]
            The `Customer` object(s).

        """
        if id is not None:
            logging.debug(f"Getting Customer with ID: {id}")
            data = self._api.get(url=f"Customers/{id}")
            return Customer.model_validate(data.json())

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

        data = self._api.get(url="Customers", params=params)

        if data.status_code == 204:
            return []

        customers = [Customer.model_validate(row) for row in data.json()]

        if include_soft_delete:
            return customers

        return [customer for customer in customers if customer.deleted_date is None]

    def _check_select(self, select: list[str]) -> list[str]:
        important_fields = ["id"]
        for field in important_fields:
            if field not in select:
                select.append(field)
        return select
