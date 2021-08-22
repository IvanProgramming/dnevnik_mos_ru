from re import split
from typing import List


def normalize_phone(phone_number: str) -> str:
    """
    Normalizes phone number for correct work with it
    E.G:
        normalize_phone("+79999999999") -> "79999999999"
        normalize_phone("9999999999") -> "79999999999"
        normalize_phone("89999999999") -> "79999999999"
    :param phone_number: phone_number in any state
    :return: Normalized phone number
    """
    # Saving only digits
    phone_number = "".join(split("[^0-9]", phone_number))
    if len(phone_number) == 10:
        return f"7{phone_number}"
    if len(phone_number) == 11:
        if phone_number.startswith("8"):
            return f"7{phone_number[1:]}"
        if phone_number.startswith("7"):
            return phone_number


def normalize_phones(phone_numbers: List[str]) -> List[str]:
    """
    The same as previous, but iterates through list
    :param phone_numbers: phone numbers
    :return: list of normalized phone numbers
    """
    return list(map(normalize_phone, phone_numbers))
