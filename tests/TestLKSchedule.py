from unittest import TestCase

import requests

from bonch.common.model.DayScheduleModel import DayScheduleModel
from bonch.common.model.WeekScheduleModel import WeekScheduleModel
from bonch.schedule.ScheduleBuilder import ScheduleBuilder


class TestLKSchedule(TestCase):

    def setUp(self):
        builder = ScheduleBuilder(
            session=requests.session()
        )
        self.client = builder.with_lk(session_id="changeme")

    def test_today(self):
        today = self.client.today()
        print(f"{today=}")
        self.assertIsInstance(today, DayScheduleModel)

    def test_weeK(self):
        week = self.client.week()
        print(f"{week=}")
        self.assertNotEqual(week, [])
        self.assertIsInstance(week, WeekScheduleModel)
