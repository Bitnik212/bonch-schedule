import datetime
from dataclasses import dataclass


@dataclass
class WeekModel:
    start_week: datetime.date
    end_week: datetime.date
    number: int
