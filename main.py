import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils.CommandMap import CommandMap
from utils.MessageHandler import text_message_handler, sticker_handler, voice_handler, animation_handler, \
    contact_handler, audio_handler, video_handler, photo_handler, video_note_handler, poll_handler, document_handler
from utils.commnads import start, begin_command, end_command, add_command, list_command, \
    branch_command, report_command, send_command, update_command, help_command, reset_command, random_command

from utils.initial_actions import read_token, read_users


def main():
    logging.info('bot started')
    token = read_token()

    read_users()

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    command_map = CommandMap.get_instance()

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, text_message_handler))
    dispatcher.add_handler(MessageHandler(Filters.sticker, sticker_handler))
    dispatcher.add_handler(MessageHandler(Filters.voice, voice_handler))
    dispatcher.add_handler(MessageHandler(Filters.animation, animation_handler))
    dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
    dispatcher.add_handler(MessageHandler(Filters.audio, audio_handler))
    dispatcher.add_handler(MessageHandler(Filters.video, video_handler))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
    dispatcher.add_handler(MessageHandler(Filters.video_note, video_note_handler))
    dispatcher.add_handler(MessageHandler(Filters.poll, poll_handler))
    dispatcher.add_handler(MessageHandler(Filters.document, document_handler))

    command_map.add_command('begin', begin_command, 'begin command help')
    command_map.add_command('end', end_command, 'end command help')
    command_map.add_command('add', add_command, 'add command help')
    command_map.add_command('list', list_command, 'list command help')
    command_map.add_command('branch', branch_command, 'branch help')
    command_map.add_command('report', report_command, 'report command help')
    command_map.add_command('send', send_command, 'send command help')
    command_map.add_command('update', update_command, 'update command help')
    command_map.add_command('help', help_command, 'help command help')
    command_map.add_command('reset', reset_command, 'reset command help')
    command_map.add_command('random', random_command, 'random command help')

    updater.start_polling()


if __name__ == '__main__':
    main()
