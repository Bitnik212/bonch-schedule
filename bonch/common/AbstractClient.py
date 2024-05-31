
from requests.sessions import Session
from requests import Response


class AbstractClient:

    def __init__(self, session: Session):
        self._session = session

    @staticmethod
    def __build_query(query: dict) -> str:
        if query is None or None in query.values():
            return ""
        else:
            query_list = [f"{str(key)}={str(value)}" for key, value in query.items()]
            return "?" + "&".join(query_list)

    def _get(self, url: str, query: dict = None) -> Response:
        url = url + self.__build_query(query)
        return self._session.get(url=url)

    def _post(self, url: str, body: dict = None, query: dict = None) -> Response:
        url = url + self.__build_query(query)
        return self._session.post(url=url, data=body)
