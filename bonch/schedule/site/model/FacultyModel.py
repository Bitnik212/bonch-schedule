from dataclasses import dataclass
from typing import List

from bonch.schedule.site.model.GroupItem import GroupItem


@dataclass
class FacultyModel:
    name: str
    description: str
    groups: List[GroupItem]
