from typing import List

from dnevnik import ClassUnit
from .utils import *


class Group:
    """ Класс для группы """
    __client = None
    id: int = None
    name: str = None
    begin_date: datetime = None
    end_date: datetime = None

    # Service properties
    __class_units_ids: List[int] = None
    __user_profile_id: int = None

    def __init__(self, client, id: int, name: str, begin_date: str, end_date: str, class_unit_ids: List[int], user_profile_id: int):
        """ В отличии от других классов, этот не может быть получен через API, так что может быть составлени лишь из
            доп данных ответа """
        self.__client = client
        self.id = id
        self.name = name
        self.begin_date = reformat_birthday_date(begin_date)
        self.end_date = reformat_birthday_date(end_date)
        self.__class_units_ids = class_unit_ids
        self.__user_profile_id = user_profile_id

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    @property
    def class_units(self):
        """ Возвращает список объектов ClassUnit """
        units_list = []
        for class_unit_id in self.__class_units_ids:
            units_list.append(ClassUnit(self.__client, class_unit_id))
        return units_list

