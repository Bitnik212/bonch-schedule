"""
    @author Николай Витальевич Никоноров (Bitnik212)
    @date 14.06.2023 23:35
"""
import datetime
from bs4 import BeautifulSoup as bs, NavigableString, BeautifulSoup

from bonch.schedule.lk.Client import Client


class Parser:

    def __init__(self, client: Client):
        self.client = client

    @property
    def now_date(self) -> str:
        return datetime.datetime.now().isoformat().split('T')[0].split("-")[2] + '.' + \
                       datetime.datetime.now().isoformat().split('T')[0].split("-")[1] + '.' + \
                       datetime.datetime.now().isoformat().split('T')[0].split("-")[0]

    @property
    def reverse_now_date(self) -> str:
        return datetime.datetime.now().isoformat().split('T')[0]

    def parse_today(self, content: str):
        """
        Парсер расписания на день

        :param content:
        :return: list
        """
        soup = self.soup(content)
        try:
            resp = []
            items = soup.find_all('tr', attrs={'style': 'background: #FF9933 !important '})
            for item in items:
                parsed_item = self.__parse_item(item, self.reverse_now_date)
                resp.append(parsed_item)
            return {"status": 200, "response": resp}
        except IndexError as e:
            return {"status": 404}

    def parse_week(self, content: str):
        """
        Парсер недели

        :param soup:
        :return: list
        """
        soup = self.soup(content)
        resp = {
            "Понедельник": {
                "date": "",
                "items": []
            },
            "Вторник": {
                "date": "",
                "items": []
            },
            "Среда": {
                "date": "",
                "items": []
            },
            "Четверг": {
                "date": "",
                "items": []
            },
            "Пятница": {
                "date": "",
                "items": []
            },
            "Суббота": {
                "date": "",
                "items": []
            }
        }  # Должны быть такими же как в лк
        dates = list(resp.keys())

        tbody = soup.find("tbody", attrs={'style': 'text-shadow:none;'})
        for item in tbody.find_all("tr"):
            now_date_index = dates.index(item.b.text) if item.b.text in dates else -1
            if now_date_index != -1:
                now_date = dates[now_date_index]
                now_datetime = str(item.small.text)
            else:
                parsed_item = self.__parse_item(item, self.reverse_date(now_datetime))
                parent_items = resp.get(now_date).get("items") if resp.get(now_date).get("items") is not None else []
                parent_items.append(parsed_item)
                resp.update(
                    {
                        now_date: {
                            "date": now_datetime,
                            "items": parent_items
                        }
                    }
                )
        return resp

    @staticmethod
    def soup(content: str) -> BeautifulSoup:
        return bs(content, "html.parser")

    @staticmethod
    def __parse_item(item: NavigableString, revnowdate: str):
        """
        Парсер пары

        :param item: soup элемент с парой
        :param revnowdate: str. Время
        :return: dict
        """
        sub_items = item.find_all('td')

        def parse_time(sub_item: NavigableString) -> dict:
            """
            Парсинг времени

            :param sub_item:
            :return:
            """
            para_number = sub_item.text[:sub_item.text.index("(")].replace(" ", "")
            para_time_str = sub_item.text[sub_item.text.index("("):]
            para_time_str = para_time_str.replace("(", "").replace(")", "").replace(" ", "")  # clean time
            if len(para_time_str) == 10:
                para_time_str = "0" + para_time_str
            return {
                "number": para_number,
                "start": revnowdate.replace('.', '-') + "T" + para_time_str.split('-')[0] + ":00",
                "end": revnowdate.replace('.', '-') + "T" + para_time_str.split('-')[1] + ":00"
            }

        def parse_item(sub_item: NavigableString) -> dict:
            """
            Парсинг предмета. Его название и тип пары

            :param sub_item:
            :return:
            """
            item_type = sub_item.find("small").text
            item_type = str(item_type.split("занятие началось")[0])  # Убираем лишнуюю часть
            item_type = item_type.strip(" ")  # Убираем пробелы по бокам
            item_title = sub_item.find("b").text
            return {
                "title": item_title,
                "type": item_type
            }

        def parse_address(sub_item: NavigableString) -> dict:
            """
            Парсинг адреса

            :param sub_item:
            :return:
            """
            sub_item_str = sub_item.text.replace(" ", "")
            sub_item_split = sub_item_str.split(";")
            cabinet_number = sub_item_split[0]
            building = sub_item_split[1]
            return {
                "cabinet_number": cabinet_number,
                "building": building
            }

        def parse_professor(sub_item: NavigableString) -> str:
            return sub_item.text

        para_time = parse_time(sub_items[0])
        para_subject = parse_item(sub_items[1])
        para_address = parse_address(sub_items[3])
        para_professor = parse_professor(sub_items[4])

        data = {}
        data.update(para_time)
        data.update(para_subject)
        data.update(para_address)
        data.update(
            {
                "professor": para_professor
            }
        )
        return data

    @staticmethod
    def __convert_date_to_ico(date):
        """
        конвертирование даты в формат ico
        :param date:
        :return:
        """
        return date.split(".")[2] + '-' + date.split(".")[1] + '-' + date.split(".")[0]

    @staticmethod
    def reverse_date(date: str) -> str:
        """
        from 14.06.2023 to 2023-06-15

        :param date: dd.MM.YYYY
        :return: YYYY-MM-dd
        """
        date_split = date.split(".")
        return f"{date_split[2]}-{date_split[1]}-{date_split[0]}"
