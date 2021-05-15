import json
import requests
from datetime import datetime
from typing import List
from dnevnik import StudentProfile
from dnevnik.scheduled_items import Lesson
from dnevnik.student_homework import StudentHomework
from dnevnik.utils import remove_unused_keys, sort_lessons
from dnevnik.auth_providers.selenium_auth import SeleniumAuthorization
from dnevnik.exceptions.request_exceptions import UnknownStatusCodeError


class Client:
    """
    Клиент. Нужен для выполнения различных запросов
    """
    auth_token = None
    profile_id = None

    def __init__(self, auth_provider=SeleniumAuthorization, **auth_provider_kwargs):
        """
        Конструктор класса.
        :param auth_provider: Класс, наследующийся от класса  BaseAuthProvider. По умолчанию Selenium Auth
        :param auth_provider_kwargs: named-параметры для объекта AuthProvider
        """
        self.provider = auth_provider(**auth_provider_kwargs)
        self.provider.proceed_authorization()
        self.auth_token = self.provider.auth_token
        self.profile_id = self.provider.profile_id

    def make_request(self, method: str, raw=False, token_refresh_on_fail=True, **query_options):
        """
        Позволяет сделать запрос с передачей всех необходимых параметров. Дополнительные аргументы передаются как
        kwargs, параметр raw указывает на требования возврата без обработки модулем json, method позволяет указать
        метод API
        :param method: Адрес метода
        :param raw: Флаг, указывающий на необходимость "чистого" возврата
        :param token_refresh_on_fail: флаг, который позволяет получить токен заново, при ошибке
        :param query_options: Параметры запроса
        :return: Dict или Str (в зависимости от raw)
        """
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

        request = requests.get("https://dnevnik.mos.ru" + method, headers=parameters, params=query_options)
        if request.status_code in range(400, 501):
            # Пытаемся получить токен заново и повторить запрос
            # 500 статус код означает также проблемы с авторизацией
            if token_refresh_on_fail:
                self.provider.refresh_token()
                return self.make_request(method=method, raw=raw, token_refresh_on_fail=False, **query_options)
            else:
                raise UnknownStatusCodeError(request.status_code)
        elif request.status_code not in range(200, 300):
            raise UnknownStatusCodeError(request.status_code)
        if not raw:
            # Отпарсеный вывод
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

        date_from = datetime.today() if not date_from else date_from
        date_to = datetime.today() if not date_to else date_to

        lessons = self.make_request("/jersey/api/schedule_items",
                                    group_id=",".join(map(lambda gr: str(gr.id), self.profile.groups)),
                                    **{"from": date_from.strftime("%Y-%m-%d")}, to=date_to.strftime("%Y-%m-%d"),
                                    with_group_class_subject_info=True)
        result = []
        for lesson in lessons:
            result.append(Lesson(self, **remove_unused_keys(Lesson.UNUSED_DICT_KEYS, lesson)))
        return sort_lessons(result)
