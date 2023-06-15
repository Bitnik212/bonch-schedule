"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 23:08
"""
import requests

from bonch.schedule.ISchedule import ISchedule
from bonch.schedule.lk.Client import Client
from bonch.schedule.lk.Parser import Parser


class ScheduleFromLK(ISchedule):

    def __init__(self, session_id: str):
        self.client = Client(session_id)
        self.parser = Parser(self.client)

    def today(self):
        try:
            response = self.client.schedule_page()
            if len(response.text) < 400:
                return {'status': 401}
            else:
                try:
                    res = self.parser.parse_today(response.text)
                    if res['status'] == 404:
                        return {"status": 404}
                    else:
                        return {"status": 200, "response": res['response']}
                except AttributeError:
                    return {"status": 404}
        except requests.exceptions.Timeout:  # or requests.exceptions.ReadTimeout
            return {"status": 523}

    def week(self, number: int | None = None):
        # todo сделаит обработки событий на все случаи жизни
        response = self.client.schedule_page(week=number) if number != 0 and not None else self.client.schedule_page()
        if response.text.find("Занятий не найдено") != -1:
            resp = {"status": 404}
        else:
            resp = {"status": 200, "response": self.parser.parse_week(response.text)}
        return resp
