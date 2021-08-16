"""
    API methods for devs, works only in DEBUG mode
"""
from starlette.responses import JSONResponse
from starlette.schemas import SchemaGenerator


def get_openapi_schema(request):
    """ responses:
            200:
                description: OpenAPI schema
    """
    # I'm using this for avoiding cycle import error
    from routes import APP_ROUTES
    schemas = SchemaGenerator(
        {"openapi": "3.0.0", "info": {"title": "Lastic REST API", "version": "1.0.0"}}
    )
    return JSONResponse(schemas.get_schema(routes=APP_ROUTES))
