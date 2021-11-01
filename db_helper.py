import sqlite3
from sqlite3 import Error


class db_helper:
    db_file = "goaldiggers_prescription.db"
    conn = None

    def __init__(self):
        self.conn = self.__create_connection()

    # db connection
    def __create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        return self.conn

    def query_db(self, query):
        print(f'{query = }')
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        self.conn.commit()
        return rows
