from aiohttp import request

from exceptions.providers import TokenInvalidException, PhoneIsNotPresented
from model.diary_providers.base_diary_provider import BaseDiaryProvider
from model.profile import Profile


class MeshDiary(BaseDiaryProvider):
    """
        MESH Diary is moscow digital dairy.
        You can find it on https://dnevnik.mos.ru
    """
    name = "Дневник МЭШ"
    token_verification_url = "https://dnevnik.mos.ru/lms/api/sessions"
    unique_name = "mesh"

    @staticmethod
    async def get_phone_number(token: str, sudir_access_token: str = None) -> str:
        async with request("POST", MeshDiary.token_verification_url, json={
            "auth_token": token
        }) as resp:
            if resp.status == 200:
                return (await resp.json())["info"]["phone_number"]
            raise TokenInvalidException

    @staticmethod
    async def get_profile_instance(token: str) -> Profile:
        async with request("POST", MeshDiary.token_verification_url, json={
            "auth_token": token
        }) as resp:
            if resp.status == 200:
                response_dict = await resp.json()
                if response_dict["phone_number"] == "":
                    raise PhoneIsNotPresented
                return Profile(name=response_dict["first_name"],
                               phone_number=response_dict["phone_number"],
                               school_name=response_dict["profiles"][0]["school_shortname"])
            raise TokenInvalidException
