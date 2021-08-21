from base64 import b64decode
from json import loads

from exceptions.providers import TokenInvalidException
from model.diary_providers.base_diary_provider import BaseDiaryProvider
from model.profile import Profile


class FakeDiaryProvider(BaseDiaryProvider):
    """
    This is parabola's fake diary provider
    Token format: {any15symbols}: (json with fields "name", "")
    """
    name = "Parabola Fake Diary"
    unique_name = "fake"

    @staticmethod
    async def is_token_correct(token: str) -> bool:
        return True

    @staticmethod
    async def get_phone_number(token: str) -> str:
        if await FakeDiaryProvider.is_token_correct(token):
            token_json = loads(b64decode(token.split(":")[1]).decode("utf-8"))
            return token_json["phone_number"]
        raise TokenInvalidException

    @staticmethod
    async def get_profile_instance(token: str) -> Profile:
        if await FakeDiaryProvider.is_token_correct(token):
            token_json = loads(b64decode(token.split(":")[1]).decode("utf-8"))
            return Profile(**token_json)
        raise TokenInvalidException
