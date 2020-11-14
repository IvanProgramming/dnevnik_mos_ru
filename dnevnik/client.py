from datetime import datetime
from typing import List

import requests
import json
import dnevnik
from dnevnik.homework import Homework


class Client:
    """
    Клиент. Нужен для выполнения различных запросов
    """
    auth_token = None
    profile_id = None

    def __init__(self, auth_token: str, profile_id: int):
        """
        Конструктор клиента:
        param auth_token: Токен авторизации:
        param profile_id: ID профиля
        """
        self.auth_token = auth_token
        self.profile_id = profile_id

    def make_request(self, method: str, raw=False, **query_options):
        """ Позволяет сделать запрос с передачей всех необходимых параметровю. Дополнительные аргументы передаются как
            kwargs, параметр raw указывает на требования возврата без обработки модулем json, method позволяет указать
            метод API """
        parameters = {
            "Auth-Token": self.auth_token,
            "Content-Type": "application/json",
            "Profile-Id": str(self.profile_id),
            "Profile-Type": "student",
            "Referer": "https://dnevnik.mos.ru/diary/diary/lessons",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/80.0.3987.87 Safari/537.36 RuxitSynthetic/1.0 v8662719366318635631 "
                          "t6281935149377429786 ",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Accept": "*/*"
        }
        data = query_options
        request = requests.get("https://dnevnik.mos.ru" + method, headers=parameters, params=query_options)
        if request.status_code != 200:
            print(request.content.decode("utf-8"))
            raise Exception(f"Incorrect status_code ({request.status_code})!")
        if not raw:
            return json.loads(request.content)
        return request.content.decode("utf-8")

    @property
    def profile(self) -> dnevnik.student_profile.StudentProfile:
        """ Свойство, позволяет получить профиль пользователя """
        return dnevnik.student_profile.StudentProfile(self)

    def get_homeworks(self, begin_prepared_date: datetime) -> List[Homework]:
        """ Свойство для получаения домашних работ """

