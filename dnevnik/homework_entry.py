from typing import List
from .utils import *


class HomeworkEntry:
    id: int = None
    created_at: datetime = None
    updated_at: datetime = None
    description: str = None
    duration: int = None
    no_duration: bool = None
    attachments: list = None
    homework = None

    # Service properties
    __homework_id: int = None
    __attachment_ids: List[int] = None
    __client = None

    def __init__(self, client, id: int, created_at: str, updated_at: str, description: str, duration: int,
                 no_duration: bool, attachment_ids: List[int], attachments: list, homework_id: int, homework: dict):
        self.__homework_id = homework_id
        self.duration = duration
        self.description = description
        self.attachments = attachments
        self.__attachment_ids = attachment_ids
        self.no_duration = no_duration
        self.updated_at = reformat_date(updated_at)
        self.created_at = reformat_date(created_at)
        self.id = id
        self.__client = client
        self.homework = homework
