from typing import Optional

from requests import Session

from .api import IDEXApi
from .auth import IDEXAuth
from .modules import Customers, Fields, Runs, Soe, Surveys, Units, Wellbores, Wells


class IDEXClient:
    def __init__(self, *, auth: IDEXAuth, session: Optional[Session] = None) -> None:
        if session is None:
            session = Session()

        self._api = IDEXApi(auth=auth, session=session)

        self.customers = Customers(api=self._api)
        self.fields = Fields(api=self._api)
        self.runs = Runs(api=self._api)
        self.soe = Soe(api=self._api)
        self.surveys = Surveys(api=self._api)
        self.units = Units(api=self._api)
        self.wells = Wells(api=self._api)
        self.wellbores = Wellbores(api=self._api)
