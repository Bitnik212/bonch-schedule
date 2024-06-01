from datetime import datetime
from typing import List

import bs4

from bonch.common.model import SubjectType, subject_type_map
from bonch.common.model.SubjectModel import SubjectModel
from bonch.common.model.SubjectTimeModel import SubjectTimeModel


class TimeTableParser:

    @classmethod
    def parse_week(cls, div: bs4.element.Tag) -> List[SubjectModel]:
        """
        Парсим расписание в формате таблицы
        :param div:
        :return:
        """
        remapped_table_map = cls.remap_table(div.find("div", attrs={"class": "vt244"}))
        table_body = div.find("div", attrs={"class": "vt244b"})
        all_subjects = []
        for subjects_div in table_body.childGenerator():
            [all_subjects.append(subject) for subject in cls.map_line(subjects_div, remapped_table_map)]

        return all_subjects

    @staticmethod
    def parse_subject(subject_div: bs4.element.Tag) -> dict:
        name_div = subject_div.find("div", attrs={"class": "vt240"})
        teacher_span = subject_div.find("span", attrs={"class": "teacher"})
        address_div = subject_div.find("div", attrs={"class": "vt242"})
        subject_type_div = subject_div.find("div", attrs={"class": "vt243"})
        return {
            "name": name_div.getText(strip=True),
            "teacher": teacher_span.getText(strip=True),
            "address": address_div.getText(strip=True),
            "type": subject_type_div.getText(strip=True)
        }

    @classmethod
    def map_subject(cls, subject: dict, time: dict) -> SubjectModel:
        return SubjectModel(
            number=time["number"],
            name=subject["name"],
            time=cls.map_time_to_model(time),
            audience=subject["address"],
            type=subject_type_map.get(subject["type"], SubjectType.OTHER),
            teachers=[subject["teacher"]]
        )

    @staticmethod
    def map_time_to_model(time: dict) -> SubjectTimeModel:
        now_year = str(datetime.now().year)
        date_list: List[str] = f"{time['short_date']}.{now_year}".split(".")
        date_list.reverse()
        ico_date = "-".join(date_list)
        start_datetime = datetime.fromisoformat(f"{ico_date}T{time['time']['start']}:00")
        end_datetime = datetime.fromisoformat(f"{ico_date}T{time['time']['end']}:00")
        return SubjectTimeModel(
            from_time=start_datetime,
            to_time=end_datetime
        )

    @classmethod
    def map_line(cls, subjects_div: bs4.element.Tag, table_map: dict) -> List[SubjectModel]:
        subjects_div_list = list(subjects_div.childGenerator())
        subject_time_div = subjects_div_list[0]
        subject_number = subject_time_div.find("div", attrs={"class": "vt283"}).getText(strip=True)
        subject_time = subject_time_div.getText(strip=True)[len(subject_number):]
        subject_time_start = subject_time[:5]
        subject_time_end = subject_time[5:]
        subject_time_map = {
            "number": subject_number,
            "time": {
                "start": subject_time_start,
                "end": subject_time_end
            }
        }
        subjects = []
        for index, subject_container_div in enumerate(subjects_div_list[1:]):
            subjects_divs = list(subject_container_div.childGenerator())
            subject_time_map.update({
                "short_date": table_map[index]["short_date"]
            })
            if len(subjects_divs) == 1:
                subjects.append(
                    cls.map_subject(cls.parse_subject(subjects_divs[0]), subject_time_map)
                )
            elif len(subjects_divs) == 2:
                subjects.append(
                    cls.map_subject(cls.parse_subject(subjects_divs[0]), subject_time_map),
                )
                subjects.append(
                    cls.map_subject(cls.parse_subject(subjects_divs[1]), subject_time_map),
                )
        return subjects

    @staticmethod
    def remap_table(table_head: bs4.element.Tag) -> dict:
        table_map = {}
        for day_div in table_head.childGenerator():
            if type(day_div) is bs4.element.Tag:
                index = day_div.get("data-i", None)
                if index is not None:
                    day_name = day_div.div.getText(strip=True)
                    day_short_date = day_div.getText(strip=True).replace(day_name, "")
                    table_map.update({
                        (int(index) - 1): {
                            "name": day_name,
                            "short_date": day_short_date,
                            "subjects": []
                        }
                    })
        return table_map
