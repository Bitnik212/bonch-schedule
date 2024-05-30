from dataclasses import dataclass
from typing import List

from bonch.common.model.DayScheduleModel import DayScheduleModel


@dataclass
class WeekScheduleModel:
    days: List[DayScheduleModel]
