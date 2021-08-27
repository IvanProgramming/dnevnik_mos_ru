from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from firebase_admin.messaging import send, Message, UnregisteredError
from firebase_admin.exceptions import InvalidArgumentError
from settings import FCMED_ENDPOINTS
from model.connections import connections
from exceptions.providers import FCMTokenIsInvalid, AuthDataRequired
from exceptions.base_exception import ApiException

def is_fcm_valid(fcm_token: str):
    """ Checking is FCM valid """
    try:
        test_message = Message(
            data={
                "text": "text"
            },
            token=fcm_token
        )
        response = send(test_message, dry_run=True)
        print(response)
        return True
    except InvalidArgumentError:
        return False
    except UnregisteredError:
        return False

class FCMMidlleware(BaseHTTPMiddleware):
    """ This middleware is used for FCM confirmation and FCM saving """
    async def dispatch(self, request: Request, call_next):
        try:
            if request.url.path in FCMED_ENDPOINTS:
                try:
                    fcm_token = request.headers["fcm_token"]
                    if not is_fcm_valid(fcm_token):
                        raise FCMTokenIsInvalid
                    request.state.current_fcm = fcm_token
                    if fcm_token not in request.state.profile.fcms:
                        request.state.profile.save_fcm(fcm_token)
                except KeyError:
                    raise AuthDataRequired
            response = await call_next(request)
            return response
        except ApiException as e:
            return e.response
