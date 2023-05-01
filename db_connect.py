import sqlite3
from sqlite3 import Error


class DB:
    def __init__(self, db_filename):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_filename)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def create_table(self, create_table_sql):
        try:
            self.conn.cursor().execute(create_table_sql)
        except Error as e:
            print(e)

    def insert_new_word(self, word_data):
        sql = """INSERT INTO words(word,reading,meaning,level,completed)
                VALUES(?,?,?,?,0)"""
        try:
            self.conn.cursor().execute(sql, word_data)
            self.conn.commit()
        except  Error as e:
            print(e)

    def insert_new_example(self, example_data):
        sql = """INSERT INTO examples(example,reading,meaning,word_id)
                VALUES(?,?,?,?)"""
        try:
            self.conn.cursor().execute(sql, example_data)
            self.conn.commit()
        except  Error as e:
            print(e)

    def get_word_id(self, word):
        sql = """SELECT * FROM words WHERE word=?"""
        try:
            return self.conn.cursor().execute(sql, [word]).fetchall()[0]
        except  Error as e:
            print(e)

    def get_words_by_level(self, level):
        sql = """SELECT * FROM words WHERE completed=0 and level=?"""
        try:

            return self.conn.cursor().execute(sql, [level]).fetchall()
        except Error as e:
            print(e)

    def get_examples_by_word_id(self, word_id):
        sql = """SELECT * FROM examples WHERE word_id=?"""
        try:
            return self.conn.cursor().execute(sql, [word_id]).fetchall()
        except Error as e:
            print(e)

    def set_completed(self, completed, word_id):
        sql = """UPDATE words SET completed=? WHERE word_id=?"""
        try:
            self.conn.cursor().execute(sql, [completed, word_id])
            self.conn.commit()
        except Error as e:
            print(e)

    def get_completed_words(self, level):
        sql = """SELECT * FROM words WHERE completed!=0 and level=?"""
        try:
            return self.conn.cursor().execute(sql, [level]).fetchall()
        except Error as e:
            print(e)


