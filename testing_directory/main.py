from pprint import pp

from dnevnik import Client
from .settings import *
me = Client(AUTH_TOKEN, PROFILE_ID)
pp(me.make_request("/core/api/student_homeworks", begin_prepared_date="12.11.2020", end_prepared_date="12.11.2020"))
pp("")
pp(me.make_request("/core/api/student_homeworks/280243649"))
