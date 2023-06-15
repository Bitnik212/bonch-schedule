"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 23:10
"""
from http.cookiejar import Cookie

import requests as requests
from requests import Response

from bonch.schedule.lk import ScheduleLkClient


class Client:

    def __init__(self, session_id: str):
        self.links = ScheduleLkClient
        self.__session_id = session_id
        self.__session = requests.session()
        self.__build_session()

    def schedule_page(self, week: int | None = None):
        return self.__post(url=self.links.schedule_link.value, query={"week": week})

    def __build_session(self):
        cookie = Cookie(
            name="miden",
            domain=self.links.base_domain.value,
            value=self.__session_id,
            path="/",
            expires=None,
            port=None,
            port_specified=None,
            domain_specified=False,
            domain_initial_dot=False,
            path_specified=False,
            secure=False,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None,
            rfc2109=False,
            version=0
        )
        self.__session.cookies.set_cookie(cookie=cookie)
        self.__session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }
        )

    def __get(self, url: str, query: dict = None) -> Response:
        url = url + self.__build_query(query)
        return self.__session.get(url=url)

    def __post(self, url: str, body: dict = None, query: dict = None) -> Response:
        url = url + self.__build_query(query)
        print(f"url: {url}")
        return self.__session.post(url=url, data=body)

    @staticmethod
    def __build_query(query: dict) -> str:
        if query is None or None in query.values():
            return ""
        else:
            query_list = [f"{str(key)}={str(value)}" for key, value in query.items()]
            return "?"+"&".join(query_list)
