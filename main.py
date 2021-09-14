from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils.CommandMap import CommandMap
from utils.DataHolder import DataHolder
from utils.commnads import start, text_message_handler, begin_command, end_command, add_command, list_command, branch


def read_token():
    with open('token.txt') as file:
        token = file.read()

    return token


def read_users():
    data_holder = DataHolder.get_instance()

    with open('users.txt') as file:
        for line in file:
            username, roll = line.strip().split(' ')
            data_holder.push_new_valid_user(username,
                                            DataHolder.ADMIN if roll == 'admin' else DataHolder.USER)


def main():
    token = read_token()

    read_users()

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    command_map = CommandMap.get_instance()

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, text_message_handler))

    command_map.add_command('begin', begin_command, 'begin command help')
    command_map.add_command('end', end_command, 'end command help')
    command_map.add_command('add', add_command, 'add command help')
    command_map.add_command('list', list_command, 'list command help')
    command_map.add_command('branch', branch, 'branch help')

    updater.start_polling()


if __name__ == '__main__':
    main()
