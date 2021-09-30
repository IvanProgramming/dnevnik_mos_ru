from typing import List

from dnevnik import School, ClassUnit
from dnevnik.utils import *


class Teacher:
    id: int = None
    created_at: datetime = None
    updated_at: datetime = None
    user_id: int = None
    name: str = None
    type: str = None
    mobility: str = None
    education_level_ids = None
    deleted: bool = None
    workload: int = None
    comment: str = None
    virtual: bool = None
    is_gap_allowed: bool = None
    for_consideration: bool = None
    is_newcomer: bool = None

    # Service properties
    __school_id: int = None
    __client = None
    __subject_ids: List[int] = None
    __class_unit_ids: List[int] = None
    __managed_class_unit_ids: List[int] = None
    __building_ids: List[int] = None
    __room_ids: List[int] = None
    __week_day_ids: List[int] = None

    def __init__(self, client, _id: int):
        self.id = _id
        self.__client = client
        data: dict = client.make_request(f"/core/api/teachers/{_id}")
        self.created_at = reformat_date(data["created_at"])
        self.updated_at = reformat_date(data["updated_at"])
        self.user_id = data["user_id"]
        self.name = data["name"]
        self.type = data["type"]
        self.education_level_ids = data["education_level_ids"]
        self.deleted = data["deleted"]
        self.workload = data["workload"]
        self.virtual = data["virtual"]
        self.is_gap_allowed = data["is_gap_allowed"]
        self.for_consideration = data["for_consideration"]
        self.is_newcomer = data["is_newcomer"]
        self.__school_id = data["school_id"]
        self.__subject_ids = data["subject_ids"]
        self.__class_unit_ids = data["class_unit_ids"]
        self.__managed_class_unit_ids = data["managed_class_unit_ids"]
        self.__building_ids = data["building_ids"]
        self.__room_ids = data["room_ids"]
        self.__week_day_ids = data["week_day_ids"]

    @property
    def school(self):
        return School(self.__client, self.__school_id)

    @property
    def class_unit_ids(self) -> List[ClassUnit]:
        res = []
        for unit_id in self.__class_unit_ids:
            res.append(ClassUnit(self.__client, unit_id))
        return res

    @property
    def managed_class_units(self) -> List[ClassUnit]:
        res = []
        for unit_id in self.__class_unit_ids:
            res.append(ClassUnit(self.__client, unit_id))
        return res
