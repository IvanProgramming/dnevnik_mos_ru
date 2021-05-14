class CredentialsInvalidException(Exception):
    def __init__(self, danger_text=""):
        self.danger_text = danger_text

    def __str__(self):
        return f"Login error. Login or password is incorrect!\n({self.danger_text})"


class SeleniumNotFoundException(Exception):
    def __str__(self):
        return "Can't find selenium in execution path, selenium auth can't be proceed!"


class UnknownErrorException(Exception):
    def __str__(self):
        return "Unknown error occurred!"


class IpBanError(Exception):
    def __str__(self):
        return "(https://youtu.be/PlPeZHGF6Uk)\nMaybe Moscow DIT changed procedure, so your IP was banned in mos.ru. " \
               "Reload your router IP or " \
               "Try to use proxies. Or just report it in Github Issue and on Discord Server"


class UnknownTokenError(Exception):
    def __str__(self):
        return "Your Token is expired, so use another!"
