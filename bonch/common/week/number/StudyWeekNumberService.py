import datetime

from bonch.common.week.WeekModel import WeekModel
from bonch.common.week.number.WeekNumberService import WeekNumberService


class StudyWeekNumberService(WeekNumberService):
    MAX_WEEK_NUMBER = 52
    STUDY_WEEK_NUMBER_SHIFT = 6

    @classmethod
    def from_date(cls, date: datetime.date) -> int:
        study_week_number = super().from_date(date) - cls.STUDY_WEEK_NUMBER_SHIFT
        if study_week_number <= 0:
            return cls.MAX_WEEK_NUMBER + study_week_number
        else:
            return study_week_number

    @classmethod
    def from_week_number(cls, study_week_number: int) -> WeekModel:
        """
        :param study_week_number: номер учебной недели
        :return:
        """
        return super().from_week_number(study_week_number + cls.STUDY_WEEK_NUMBER_SHIFT)
