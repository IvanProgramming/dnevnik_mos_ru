from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from settings import DEBUG
from .api_methods import *

dev_routes = [
    Route("/schema", endpoint=get_openapi_schema)
]

routes = (dev_routes if DEBUG else []) + [
    Route("/ping", endpoint=ping, methods=["GET"]),
    Route("/profile", endpoint=ProfileEndpoint),
    Route("/friends", endpoint=FriendsEndpoint),
    Route("/friends/search", endpoint=search_friend, methods=["GET"]),
    Route("/events", endpoint=EventEndpoint),
    Route("/push", endpoint=ping, methods=["GET"]),
    Mount("", app=StaticFiles(directory="static"), name="static")

]
