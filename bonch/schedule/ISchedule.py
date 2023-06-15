"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 22:58
"""


class ISchedule:

    def today(self): ...

    def week(self, number: int | None = None): ...

    # TODO def start_lesson(self): ...
