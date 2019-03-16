import mysql.connector
from config.params import Params
from classes.deal import Deal

class DatabaseManager:

    TRACKER_TABLE = "tracker"
    DEAL_TABLE = "deal"

    def __init__(self):
        self.DATABASE_CON = self.connect_database(
                Params.HOST,
                Params.USER,
                Params.PASSWORD,
                Params.DATABASE
        )

    @staticmethod
    def connect_database(host, username, password, database):
        return mysql.connector.connect(
            host=host,
            user=username,
            passwd=password,
            database=database
        )

    def prepare(self, query_string):
        cursor = self.DATABASE_CON.cursor()
        cursor.execute(query_string)
        return cursor

    def add_tracker(self, name, url):
        query_string = "INSERT INTO {} VALUES(0,'{}','{}')".format(self.TRACKER_TABLE, url, name)
        self.prepare(query_string)
        self.DATABASE_CON.commit()

        print("[Success] Added new tracker")

    def get_data(self,table_name):
        query_string = "SELECT * FROM {}".format(table_name)
        return self.prepare(query_string).fetchall()

    def clear_data(self,table_name):
        query_string = "DELETE FROM {}".format(table_name)
        cursor = self.prepare(query_string)
        self.DATABASE_CON.commit()

        return cursor

    def get_trackers(self):
        return self.get_data(self.TRACKER_TABLE)

    def clear_trackers(self):
        return self.clear_data(self.TRACKER_TABLE)

    def get_deals(self):
        deals = []
        for deal in self.get_data(self.DEAL_TABLE):

            deal = Deal(
                deal[0],
                deal[1],
                deal[2],
                deal[3],
                deal[4],
                deal[5],
                deal[6]
            )

            deals.append(deal)

        return deals

    def clear_deals(self):
        return self.clear_data(self.DEAL_TABLE)
