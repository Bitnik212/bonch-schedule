"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 23:09
"""
from bonch.schedule.ISchedule import ISchedule


class ScheduleFromSite(ISchedule):

    def today(self, date_str: str | None = None):
        super().today(date_str)

    def week(self, number: int | None = None):
        super().week(number)
