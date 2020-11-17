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


def remove_unused_keys(unused_keys_list: list, source: dict):
    """ Позволяет по списку ключей удалить из словаря ненужные значения """
    for unused_key in unused_keys_list:
        if unused_key in source:
            del source[unused_key]
    return source


def sort_lessons(lessons):
    return sorted(lessons, key=lambda l: l.lesson_number)
