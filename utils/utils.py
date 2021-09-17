from utils.DataHolder import DataHolder
import re


def role_to_string(role):
    if role == DataHolder.ADMIN:
        return 'admin'
    if role == DataHolder.USER:
        return 'user'


def string_to_role(string):
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
        if DataHolder.get_instance().effective_chat_id:
            return [DataHolder.get_instance().effective_chat_id]
        return []
    if title == 'all':
        ins = DataHolder.get_instance()
        result = []

        temp = list(ins.registered_users.keys())
        if len(temp) > 0:
            result.extend(temp)

        temp = ins.branches
        if len(temp) > 0:
            result.extend(temp)

        if ins.effective_chat_id:
            result.append(ins.effective_chat_id)

        return result


def translate_role(role):
    if role == 'admin':
        return 'مدیر'
    if role == 'user':
        return 'کاربر'

    return '---'


def read_token():
    with open('token.txt') as file:
        token = file.read()

    return token


def read_users():
    data_holder = DataHolder.get_instance()

    block_role = None
    with open('users.txt', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if line.startswith('#'):
                continue
            if line == 'end':
                block_role = None
            elif block_role is not None:
                data_holder.push_new_valid_user(line, block_role)
            elif line.startswith('multiple-input'):
                regex = r'multiple-input \((.+)?\)'
                block_role = string_to_role(re.findall(regex, line)[0])
            elif line.count(' ') == 1:
                username, role = line.split(' ')
                data_holder.push_new_valid_user(username,
                                                string_to_role(role))
