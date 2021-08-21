from datetime import datetime, timedelta

from exceptions.providers import TokenInvalidException
from model.connections import connections
from settings import EXP_TIME


def exists(token, diary):
    """
    This method checks, if token with specified diary already cached
    :param token: auth token
    :param diary: diary provider unique name
    :return: True if already cache of False if token is not cached yet
    """
    if connections.tokens_db.find_one({"token": token, "diary": diary}):
        return True
    return False


async def save_token(token, diary, phone_number):
    """
    This method creates new Document in tokens collection, that stores token, diary and phone number (for profile)
    :param token: auth token
    :param diary: diary provider unique name
    :param phone_number: phone number of user (can be obtained in special method of diary provider)
    """
    if not exists(token, diary):
        token_document = {
            "expiresAt": datetime.utcnow() + timedelta(seconds=EXP_TIME),
            "diary": diary,
            "token": token,
            "phone_number": phone_number
        }
        connections.tokens_db.insert_one(token_document)


async def get_cached_phone(token, diary):
    """
    This method returns cached phone from DB-storage
    :param token: auth token
    :param diary: diary provider unique name
    :return: Phone number of user
    :raise TokenInvalidException if token/diary-alias is not stored in database
    """
    if exists(token, diary):
        data = connections.tokens_db.find_one({"token": token, "diary": diary})
        return data["phone_number"]
    raise TokenInvalidException
