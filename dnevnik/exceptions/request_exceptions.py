class UnknownStatusCodeError(Exception):
    """ Неизвестный статус код во время запроса к API """
    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        return f"Status code {self.status_code} is incorrect"
