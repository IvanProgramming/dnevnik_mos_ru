from datetime import date
from pydantic import BaseModel


class AcademicYear(BaseModel):
    """ Объект учебного года """
    id: int
    name: str
    begin_date: date
    end_date: date
    calendar_id: int
    current_year: bool
