from starlette.routing import Route

from settings import DEBUG
from .api_methods import *

dev_routes = [
    Route("/schema", endpoint=get_openapi_schema)
]

routes = [
    Route("/ping", endpoint=ping)
] + dev_routes if DEBUG else []
