from datetime import datetime
from pprint import pp
from typing import List
import json

from dnevnik import Teacher
from dnevnik.school import School
from dnevnik.class_unit import ClassUnit
from dnevnik.group import Group
from dnevnik.utils import *


class StudentProfile:
    """ Объект, возвращаемый методом /core/api/student_profile"""
    __client = None
    id: int = None
    created_at: datetime = None
    updated_at: datetime = None
    deleted_at: datetime = None
    transferred: bool = None
    study_mode_id: int = None
    user_name: str = None
    short_name: str = None
    change_password_required: bool = None
    birth_date: datetime = None
    mentors: List[Teacher] = None
    age: int = None
    sex: str = None
    deleted: bool = None

    # Service properties
    __groups_list: list = None
    __school_id: int = None
    __class_unit_id: int = None

    def __init__(self, client):
        """ Получаем данные и записываем их в объект """
        self.__client = client
        self.id = client.profile_id
        data = client.make_request(f"/core/api/student_profiles/{self.id}", with_groups=True)
        self.created_at = reformat_date(data["created_at"])
        self.updated_at = reformat_date(data["updated_at"])
        self.deleted_at = reformat_date(data["deleted_at"])
        self.transferred = data["transferred"]
        self.study_mode_id = data["study_mode_id"]
        self.username = data["user_name"]
        self.short_name = data["short_name"]
        self.change_password_required = data["change_password_required"]
        self.birth_date = reformat_birthday_date(data["birth_date"])

        self.__school_id = data["school_id"]
        self.__class_unit_id = data["class_unit"]["id"]
        self.__groups_list = data["groups"]

    @property
    def class_unit(self):
        """ Свойство, используется для получение объекта Class Unit """
        return ClassUnit(self.__client, class_unit_id=self.__class_unit_id)

    @property
    def school(self):
        """ Свойство, используется дл получения объекта School """
        return School(self.__client, school_id=self.__school_id)

    @property
    def groups(self):
        """ Свойство, для получения групп, в которых состоит учащийся """
        groups_list = []
        for group in self.__groups_list:
            del group["subgroup_ids"]
            del group["metagroup"]
            del group["archived"]
            groups_list.append(Group(self.__client, **group))
        return groups_list

