# Модуль расписания СПБГУТ

# Установка

```bash
pip install bonch-schedule
```

# Пример

## Через билдер

```python
import requests
from bonch.schedule.ScheduleBuilder import ScheduleBuilder
from bonch.schedule.site.SiteScheduleType import SiteScheduleType
from bonch.schedule.site.groups.GroupListService import GroupListService


session = requests.session()

builder = ScheduleBuilder(
    session=session
)
# Расписание из лк
schedule = builder.with_lk(session_id="yourmidenfromlkcookies") 

# Или

# Расписание с сайта
schedule_type = SiteScheduleType.FULL_TIME_AND_EVENING_LESSONS

# Получаем факультеты и группы в них по типу расписания 
groups_service = GroupListService(session)
faculties = groups_service.faculties(schedule_type)
selected_group = faculties[0].groups[0]

schedule = builder.with_site(
    group_id=selected_group.group_id,  # Id группы с сайта
    schedule_type=schedule_type  # Тип расписания
)

print(f"today schedule: {schedule.today()}")

print(f"today week schedule: {schedule.week()}")
```