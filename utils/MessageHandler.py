from telegram import Update
from telegram.ext import CallbackContext

from utils.DataHolder import DataHolder
from utils.commnads import process_text_commands
from utils.utils import get_destinations, roll_to_string


def text_message_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.USERNAME_INPUT:
        if data_holder.get_valid_user(update.effective_message.text) != DataHolder.INVALID_USERNAME:
            roll = data_holder.register(user.id, update.effective_message.text)
            if roll:
                bot.send_message(user.id, f'You have been registered as {roll_to_string(roll)}')
            else:
                bot.send_message(user.id, 'You have already registered')
        else:
            bot.send_message(user.id, 'Invalid username')
    elif data_holder.get_state(user.id) == DataHolder.COMMAND_INPUT:
        process_text_commands(update, callback)
    elif data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count('text')
        bot.send_message(data_holder.get_instance().effective_chat_id, update.message.text)

        for chat in DataHolder.get_instance().branches:
            bot.send_message(chat, update.message.text)
    elif data_holder.get_state(user.id) == DataHolder.SEND_INPUT:
        if update.message.text == '# cancel':
            data_holder.set_state(user.id, DataHolder.COMMAND_INPUT)
            bot.send_message(update.effective_chat.id, 'process canceled')
            return

        destinations = get_destinations(data_holder.get_data(user.id))

        if destinations is not None:
            for destination in destinations:
                message = bot.send_message(destination, 'admin message:')
                bot.send_message(destination, update.message.text, reply_to_message_id=message.message_id)
        else:
            bot.send_message(update.effective_chat.id, 'invalid destination')
        data_holder.set_state(user.id, DataHolder.COMMAND_INPUT)

    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def sticker_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count('sticker')
        bot.send_sticker(data_holder.get_instance().effective_chat_id, update.message.sticker)

        for chat in DataHolder.get_instance().branches:
            bot.send_sticker(chat, update.message.sticker)

    elif data_holder.get_state(user.id) == DataHolder.SEND_INPUT:
        destinations = get_destinations(data_holder.get_data(user.id))

        if destinations is not None:
            for destination in destinations:
                message = bot.send_message(destination, 'admin message:')
                bot.send_sticker(destination, update.message.sticker, reply_to_message_id=message.message_id)
        else:
            bot.send_message(update.effective_chat.id, 'invalid destination')
        data_holder.set_state(user.id, DataHolder.COMMAND_INPUT)
    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def voice_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count('voice')
        bot.send_voice(data_holder.get_instance().effective_chat_id, update.message.voice,
                       caption=update.message.caption)

        for chat in DataHolder.get_instance().branches:
            bot.send_voice(chat, update.message.voice, caption=update.message.caption)
    elif data_holder.get_state(user.id) == DataHolder.SEND_INPUT:
        destinations = get_destinations(data_holder.get_data(user.id))

        if destinations is not None:
            for destination in destinations:
                message = bot.send_message(destination, 'admin message:')
                bot.send_voice(destination, update.message.voice, caption=update.message.caption,
                               reply_to_message_id=message.message_id)
        else:
            bot.send_message(update.effective_chat.id, 'invalid destination')
        data_holder.set_state(user.id, DataHolder.COMMAND_INPUT)
    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def photo_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count('photo')

        for item in update.message.photo:
            bot.send_photo(data_holder.get_instance().effective_chat_id, item.file_id,
                           caption=update.message.caption)

        for item in update.message.photo:
            for chat in DataHolder.get_instance().branches:
                bot.send_photo(chat, item.file_id, caption=update.message.caption)

    elif data_holder.get_state(user.id) == DataHolder.SEND_INPUT:
        destinations = get_destinations(data_holder.get_data(user.id))

        if destinations is not None:
            for destination in destinations:
                message = bot.send_message(destination, 'admin message:')
                bot.send_photo(destination, update.message.photo[0], caption=update.message.caption,
                               reply_to_message_id=message.message_id)
        else:
            bot.send_message(update.effective_chat.id, 'invalid destination')
        data_holder.set_state(user.id, DataHolder.COMMAND_INPUT)
    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def contact_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count('contact')
        bot.send_contact(data_holder.get_instance().effective_chat_id, update.message.contact)

        for chat in DataHolder.get_instance().branches:
            bot.send_contact(chat, update.message.contact)

    elif data_holder.get_state(user.id) == DataHolder.SEND_INPUT:
        destinations = get_destinations(data_holder.get_data(user.id))

        if destinations is not None:
            for destination in destinations:
                message = bot.send_message(destination, 'admin message:')
                bot.send_contact(destination, update.message.contact, reply_to_message_id=message.message_id)
        else:
            bot.send_message(update.effective_chat.id, 'invalid destination')
        data_holder.set_state(user.id, DataHolder.COMMAND_INPUT)
    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def animation_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count('gif')
        bot.send_animation(data_holder.get_instance().effective_chat_id, update.message.animation)

        for chat in DataHolder.get_instance().branches:
            bot.send_animation(chat, update.message.animation)
    elif data_holder.get_state(user.id) == DataHolder.SEND_INPUT:
        destinations = get_destinations(data_holder.get_data(user.id))

        if destinations is not None:
            for destination in destinations:
                message = bot.send_message(destination, 'admin message:')
                bot.send_animation(destination, update.message.animation, reply_to_message_id=message.message_id)
        else:
            bot.send_message(update.effective_chat.id, 'invalid destination')
    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def document_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance('file')

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count()
        bot.send_document(data_holder.get_instance().effective_chat_id, update.message.document,
                          caption=update.message.caption)

        for chat in DataHolder.get_instance().branches:
            bot.send_document(chat, update.message.document, caption=update.message.caption)
    elif data_holder.get_state(user.id) == DataHolder.SEND_INPUT:
        destinations = get_destinations(data_holder.get_data(user.id))

        if destinations is not None:
            for destination in destinations:
                message = bot.send_message(destination, 'admin message:')
                bot.send_document(destination, update.message.document, caption=update.message.caption,
                                  reply_to_message_id=message.message_id)
        else:
            bot.send_message(update.effective_chat.id, 'invalid destination')
        data_holder.set_state(user.id, DataHolder.COMMAND_INPUT)
    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def video_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count('video')
        bot.send_video(data_holder.get_instance().effective_chat_id, update.message.video,
                       caption=update.message.caption)

        for chat in DataHolder.get_instance().branches:
            bot.send_video(chat, update.message.video, caption=update.message.caption)
    elif data_holder.get_state(user.id) == DataHolder.SEND_INPUT:
        destinations = get_destinations(data_holder.get_data(user.id))

        if destinations is not None:
            for destination in destinations:
                message = bot.send_message(destination, 'admin message:')
                bot.send_video(destination, update.message.video, caption=update.message.caption,
                               reply_to_message_id=message.message_id)
        else:
            bot.send_message(update.effective_chat.id, 'invalid destination')
        data_holder.set_state(user.id, DataHolder.COMMAND_INPUT)

    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def audio_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count('audio')
        bot.send_audio(data_holder.get_instance().effective_chat_id, update.message.audio,
                       caption=update.message.caption)

        for chat in DataHolder.get_instance().branches:
            bot.send_audio(chat, update.message.audio, caption=update.message.audio)
    elif data_holder.get_state(user.id) == DataHolder.SEND_INPUT:
        destinations = get_destinations(data_holder.get_data(user.id))

        if destinations is not None:
            for destination in destinations:
                message = bot.send_message(destination, 'admin message:')
                bot.send_audio(destination, update.message.audio, caption=update.message.caption,
                               reply_to_message_id=message.message_id)
        else:
            bot.send_message(update.effective_chat.id, 'invalid destination')
        data_holder.set_state(user.id, DataHolder.COMMAND_INPUT)

    else:
        bot.send_message(update.effective_chat.id, 'Invalid message')


def video_note_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        data_holder.increase_message_count('video message')
        bot.send_video_note(data_holder.get_instance().effective_chat_id, update.message.video_note)

        for chat in DataHolder.get_instance().branches:
            bot.send_video_note(chat, update.message.video_note)
    elif data_holder.get_state(user.id) == DataHolder.SEND_INPUT:
        destinations = get_destinations(data_holder.get_data(user.id))

        if destinations is not None:
            for destination in destinations:
                message = bot.send_message(destination, 'admin message:')
                bot.send_video_note(destination, update.message.video_note, caption=update.message.caption,
                                    reply_to_message_id=message.message_id)
        else:
            bot.send_message(update.effective_chat.id, 'invalid destination')
        data_holder.set_state(user.id, DataHolder.COMMAND_INPUT)

    else:
        bot.send_video_note(update.effective_chat.id, 'Invalid message')


def poll_handler(update: Update, callback: CallbackContext):
    user = update.effective_user
    bot = callback.bot
    data_holder = DataHolder.get_instance()

    if data_holder.get_state(user.id) == DataHolder.MESSAGE_INPUT:
        bot.send_message(update.effective_chat.id, 'You can not send polls')

    elif data_holder.get_state(user.id) == DataHolder.SEND_INPUT:
        destinations = get_destinations(data_holder.get_data(user.id))

        if destinations is not None:
            for destination in destinations:
                bot.forward_message(destination, update.effective_chat.id, update.effective_message.message_id)
        else:
            bot.send_message(update.effective_chat.id, 'invalid destination')
        data_holder.set_state(user.id, DataHolder.COMMAND_INPUT)

    else:
        bot.send_video_note(update.effective_chat.id, 'Invalid message')
