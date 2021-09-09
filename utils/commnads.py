from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot

    bot.send_message(user.id, "Welcome to Bitoks Q&A bot!")
