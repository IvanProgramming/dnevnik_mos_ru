from datetime import date
from pydantic import BaseModel


class AcademicYear(BaseModel):
    """ Объект учебного года """
    id: int
    # Название года для показа ({год-начала} - {год-конца})
    name: str
    # Даты начала и конца учебного года
    begin_date: date
    end_date: date
    calendar_id: int
    # Текущий ли год?
    current_year: bool
