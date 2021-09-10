class DataHolder:
    __instance = None

    ADMIN = 2
    USER = 1
    INVALID_USERNAME = -1

    def __init__(self):
        if DataHolder.__instance is None:
            self.__registered_users = {}

    @staticmethod
    def get_instance():
        if DataHolder.__instance is None:
            DataHolder.__instance = DataHolder()

        return DataHolder.__instance

    def push_new_registered_user(self, username, roll):
        self.__registered_users[username] = roll

    def get_registered_user(self, username):
        return self.__registered_users.get(username, DataHolder.INVALID_USERNAME)
