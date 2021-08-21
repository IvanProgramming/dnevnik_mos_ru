from model.profile import Profile


class BaseDiaryProvider:
    """ Base Dairy Provider. Any Dairy provider should inherent this class"""
    name: str
    """ Displayed name of diary provider """
    token_verification_url: str
    """ URL for diary token verification """
    unique_name: str
    """ Unique name is a short name, that is used in database and in DiaryProvider header """

    @staticmethod
    async def is_token_correct(token: str) -> bool:
        """ Is token correct checks token and returns boolean """
        pass

    @staticmethod
    async def get_phone_number(token: str) -> str:
        """ Makes request to server and returns phone number by token """
        pass

    @staticmethod
    async def get_profile_instance(token: str) -> Profile:
        """ Returns user profile, fetched from diary"""
        pass
