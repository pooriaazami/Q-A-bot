class User:
    def __init__(self, telegram_id, firstname, roll=1):
        self.__id = telegram_id
        self.__firstname = firstname
        self.__roll = roll

    @property
    def id(self):
        return self.__id

    @property
    def firstname(self):
        return self.__firstname

    @property
    def roll(self):
        return self.__roll
