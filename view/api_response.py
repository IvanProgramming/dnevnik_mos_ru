from json import dumps
from typing import Any

from starlette.responses import JSONResponse


class OKResponse(JSONResponse):
    """ This type of response is JSONResponse, but with OK status and data wrap """

    def render(self, content: Any):
        return dumps({"status": True, "data": content}, ensure_ascii=False).encode("utf-8")


class ErrorResponse(JSONResponse):
    """ The same as previous, but with error status """

    def render(self, content: Any):
        return dumps({"status": False, "data": content}, ensure_ascii=False).encode("utf-8")
