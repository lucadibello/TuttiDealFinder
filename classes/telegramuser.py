class TelegramUser:

    def __init__(self,user_id,user_firstname,user_lastname, notify = True):
        self.user_id = user_id
        self.user_firstname = user_firstname
        self.user_lastname = user_lastname
        self.notify = notify

    def to_dict(self):
        return {
            self.user_id:
                {
                    "firstname": self.user_lastname,
                    "lastname": self.user_firstname,
                    "nofify": self.notify
                }
        }

    def toggle_notify(self):
        self.notify = not self.notify
