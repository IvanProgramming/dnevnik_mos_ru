from bson import encode


def generate_token(name, school_name, phone_number, gender="male"):
    return encode({
        "name": name,
        "school_name": school_name,
        "phone_number": phone_number,
        "gender": gender
    }).hex()
