import requests
from requests import session, get

from ..base_auth_provider import BaseAuthProvider


class CodeBasedProvider(BaseAuthProvider):
    """ CodeBasedProvider - провайдер авторизации, который испоьлзует callback_code, который генерируется на странице
        авторизации. Теоретически код можно даже обновлять, а значит это можно использовать бесконечно долго
    """
    def __init__(self, callback_code, profile_index=0):
        """
        Конструктор браузера

        :param callback_code: callback_code. Вытащить можно из адресной строки
        """
        self.profiles = None
        self.callback_code = callback_code
        self.profile_index = profile_index

    def proceed_authorization(self):
        ss = session()
        ss.get(f"https://school.mos.ru/auth/main/callback?code={self.callback_code}")

        req = ss.get(f"https://school.mos.ru/v1/sudir/main/callback?code={self.callback_code}")
        role_id = req.json()["roles"][0]["id"]
        subsystem_id = req.json()["roles"][0]["subsystems"][0]
        aupd = ss.cookies['aupd_token']
        new_aupd = get(f"https://school.mos.ru/v2/token/refresh?role={role_id}&subsystem_id={subsystem_id}",
                          headers={
                              "authorization": f"Bearer {aupd}"
                          }).content.decode("utf-8")
        ss.get("https://dnevnik.mos.ru/aupd/auth")
        resp = requests.post("https://dnevnik.mos.ru/lms/api/sessions", json={"auth_token": aupd})
        self.profiles = resp.json()["profiles"]
        self.profile_id = resp.json()["profiles"][self.profile_index]["id"]
        self.auth_token = resp.json()["authentication_token"]

    def refresh_token(self):
        pass
