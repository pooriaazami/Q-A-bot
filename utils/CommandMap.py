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
        bot = callback.bot
        bot.send_message(update.effective_chat.id, 'Command not found')

    def add_command(self, command_name, function, helper_data):
        self.__map[command_name] = {
            'function': function,
            'help': helper_data
        }

    def get_command(self, command):
        if command in self.__map.keys():
            return self.__map[command]['function']

        return self.error_command
