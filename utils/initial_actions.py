import logging

from utils.DataHolder import DataHolder
from utils.utils import string_to_role

import re


def read_users():
    logging.info('read_users()')
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
                if line.count(' ') != 0:
                    username, count = line.split(' ')
                    data_holder.push_new_valid_user(username, block_role, int(count))
                else:
                    data_holder.push_new_valid_user(line, block_role, 1)
            elif line.startswith('multiple-input'):
                regex = r'multiple-input \((.+)?\)'
                block_role = string_to_role(re.findall(regex, line)[0])
            elif line.count(' ') == 1:
                username, role = line.split(' ')
                data_holder.push_new_valid_user(username,
                                                string_to_role(role), 1)
            elif line.count(' ') == 2:
                username, role, count = line.split(' ')
                data_holder.push_new_valid_user(username,
                                                string_to_role(role), int(count))
            else:
                if len(line) != 0:
                    logging.warning(f'Invalid line: {line}')


def read_token():
    logging.info('read_token()')
    with open('token.txt') as file:
        token = file.read()

    return token
