from datetime import datetime
from pprint import pp

from dnevnik import Client
from testing_directory.settings import *
me = Client(AUTH_TOKEN, PROFILE_ID)
pp(me.get_homeworks(datetime(2020, 11, 16), datetime(2020, 11, 16)))
