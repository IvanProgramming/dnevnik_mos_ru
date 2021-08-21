from view.api_response import OKResponse


async def ping(request):
    """
    responses:
        200:
            description: pong anwser
            examples:
                {"status": true, "data": {}}
    """
    return OKResponse({})
