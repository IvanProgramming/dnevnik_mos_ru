from unittest import TestCase, skip
from os import getenv

from dnevnik.client import Client
from dnevnik.auth_providers import TokenAuthorization, RequestsAuthorization
from dnevnik.exceptions import UnknownTokenError, CredentialsInvalidException


class TokenAuthorizationTest(TestCase):
    def test_valid_auth(self):
        """ Testing valid token authorization """
        auth_token = getenv("auth_token")
        profile_id = int(getenv("profile_id"))
        client = Client(auth_provider=TokenAuthorization, auth_token=auth_token, profile_id=profile_id)
        self.assertIsNotNone(client.profile)

    def test_invalid_auth(self):
        auth_token = 'a'
        profile_id = 3051555
        client = Client(auth_provider=TokenAuthorization, auth_token=auth_token, profile_id=profile_id)
        self.assertRaises(UnknownTokenError, lambda: client.profile)


class SeleniumAuthorizationTest(TestCase):
    def test_valid_auth(self):
        login = getenv('mosru_login')
        password = getenv('mosru_password')
        client = Client(login=login, password=password, executable_path=getenv('selenium_path'))
        self.assertIsNotNone(client.profile)

    def test_invalid_auth(self):
        login = 'a'
        password = 'b'
        try:
            client = Client(login=login, password=password, executable_path=getenv('selenium_path'))
            self.assertIsNotNone(client.profile)
        except CredentialsInvalidException as e:
            self.assertIsNotNone(e)


@skip('RequestsAuth is not working now')
class RequestsAuthorizationTest(TestCase):
    def test_valid_auth(self):
        login = getenv('mosru_login')
        password = getenv('mosru_password')
        client = Client(auth_provider=RequestsAuthorization, login=login, password=password)
        self.assertIsNotNone(client.profile)

    def test_invalid_auth(self):
        login = 'a'
        password = 'b'
        try:
            client = Client(auth_provider=RequestsAuthorization, auth_token=login, profile_id=password)
            self.assertIsNotNone(client.profile)
        except CredentialsInvalidException as e:
            self.assertIsNotNone(e)
