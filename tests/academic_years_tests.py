from os import getenv
from unittest import TestCase

from dnevnik import Client, TokenAuthorization


class AcademicYearTest(TestCase):
    def test_all_years(self):
        client = Client(auth_provider=TokenAuthorization,
                        auth_token=getenv('auth_token'),
                        profile_id=int(getenv('profile_id')))
        academic_years = client.get_academic_years()
        self.assertGreater(len(academic_years), 1)

    def test_current_year(self):
        client = Client(auth_provider=TokenAuthorization,
                        auth_token=getenv('auth_token'),
                        profile_id=int(getenv('profile_id')))
        academic_years = client.get_academic_years(only_current_year=True)
        self.assertIs(len(academic_years), 1)
