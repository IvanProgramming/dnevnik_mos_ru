from view.api_response import ErrorResponse


class ApiException(Exception):
    """
     This is exception should be inherented by all exceptions.
     By using details property you can get detais in string.
     By using status_code, you can get a status code of Exception.
     By using response, you can get Starlette Error response, for proceeding it into request return
    """
    details: str
    status_code: int
    http_code: int = 500

    @property
    def response(self):
        return ErrorResponse({"details": self.details, "status_code": self.status_code}, status_code=self.http_code)
