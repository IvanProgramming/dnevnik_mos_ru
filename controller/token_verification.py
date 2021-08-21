
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from exceptions.base_exception import ApiException
from model.diary_providers.utils import get_provider_by_unique_name
from model.profile import Profile
from model.token_caching import save_token, exists, get_cached_phone
from view.api_response import ErrorResponse


async def verify_token(token, diary, **additional_params) -> Profile:
    """
    Verifies token
    :param token: auth-token
    :param diary: diary provider unique name
    :param additional_params: some additional params (NOT REALIZED)
    :return:
    """
    diary_provider = get_provider_by_unique_name(diary)
    if not exists(token, diary):
        profile = await diary_provider.get_profile_instance(token)
        phone_number = profile.phone_number
        await save_token(token, diary, phone_number)
        return profile
    return Profile.profile_by_phone(await get_cached_phone(token, diary))


class TokenVerificationMiddleware(BaseHTTPMiddleware):
    """
    This token verification middleware checks token every http request
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        from settings import TOKEN_FREE_METHODS
        try:
            if request.url.path not in TOKEN_FREE_METHODS:
                token = request.headers["authorization"][7:]
                diary = request.headers["diary-alias"]
                profile = await verify_token(token, diary)
                profile.register_new()
                request.state.profile = profile
            response = await call_next(request)
            return response
        except ApiException as e:
            return e.response
        except KeyError:
            return ErrorResponse({"details": "Not all data is provided", "status_code": 10}, status_code=403)
