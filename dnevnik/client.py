import json
import requests
from datetime import datetime
from typing import List
from dnevnik import StudentProfile
from dnevnik.mos_ru import MosRu
from dnevnik.scheduled_items import Lesson
from dnevnik.student_homework import StudentHomework
from dnevnik.utils import remove_unused_keys, sort_lessons


class Client:
    """
    Клиент. Нужен для выполнения различных запросов
    """
    auth_token = None
    profile_id = None
    mos_ru_obj = None
    profile_index: int = None

    def __init__(self, profile_id: int = 0, login: str = None, password: str = None, auth_token=None,
                 profile_index: int = 0, use_selenium: bool = True, selenium_executable_path: str = "chromedriver"):
        """
        Конструктор клиента:
        param auth_token: Токен авторизации
        param profile_id: ID профиля
        param login: Логин профиля на Mos.Ru
        param password: Пароль профиля на Mos.Ru
        profile_index: Номер профиля в аккаунте, начиная с нуля. Не работает при использовании Selenium
        use_selenium: Флаг, определяющий использование Selenium
        selemium_executable_path: Путь до исполняемого файла. Настоятельно рекомендуется выставить, если этот путь не прописан в path
        """
        self.auth_token = auth_token
        self.profile_id = profile_id
        self.profile_index = profile_index

        if self.auth_token and self.profile_id != 0:
            pass
        # Логин через Selenium вместе с паролем и логином
        elif use_selenium and login and password:
            from dnevnik.selenium_auth import SeleniumAuth
            self.selenium = SeleniumAuth(login, password, selenium_executable_path)
            self.auth_token = self.selenium.auth_token
            # Да, я знаю, это надо починить!!!
            self.profile_id = self.selenium.profile_id
        # Логин через реквесты (устаревший метод)
        elif login and password and not use_selenium:
            self.mos_ru_obj = MosRu(login, password)
            answer = self.mos_ru_obj.dnevnik_authorization()
            self.auth_token = answer["user_details"]["authentication_token"]
            if not profile_id:
                self.profile_id = answer["user_details"]["profiles"][self.profile_index]["id"]
        print(f"[i] Auth-Token = {self.auth_token}\n[i] Profile-Id = {self.profile_id}")

    def make_request(self, method: str, raw=False, **query_options):
        """ Позволяет сделать запрос с передачей всех необходимых параметров. Дополнительные аргументы передаются как
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
            "Accept": "*/*"
        }
        data = query_options
        request = requests.get("https://dnevnik.mos.ru" + method, headers=parameters, params=query_options)
        if request.status_code in range(400, 500):
            print(request.content.decode("utf-8"))
            if not self.selenium:
                answer = self.mos_ru_obj.dnevnik_authorization()
                if answer:
                    self.auth_token = answer["user_details"]["authentication_token"]
                else:
                    raise Exception("Unauthorizated (403)!")
            else:
                self.selenium.refresh_token()
                self.auth_token = self.selenium.auth_token
        elif request.status_code not in range(200, 300):
            print(request.content.decode("utf-8"))
            raise Exception(f"Incorrect status_code ({request.status_code})!")
        if not raw:
            return json.loads(request.content)
        return request.content.decode("utf-8")

    @property
    def profile(self) -> StudentProfile:
        """ Свойство позволяет получить профиль пользователя """
        return StudentProfile(self)

    def get_homeworks(self, begin_prepared_date: datetime = None, end_prepared_date: datetime = None) -> \
            List[StudentHomework]:
        """ 
        Шорткат для получения домашних работ:
        param begin_prepared_date: Указывает на то, с какого числа нужно получить дз (По умолчанию сегодня)
        param end_prepared_date: Указывает на то, по какое число нужно получить дз (По умолчанию сегодня)
        """
        homeworks = []
        begin_prepared_date = datetime.today() if not begin_prepared_date else begin_prepared_date
        end_prepared_date = datetime.today() if not end_prepared_date else end_prepared_date
        homeworks_raw = self.make_request("/core/api/student_homeworks",
                                          begin_prepared_date=begin_prepared_date.strftime("%d.%m.%Y"),
                                          end_prepared_date=end_prepared_date.strftime("%d.%m.%Y"))
        for homework in homeworks_raw:
            del homework["deleted_at"]
            del homework["homework_entry_id"]
            del homework["student_name"]
            homeworks.append(StudentHomework(self, **homework))
        return homeworks

    def get_lessons(self, date_from: datetime = None, date_to: datetime = None):
        """
        Шорткат для получения уроков:
        param date_from: Указывает с какого дня надо получить уроки (По умолчанию сегодня)
        param date_to: Указывает по какой день надо получить уроки (По умолчанию сегодня)
        """
        if not date_to:
            date_to = datetime.today()
        if not date_from:
            date_from = datetime.today()
        lessons = self.make_request("/jersey/api/schedule_items",
                                    group_id=",".join(map(lambda gr: str(gr.id), self.profile.groups)),
                                    **{"from": date_from.strftime("%Y-%m-%d")}, to=date_to.strftime("%Y-%m-%d"),
                                    with_group_class_subject_info=True)
        result = []
        for lesson in lessons:
            result.append(Lesson(self, **remove_unused_keys(Lesson.UNUSED_DICT_KEYS, lesson)))
        return sort_lessons(result)

