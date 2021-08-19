from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from settings import ALLOWED_HOSTS
from controller.token_verification import TokenVerificationMiddleware

APP_MIDDLEWARES = [
    Middleware(TokenVerificationMiddleware),
    Middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
]
