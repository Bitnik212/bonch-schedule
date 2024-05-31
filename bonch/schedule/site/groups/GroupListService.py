import bs4
from requests.sessions import Session

from typing import List, Tuple

from bonch.common import DEFAULT_USER_AGENT
from bonch.common.AbstractClient import AbstractClient
from bonch.schedule.site import BASE_URL
from bonch.schedule.site.SiteScheduleType import SiteScheduleType
from bonch.schedule.site.model.FacultyModel import FacultyModel
from bonch.schedule.site.model.GroupItem import GroupItem


class GroupListService:

    def __init__(self, session: Session):
        session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
        self.__client = AbstractClient(session)

    def faculties(self, schedule_type: SiteScheduleType) -> List[FacultyModel]:
        response = self.__client._get(f"{BASE_URL}/{schedule_type.value}")
        if response.status_code == 200:
            return self.__parse(response.content)
        else:
            return []

    @staticmethod
    def __parse(data: str) -> List[FacultyModel]:

        def parse_faculty_div(div: bs4.element.Tag) -> Tuple[str, str, List[GroupItem]]:
            name_div = div.find("div", attrs={"class": "vt253"})
            description_div = div.find("div", attrs={"class": "vt254"})
            groups_div = div.find("div", attrs={"class": "vt255"})
            return str(name_div.getText(strip=True)), str(description_div.getText(strip=True)), parse_groups_div(groups_div)

        def parse_groups_div(div: bs4.element.Tag) -> List[GroupItem]:
            groups = []
            for group_div in div.childGenerator():
                group_id = group_div["data-i"]
                group_name = group_div["data-nm"]
                groups.append(
                    GroupItem(
                        group_id=int(group_id),
                        name=group_name
                    )
                )
            return groups

        faculties = []
        soup = bs4.BeautifulSoup(data, "html.parser")
        main_div = soup.find("div", attrs={"class": "vt251"})
        for faculty_div in main_div.childGenerator():
            name, description, groups = parse_faculty_div(faculty_div)
            faculties.append(
                FacultyModel(
                    name=name,
                    description=description,
                    groups=groups
                )
            )
        return faculties
