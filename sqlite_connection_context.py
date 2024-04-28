import sqlite3

class SqliteConnectionContext():
    """A context manager that automatically closes the cursor and the database.
    Return a cursor object upon entering.
    https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
    https://stackoverflow.com/questions/62034314/automatically-close-database-in-sqlite3-of-python
    """

    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)

    def __enter__(self):
        # self.conn = self.conn.__enter__()
        self.cur = self.conn.cursor()
        # return self.cur

    def __exit__(self, *exc_info):
        # result = self.conn.__exit__(*exc_info)
        self.cur.close()
        self.conn.close()
        # return result