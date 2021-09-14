from telegram import Update, Bot, User, Message, Chat
from telegram.ext import CallbackContext

from utils.CommandMap import CommandMap
from utils.DataHolder import DataHolder, string_to_roll, roll_to_string


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
        bot.send_message(update.effective_chat.id, 'You can only use start command in groups',
                         reply_to_message_id=update.effective_message.message_id)


# begin
def begin_command(update: Update, callback: CallbackContext, args):
    if DataHolder.get_instance().effective_chat_id is None:
        DataHolder.get_instance().effective_chat_id = update.effective_chat.id
        DataHolder.get_instance().update_all_states(DataHolder.WAIT, DataHolder.MESSAGE_INPUT)
        callback.bot.send_message(DataHolder.get_instance().effective_chat_id, 'Q&A started')
    else:
        callback.bot.send_message(update.effective_chat.id, 'Q&A is in progress')


# end
def end_command(update: Update, callback: CallbackContext, args):
    bot = callback.bot

    if update.effective_chat.id == DataHolder.get_instance().effective_chat_id:
        DataHolder.get_instance().effective_chat_id = None
        DataHolder.get_instance().remove_branches()
        bot.send_message(update.effective_chat.id, 'Done')
    elif update.effective_chat.id in DataHolder.get_instance().branches:
        bot.send_message(update.effective_chat.id, 'You can not end Q&A in a branch or pv')


# add <username> <roll>
def add_command(update: Update, callback: CallbackContext, args):
    bot = callback.bot
    args[1] = args[1].lower()

    if len(args) == 2:
        DataHolder.get_instance().push_new_valid_user(args[0], string_to_roll(args[1]))
    else:
        bot.send_message(update.effective_chat.id, 'Check your command')


# list <registered | remaining>
def list_command(update: Update, callback: CallbackContext, args):
    bot = callback.bot

    if len(args) == 1:
        if args[0] == 'registered':
            users = DataHolder.get_instance().registered_users

            data = []
            for user, roll in users.items():
                chat = bot.get_chat(user)
                data.append(f'firstname: {chat.first_name},'
                            f' username: @{chat.username},'
                            f' roll: {roll_to_string(roll)}')

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

    count = DataHolder.get_instance().count
    users = DataHolder.get_instance().registered_users
    average = count / len(users)

    bot.send_message(update.effective_chat.id, f'message_count: {count}\nusers: {len(users)}\naverage: {average}')


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
    elif data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count()
        bot.send_message(data_holder.get_instance().effective_chat_id, update.message.text)

        for chat in DataHolder.get_instance().branches:
            bot.send_message(chat, update.message.text)

    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def sticker_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count()
        bot.send_sticker(data_holder.get_instance().effective_chat_id, update.message.sticker)

        for chat in DataHolder.get_instance().branches:
            bot.send_sticker(chat, update.message.sticker)

    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def voice_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count()
        bot.send_voice(data_holder.get_instance().effective_chat_id, update.message.voice,
                       caption=update.message.caption)

        for chat in DataHolder.get_instance().branches:
            bot.send_voice(chat, update.message.voice, caption=update.message.caption)

    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def photo_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count()

        for item in update.message.photo:
            bot.send_photo(data_holder.get_instance().effective_chat_id, item.file_id,
                           caption=update.message.caption)

        for item in update.message.photo:
            for chat in DataHolder.get_instance().branches:
                bot.send_photo(chat, item.file_id, caption=update.message.caption)

    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def contact_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count()
        bot.send_contact(data_holder.get_instance().effective_chat_id, update.message.contact)

        for chat in DataHolder.get_instance().branches:
            bot.send_contact(chat, update.message.contact)

    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def animation_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count()
        bot.send_animation(data_holder.get_instance().effective_chat_id, update.message.animation)

        for chat in DataHolder.get_instance().branches:
            bot.send_animation(chat, update.message.animation)

        else:
            bot.send_message(update.effective_chat.id, 'Invalid message')


def document_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count()
        bot.send_document(data_holder.get_instance().effective_chat_id, update.message.document,
                          caption=update.message.caption)

        for chat in DataHolder.get_instance().branches:
            bot.send_document(chat, update.message.document, caption=update.message.caption)

    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def video_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count()
        bot.send_video(data_holder.get_instance().effective_chat_id, update.message.video,
                       caption=update.message.caption)

        for chat in DataHolder.get_instance().branches:
            bot.send_video(chat, update.message.video, caption=update.message.caption)

    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def audio_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count()
        bot.send_audio(data_holder.get_instance().effective_chat_id, update.message.audio,
                       caption=update.message.caption)

        for chat in DataHolder.get_instance().branches:
            bot.send_audio(chat, update.message.audio, caption=update.message.audio)

    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def video_note_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count()
        bot.send_video_note(data_holder.get_instance().effective_chat_id, update.message.video_note)

        for chat in DataHolder.get_instance().branches:
            bot.send_video_note(chat, update.message.video_note)

    else:
        bot.send_video_note(update.effective_chat.id, 'Invalid message')
