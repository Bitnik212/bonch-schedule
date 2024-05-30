from dataclasses import dataclass
from datetime import date
from typing import List

from bonch.common.model.SubjectModel import SubjectModel


@dataclass
class DayScheduleModel:
    date: date
    subjects: List[SubjectModel]
