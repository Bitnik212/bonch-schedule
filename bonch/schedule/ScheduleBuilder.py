"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 22:57
"""
from bonch.schedule.ISchedule import ISchedule
from bonch.schedule.lk.ScheduleFromLK import ScheduleFromLK


class ScheduleBuilder:

    @staticmethod
    def build(session_id: str | None = None, group_name: str | None = None) -> ISchedule | None:
        if session_id is not None and session_id != "":
            return ScheduleFromLK(session_id=session_id)
        else:
            return None

