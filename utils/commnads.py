from telegram import Update
from telegram.ext import CallbackContext

from utils.DataHolder import DataHolder


def start(update: Update, callback: CallbackContext):
    data_holder = DataHolder.get_instance()

    user = update.effective_user
    bot = callback.bot

    bot.send_message(user.id, "Welcome to Bitoks Q&A bot!")
    bot.send_message(user.id, 'Please enter your username')

    data_holder.set_state(user.id, DataHolder.USERNAME_INPUT)
