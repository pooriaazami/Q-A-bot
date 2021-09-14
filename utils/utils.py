from utils.DataHolder import DataHolder


def roll_to_string(roll):
    if roll == DataHolder.ADMIN:
        return 'admin'
    if roll == DataHolder.USER:
        return 'user'


def string_to_roll(string):
    if string == 'admin':
        return DataHolder.ADMIN
    if string == 'user':
        return DataHolder.USER


def get_destinations(title):
    if title == 'users':
        return DataHolder.get_instance().users
    if title == 'admins':
        return DataHolder.get_instance().admins
    if title == 'branches':
        return DataHolder.get_instance().branches
    if title == 'main':
        return [DataHolder.get_instance().effective_chat_id]
    if title == 'all':
        ins = DataHolder.get_instance()
        return list(ins.registered_users.keys()) + ins.branches + [ins.effective_chat_id]
