from datetime import datetime


def reformat_date(date_str: str) -> datetime:
    """ Превращает дату в объект datetime """
    if date_str:
        if len(date_str) == 8:
            if datetime.strptime(date_str, "%d.%m.%y"):
                return datetime.strptime(date_str, "%d.%m.%y")
            return datetime.strptime(date_str, "%d-%m-%Y")
        return datetime.strptime(date_str, "%d.%m.%Y %H:%M")
    return None


def reformat_birthday_date(date_str: str) -> datetime:
    """ Превращает дату рождения в объект datetime """
    return datetime.strptime(date_str, "%d.%m.%Y")
