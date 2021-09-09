from json import dumps

import requests
from requests import session
from urllib3.util import parse_url
from ..base_auth_provider import BaseAuthProvider
from dnevnik.auth_providers.code_based_provider import CodeBasedProvider


class BLoginProvider(BaseAuthProvider):
    """ Auth Provider, основанный на Куках из login.mos.ru. Можно достать в настройках google chrome """
    OAUTH_URL = "https://login.mos.ru/sps/oauth/ae?response_type=code&access_type=offline&client_id=dnevnik.mos.ru&scope=openid+profile+birthday+contacts+snils+blitz_user_rights+blitz_change_password&redirect_uri=https%3A%2F%2Fschool.mos.ru%2Fauth%2Fmain%2Fcallback"

    def __init__(self, bfp, bkd, blu, blg, bud, bls):
        """ Каждый параметр Cookie """
        self.bud = bud
        self.blu = blu
        self.bkd = bkd
        self.bfp = bfp
        self.blg = blg
        self.bls = bls
        self.code_provider = None

    def proceed_authorization(self):
        req = requests.get(self.OAUTH_URL, cookies={
            "bud": self.bud,
            "blu": self.blu,
            "bkd": self.bkd,
            "bfp": self.bfp,
            "blg": self.blg,
            "bls": self.bls
        })
        self.code_provider = CodeBasedProvider(callback_code=parse_url(req.url).query.split("=")[1])
        self.code_provider.proceed_authorization()
        self.profile_id = self.code_provider.profile_id
        self.auth_token = self.code_provider.auth_token

    def refresh_token(self):
        self.proceed_authorization()
