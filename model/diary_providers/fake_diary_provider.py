from exceptions.providers import TokenInvalidException
from model.diary_providers.base_diary_provider import BaseDiaryProvider


class FakeDiaryProvider(BaseDiaryProvider):
    """
    This is parabola's fake diary provider
    Token format: {any15symbols}:{phoneNumber}(70000000000)
    """
    name = "Parabola Fake Diary"
    unique_name = "fake"

    @staticmethod
    async def is_token_correct(token: str) -> bool:
        return len(token) == 27 and len(token.split(":")[0]) == 15

    @staticmethod
    async def get_phone_number(token: str) -> str:
        print(len(token))
        if await FakeDiaryProvider.is_token_correct(token):
            return token.split(":")[1]
        raise TokenInvalidException

