from pprint import pp

from .homework_entry import HomeworkEntry
from .utils import *


class StudentHomework:
    id: int = None
    created_at: datetime = None
    updated_at: datetime = None
    is_ready: bool = None
    comment: str = None
    attachments: list = None
    remote_attachments: list = None

    # Service properties
    __attachment_ids = None
    __client = None
    __student_id: int = None
    __homework_entry = None
    __unused_keys_homework_entry = [
        "homework_entry_student_answer",
        "controllable_items",
        "homework_entry_comments",
        "student_ids",
        "controllable_item_ids",
        "books",
        "tests",
        "scripts",
        "update_comment",
        "is_long_term",
        "game_apps",
        "atomic_objects",
        "related_materials",
        "eom_urls",
        "is_digital_homework",
        "deleted_at"
    ]

    def __init__(self, client, id, created_at, updated_at, is_ready, comment, attachments, remote_attachments,
                 attachment_ids, homework_entry, student_id):
        self.__client = client
        self.attachments_remote = remote_attachments
        self.__student_id = student_id
        self.attachments = attachments
        self.comment = comment
        self.__attachment_ids = attachment_ids
        self.is_ready = is_ready
        self.id = id
        self.updated_at = reformat_date(updated_at)
        self.created_at = reformat_date(created_at)
        self.__homework_entry = homework_entry

    def __str__(self):
        return self.entry.description

    def __repr__(self):
        return str(self)


    @property
    def entry(self):
        if self.__homework_entry:
            for unused_key in self.__unused_keys_homework_entry:
                if unused_key in self.__homework_entry:
                    del self.__homework_entry[unused_key]
            return HomeworkEntry(self.__client, **self.__homework_entry)
        return None
