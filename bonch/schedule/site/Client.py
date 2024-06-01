"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 23:10
"""
from typing import Optional
from requests.sessions import Session

from bonch.common.AbstractClient import AbstractClient
from bonch.schedule.site import BASE_URL
from bonch.schedule.site.SiteScheduleType import SiteScheduleType


class Client(AbstractClient):

    def __init__(self, session: Session):
        super().__init__(session)

    def page(self, page_type: SiteScheduleType, group_id: int, date: Optional[str] = None) -> Optional[str]:
        query = {"group": group_id}
        if date is not None:
            query.update({
                "date": date
            })
        response = self._get(url=f"{BASE_URL}/{page_type.value}", query=query)
        if response.status_code == 200:
            return response.content.decode()
        else:
            return None
