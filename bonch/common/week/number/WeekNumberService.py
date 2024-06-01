import datetime

from bonch.common.week.WeekModel import WeekModel


class WeekNumberService:

    @classmethod
    def from_date(cls, date: datetime.date) -> int:
        return date.isocalendar().week

    @classmethod
    def from_week_number(cls, week_number: int) -> WeekModel:
        now_year = datetime.datetime.now().year
        return WeekModel(
            start_week=datetime.date.fromisocalendar(year=now_year, week=week_number, day=1),
            end_week=datetime.date.fromisocalendar(year=now_year, week=week_number, day=7),
            number=week_number
        )
