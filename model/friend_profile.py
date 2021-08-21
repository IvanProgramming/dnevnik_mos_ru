from typing import List

from pydantic import BaseModel


class FriendProfile(BaseModel):
    name: str
    phone_number: str
    school_name: str
    friends_count: int
    color: List[int]
    emoji: str
    is_online: bool
