"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 23:05
"""
from enum import Enum


class ScheduleLkClient(Enum):
    base_domain = "lk.sut.ru"
    base_link = f"https://{base_domain}/"
    schedule_link = f"{base_link}cabinet/project/cabinet/forms/raspisanie.php"


class Settings(Enum):
    timeout = 120
