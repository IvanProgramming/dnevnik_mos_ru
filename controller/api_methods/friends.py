from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request

from exceptions.profiles import InvalidPhoneNumberError
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
        return OKResponse({
            "friends": profile.get_friends(),
            "pending": profile.get_pending(),
            "requests": profile.get_requests()
        })

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
        if phone_number:
            return OKResponse(profile.add_friend(phone_number))
        raise InvalidPhoneNumberError
