from telegram.ext import Updater, CommandHandler

from utils.DataHolder import DataHolder
from utils.commnads import start


def read_token():
    with open('token.txt') as file:
        token = file.read()

    return token


def read_users():
    data_holder = DataHolder.get_instance()

    with open('users.txt') as file:
        for line in file:
            username, roll = line.strip().split(' ')
            data_holder.push_new_registered_user(username,
                                                 DataHolder.ADMIN if roll == 'admin' else DataHolder.USER)


def main():
    token = read_token()

    read_users()

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()


if __name__ == '__main__':
    main()
