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
                data_holder.push_new_valid_user(line, block_role)
            elif line.startswith('multiple-input'):
                regex = r'multiple-input \((.+)?\)'
                block_role = string_to_role(re.findall(regex, line)[0])
            elif line.count(' ') == 1:
                username, role = line.split(' ')
                data_holder.push_new_valid_user(username,
                                                string_to_role(role))


def read_token():
    logging.info('read_token()')
    with open('token.txt') as file:
        token = file.read()

    return token
