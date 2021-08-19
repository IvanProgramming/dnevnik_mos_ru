"""
    App instance is storing here. Use
        from app import app
    to access app instance from the outside of middlewares and requests.
    Connecting middlewares, routes, exceptions and other is also made here
"""

from starlette.applications import Starlette

from middlewares import APP_MIDDLEWARES
from model.connections import connections
from routes import APP_ROUTES


async def init_connections():
    connections.start_connections()


app = Starlette(routes=APP_ROUTES,
                middleware=APP_MIDDLEWARES,
                on_startup=[init_connections])
