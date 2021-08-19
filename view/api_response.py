from json import dumps
from typing import Any

from starlette.responses import JSONResponse


class OKResponse(JSONResponse):
    """ This type of response is JSONResponse, but with OK status and data wrap """
    def render(self, content: Any):
        return dumps({"status": "ok", "data": content}, ensure_ascii=False).encode("utf-8")


class ErrorResponse(JSONResponse):
    """ The same as previous, but with error status """
    def render(self, content: Any):
        return dumps({"status": "error", "data": content}, ensure_ascii=False).encode("utf-8")
