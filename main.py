from pprint import pp

from dnevnik import Client
from testing_directory.settings import *

me = Client(AUTH_TOKEN, PROFILE_ID)
pp(me.make_request("/jersey/api/schedule_items", group_id=",".join(map(lambda gr: str(gr.id), me.profile.groups)),
                   **{"from": "2020-11-16"}, to="2020-11-16", with_group_class_subject_info=True))
