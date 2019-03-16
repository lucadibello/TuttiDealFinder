class Ad:

    def __init__(self, title, price, loc, date, url):
        self.title = title
        self.price = price
        self.loc = loc
        self.date = date
        self.url = url

    def to_dict(self):
        return {"title": self.title, "price": self.price, "loc": self.loc, "date": self.date, "url": self.url}
