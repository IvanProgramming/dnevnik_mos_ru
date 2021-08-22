"""
    API methods for devs, works only in DEBUG mode
"""
from starlette.schemas import SchemaGenerator


def get_openapi_schema(request):
    """ responses:
            200:
                description: OpenAPI schema
    """
    schemas = SchemaGenerator(
        {"openapi": "3.0.0", "info": {"title": "Lastic REST API", "version": "1.0.0"}}
    )
    return schemas.OpenAPIResponse(request)
