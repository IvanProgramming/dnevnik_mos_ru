"""
    App instance is storing here. Use
        from app import app
    to access app instance from the outside of middlewares and requests.
    Connecting middlewares, routes, exceptions and other is also made here
"""

from starlette.applications import Starlette
from routes import APP_ROUTES
from middlewares import APP_MIDDLEWARES

app = Starlette(routes=APP_ROUTES, middleware=APP_MIDDLEWARES)
 
