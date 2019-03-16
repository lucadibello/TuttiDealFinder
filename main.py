#
# main program, this this is used as a desktop app (telegram bot manager)
#

# imports
import argparse
from classes.databasemanager import DatabaseManager

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


def main():

    if len(args.name) > 0 and len(args.url) > 0:
        # SAVE TRACKER IN DATABASE
        db.add_tracker(args.name, args.url)
    if args.list_trackers:
        trackers = db.get_trackers()

        print("Total trackers {} avaible:".format(len(trackers)))
        for index, tracker in enumerate(trackers):
            print_tracker(index, tracker)

    if args.clear_trackers:
        result = db.clear_trackers()
        print("Removed {} tracker(s) from database".format(result.rowcount))

    if args.list_deals:
        deals = db.get_deals()

        print("Total deals {} avaible:".format(len(deals)))
        for deal in deals:
            print(deal.to_dict())

    if args.clear_deals:
        result = db.clear_deals()
        print("Removed {} deal(s) from database".format(result.rowcount))


def print_tracker(index, tracker):
    print()
    print("Tracker N.", index + 1)
    print("Tracker name:", tracker[1])
    print("Tracker url:", tracker[2])
    print("----------------------------------")


main()
