#
# main program, this this is used as a desktop app (telegram bot manager)
#

# imports

# TODO: Refresh every a certain timespan

import argparse
from classes.databasemanager import DatabaseManager
from classes.webscraper import WebScraper
from classes.telegrambot import TelegramBot
import threading
import time

# Debugging
from pprint import pprint

#<editor-fold desc="Argument parser">
parser = argparse.ArgumentParser(
    description="This program helps you to find the best deals on Tutti.ch as fast as possible :). Coder: Luca Di Bello",
    epilog="If you like the program don't mind to contact me by mail: luca.dibello@samtrevano.ch"
)

parser.add_argument(
    '--name', '-N',
    default="",
    dest="name",
    metavar='name',
    type=str,
    help="Name that will be visible in the program. Example: 'MacBook Pro 256GB'"
)

parser.add_argument(
    '--url', '-U',
    default="",
    dest="url",
    metavar='name',
    type=str,
    help="Query url that defines the research"
)

parser.add_argument(
    '--list-trackers', '-LT',
    dest="list_trackers",
    action="store_true",
    help="List all tracked research"
)

parser.add_argument(
    '--clear-trackers',
    dest="clear_trackers",
    action="store_true",
    help="clear all tracked research"
)


parser.add_argument(
    '--list-deals', '-LD',
    dest="list_deals",
    action="store_true",
    help="clear all tracked research"
)

parser.add_argument(
    '--clear-deals',
    dest="clear_deals",
    action="store_true",
    help="clear all tracked research"
)


parser.add_argument(
    '--clear-users',
    dest="clear_users",
    action="store_true",
    help="clear all tracked research"
)

parser.add_argument(
    '--refresh',
    dest="refresh",
    action="store_true",
    help="Refresh all tracked researches"
)

parser.add_argument(
    '--telegram-bot',
    dest="telegram",
    action="store_true",
    help="Starts the telegram bot"
)

parser.add_argument(
    '--start-deamon',
    dest="deamon",
    action="store_true",
    help="The program will be executed autonomously every timespan"
)

# Parse all passed parameters
#</editor-fold>
args = parser.parse_args()
db = DatabaseManager()
scraper = WebScraper()
bot = TelegramBot(db)

def main():
    global bot

    if args.telegram:
        # wait until the telegram bot is started

        while not bot.bot_status:
            time.sleep(0.5)
        print("[Success] Bot and application are in sync")

    if len(args.name) > 0 and len(args.url) > 0:
        # SAVE TRACKER IN DATABASE

        print(args.url)

        db.add_tracker(args.name, args.url)

    if args.list_trackers:
        # Prints all saved trackers
        trackers = db.get_trackers()

        print("Total trackers {} avaible:".format(len(trackers)))
        for tracker in trackers:
            print(tracker.to_dict())

    if args.clear_trackers:
        # Delete all saved trackers
        result = db.clear_trackers()
        print("Removed {} tracker(s) from database".format(result.rowcount))

    if args.list_deals:
        # Prints all saved deals
        deals = db.get_deals()

        print("Total deals {} avaible:".format(len(deals)))
        for deal in deals:
            print(deal.to_dict())

    if args.clear_deals:
        # Delete all saved Deals
        result = db.clear_deals()
        print("Removed {} deal(s) from database".format(result.rowcount))

    if args.clear_users:
        # Delete all saved Users
        result = db.clear_users()
        print("Removed {} user(s) from database".format(result.rowcount))

    if args.refresh:
        trackers = db.get_trackers()

        if len(trackers) == 0:
            print("No trackers avaible")
        else:
            for tracker in trackers:
                found_deals = scraper.get_deals(tracker)

                new = new_deals(
                    db.get_deal_by_tracker(tracker.id),
                    found_deals
                )

                for deal in new:
                    db.add_deal(deal)

                    if bot.bot_status:
                        bot.send_broadcast(bot.deal_text_generator(deal))
                print("[Info] Added in dictionary {} new deal(s)".format(len(new)))


def new_deals(old, new):
    if len(old) > 0:
        newest_old = old[0].to_dict()
        newest_new = new[0].to_dict()

        if newest_old == newest_new:
            print("[Info] No new deals")
            return list()
        else:
            print("[Info] New deals detected")
            new.reverse()
            new_deals = new[len(old):len(new)]
            return new_deals

    else:
        print("[Info] No saved deals detected")
        return new


if args.telegram:
    # create thread
    t1 = threading.Thread(target=main)

    # start thread
    t1.start()

    bot.start_bot()
else:
    main()
