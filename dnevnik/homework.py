from datetime import datetime
from .utils import reformat_date

class Homework:
    """ Домашняя работа """
    id: int = None
    created_at: datetime = None
    updated_at: datetime = None
    is_required: bool = None
    mark_requires: bool = None
    date_assigned_on: datetime = None
    date_prepared_for: datetime = None

    # Service properties
    __teacher_id: int = None
    __subject_id: int = None
    __group_id: int = None
    __client: int = None

    def __init__(self, client, _id, created_at, updated_at, teacher_id, subject_id, is_required, mark_required, group_id,
                 date_assigned_on, date_prepared_for):
        """ Как я понимаю, эту фигню тоже через API получить нельзя, так что будем указываться напрямую """
        self.mark_required = mark_required
        self.is_required = is_required
        self.__subject_id = subject_id
        self.__teacher_id = teacher_id
        self.updated_at = reformat_date(updated_at)
        self.created_at = reformat_date(created_at)
        self.date_assigned_on = reformat_date(date_assigned_on)
        self.date_prepared_for = reformat_date(date_prepared_for)
        self.__group_id = group_id
        self.id = _id
        self.__client = client

