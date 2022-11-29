import psycopg2
from config import db_config


class DbCreator:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=db_config.DB_HOST,
            dbname=db_config.DB_NAME,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD,
            port=db_config.DB_PORT,

        )
        self.cursor = self.conn.cursor()

    def __create_users_table(self):
        with self.conn:
            self.cursor.execute("""CREATE TABLE users (
                            tg_id bigint PRIMARY KEY,
                            first_name text,
                            username text,
                            type text,
                            message text,
                            message_timestamp text
                            )""")

    def __create_admins_table(self):
        with self.conn:
            self.cursor.execute("""CREATE TABLE admins (
                            tg_id bigint PRIMARY KEY,
                            first_name text,
                            username text,
                            type text,
                            )""")

    def __create_offer_table(self):
        with self.conn:
            self.cursor.execute("""CREATE TABLE offers (
                            tg_id bigint PRIMARY KEY,
                            message_to_user_sends boolean
                            )""")

    def __init_db__(self):
        try:
            self.__create_users_table()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create users table\n'
                  f'[ERR] {ex}')
        try:
            self.__create_admins_table()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create admins table\n'
                  f'[ERR] {ex}')

        try:
            self.__create_offer_table()
        except Exception as ex:
            print(f'[ERR] PostreSQL: Cant create offers table\n'
                  f'[ERR] {ex}')
