from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from settings import ALLOWED_HOSTS
from controller.token_verification import TokenVerificationMiddleware
from controller.pushes.fcm_middleware import FCMMidlleware

APP_MIDDLEWARES = [
    Middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS),
    Middleware(TokenVerificationMiddleware),
    Middleware(FCMMidlleware),
]
