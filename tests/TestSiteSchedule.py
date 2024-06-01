from unittest import TestCase
import requests
from bonch.schedule.ScheduleBuilder import ScheduleBuilder
from bonch.schedule.site.SiteScheduleType import SiteScheduleType


class TestSiteSchedule(TestCase):

    def setUp(self):
        builder = ScheduleBuilder(
            session=requests.session()
        )

        self.client = builder.with_site(55522, SiteScheduleType.FULL_TIME_AND_EVENING_LESSONS)
        # self.client = builder.with_site(55763, SiteScheduleType.SESSION_SCHEDULE_FOR_CORRESPONDENCE)

    def test_week_schedule(self):
        result = self.client.week()
        print(f"{result=}")
        self.assertIsNotNone(result)

    def test_today_schedule(self):
        result = self.client.today()
        print(f"{result=}")
        self.assertIsNotNone(result)
