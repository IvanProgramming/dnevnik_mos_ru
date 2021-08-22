from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pymongo import DESCENDING

from model.connections import connections
from model.friend_profile import FriendProfile
from model.profile import Profile


class Event(BaseModel):
    _id: str
    event_type: str
    payload: dict
    event_time: datetime
    phone_number: Optional[str]
    profile: Optional[FriendProfile]

    @staticmethod
    def register_many(events, phone_number):
        events_list = []
        for event in events:
            event_obj = Event(**event)
            event_obj.phone_number = phone_number
            del event_obj.profile
            events_list.append(event_obj.dict())
        connections.events_db.insert_many(events_list)

    @staticmethod
    def get_events_for_user(profile: Profile, as_dicts=True):
        phones_map = {}
        for friend in profile.get_friends(as_dict=False):
            phones_map[friend.phone_number] = friend
        events_cursor = connections.events_db.find({"phone_number": {"$in": list(phones_map.keys())}}).sort(
            "event_time",
            DESCENDING)
        events = []
        for event in events_cursor:
            phone = event["phone_number"]
            event["profile"] = phones_map[phone]
            del event["phone_number"]
            if as_dicts:
                event_dict = Event(**event).dict()
                event_dict["event_time"] = event_dict["event_time"].strftime("%Y-%m-%d %H:%M")
                events.append(event_dict)
            else:
                event.append(Event(**event))
        return events
