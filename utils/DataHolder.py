class DataHolder:
    __instance = None

    ADMIN = 2
    USER = 1
    INVALID_USERNAME = -1

    USERNAME_INPUT = 1
    COMMAND_INPUT = 2
    TEXT_MESSAGE_INPUT = 3
    INVALID = -1

    def __init__(self):
        if DataHolder.__instance is None:
            self.__valid_users = {}
            self.__states = {}
            self.__registered_users = {}
            self.__effective_chat_id = None
            self.__branches = []

    @staticmethod
    def get_instance():
        if DataHolder.__instance is None:
            DataHolder.__instance = DataHolder()

        return DataHolder.__instance

    @property
    def effective_chat_id(self):
        return self.__effective_chat_id

    @effective_chat_id.setter
    def effective_chat_id(self, value):
        self.__effective_chat_id = value

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

            if self.__registered_users[user_id] == DataHolder.ADMIN:
                self.__states[user_id] = DataHolder.COMMAND_INPUT
            elif self.__registered_users[user_id] == DataHolder.USER:
                self.__states[user_id] = DataHolder.TEXT_MESSAGE_INPUT

            del self.__valid_users[username]
            return self.__registered_users[user_id]
        return None

    @property
    def remaining_valid_usernames(self):
        return list(self.__valid_users.keys())

    @property
    def registered_users(self):
        return {username: self.__registered_users[username] for username in self.__registered_users.keys()}

    def add_branch(self, chat_id):
        self.__branches.append(chat_id)

    @property
    def branches(self):
        return self.__branches

    def remove_branches(self):
        self.__branches = []
