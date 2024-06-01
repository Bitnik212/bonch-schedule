from datetime import datetime
from typing import List, Optional

import bs4

from bonch.common.model import subject_type_map, SubjectType
from bonch.common.model.DayScheduleModel import DayScheduleModel
from bonch.common.model.SubjectModel import SubjectModel
from bonch.common.model.SubjectTimeModel import SubjectTimeModel
from bonch.common.model.WeekScheduleModel import WeekScheduleModel
from bonch.schedule.site.parser.TimeTableParser import TimeTableParser


class Parser:

    @classmethod
    def parse_week(cls, data: str) -> Optional[WeekScheduleModel]:
        soup = bs4.BeautifulSoup(data, "html.parser")
        list_div = soup.find("table", attrs={"class": "vt-table"})
        timetable_div = soup.find("div", class_="vt236")
        if list_div is not None:
            return WeekScheduleModel(
                days=cls.__group_by_date(cls.__parse_list(list_div))
            )
        elif timetable_div is not None:
            return WeekScheduleModel(
                days=cls.__group_by_date(
                    subjects=TimeTableParser().parse_week(timetable_div)
                )
            )
        else:
            return None

    @staticmethod
    def __group_by_date(subjects: List[SubjectModel]) -> List[DayScheduleModel]:
        subjects_map = {}
        for subject in subjects:
            subject_map = subjects_map.get(subject.time.from_time.date(), None)
            if subject_map is None:
                subjects_map.update({
                    subject.time.from_time.date(): {
                        "subjects": [subject]
                    }
                })
            else:
                updated_subject_list: List = subject_map.get("subjects", [])
                updated_subject_list.append(subject)
                subjects_map.update({
                    subject.time.from_time.date(): {
                        "subjects": updated_subject_list
                    }
                })

        return [DayScheduleModel(date=date, subjects=subjects_dict["subjects"])
                for date, subjects_dict in subjects_map.items()]

    @staticmethod
    def __parse_list(div: bs4.element.Tag) -> List[SubjectModel]:
        """
        Парсим расписание списком
        :param div:
        :return:
        """

        week_names = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "воскресенье"]

        def parse_datetime(date: str, time: str) -> SubjectTimeModel:
            time_items = time.split("-")
            start_time = time_items[0].replace(".", ":")
            end_time = time_items[1].replace(".", ":")
            date_items = date.split(".")
            date_items.reverse()
            ico_date = "-".join(date_items)
            ico_datetime_start = f"{ico_date}T{start_time}:00"
            ico_datetime_end = f"{ico_date}T{end_time}:00"
            return SubjectTimeModel(
                from_time=datetime.fromisoformat(ico_datetime_start),
                to_time=datetime.fromisoformat(ico_datetime_end),
            )

        def parse_subject_line(tr: bs4.element.Tag) -> Optional[SubjectModel]:
            # weekday = tr["weekday"]
            # print(f"{weekday=}")
            subject_items = tr.find_all("td")
            if len(subject_items) == 6:
                subject_date_div, subject_number_div, subject_type_div, subject_name_div, subject_teacher_div, subject_address_div = subject_items
                subject_date = subject_date_div.getText(strip=True).lower()
                for week_name in week_names:
                    subject_date = subject_date.replace(week_name.lower(), "")
                subject_number_items = subject_number_div.getText(strip=True).split("(")
                subject_number = subject_number_items[0].strip()
                subject_time = subject_number_items[1].strip().replace(")", "")
                subject_type = subject_type_div.getText(strip=True)
                subject_name = subject_name_div.getText(strip=True)
                subject_teacher = subject_teacher_div.getText(strip=True)
                subject_address = subject_address_div.getText(strip=True)
                return SubjectModel(
                    number=subject_number,
                    name=subject_name,
                    type=subject_type_map.get(subject_type, SubjectType.OTHER),
                    teachers=subject_teacher.split(";"),
                    audience=subject_address,
                    time=parse_datetime(subject_date, subject_time)
                )
            else:
                return None

        head = div.thead
        body = div.tbody
        subject_lines = body.find_all("tr")
        if head is None:
            columns = subject_lines[0].find_all("th")
        else:
            columns = head.find_all("th")
        if len(columns) == 6:
            return [parse_subject_line(subject_line) for subject_line in subject_lines[1:] if subject_line is not None]
        else:
            return []
