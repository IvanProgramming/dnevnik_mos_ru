from typing import List, Optional

from pydantic import BaseModel


class FriendProfile(BaseModel):
    name: Optional[str]
    nickname: str
    phone_number: str
    school_name: Optional[str]
    friends_count: int
    color: List[int]
    emoji: str
    is_online: bool
    gender: Optional[str]
    status: Optional[str]
