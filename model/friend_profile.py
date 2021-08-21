from pydantic import BaseModel


class FriendProfile(BaseModel):
    name: str
    phone_number: str
    school_name: str
    friends_count: int
    color: list[int]
    emoji: str
    is_online: bool
