from datetime import datetime
from random import randint
from time import sleep

import requests
from bs4 import BeautifulSoup
from urllib3.util import parse_url

from ..base_auth_provider import BaseAuthProvider
from dnevnik.exceptions import CredentialsInvalidException, UnknownErrorException, IpBanError


class RequestsAuthorization(BaseAuthProvider):
    """ Класс для авторизации через логин/пароль Mos.Ru """

    _login: str = None
    _password: str = None
    OAUTH_URL = "https://login.mos.ru/sps/oauth/ae?" \
                "scope=openid+profile+blitz_user_rights+snils+contacts+blitz_change_password&" \
                "access_type=offline&" \
                "response_type=code&" \
                "redirect_uri=https://dnevnik.mos.ru/sudir" \
                "&client_id=dnevnik.mos.ru"
    EVENT = "361e8e40a297ed04767fb8c93b686874942ae3159e4445afa9fd864b4b501ee1"
    CSRF_ENDPOINT = "https://login.mos.ru/7ccd851171c76f27e541d264c4186df3"
    FORM_ACTION = "https://login.mos.ru/sps/login/methods/password"
    auth_token = 0

    def __init__(self, login: str, password: str, **requests_params):
        """
        Конструктор объекта
        :param login: Логин пользователя
        :param password: Пароль пользователя
        :param requests_params: Необязательный параметр. Позволяет добавить к каждому запросу дополнительные параметры.
        Список параметров можно найти в документации (https://requests.readthedocs.io/en/latest/api/#requests.request).
        """
        self._login: str = login
        self._password = password
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                " Chrome/89.0.4389.91 Safari/537.36"})
        self.requests_params: dict = requests_params

    def proceed_authorization(self):
        """ Функция для проведения авторизации, возвращает ответ сервера с токеном и профайлами """
        oauth_page = self.session.get(self.OAUTH_URL, **self.requests_params)
        if oauth_page.status_code == 403:
            raise IpBanError
        sleep(randint(10, 30) / 10)
        self.session.get(
            "https://stats.mos.ru/handler/handler.js?time={time}".format(time=datetime.today().timestamp()), timeout=5)
        sleep(randint(10, 30) / 10)
        bs = BeautifulSoup(oauth_page.content.decode("utf-8"), features="lxml")
        csrftokenw = bs.select_one("meta[name=csrf-token-value]")
        csrf_token = self.generate_csrf_token(csrftokenw.attrs["content"])
        data = {
            "login": self._login,
            "password": self._password,
            "csrftokenw": csrf_token,
            "isDelayed": False,
            "alien": False
        }
        login_request = self.session.post(self.FORM_ACTION, data=data, allow_redirects=False)
        if login_request.status_code in range(301, 400):
            redirect_uri = login_request.headers["Location"]
            code = parse_url(redirect_uri).query.split("=")[1]
            req = self.session.get("https://dnevnik.mos.ru/lms/api/sudir/oauth/te?code={}".format(code), headers={
                "Accept": "application/vnd.api.v3+json"
            }, timeout=5)
            return req.json()
        elif login_request.status_code == 200:
            bs = BeautifulSoup(login_request.content.decode("utf-8"))
            danger_element = bs.select_one("blockquote.blockquote-danger")
            if danger_element:
                raise CredentialsInvalidException(danger_element.text)
            else:
                raise UnknownErrorException
        elif login_request.status_code == 403:
            raise IpBanError
        else:
            raise UnknownErrorException

    def generate_csrf_token(self, csrftokenw) -> str:
        headers = {
            "x-csrftokenw": csrftokenw,
            "x-requested-with": "XMLHttpRequest",
            "x-ajax-token": self.EVENT
        }
        try:
            request = self.session.get(self.CSRF_ENDPOINT, headers=headers)
            if request.status_code != 200:
                raise UnknownErrorException
            return self.session.cookies["csrf-token-value"]
        except KeyError:
            raise UnknownErrorException
