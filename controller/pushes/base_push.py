from firebase_admin.messaging import Message, Notification, MulticastMessage, send_multicast, send
from model.pushes import fcms_list

class BasePush:
    """ BasePush is parent of any class, that represents push. It can send messages and multicast messages to users """
    body = ""
    title = ""
    picture = ""
    data = {}
    ttl = 3600

    def as_notification(self) -> Notification:
        """ Returns notification instance. Can return none, if body and title are not defined"""
        if self.body and self.title:
            return Notification(
                body=self.body,
                title=self.title,
                image=self.picture
            )
        return None


    def as_message(self, token) -> Message:
        """ Returns message with notification and data.
            :params token: FCM token of device
        """
        return Message(
            ttl=self.ttl,
            data=self.data,
            notification=self.as_notification(),
            token=token
        )
    
    def as_multicast_message(self, tokens) -> MulticastMessage:
        """ Returns multicast message made from notification """
        return MulticastMessage(
            ttl=self.ttl,
            data=self.data,
            notification=self.as_notification(),
            tokens=tokens
        )
    
    def cast_message(self, phones: list):
        """ Sending single message for one or many phones by phone_numbers list """
        fcms = get_recepient_fcms(phones)
        if len(fcms) > 1:
            multicast_message = self.as_multicast_message(fcms)
            return send_multicast(multicast_message)
        if len(fcms) == 1:
            message = self.as_message(fcms[0])
            return send(message)
        return None
