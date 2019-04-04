from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from classes.databasemanager import DatabaseManager
from classes.deal import Deal
from classes.webscraper import WebScraper
from config.params import Params
from pprint import pprint
from classes.tracker import Tracker
import logging




class TelegramBot:
    TOKEN = Params.TOKEN
    bot_status = False
    scraper = WebScraper()
    SET_TARGET_NAME, SET_TARGET_URL = range(2)

    tracker = Tracker("nome", "url", -1)

    def __init__(self,database_manager: DatabaseManager):
        self.db = database_manager
        self.DP = None

    def start_bot(self):

        updater = Updater(self.TOKEN)

        # Get the dispatcher to register handlers
        self.DP = updater.dispatcher

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.bot_status = True
        print("Telegram bot started successfully")

        #Conversation handler for adding target
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('addtracker',self.addtracker)],
            states={
                self.SET_TARGET_NAME: [MessageHandler(Filters.text, self.check_target_name, pass_user_data=True)],
                self.SET_TARGET_URL: [MessageHandler(Filters.text, self.check_target_url, pass_user_data=True)]
            },
            fallbacks=[MessageHandler(Filters.regex('exit'),self.cancel_tracker_wizard)]
        )

        #Add conversation handler
        self.DP.add_handler(conversation_handler)

        #Setup commands
        self.DP.add_handler(CommandHandler("start", self.start))
        self.DP.add_handler(CommandHandler("stop", self.stop))
        self.DP.add_handler(CommandHandler("refresh", self.refresh))

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

    def start(self, update, context):
        user_id = update.effective_user.id

        # Check if users exists already
        if self.is_new_user(user_id):
            print("[INFO] New user detected!!!")
            self.db.add_user(int(user_id))
            update.message.reply_text('Hello {} welcome in TuttiDealFinder! Digit /help for the list of the avaible commands'.format(update.message.from_user.first_name))
        else:
            update.message.reply_text('Hello {}, we know each other already.'.format(update.message.from_user.first_name))

    def refresh(self, update, context):
        user_id = update.effective_user.id

        if not self.is_new_user(user_id):
            print("Refreshing all trackers for user with id:", user_id)
            trackers = self.db.get_trackers_by_user_identifier(user_id)

            if len(trackers) == 0:
                print("No trackers avaible")
                update.message.reply_text('No trackers avaible, first you have to add them!')
            else:
                for tracker in trackers:
                    found_deals = self.scraper.get_deals(tracker)
                    message = "I'm scanning for new deals on '{}' tracker".format(tracker.name)
                    update.message.reply_text(message)

                    new = self.new_deals(
                        self.db.get_deal_by_tracker(tracker.id),
                        found_deals
                    )

                    for deal in new:
                        self.db.add_deal(deal)
                        update.message.reply_text(self.deal_text_generator(deal))

                    message = "I've found {} new deal(s)".format(len(new))
                    update.message.reply_text(message)
        else:
            update.message.reply_text("You have to do /start first!")

    def addtracker(self, update, context):
        update.message.reply_text("Oh hello! I'm here to guide you inside the 'target adder' wizard!, let's start!")

        update.message.reply_text("First step: send me a name for your target! (Ex: 'New bike'")
        return self.SET_TARGET_NAME

    def check_target_name(self, update, context):
        # Save tracker id
        self.tracker.id = update.effective_user.id

        #Read message
        text = update.message.text

        # Check text data
        if len(text) > 0:
            update.message.reply_text("Okay, that's an awesome name for your target")

            # Save name
            self.tracker.name = text

            update.message.reply_text("Second step: send me a tutti.ch valid query link!")
            return self.SET_TARGET_URL
        else:
            update.message.reply_text("Nope, you have to send me a right name! .-.")
            return self.SET_TARGET_NAME

    def check_target_url(self, update, context):
        text = update.message.text

        # Check url data
        if len(text) > 0:
            update.message.reply_text("Okay, thanks for the url!")
            self.tracker.url = text

            self.insert_tracker(self.tracker)
            update.message.reply_text("Tracker save to my data center")
        else:
            update.message.reply_text("Nope, you gaz af! .-.")

        return ConversationHandler.END

    def insert_tracker(self, tracker):
        # Insert tracker to database
        self.db.add_tracker(self.tracker.id,self.tracker.name,self.tracker.url,False)

    def cancel_tracker_wizard(self, update, context):
        self.tracker = Tracker("nome", "url", -1, False)
    def stop(self, update, context):
        self.db.remove_user(update.effective_user.id)

        update.message.reply_text('Bye {}! I hope we meet again soon!'.format(
            update.message.from_user.first_name))

    def send_broadcast(self,message: str):
        for user in self.db.get_users():
            print("Sending to ", user.user_id, "...")
            self.DP.bot.send_message(user.user_id, message)

    @staticmethod
    def deal_text_generator(deal: Deal):
        message = "Offerta trovata!🔥\n" \
                  "Titolo: {}📜\n" \
                  "Prezzo: {}💰\n" \
                  "Zona: {},{}📍\n" \
                  "Data caricamento: {}📅\n" \
                  "Url annuncio: {}".format(deal.title, deal.price, deal.loc_city, deal.loc_cap, deal.date, deal.url)

        return message

    def is_new_user(self, user_id):
        found = False
        for user in self.db.get_users():
            if user.user_id == user_id:
                print("[Info] User already in database")
                found = True
                break

        return not found

    @staticmethod
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
<<<<<<< HEAD
=======
                pprint(new_deals)
                return new_deals
>>>>>>> 9356d9cd85718b52effa301f9ec0666cf9f0eb28

                new_deals.reverse()
                return new_deals
        else:
            print("[Info] No saved deals detected")
            new.reverse()
            return new