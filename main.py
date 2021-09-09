from telegram.ext import Updater, CommandHandler

from utils.commnads import start


def read_token():
    with open('token.txt') as file:
        token = file.read()

    return token


def main():
    token = read_token()

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()


if __name__ == '__main__':
    main()
