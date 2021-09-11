class DataHolder:
    __instance = None

    ADMIN = 2
    USER = 1
    INVALID_USERNAME = -1

    USERNAME_INPUT = 1
    INVALID = -1

    def __init__(self):
        if DataHolder.__instance is None:
            self.__valid_users = {}
            self.__states = {}
            self.__registered_users = {}

    @staticmethod
    def get_instance():
        if DataHolder.__instance is None:
            DataHolder.__instance = DataHolder()

        return DataHolder.__instance

    def push_new_valid_user(self, username, roll):
        self.__valid_users[username] = roll

    def get_valid_user(self, username):
        return self.__valid_users.get(username, DataHolder.INVALID_USERNAME)

    def set_state(self, user_id, state):
        self.__states[user_id] = state

    def get_state(self, user_id):
        return self.__states.get(user_id, DataHolder.INVALID_USERNAME)

    def register(self, user_id, username):
        if user_id not in self.__registered_users.keys():
            self.__registered_users[user_id] = self.__valid_users[username]

            del self.__valid_users[username]
            return self.__registered_users[user_id]
        return None
