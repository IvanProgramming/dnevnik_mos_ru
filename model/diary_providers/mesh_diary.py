from aiohttp import request
from bson import decode

from exceptions.providers import TokenInvalidException
from model.diary_providers.base_diary_provider import BaseDiaryProvider
from model.profile import Profile


class MeshDiary(BaseDiaryProvider):
    """
        MESH Diary is moscow digital dairy.
        You can find it on https://dnevnik.mos.ru
    """
    name = "Дневник МЭШ"
    token_verification_url = "https://school.mos.ru/v1/sudir/user/info"
    unique_name = "mesh"

    @staticmethod
    async def get_phone_number(token: str) -> str:
        decoded_token = MeshDiary.decode_token(token)

    @staticmethod
    async def get_profile_instance(token: str) -> Profile:
        decoded_token = MeshDiary.decode_token(token)
        async with request(
                "POST", MeshDiary.token_verification_url,
                headers={"Authorization": f'Bearer {decoded_token["aupd_token"]}'},
                cookies={"sudir_access_token": decoded_token["sudir_access_token"]}) as resp:
            if resp.status == 200:
                data = resp
                return Profile()
            raise TokenInvalidException

    @staticmethod
    def decode_token(token: str):
        try:
            return decode(bytes.fromhex(token))
        except TypeError:
            raise TokenInvalidException
