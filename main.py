from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from utils.DataHolder import DataHolder
from utils.commnads import start, text_message_handler


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

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, text_message_handler))

    updater.start_polling()


if __name__ == '__main__':
    main()
