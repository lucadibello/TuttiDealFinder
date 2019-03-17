class Tracker:

    def __init__(self, name, url, tracker_id=0):
        self.id = tracker_id
        self.name = name
        self.url = url

    def to_dict(self):
        return {
            "name": self.name,
            "url": self.url
        }
