"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 23:08
"""
from datetime import datetime
from typing import Optional, List

import requests
from requests.sessions import Session

from bonch.common.model import subject_type_map, SubjectType
from bonch.common.model.DayScheduleModel import DayScheduleModel
from bonch.common.model.SubjectModel import SubjectModel
from bonch.common.model.SubjectTimeModel import SubjectTimeModel
from bonch.common.model.WeekScheduleModel import WeekScheduleModel
from bonch.common.ISchedule import ISchedule
from bonch.schedule.lk.Client import Client
from bonch.schedule.lk.Parser import Parser


class ScheduleFromLK(ISchedule):

    def __init__(self, session: Session):
        self.client = Client(session)
        self.parser = Parser(self.client)

    def today(self) -> Optional[DayScheduleModel]:
        try:
            response = self.client.schedule_page()
            if len(response.text) < 400:
                return None
            else:
                try:
                    res = self.parser.parse_today(response.text)
                    if res['status'] == 404:
                        return None
                    else:
                        return self.__map_subject_to_model(res["response"])
                except AttributeError:
                    return None
        except requests.exceptions.Timeout:  # or requests.exceptions.ReadTimeout
            return None

    def week(self, number: int | None = None) -> Optional[WeekScheduleModel]:
        # todo сделаит обработки событий на все случаи жизни
        response = self.client.schedule_page(week=number) if number != 0 and not None else self.client.schedule_page()
        if response.text.find("Занятий не найдено") != -1:
            return None
        else:
            data = self.parser.parse_week(response.text)
            return WeekScheduleModel(days=[self.__map_subject_to_model(day_value['items']) for day_name, day_value in data.items()])

    @staticmethod
    def __map_subject_to_model(data: List[dict]) -> DayScheduleModel:
        subjects = []
        for subject in data:
            subjects.append(
                SubjectModel(
                    number=subject["number"],
                    name=subject["title"],
                    time=SubjectTimeModel(
                        from_time=datetime.fromisoformat(subject["start"]),
                        to_time=datetime.fromisoformat(subject["end"])
                    ),
                    type=subject_type_map.get(subject["type"], SubjectType.OTHER),
                    teachers=[subject["professor"]],
                    audience=f"каб.: {subject['cabinet_number']}, {subject['building']}"
                )
            )
        return DayScheduleModel(
            date=datetime.fromisoformat(data[0].get("start")).date(),
            subjects=subjects)
