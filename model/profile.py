from typing import List

from controller.utils import normalize_phones, normalize_phone
from exceptions.profiles import SelfPhoneNumberError, InvalidPhoneNumberError, AlreadyInFriendsError, \
    EmojiIsNotSupported, ColorModelError, NicknameTooLongError
from model.connections import connections
from model.friend_profile import FriendProfile
from settings import AVAILABLE_EMOJI


class Profile:
    def __init__(self, name: str, phone_number: str, school_name: str, friends=None, _id=0, color=None, emoji=None,
                 nickname=None):
        """ Constructor of model """
        if friends is None:
            friends = []
        if color is None:
            color = Profile.generate_color(phone_number, name)
        if emoji is None:
            emoji = Profile.generate_emoji(phone_number, name)
        if nickname is None:
            nickname = name
        self.name = name
        self.nickname = nickname
        self.phone_number = normalize_phone(phone_number)
        self.school_name = school_name
        self.color = color
        self.emoji = emoji
        self.friends = friends
        self._id = _id

    def register_new(self):
        """ This function is used in controller, it is used for saving new profile, if it doesn't exists or to sync
         already existed profile """
        if not Profile.exists(self.phone_number):
            new_profile = {
                "name": self.name,
                "nickname": self.name,
                "phone_number": normalize_phone(self.phone_number),
                "school_name": self.school_name,
                "friends": self.friends,
                "color": self.color,
                "emoji": self.emoji
            }
            new_id = connections.profiles_db.insert_one(new_profile).inserted_id
            self._id = new_id
        else:
            self.sync_with_db()

    def sync_with_db(self):
        """ Syncs profile instance with database or makes new, if it doesn't exists """
        if Profile.exists(self.phone_number):
            db_object = connections.profiles_db.find_one({"phone_number": self.phone_number})
            self.friends = db_object["friends"]
            self.color = db_object["color"]
            self.emoji = db_object["emoji"]
            self.name = db_object["name"]
            self._id = db_object["_id"]
            self.nickname = db_object["nickname"]
        else:
            self.register_new()

    def count_friends(self):
        """ Count friends and returns it """
        if self.friends:
            return connections.profiles_db.count_documents(
                # Everyone, who is in my friends list and who has my phone in their friends list is my friend
                {
                    "$and": [
                        {"phone_number": {"$in": self.friends}},
                        {"friends": self.phone_number}
                    ]
                })
        return 0

    def as_json(self):
        """ Makes json from profile for sending it as a response """
        return {
            "name": self.name,
            "nickname": self.nickname,
            "phone_number": self.phone_number,
            "school_name": self.school_name,
            "friends_count": self.count_friends(),
            "color": self.color,
            "emoji": self.emoji
        }

    def get_friends(self, as_dict=True):
        """ Returns profiles friends """
        friends_cursor = connections.profiles_db.find({
            "$and": [
                {"phone_number": {"$in": self.friends}},
                {"friends": self.phone_number}
            ]})
        return Profile.parse_friends_cursor(friends_cursor, as_dict)

    def add_friend(self, phone_number: str):
        """ Adding friend by his phone_number """
        phone_number = normalize_phone(phone_number)
        if not self.exists(phone_number):
            raise InvalidPhoneNumberError
        if phone_number in self.friends:
            raise AlreadyInFriendsError
        if phone_number == self.phone_number:
            raise SelfPhoneNumberError
        connections.profiles_db.update_one({"phone_number": self.phone_number},
                                           {"$push": {"friends": phone_number}})
        self.friends.append(phone_number)
        is_online = bool(connections.tokens_db.count_documents({"phone_number": phone_number}))
        return FriendProfile(**Profile.profile_by_phone(phone_number).as_json(), is_online=is_online).dict()

    def get_pending(self, as_dict=True):
        """ Returns pending requests """
        pending_cursor = connections.profiles_db.find({
            "$and": [
                {"friends": self.phone_number},
                {"phone_number": {"$not": {"$in": self.friends}}}
            ]
        })
        return Profile.parse_friends_cursor(pending_cursor, as_dict)

    def get_requests(self, as_dict=True):
        """ Returns your friend requests """
        request_cursor = connections.profiles_db.find({
            "$and": [
                {"friends": {"$not": {"$eq": self.phone_number}}},
                {"phone_number": {"$in": self.friends}}
            ]
        })
        return Profile.parse_friends_cursor(request_cursor, as_dict)

    def edit_profile(self, nickname=None, emoji=None, color=None):
        """ Edits user profile """
        if nickname is None:
            nickname = self.nickname
        if emoji is None:
            emoji = self.emoji
        if color is None:
            color = self.color

        if type(color) != list \
                or len(color) != 3 \
                or max(color) > 255 \
                or min(color) < 0:
            raise ColorModelError
        if emoji not in AVAILABLE_EMOJI:
            raise EmojiIsNotSupported
        if not 0 < len(nickname) <= 16:
            raise NicknameTooLongError
        connections.profiles_db.update_one({"phone_number": self.phone_number}, {"$set": {
            "nickname": nickname,
            "emoji": emoji,
            "color": color
        }})

    @staticmethod
    def parse_friends_cursor(friends_cursor, as_dict=True):
        """ Parses MongoDB query to FriendProfile list]
            :param as_dict: Shows, if returned result should be a dict
        """
        friends_list = []
        phones_list = []
        for friend in friends_cursor:
            friend_profile = Profile(**friend)
            friends_list.append(friend_profile.as_friend_profile(fetch_online=False))
            phones_list.append(friend_profile.phone_number)
        online_phones = list(map(lambda x: x["phone_number"], connections.tokens_db.find({
            "phone_number": {"$in": phones_list}
        })))
        for friend in friends_list:
            if friend.phone_number in online_phones:
                friend.is_online = True
        if as_dict:
            dicted_friends_list = []
            for friend in friends_list:
                dicted_friends_list.append(friend.dict())
            return dicted_friends_list
        return friends_list

    @staticmethod
    def exists(phone_number: str):
        """ Checks is profile exists """
        return bool(connections.profiles_db.find_one({"phone_number": normalize_phone(phone_number)}))

    @staticmethod
    def generate_color(phone_number, name):
        """ Generates color from mobile phone and name """
        hash = 0
        for char in (name + phone_number):
            hash += ord(char) + ((hash << 5) - hash)
        colors = []
        for _ in range(3):
            colors.append(hash % 255)
            hash //= 255
        return colors

    @staticmethod
    def generate_emoji(phone_number, name):
        """ Generates emoji from mobile_phone and name """
        hash = 0
        for char in (name + phone_number):
            hash += ord(char) + ((hash << 5) - hash)
        return AVAILABLE_EMOJI[hash % len(AVAILABLE_EMOJI)]

    @staticmethod
    def profile_by_phone(phone_number):
        """ Returns profile by phone number """
        phone_number = normalize_phone(phone_number)
        result = connections.profiles_db.find_one({"phone_number": phone_number})
        if result:
            return Profile(**result)
        return None

    @staticmethod
    def fetch_existing(phone_numbers: List[str]):
        """ Returns friends profiles from contact book (passed in phone_numbers)"""
        phone_numbers = normalize_phones(phone_numbers)
        exists_friends = connections.profiles_db.find({
            "phone_number": {"$in": phone_numbers}
        })
        friends = []
        for friend in exists_friends:
            friends.append(Profile(**friend).as_friend_profile().dict())
        return friends

    def as_friend_profile(self, fetch_online=False):
        if fetch_online:
            is_online = bool(connections.tokens_db.count_documents({"phone_number": self.phone_number}))
        else:
            is_online = False
        return FriendProfile(**self.as_json(), is_online=is_online)
