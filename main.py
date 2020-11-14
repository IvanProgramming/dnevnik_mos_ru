from datetime import datetime
from pprint import pp

from dnevnik import Client
from settings import *
me = Client(AUTH_TOKEN, PROFILE_ID)
pp(me.get_homeworks())
