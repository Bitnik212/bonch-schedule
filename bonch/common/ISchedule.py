"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 22:58
"""
from typing import Optional

from bonch.common.model.DayScheduleModel import DayScheduleModel
from bonch.common.model.WeekScheduleModel import WeekScheduleModel


class ISchedule:

    def today(self) -> Optional[DayScheduleModel]: ...

    def week(self, number: int | None = None) -> Optional[WeekScheduleModel]: ...

    # TODO def start_lesson(self): ...
