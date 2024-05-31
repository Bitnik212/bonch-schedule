from unittest import TestCase

import requests

from bonch.schedule.site.SiteScheduleType import SiteScheduleType
from bonch.schedule.site.groups.GroupListService import GroupListService


class TestGroupList(TestCase):

    def setUp(self):
        self.service = GroupListService(requests.session())

    def test_get_groups(self):
        result = self.service.faculties(SiteScheduleType.FULL_TIME_AND_EVENING_LESSONS)
        print(f"{result=}")
        self.assertGreater(len(result), 0)
