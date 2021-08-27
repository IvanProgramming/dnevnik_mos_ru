from model.connections import connections

def get_recepient_fcms(phones: list):
    profiles_cursor = connections.profiles_db.find(
        {"phone_number": {"$in": phones}}, {"_id": 0, "fcm": 1})
    fcms_list = []
    for profile_fcms in profiles_cursor:
        fcms_lis + profile_fcms
    return fcms_list
