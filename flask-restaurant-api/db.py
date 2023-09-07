import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def execute_query(self, query, params=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            conn.commit()
            return cursor.lastrowid  # Return the ID of the last inserted row
        except sqlite3.Error as err:
            print(f"SQLite Error: {err}")
            return None
        finally:
            conn.close()

    def execute_select_query(self, query, params=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as err:
            print(f"SQLite Error: {err}")
            return None
        finally:
            conn.close()
