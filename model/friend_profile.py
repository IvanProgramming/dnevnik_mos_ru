from pydantic import BaseModel


class FriendProfile(BaseModel):
    name: str
    phone_number: str
    school_name: str
    friends_count: str
    color: list[str]
    emoji: str
    is_online: bool
