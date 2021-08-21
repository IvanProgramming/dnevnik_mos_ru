from base64 import b64encode
from json import dumps


def generate_token(name, phone, school):
    token = "q" * 15 + ":"
    token += b64encode(dumps({
        "name": name,
        "phone_number": phone,
        "school_name": school
    }).encode("utf-8")).decode("utf-8")
    return token
