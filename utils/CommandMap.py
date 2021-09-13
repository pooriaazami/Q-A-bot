class CommandMap:
    __instance = None

    def __init__(self):
        if CommandMap.__instance is None:
            self.__map = {}

    @staticmethod
    def get_instance():
        if CommandMap.__instance is None:
            CommandMap.__instance = CommandMap()

        return CommandMap.__instance

    @staticmethod
    def error_command(update, callback, args):
        user = update.effective_user
        bot = callback.bot
        bot.send_message(user.id, 'Command not found')

    def add_command(self, command_name, function, helper_data):
        self.__map[command_name] = {
            'function': function,
            'help': helper_data
        }

    def get_command(self, command):
        return self.__map.get(command, self.error_command)['function']
