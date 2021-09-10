import os
import sqlite3


def create_database():
    connection = sqlite3.connect('database\\users.sqlite3')
    cursor = connection.cursor()

    query = 'CREATE TABLE "users" ( ' \
            '"id" INTEGER NOT NULL, "firstname" ' \
            'VARCHAR(64) NOT NULL,' \
            ' "roll" INTEGER NOT NULL DEFAULT 1 );'

    cursor.execute(query)

    connection.commit()
    connection.close()


def create_database_path():
    if not os.path.isdir('database'):
        os.mkdir('database')
