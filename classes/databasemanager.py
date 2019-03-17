import mysql.connector
from config.params import Params
from classes.deal import Deal
from classes.tracker import Tracker
from classes.user import User


class DatabaseManager:

    # Table names
    TRACKER_TABLE = "tracker"
    DEAL_TABLE = "deal"
    USER_TABLE = "user"

    def __init__(self):
        # Create connection
        self.DATABASE_CON = self.connect_database(
                Params.HOST,
                Params.USER,
                Params.PASSWORD,
                Params.DATABASE
        )

    #BASE FUNCTIONS
    @staticmethod
    def connect_database(host, username, password, database):
        return mysql.connector.connect(
            host=host,
            user=username,
            passwd=password,
            database=database
        )

    def prepare(self, query_string):
        # Get cursor
        cursor = self.DATABASE_CON.cursor()

        # Exec passed query string
        cursor.execute(query_string)

        # Return cursor
        return cursor

    #GENERIC FUNCTIONS
    def get_data(self, table_name):
        # Format query string
        query_string = "SELECT * FROM {}".format(table_name)

        # Exec query and return data
        return self.prepare(query_string).fetchall()

    def clear_data(self, table_name):
        # Format query string
        query_string = "DELETE FROM {}".format(table_name)

        # Get cursor from db
        cursor = self.prepare(query_string)

        # Commit changes to database
        self.DATABASE_CON.commit()

        # Return cursor
        return cursor

    #TRACKER FUNCTIONS
    def add_tracker(self, name, url):
        # Format query
        query_string = "INSERT INTO {} VALUES(0,'{}','{}')".format(self.TRACKER_TABLE,url, name)

        # Exec query
        self.prepare(query_string)

        # Commit changes to database
        self.DATABASE_CON.commit()

        print("[Success] Added new tracker")

    def get_trackers(self):
        trackers = []
        for tracker in self.get_data(self.TRACKER_TABLE):

            # Create a deal object for each row
            tracker = Tracker(
                tracker[2],
                tracker[1],
                tracker[0]
            )

            # Add deal to the main list
            trackers.append(tracker)

        # Return deal object list
        return trackers

    def clear_trackers(self):
        return self.clear_data(self.TRACKER_TABLE)

    #DEAL FUNCTIONS
    def get_deals(self):
        deals = []
        for deal in self.get_data(self.DEAL_TABLE):
            # Create a deal object for each row
            deal = Deal(
                deal[2],
                deal[3],
                deal[4],
                deal[5],
                deal[6],
                deal[7],
                deal[1],
                deal[0]
            )
            # Add deal to the main list
            deals.append(deal)

        # Return deal object list
        return deals

    def clear_deals(self):
        return self.clear_data(self.DEAL_TABLE)

    def add_deal(self, deal: Deal):
        # Format query
        query_string = 'INSERT INTO {} VALUES(0,{},"{}","{}","{}","{}","{}","{}")'.format(
            self.DEAL_TABLE,
            deal.tracker_id,
            deal.title,
            deal.price,
            deal.loc_city,
            deal.loc_cap,
            deal.date,
            deal.url
        )

        # Exec query
        self.prepare(query_string)

        # Commit changes to database
        self.DATABASE_CON.commit()

    def get_deal_by_tracker(self,tracker_id):
        query_string = "SELECT * FROM {} WHERE tracker_id = {}".format(self.DEAL_TABLE,tracker_id)

        deals = []
        for deal in self.prepare(query_string).fetchall():
            # Create a deal object for each row
            deal = Deal(
                deal[2],
                deal[3],
                deal[4],
                deal[5],
                deal[6],
                deal[7],
                deal[1],
                deal[0]
            )
            # Add deal to the main list
            deals.append(deal)

        # Return deal object list
        return deals

    #USER FUNCTIONS
    def add_user(self, chat_id, notify_flag = True):
        # Format query
        query_string = "INSERT INTO {} VALUES({},'{}')".format(self.USER_TABLE, chat_id, (1 if notify_flag == True else 0))

        # Exec query
        self.prepare(query_string)

        # Commit changes to database
        self.DATABASE_CON.commit()

    def get_users(self):
        users = []
        for user in self.get_data(self.USER_TABLE):
            user = User(
                user[0],
                user[1]
            )

            users.append(user)

        return users

    def clear_users(self):
        return self.clear_data(self.USER_TABLE)

    def remove_user(self, user_id):
        # Format query
        query_string = 'DELETE FROM {} WHERE user_id = {}'.format(
            self.USER_TABLE,
            int(user_id),
        )

        print(query_string)

        # Exec query
        cursor = self.prepare(query_string)

        # Commit changes to database
        self.DATABASE_CON.commit()

        print("[Success] Removed user from database")

        # Return cursor
        return cursor