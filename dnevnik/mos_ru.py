from datetime import datetime

import requests
from bs4 import BeautifulSoup


class MosRu:
    """ Класс для авторизации через логин/пароль Mos.Ru """
    # TODO Realize CSRF Token Bypass
    # TODO Add authorization mechanism

    _login: str = None
    _password: str = None
    OAUTH_URL = "https://login.mos.ru/sps/oauth/ae?" \
                "scope=openid+profile+blitz_user_rights+snils+contacts+blitz_change_password&" \
                "access_type=offline&" \
                "response_type=code&" \
                "redirect_uri=https://dnevnik.mos.ru/sudir" \
                "&client_id=dnevnik.mos.ru"

    def __init__(self, login, password):
        self._login = login
        self._password = password

    def dnevnik_authorization(self):
        """ Функция для проведения авторизации
            Алгоритм:
                Переходим по ссылке авторизации (allow_redirects=False!)

                    (https://login.mos.ru/sps/oauth/ae?
                    scope=openid+profile+blitz_user_rights+snils+contacts+blitz_change_password&
                    access_type=offline&
                    response_type=code&
                    redirect_uri=https://dnevnik.mos.ru/sudir&
                    client_id=dnevnik.mos.ru)

                    Получаем требуемые куки
                    Получаем отдельно mos_id
                    Переходим по редиректу в Форму Авторизации
                    Обходим CSRF токен
                    Отправляем форму
                А хрен знает что дальше """
        with requests.Session() as session:
            session.headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/78.0.3904.108 Safari/537.36 "
                              "RuxitSynthetic/1.0 v7519287627865176686 t7607367907735283829",
                "Referer": "dnevnik.mos.ru"
            }
            login_from_request = session.get(self.OAUTH_URL)
            session.get("https://stats.mos.ru/handler/handler.js?time={time}".format(time=datetime.today().timestamp()))
            login_from_bs = BeautifulSoup(login_from_request.content, "lxml")
            csrftokenw = login_from_bs.find("meta", attrs={"name": "csrf-token-value"}).attrs["value"]
            generated_token = self.csrf_generate(csrftokenw)
            login_request = session.post("https://login.mos.ru/sps/login/methods/password", data={
                "isDelayed": False,
                "login": self._login,
                "password": self._password,
                "alien": False
            }, follow_redirects=False)


    @staticmethod
    def csrf_generate(self, csrftokenw):
        """ Было два козла. Сколько? """
        pass
