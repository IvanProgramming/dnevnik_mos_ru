from datetime import datetime
from hashlib import md5
from typing import Optional

from pydantic import BaseModel
from pymongo import DESCENDING

from model.connections import connections
from model.friend_profile import FriendProfile
from model.profile import Profile


class Event(BaseModel):
    _id: str
    type: str
    payload: dict
    time: int
    phone_number: Optional[str]
    profile: Optional[FriendProfile]

    @staticmethod
    def register_many(events, phone_number):
        events_list = []
        hashlist = []
        for event in events:
            event_obj = Event(**event)
            event_obj.phone_number = phone_number
            del event_obj.profile
            event_dict = event_obj.dict()
            event_dict["hash"] = md5(event_obj.json().encode("utf-8")).hexdigest()
            hashlist.append(event_dict["hash"])
            events_list.append(event_dict)
        already_added = list(connections.events_db.find({"hash": {"$in": hashlist}}, {"_id": 0, "hash": 1}))
        for already_added_hash in already_added:
            del events_list[hashlist[already_added_hash]]
        connections.events_db.insert_many(events_list)

    @staticmethod
    def get_events_for_user(profile: Profile, as_dicts=True):
        phones_map = {}
        for friend in profile.get_friends(as_dict=False):
            phones_map[friend.phone_number] = friend
        events_cursor = connections.events_db.find({"phone_number": {"$in": list(phones_map.keys())}}).sort(
            "time",
            DESCENDING)
        events = []
        for event in events_cursor:
            phone = event["phone_number"]
            event["profile"] = phones_map[phone]
            del event["phone_number"]
            if as_dicts:
                events.append(Event(**event).dict())
            else:
                event.append(Event(**event))
        return events
