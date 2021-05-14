class BaseAuthProvider:
    auth_token: str = None
    profile_id: int = None

    def proceed_authorization(self):
        pass

    def refresh_token(self):
        pass
