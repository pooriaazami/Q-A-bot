class DataHolder:
    __instance = None

    ADMIN = 2
    USER = 1
    INVALID_USERNAME = -1

    USERNAME_INPUT = 1
    COMMAND_INPUT = 2
    MESSAGE_INPUT = 3
    WAIT = 4
    SEND_INPUT = 5
    INVALID = -1

    def __init__(self):
        if DataHolder.__instance is None:
            self.__valid_users = {}
            self.__states = {}
            self.__registered_users = {}
            self.__data = {}
            self.__effective_chat_id = None
            self.__branches = []
            self.__message_count = {
                'text': 0,
                'voice': 0,
                'audio': 0,
                'video message': 0,
                'video': 0,
                'file': 0,
                'sticker': 0,
                'photo': 0,
                'contact': 0,
                'gif': 0
            }

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
                if self.__effective_chat_id is None:
                    self.__states[user_id] = DataHolder.WAIT
                else:
                    self.__states[user_id] = DataHolder.MESSAGE_INPUT

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
    def users(self):
        return [user_id for user_id, roll in self.__registered_users.items() if roll == DataHolder.USER]

    @property
    def admins(self):
        return [user_id for user_id, roll in self.__registered_users.items() if roll == DataHolder.ADMIN]

    @property
    def branches(self):
        return self.__branches

    def remove_branches(self):
        self.__branches = []

    def increase_message_count(self, message_type):
        if message_type in self.__message_count.keys():
            self.__message_count[message_type] += 1

    @property
    def count(self):
        return self.__message_count

    def reset_counts(self):
        for key in self.__message_count.keys():
            self.__message_count[key] = 0

    def update_all_states(self, first, second):
        for key, item in self.__states.items():
            if item == first:
                self.__states[key] = second

    def push_data(self, user_id, data):
        self.__data[user_id] = data

    def get_data(self, user_id):
        return self.__data.get(user_id, None)

    def pop_data(self, user_id):
        del self.__data[user_id]

    def set_roll(self, user_id, new_roll):
        if user_id in self.__registered_users.keys():
            self.__registered_users[user_id] = new_roll

            if new_roll == DataHolder.ADMIN:
                self.__states[user_id] = DataHolder.COMMAND_INPUT
            elif new_roll == DataHolder.USER:
                self.__states[user_id] = DataHolder.MESSAGE_INPUT

            return True

        return False
