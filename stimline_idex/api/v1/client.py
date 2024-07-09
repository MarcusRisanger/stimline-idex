from typing import Optional
from requests import Session
from .auth import IDEXAuth
from .api import IDEXApi
from .modules import Wells, Wellbores, Soe, Surveys


class IDEXClient:
    def __init__(self, *, auth: IDEXAuth, session: Optional[Session] = None) -> None:
        if session is None:
            session = Session()

        self._api = IDEXApi(auth=auth, session=session)
        self.wells = Wells(api=self._api)
        self.wellbores = Wellbores(api=self._api)
        self.soe = Soe(api=self._api)
        self.surveys = Surveys(api=self._api)
