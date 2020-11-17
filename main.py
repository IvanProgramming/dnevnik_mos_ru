from pprint import pp
from datetime import datetime
from dnevnik import Client
from testing_directory.settings import *
from dnevnik.utils import *

me = Client(AUTH_TOKEN, PROFILE_ID)
lessons = me.get_lessons(datetime.today(), datetime.today())

for lesson in sort_lessons(lessons):
    print(f"{lesson.subject_name} - {lesson.get_teams_link()}")
