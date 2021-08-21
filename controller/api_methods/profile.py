from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request

from view.api_response import OKResponse


class ProfileEndpoint(HTTPEndpoint):
    def get(self, request: Request):
        """
        responses:
            200:
                description: My profile information
                example: {"status":true,"data":{"name":"Ivan","phone_number":"79999999999","school_name":"Some's school","friends_count":1,"color":[201,146,208],"emoji":"cookie"}}
        """
        profile = request.state.profile
        return OKResponse(profile.as_json())
