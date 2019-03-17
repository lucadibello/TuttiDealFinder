class Deal:

    def __init__(self, title, price, loc_city, loc_cap, date, url,tracker_id,deal_id=0):
        self.id = deal_id
        self.title = title
        self.price = price
        self.loc_city = loc_city
        self.loc_cap = loc_cap
        self.date = date
        self.url = url
        self.tracker_id = tracker_id

    def to_dict(self):
        return {
            "title": self.title,
            "price": self.price,
            "loc_city": self.loc_city,
            "loc_cap": self.loc_cap,
            "date": self.date,
            "url": self.url
        }
