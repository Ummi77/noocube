# import sqlite3
from time import sleep
import sqlalchemy as alchdb

from bonds.settings import DB_BONDS_

class SqliteAlchemyConnection():
    """ Класс подключения к БД sqlite """

    def __init__(self, dbName):
        try:
            self.dataBase = dbName
            self.engine = alchdb.create_engine(f"sqlite:///{dbName}")
            
            self.connection = self.engine.connect()
            sleep(1)
            print(f"Connection created (if was not any) and Successfully Connected to SQLite : {dbName}") 

         
           

        except :
            print("Error while connecting to sqlite")
        # finally:
        #     if self.connection:
        #         self.connection.close()
        #         print("The SQLite connection is closed")



if __name__ == "__main__":
    pass


    alch_conn = SqliteAlchemyConnection(DB_BONDS_)