"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 23:10
"""
from requests.sessions import Session

from bonch.common.AbstractClient import AbstractClient
from bonch.schedule.lk import ScheduleLkClient


class Client(AbstractClient):

    def __init__(self, session: Session):
        super().__init__(session)
        self.links = ScheduleLkClient

    def schedule_page(self, week: int | None = None):
        return self._post(url=self.links.schedule_link.value, query={"week": week})
