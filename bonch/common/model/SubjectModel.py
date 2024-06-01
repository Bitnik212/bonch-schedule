from dataclasses import dataclass
from typing import List

from bonch.common.model.SubjectTimeModel import SubjectTimeModel
from bonch.common.model.SubjectType import SubjectType


@dataclass
class SubjectModel:
    number: str
    name: str
    time: SubjectTimeModel
    type: SubjectType
    teachers: List[str]
    audience: str
