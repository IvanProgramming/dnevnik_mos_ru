from exceptions.base_exception import ApiException


class NoSuchDairyProvider(ApiException):
    """ This exception is raised in get_provider_by_unique_name() if provider name doesn't exists """
    status_code = 8
    http_code = 400

    def __init__(self, diary_name):
        self.dairy_name = diary_name
        self.details = f"Diary {diary_name} doesn't exists"


class TokenInvalidException(ApiException):
    """ Token is not valid. This exception is raised in TokenValidate middleware """
    status_code = 7
    details = "Specified token is not set, expired or invalid"
    http_code = 403


class PhoneIsNotPresented(ApiException):
    """ This exception is raised if mobile phone is not provided in Diary Provider """
    status_code = 4
    details = "Mobile phone is not presented in API response"
    http_code = 403

class FCMTokenIsInvalid(ApiException):
    status_code = 17
    details = "FCM token is not presented"
    http_code = 403

class AuthDataRequired(ApiException):
    status_code = 10
    details = "Not all required authentification data is provided"
    http_code = 403
