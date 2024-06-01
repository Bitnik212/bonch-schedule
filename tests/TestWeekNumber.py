import datetime
from unittest import TestCase

from bonch.common.week.number.StudyWeekNumberService import StudyWeekNumberService


class TestWeekNumber(TestCase):

    def test_get_week_number(self):
        week_number = StudyWeekNumberService.from_date(date=datetime.datetime.now().date())
        print(week_number)

    def test_date_by_study_week_number(self):
        date = StudyWeekNumberService.from_week_number(15)
        print(date)
