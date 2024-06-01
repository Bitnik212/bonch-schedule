"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 23:09
"""
import datetime
from typing import Optional

from requests.sessions import Session

from bonch.common.ISchedule import ISchedule
from bonch.common.model.DayScheduleModel import DayScheduleModel
from bonch.common.model.WeekScheduleModel import WeekScheduleModel
from bonch.common.week.number.StudyWeekNumberService import StudyWeekNumberService
from bonch.schedule.site.Client import Client
from bonch.schedule.site.parser import Parser
from bonch.schedule.site.SiteScheduleType import SiteScheduleType


class ScheduleFromSite(ISchedule):

    def __init__(self, session: Session, schedule_type: SiteScheduleType, group_id: int):
        self.__schedule_type = schedule_type
        self.__group_id = group_id
        self.client = Client(session)
        self.parser = Parser()

    def today(self) -> Optional[DayScheduleModel]:
        content = self.client.page(page_type=self.__schedule_type, group_id=self.__group_id)
        if content is not None:
            week_subjects = self.parser.parse_week(content)
            today_date = datetime.datetime.now().date()
            today_subjects = [day_subjects for day_subjects in week_subjects.days if day_subjects.date == today_date]
            if len(today_subjects) == 1:
                return today_subjects[0]
            else:
                return None
        else:
            return None

    def week(self, number: int | None = None) -> Optional[WeekScheduleModel]:
        """
        :param number: номер учебной недели
        :return:
        """
        date = None if number is None else StudyWeekNumberService.from_week_number(number).start_week
        content = self.client.page(page_type=self.__schedule_type, group_id=self.__group_id, date=date)
        if content is not None:
            return self.parser.parse_week(content)
        else:
            return None
