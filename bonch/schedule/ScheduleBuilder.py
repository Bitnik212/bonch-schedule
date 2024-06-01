"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 22:57
"""
from http.cookiejar import Cookie
from typing import Optional

import requests
from requests.sessions import Session

from bonch.common import DEFAULT_USER_AGENT
from bonch.common.ISchedule import ISchedule
from bonch.schedule.lk import ScheduleLkClient
from bonch.schedule.lk.ScheduleFromLK import ScheduleFromLK
from bonch.schedule.site.ScheduleFromSite import ScheduleFromSite
from bonch.schedule.site.SiteScheduleType import SiteScheduleType


class ScheduleBuilder:

    def __init__(self, session: Optional[Session] = None, user_agent: str = DEFAULT_USER_AGENT):
        self.__session = session if session is not None else requests.session()
        self.__user_agent = user_agent

    def with_lk(self, session_id: str) -> ISchedule:
        """
        :param session_id: параметр из куки лк бонча (`miden`)
        :return:
        """
        return ScheduleFromLK(session=self.__build_with_session_id(session_id))

    def with_site(self, group_id: int, schedule_type: SiteScheduleType) -> ISchedule:
        self.__session.headers.update({"User-Agent": self.__user_agent})
        return ScheduleFromSite(session=self.__session, schedule_type=schedule_type, group_id=group_id)

    def __build_with_session_id(self, session_id: str) -> Session:
        self.__session.cookies.set_cookie(
            cookie=Cookie(
                name="miden",
                domain=ScheduleLkClient.base_domain.value,
                value=session_id,
                path="/",
                expires=None,
                port=None,
                port_specified=False,
                domain_specified=False,
                domain_initial_dot=False,
                path_specified=False,
                secure=False,
                discard=False,
                comment=None,
                comment_url=None,
                rest={},
                rfc2109=False,
                version=0
            )
        )
        self.__session.headers.update(
            {
                "User-Agent": self.__user_agent
            }
        )
        return self.__session
