from telegram import Update
from telegram.ext import CallbackContext

from utils.CommandMap import CommandMap
from utils.DataHolder import DataHolder
from utils.utils import string_to_role, role_to_string, get_destinations


def start(update: Update, callback: CallbackContext):
    data_holder = DataHolder.get_instance()

    user = update.effective_user
    bot = callback.bot

    if update.effective_chat.type == 'private':
        if user.id in DataHolder.get_instance().registered_users.keys():
            bot.send_message(user.id, 'You have already registered')
        else:
            bot.send_message(user.id, "Welcome to Bitoks Q&A bot!")
            bot.send_message(user.id, 'Please enter your username')

            data_holder.set_state(user.id, DataHolder.USERNAME_INPUT)
    else:
        bot.send_message(update.effective_chat.id, 'You can only use start command in private chats',
                         reply_to_message_id=update.effective_message.message_id)


# begin
def begin_command(update: Update, callback: CallbackContext, args):
    data_holder = DataHolder.get_instance()
    bot = callback.bot

    if data_holder.effective_chat_id is None:
        data_holder.effective_chat_id = update.effective_chat.id
        data_holder.update_all_states(DataHolder.WAIT, DataHolder.MESSAGE_INPUT)
        callback.bot.send_message(DataHolder.get_instance().effective_chat_id, 'Q&A started')

        destinations = get_destinations('users')
        for destination in destinations:
            bot.send_message(destination, 'You can now text us')
    else:
        callback.bot.send_message(update.effective_chat.id, 'Q&A is in progress')


# end
def end_command(update: Update, callback: CallbackContext, args):
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if update.effective_chat.id == data_holder.effective_chat_id:
        data_holder.effective_chat_id = None
        data_holder.remove_branches()
        data_holder.update_all_states(DataHolder.MESSAGE_INPUT, DataHolder.WAIT)
        data_holder.update_all_states(DataHolder.SEND_INPUT, DataHolder.COMMAND_INPUT)

        destinations = get_destinations('all')

        for chat in destinations:
            bot.send_message(chat, 'Q&A is over. Hope see you soon.')

        data_holder.remove_branches()
        bot.send_message(update.effective_chat.id, 'Done')
    elif update.effective_chat.id in data_holder.branches:
        bot.send_message(update.effective_chat.id, 'You can not end Q&A in a branch or pv')


# add <username> <role>
def add_command(update: Update, callback: CallbackContext, args):
    bot = callback.bot
    args[1] = args[1].lower()

    if len(args) == 2:
        DataHolder.get_instance().push_new_valid_user(args[0], string_to_role(args[1]))
    else:
        bot.send_message(update.effective_chat.id, 'Check your command')


# list <registered | remaining>
def list_command(update: Update, callback: CallbackContext, args):
    bot = callback.bot

    if len(args) == 1:
        if args[0] == 'registered':
            users = DataHolder.get_instance().registered_users

            data = []
            for user, role in users.items():
                chat = bot.get_chat(user)
                data.append(f'firstname: {chat.first_name},'
                            f' username: @{chat.username},'
                            f' role: {role_to_string(role)},'
                            f'id: {chat.id}')

            bot.send_message(update.effective_chat.id, '\n'.join(data))
        elif args[0] == 'remaining':
            bot.send_message(update.effective_chat.id, '\n'.join(DataHolder.get_instance().remaining_valid_usernames))
        else:
            bot.send_message(update.effective_chat.id, 'Check your command')
    else:
        bot.send_message(update.effective_chat.id, 'Check your command')


def process_text_commands(update: Update, callback: CallbackContext):
    args = update.message.text.split(' ')
    args[0] = args[0].lower()

    CommandMap.get_instance().get_command(args[0])(update, callback, args[1:])


def branch_command(update: Update, callback: CallbackContext, args):
    bot = callback.bot

    if len(args) == 0:
        if DataHolder.get_instance().effective_chat_id is not None:
            DataHolder.get_instance().add_branch(update.effective_chat.id)
            bot.send_message(DataHolder.get_instance().effective_chat_id,
                             f'new branch added\n{update.effective_chat.title}')
            bot.send_message(update.effective_chat.id, 'Done')
        else:
            bot.send_message(update.effective_chat.id, 'Q&A has not started yet')
    else:
        if args[0] == 'list':
            data = [str(bot.get_chat(chat).title) for chat in DataHolder.get_instance().branches]

            if len(data) != 0:
                bot.send_message(update.effective_chat.id, '\n'.join(data))
            else:
                bot.send_message(update.effective_chat.id, 'There is no branch')


def report_command(update: Update, callback: CallbackContext, args):
    bot = callback.bot

    counts = DataHolder.get_instance().count

    text = ''
    total = 0
    for key, value in counts.items():
        text += f'{key}: {value}\n'
        total += value

    users = DataHolder.get_instance().registered_users
    average = total / len(users)

    bot.send_message(update.effective_chat.id,
                     f'{text}\ntotal count: {total}\nusers: {len(users)}\naverage: {average}')


def send_command(update: Update, callback: CallbackContext, args):
    if len(args) == 1:
        DataHolder.get_instance().push_data(update.effective_user.id, args[0])
        DataHolder.get_instance().set_state(update.effective_user.id, DataHolder.SEND_INPUT)
    else:
        callback.bot.send_message(update.effective_chat.id, 'check your command',
                                  reply_to_message_id=update.effective_message.message_id)


def update_command(update: Update, callback: CallbackContext, args):
    bot = callback.bot

    if len(args) == 2:
        username = int(args[0])
        role = args[1]

        result = DataHolder.get_instance().set_role(username, string_to_role(role))

        if result:
            bot.send_message(update.effective_chat.id, 'Done')
            bot.send_message(username, f'Your role has benn changed to: {role}')
        else:
            bot.send_message(update.effective_chat.id, 'check your command')
    else:
        bot.send_message(update.effective_chat.id, 'check your command')


def help_command(update: Update, callback: CallbackContext, args):
    bot = callback.bot

    if len(args) == 1:
        text = CommandMap.get_instance().get_help(args[0])
        bot.send_message(update.effective_chat.id, text)
    else:
        bot.send_message(update.effective_chat.id, 'check your command')


def reset_command(update: Update, callback: CallbackContext, args):
    bot = callback.bot

    if len(args) == 1:
        if args[0] == 'messages':
            DataHolder.get_instance().reset_counts()
            bot.send_message(update.effective_chat.id, 'Done')
    else:
        bot.send_message(update.effective_chat.id, 'Check your command')
