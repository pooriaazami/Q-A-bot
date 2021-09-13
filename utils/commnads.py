from telegram import Update, Bot, User
from telegram.ext import CallbackContext

from utils.DataHolder import DataHolder


def start(update: Update, callback: CallbackContext):
    data_holder = DataHolder.get_instance()

    user = update.effective_user
    bot = callback.bot

    bot.send_message(user.id, "Welcome to Bitoks Q&A bot!")
    bot.send_message(user.id, 'Please enter your username')

    data_holder.set_state(user.id, DataHolder.USERNAME_INPUT)


def process_text_commands(command: str, bot: Bot, user: User):
    args = command.split(' ')
    args[0] = args[0].lower()

    if args[0] == 'start':
        pass
    elif args[0] == 'end':
        pass


def text_message_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.USERNAME_INPUT:
        if data_holder.get_valid_user(update.effective_message.text) != DataHolder.INVALID_USERNAME:
            roll = data_holder.register(user.id, update.effective_message.text)
            if roll:
                bot.send_message(user.id, f'You have been registered as {roll}')
            else:
                bot.send_message(user.id, 'You have already registered')
        else:
            bot.send_message(user.id, 'Invalid username')
    elif data_holder.get_state(user.id) == DataHolder.COMMAND_INPUT:
        pass
    elif data_holder.get_state(user.id) == DataHolder.TEXT_MESSAGE_INPUT:
        pass
    else:
        bot.send_message(user.id, 'Invalid message')
