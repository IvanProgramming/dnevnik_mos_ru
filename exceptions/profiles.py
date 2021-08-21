from exceptions.base_exception import ApiException


class InvalidPhoneNumberError(ApiException):
    status_code = 11
    http_code = 404
    details = "Phone Doesn't exists or is not valid"


class SelfPhoneNumberError(ApiException):
    status_code = 12
    http_code = 418
    details = "You can't add your self to friends"


class AlreadyInFriendsError(ApiException):
    status_code = 13
    http_code = 400
    details = "Friend is already added to your friend list"
