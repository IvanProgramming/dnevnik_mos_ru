from typing import Optional

import inject
from pydantic import BaseModel, PrivateAttr

from dnevnik import Client, Teacher


class Grade(BaseModel):
    origin: str
    five: float
    hundred: float


class Mark(BaseModel):
    _client: object = PrivateAttr(None)
    id: int
    # Вес оценки
    weight: int
    # Учитель, поставивший оценку
    teacher_id: int
    # Отображаемый вид оценки
    name: int
    # Комментарий
    comment: Optional[str]
    # Урок
    schedule_lesson_id: int
    # Экзамен ли?
    is_exam: bool
    # Группа
    group_id: int
    # Предмет
    subject_id: int
    # Оценка
    grade: Optional[Grade]

    @inject.autoparams()
    def __init__(self, client: Client = None, **data):
        super().__init__(**data)
        self.grade = data['values'][0]['grade']
        self._client = client

    @property
    def teacher(self):
        return Teacher(self._client, self.teacher_id)

