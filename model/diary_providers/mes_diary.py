from aiohttp import request

from exceptions.providers import TokenInvalidException
from model.diary_providers.base_diary_provider import BaseDiaryProvider


class MesDiary(BaseDiaryProvider):
    """
        MES Diary (Moscow Electronic School) is moscow electron dairy.
        You can find it on https://dnevnik.mos.ru
    """
    name = "Дневник МЭШ"
    token_verification_url = "https://dnevnik.mos.ru/lms/api/sessions"
    unique_name = "mes"

    @staticmethod
    async def get_phone_number(token: str, sudir_access_token: str = None) -> str:
        # TODO: Solve problem with this token verify endpoint!
        async with request("POST", MesDiary.token_verification_url, json={
            "auth_token": token
        }) as resp:
            print(await resp.text())
            if resp.status == 200:
                return (await resp.json())["info"]["phone_number"]
            raise TokenInvalidException
