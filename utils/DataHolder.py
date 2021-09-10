class DataHolder:
    __instance = None

    ADMIN = 2
    USER = 1
    INVALID_USERNAME = -1

    USERNAME_INPUT = 1
    INVALID = -1

    def __init__(self):
        if DataHolder.__instance is None:
            self.__registered_users = {}
            self.__states = {}

    @staticmethod
    def get_instance():
        if DataHolder.__instance is None:
            DataHolder.__instance = DataHolder()

        return DataHolder.__instance

    def push_new_registered_user(self, username, roll):
        self.__registered_users[username] = roll

    def get_registered_user(self, username):
        return self.__registered_users.get(username, DataHolder.INVALID_USERNAME)

    def set_state(self, user_id, state):
        self.__states[user_id] = state

    def get_state(self, user_id):
        return self.__states.get(user_id, DataHolder.INVALID_USERNAME)
