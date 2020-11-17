from datetime import datetime

from dnevnik import Teacher, ClassUnit


class Lesson:
    id: int = None
    cancelled: bool = None
    comment: str = None
    duration: int = None
    is_home_based: bool = None
    is_transferred: bool = None
    lesson_datetime: datetime = None
    lesson_name: str = None
    lesson_number: int = None
    lesson_type: str = None
    replaced: bool = None
    room_id: int = None
    group_id: int = None
    subject_id: int = None
    subject_name: str = None
    # Service properties
    __client = None
    __building_id: int = None
    __class_unit_id: int = None
    __teacher_id: int = None
    UNUSED_DICT_KEYS = [
        "bell_day_timetable_id",
        "bell_id",
        "bell_timetable_id",
        "calendar_lesson_id",
        "calendar_plan_id",
        "city_building_id",
        "controllable_items",
        "course_lesson_type",
        "current",
        "date",
        "day_number",
        "didactic_units",
        "home_base_period_id",
        "homeworks_to_give",
        "homeworks_to_verify",
        "lesson_id",
        "lesson_plan_id",
        "module_id",
        "module_name",
        "ordinal",
        "periods_schedule_id",
        "schedule_id",
        "scripts",
        "scripts_new",
        "study_ordinal",
        "topic_id",
        "topic_name",
        "transferred_from_date",
        "transferred_to_date",
        "transferring_id",
        "time",
        "building_id"  # TODO add building property
    ]

    def __init__(self, client, id, class_unit_id, is_home_based, replaced, group_id, subject_id,
                 subject_name, teacher_id, lesson_number, group_name, room_id, room_name, iso_date_time, lesson_name,
                 duration, cancelled, is_transferred, comment, lesson_type):
        self.lesson_type = lesson_type
        self.comment = comment
        self.is_transferred = is_transferred
        self.cancelled = cancelled
        self.duration = duration
        self.lesson_name = lesson_name
        self.room_name = room_name
        self.room_id = room_id
        self.group_name = group_name
        self.lesson_number = lesson_number
        self.__teacher_id = teacher_id
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.group_id = group_id
        self.replaced = replaced
        self.__class_unit_id = class_unit_id
        self.id = id
        self.__client = client
        self.is_home_based = is_home_based
        self.lesson_datetime = datetime.fromisoformat(iso_date_time)

    @property
    def teacher(self):
        return Teacher(self.__client, self.__teacher_id)

    @property
    def class_unit(self):
        return ClassUnit(self.__client, self.__class_unit_id)

    def get_teams_link(self):
        if self.lesson_type == "REMOTE":
            data = self.__client.make_request("/vcs/links/", scheduled_lesson_id=self.id)
            return data["_embed"]["link_views"][0]["link_url"]
        else:
            return None
