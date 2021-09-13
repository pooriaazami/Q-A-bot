from telegram import Update, Bot, User, Message, Chat
from telegram.ext import CallbackContext

from utils.CommandMap import CommandMap
from utils.DataHolder import DataHolder


def start(update: Update, callback: CallbackContext):
    data_holder = DataHolder.get_instance()

    user = update.effective_user
    bot = callback.bot

    if update.effective_chat.type == 'private':
        bot.send_message(user.id, "Welcome to Bitoks Q&A bot!")
        bot.send_message(user.id, 'Please enter your username')

        data_holder.set_state(user.id, DataHolder.USERNAME_INPUT)
    else:
        bot.send_message(update.effective_chat.id, 'You can only use start command in groups',
                         reply_to_message_id=update.effective_message.message_id)

        # reset states


def begin_command(update: Update, callback: CallbackContext, args):
    if DataHolder.get_instance().effective_chat_id is None:
        DataHolder.get_instance().effective_chat_id = update.effective_chat.id
        callback.bot.send_message(DataHolder.get_instance().effective_chat_id, 'Q&A started')
    else:
        callback.bot.send_message(update.effective_chat.id, 'Q&A is in progress')


def end_command(update: Update, callback: CallbackContext, args):
    DataHolder.get_instance().effective_chat_id = None


def process_text_commands(update: Update, callback: CallbackContext):
    args = update.message.text.split(' ')
    args[0] = args[0].lower()

    CommandMap.get_instance().get_command(args[0])(update, callback, args[1:])

    # if args[0] == 'start':
    #     pass
    # elif args[0] == 'end':
    #     pass


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
        process_text_commands(update, callback)
    elif data_holder.get_state(user.id) == DataHolder.TEXT_MESSAGE_INPUT:
        bot.send_message(data_holder.get_instance().effective_chat_id, update.message.text)
    else:
        bot.send_message(user.id, 'Invalid message')
