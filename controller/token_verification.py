
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from exceptions.base_exception import ApiException
from model.diary_providers.utils import get_provider_by_unique_name
from model.token_caching import save_token, exists, get_cached_phone
from view.api_response import ErrorResponse


async def verify_token(token, diary, **additional_params) -> str:
    """
    Verifies token
    :param token: auth-token
    :param diary: diary provider unique name
    :param additional_params: some additional params (NOT REALIZED)
    :return:
    """
    diary_provider = get_provider_by_unique_name(diary)
    if not exists(token, diary):
        phone_number = await diary_provider.get_phone_number(token)
        await save_token(token, diary, phone_number)
        return phone_number
    return await get_cached_phone(token, diary)


class TokenVerificationMiddleware(BaseHTTPMiddleware):
    """
    This token verification middleware checks token every http request
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            token = request.headers["authorization"][7:]
            diary = request.headers["diary-alias"]
            await verify_token(token, diary)
            response = await call_next(request)
            return response
        except ApiException as e:
            return e.response
        except KeyError:
            print(request.headers)
            return ErrorResponse({"details": "Not all data is provided", "status_code": 10}, status_code=403)
