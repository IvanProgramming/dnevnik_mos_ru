from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request

from exceptions.profiles import InvalidPhoneNumberError
from model.profile import Profile
from view.api_response import OKResponse


class FriendsEndpoint(HTTPEndpoint):
    async def get(self, request: Request):
        """
        responses:
            200:
                description: My friends, My Pendings and my Friend Requests
                example: {"status":true,"data":{"friends":[{"name":"Ivan","phone_number":"79999999999","school_name":"Some's school","friends_count":1,"color":[201,146,208],"emoji":"cookie","is_online":false}],"pending":[],"requests":[]}}
        """
        profile = request.state.profile
        return OKResponse(profile.get_friends() + profile.get_requests() + profile.get_pending())

    async def put(self, request: Request):
        """
        responses:
            200:
                description: Friend is added and you get it's data
            404:
                description: Friend is not in parabola
            418:
                description: Trying to add myself to my friends list (Feels so lonely)
        """
        profile = request.state.profile
        phone_number = (await request.json())["phone_number"]
        profile.add_friend(phone_number)
        if phone_number:
            return OKResponse({})
        raise InvalidPhoneNumberError

    async def delete(self, request: Request):
        """"""
        profile = request.state.profile
        phone_number = (await request.json())["phone_number"]
        profile.delete_friend(phone_number)
        return OKResponse({})


async def search_friend(request: Request):
    """
    responses:
        200:
            description: If more than 2 phones passed, returns data of everyone, how is in parabola, if one, returns only his profile data
        404:
            description: if one passed - Friend is not in parabola
    """
    phone_numbers = (await request.json())["phone_numbers"]
    profile = request.state.profile
    return OKResponse(profile.search_friends(phone_numbers))
