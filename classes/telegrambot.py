from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from classes.databasemanager import DatabaseManager
from classes.deal import Deal
from config.params import Params


class TelegramBot:
    TOKEN = Params.TOKEN
    bot_status = False

    def __init__(self,database_manager: DatabaseManager):
        self.db = database_manager
        self.DP = None

    def start_bot(self):

        updater = Updater(self.TOKEN, use_context=True)

        # Get the dispatcher to register handlers
        self.DP = updater.dispatcher

        self.bot_status = True
        print("Telegram bot started successfully")

        self.DP.add_handler(CommandHandler("start", self.start))
        self.DP.add_handler(CommandHandler("stop", self.stop))

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

    def start(self, update, context):
        user_id = update.effective_user.id

        # Check if users exists already
        found = False
        for user in self.db.get_users():
            if user.user_id == user_id:
                print("[Info] User already in database")
                found = True
                break

        if not found:
            print("[INFO] New user detected!!!")
            self.db.add_user(int(user_id))
            update.message.reply_text('Hello {} welcome in TuttiDealFinder! Digit /help for the list of the avaible commands'.format(update.message.from_user.first_name))
        else:
            update.message.reply_text('Hello {}, we know each other already.'.format(update.message.from_user.first_name))

    def stop(self, update, context):
        # TODO: Fix stop method
        self.db.remove_user(update.effective_user.id)

        update.message.reply_text('Bye {}! I hope we meet again soon!'.format(
            update.message.from_user.first_name))

    def send_broadcast(self,message: str):
        for user in self.db.get_users():
            print("Sending to ", user.user_id,"...")
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