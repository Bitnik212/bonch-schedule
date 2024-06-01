from enum import Enum


class SiteScheduleType(Enum):
    FULL_TIME_AND_EVENING_LESSONS = "raspisanie-zanyatiy-studentov-ochnoy-i-vecherney-form-obucheniya"
    """Расписание занятий студентов очной и вечерней форм обучения"""
    FULL_TIME_AND_EVENING_EXAMS = "raspisanie-zachetov-studentov-ochnoy-i-vecherney-form-obucheniya"
    """Расписание зачётов студентов очной и вечерней форм обучения"""
    SESSION_SCHEDULE_FOR_CORRESPONDENCE = "raspisanie-sessii-studentov-zaochnoy-formi-obucheniya"
    """Расписание сессии студентов заочной формы обучения"""
    EXAMINATION_SESSION = "raspisanie-ekzamenacionnoy-sessii"
    """Расписание экзаменационной сессии"""
