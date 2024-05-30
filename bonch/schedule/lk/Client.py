"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 23:10
"""
from requests import Response
from requests.sessions import Session

from bonch.schedule.lk import ScheduleLkClient


class Client:

    def __init__(self, session: Session):
        self.links = ScheduleLkClient
        self.__session = session

    def schedule_page(self, week: int | None = None):
        return self.__post(url=self.links.schedule_link.value, query={"week": week})

    def __get(self, url: str, query: dict = None) -> Response:
        url = url + self.__build_query(query)
        return self.__session.get(url=url)

    def __post(self, url: str, body: dict = None, query: dict = None) -> Response:
        url = url + self.__build_query(query)
        return self.__session.post(url=url, data=body)

    @staticmethod
    def __build_query(query: dict) -> str:
        if query is None or None in query.values():
            return ""
        else:
            query_list = [f"{str(key)}={str(value)}" for key, value in query.items()]
            return "?"+"&".join(query_list)
