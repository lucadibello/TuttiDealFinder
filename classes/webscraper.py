import requests
from classes.deal import Deal
from classes.tracker import Tracker
from bs4 import BeautifulSoup


class WebScraper:

    def get_deals(self, tracker: Tracker):
        print("Running query: ", tracker.url)
        soup = BeautifulSoup(requests.get(tracker.url).text, 'html.parser')
        PRODUCT_INFO_HTML_CLASS = "_3aiCi"
        PRODUCT_PRICE_CLASS = '_6HJe5'
        PRODUCT_WHEN_CLASS = '_1kvIw'
        PRODUCT_LOCATION_CLASS = '_3f6Er'
        PRODUCT_URL_CLASS = '_16dGT'
        BASE_URL = "https://www.tutti.ch"
        PRODUCT_TITLE_TAG = 'h4'

        scraped_deals = soup.find_all(class_=PRODUCT_INFO_HTML_CLASS)
        deals = []
        for item in scraped_deals:
            # Get location data
            location_data = item.find(class_=PRODUCT_LOCATION_CLASS)
            city = location_data.contents[0]
            cap = location_data.contents[6]

            deals.append(Deal(
                item.find(PRODUCT_TITLE_TAG).contents[0],
                item.find(class_=PRODUCT_PRICE_CLASS).contents[0],
                city,
                int(cap),
                item.find(class_=PRODUCT_WHEN_CLASS).contents[0],
                BASE_URL + item.find('a').get("href"),
                tracker.id
            ))

        return deals
