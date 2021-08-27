from aiohttp import request
from bson import decode

from exceptions.providers import TokenInvalidException, PhoneIsNotPresented
from model.diary_providers.base_diary_provider import BaseDiaryProvider
from model.profile import Profile
from logging import error, debug, info

class MeshDiary(BaseDiaryProvider):
    """
        MESH Diary is moscow digital dairy.
        You can find it on https://dnevnik.mos.ru
    """
    name = "Дневник МЭШ"
    token_verification_url = "https://dnevnik.mos.ru/acl/api/users"
    unique_name = "mesh"

    @staticmethod
    async def get_profile_instance(token: str) -> Profile:
        decoded_token = MeshDiary.decode_token(token)
        async with request("GET", MeshDiary.token_verification_url,
                           cookies={"auth_token": decoded_token["aupd_token"], "profile_type": "student",
                                    "profile_id": decoded_token["profile_id"]}) as resp:
            info(f"MESH Server response -> {await resp.text()}")
            if resp.status == 200:
                profile_json = (await resp.json())[0]
                if not profile_json["phone_number"]:
                    phone_number = profile_json["phone_number_ezd"]
                    if not phone_number:
                        raise PhoneIsNotPresented
                else:
                    phone_number = profile_json["phone_number"]

                return Profile(
                    name=profile_json["first_name"],
                    school_name=profile_json["profiles"][0]["school_shortname"],
                    gender=profile_json["sex"],
                    phone_number=phone_number
                )
            raise TokenInvalidException

    @staticmethod
    def decode_token(token: str):
        try:
            return decode(bytes.fromhex(token))
        except TypeError:
            raise TokenInvalidException
