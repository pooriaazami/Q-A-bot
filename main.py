from telegram.ext import Updater


def read_token():
    with open('token.txt') as file:
        token = file.read()

    return token


def main():
    token = read_token()

    updater = Updater()
    dispatcher = updater.dispatcher

    updater.start_polling()


if __name__ == '__main__':
    main()
