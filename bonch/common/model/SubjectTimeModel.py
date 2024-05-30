from dataclasses import dataclass
from datetime import datetime


@dataclass
class SubjectTimeModel:
    from_time: datetime
    to_time: datetime
