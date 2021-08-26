"""
    App instance is storing here. Use
        from app import app
    to access app instance from the outside of middlewares and requests.
    Connecting middlewares, routes, exceptions and other is also made here
"""

from starlette.applications import Starlette

from exceptions import EXCEPTION_HANDLERS
from middlewares import APP_MIDDLEWARES
from model.connections import connections
from routes import APP_ROUTES
from settings import SENTRY_URL
import sentry_sdk
import logging
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
async def init_connections():
    connections.start_connections()

sentry_logging = LoggingIntegration(
    level=logging.DEBUG,        
    event_level=logging.ERROR 
)
sentry_sdk.init(SENTRY_URL, integrations=[sentry_logging])

app = SentryAsgiMiddleware(Starlette(routes=APP_ROUTES,
                middleware=APP_MIDDLEWARES,
                on_startup=[init_connections],
                exception_handlers=EXCEPTION_HANDLERS))

