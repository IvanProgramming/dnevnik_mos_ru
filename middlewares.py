from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

import settings

APP_MIDDLEWARES = [
    Middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
]
