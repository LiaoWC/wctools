import sqlite3
from typing import *

"""
The sql below use "?" to be replaced-char.
"""


class DB:
    TABLE_SCHEMAS = {
        'users': '''
            CREATE TABLE users(
                name text primary key unique not null,
                sid text not null
            )''',
        'waiting_rooms': '''
            CREATE TABLE waiting_rooms(
                id integer unique primary key,
                player_name integer,
                player_a_name text,
                player_b_id integer,
                player_b_name
            )'''
    }
    CLEAR_BEFORE_CONN = True

    def __init__(self, filename: str):
        # PS memory: sqlite3.connect("file::memory:?cache=shared", uri=True)
        self.db_filename = filename
        self.init_tables(clear=self.CLEAR_BEFORE_CONN)
        self.last_sql = ''
        self.last_params = ()

    def execute(self, sql: str, params: Union[tuple, None] = None):
        """

        :param sql:
        :param params:
        :return: cursor object
        """
        with sqlite3.connect(self.db_filename) as conn:
            self.last_sql, self.last_params = sql, params
            params = () if params is None else params
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor

    def __failed_msg(self, msg: str, err_obj: sqlite3.Error = None):
        full_msg = '{} ({}) (sql="{}", params="{}")'.format(msg, ' '.join(err_obj.args), self.last_sql,
                                                            self.last_params)
        raise sqlite3.Error(full_msg)

    def insert_row(self, sql: str, params: Union[tuple, None] = None) -> bool:
        """

        :param sql: SQL query (use "?" as the substitution mark)
        :param params: parameters to substitute
        :return: successful or not (bool value)
        """
        try:
            rtn_cursor = self.execute(sql, params)
        except sqlite3.Error as er:
            self.__failed_msg('Execute insert query failed.', er)
            return False
        if rtn_cursor.rowcount != 1:
            self.__failed_msg('Execute insert query failed. (rowcount != 1)')
            return False
        return True

    def create_table(self, sql: str) -> bool:
        try:
            self.execute(sql)
        except sqlite3.Error as er:
            self.__failed_msg('Execute create table query failed.', er)
            return False
        return True

    def select(self, sql: str, params: Union[tuple, None] = None):
        cursor = None
        try:
            cursor = self.execute(sql, params)
        except sqlite3.Error as er:
            self.__failed_msg('Select query failed.', er)
        return cursor.fetchall()

    def drop_all_tables(self) -> None:
        try:
            self.select(sql="SELECT 'DROP TABLE ' || name || ';' FROM sqlite_master WHERE type = 'table';")
        except sqlite3.Error as er:
            self.__failed_msg('Drop all tables failed.', er)

    def item_exists(self, table: str, filter_col: str, value: Any) -> bool:
        if len(self.select("SELECT * FROM {} WHERE {} = ?".format(table, filter_col), (value,))) != 0:
            return True
        else:
            return False

    def init_tables(self, clear=False):
        # Clear
        if clear:
            self.drop_all_tables()
        # Get all table names
        rtn = self.select("SELECT name FROM sqlite_master WHERE type='table';")
        names = [x[0] for x in rtn]
        # Check all tables one by one
        for table in self.TABLE_SCHEMAS:
            # Skip existed tables
            if table in names:
                continue
            # Create table
            self.execute(self.TABLE_SCHEMAS[table])
