from dnevnik.base_auth_provider import BaseAuthProvider
from ..exceptions import UnknownTokenError


class TokenAuthorization(BaseAuthProvider):
    def __init__(self, auth_token: str, profile_id: int):
        self.auth_token = auth_token
        self.profile_id = profile_id

    def refresh_token(self):
        raise UnknownTokenError
