import sqlite3

from time import sleep


class SqliteConnection():
    """ 
    Класс подключения к БД sqlite 
    ПРИМ:  ... check_same_thread=False ... ~ https://ru.stackoverflow.com/questions/1455381/sqlite3-programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in
    """

    def __init__(self,dbName):
        
        
        self.dataBase = dbName
        
        try:
            
            self.connection = sqlite3.connect(self.dataBase, check_same_thread=False)
            sleep(1)
            print(f"PR_NC_100 --> Database created (if was not any) and Successfully Connected to SQLite : {dbName}") 
            self.cursor = self.connection.cursor()

            # TEST
            sqlite_select_Query = "select sqlite_version();"
            self.cursor.execute(sqlite_select_Query)
            record = self.cursor.fetchall()
            print("PR_NC_101 --> SQLite Database Version is: ", record)
            self.cursor.close()            
        

        except sqlite3.Error as error:
            print("PR_NC_102 --> Error while connecting to sqlite", error)
            print(f"PR_NC_103 --> Error to Connected to db : {dbName}") 
        # finally:
        #     if self.connection:
        #         self.connection.close()
        #         print("The SQLite connection is closed")





    # def get_connection(self):
    #     return self








    def connect_RAM (self):
        """ЗАГОТОВКА 
        create sqlite database into local memory (RAM)
        https://saraswatmks.github.io/2020/04/sqlite-fts-search-queries.html
        """

        # # create sqlite database into local memory (RAM)
        # db = sqlite3.connect(':memory:')
        # cur = db.cursor()





class MysqlConnection():
    """ 
    Класс подключения к БД sqlite 
    ПРИМ:  ... check_same_thread=False ... ~ https://ru.stackoverflow.com/questions/1455381/sqlite3-programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in
    """

    def __init__(self, dbData = {}):
        
        
        import mariadb
        import sys
        import warnings
        
        
        
        # Отключить ненужный warning класса UserWarning, который появляется так как pandas считыватель рекомендует подключение через Sqlalchemy
        warnings.simplefilter(action='ignore', category=UserWarning)
        
        print(f"PR_NC_231 --> dbData = {dbData}")
        # INI
        # Если не задано в словаре параметров (это для совмещения со старым проектом на данный момент)
        if len(dbData) == 0:
            
            
            self.dataBase = 'labba'

            # Connect to MariaDB Platform
            try:
                self.connection = mariadb.connect(
                    user="admin",
                    password="7731",
                    host="localhost",
                    port=3306,
                    database='labba'
                )
                print(f"PR_NC_227 --> Connection to mariaDB named: 'labba' SUCSSESFUL")
            except mariadb.Error as e:
                print(f"PR_NC_228 --> Error connecting to MariaDB Platform: {e}")
                sys.exit(1)

            # Get Cursor
            self.cursor = self.connection.cursor()
            # self.connection.commit()

        # Если заданы другие параметры соединения к БД
        else:
            
            self.dataBase = dbData['dbName']
            
            # Connect to MariaDB Platform
            try:
                self.connection = mariadb.connect(
                    user = dbData['user'],
                    password = dbData['pass'],
                    host = "localhost",
                    port=3306,
                    database = dbData['dbName']
                )
                print(f"PR_NC_229 --> Connection to mariaDB named: {dbData['dbName']} SUCSSESFUL")
            except mariadb.Error as e:
                print(f"PR_NC_230 --> Error connecting to MariaDB Platform: {e}")
                sys.exit(1)

            # Get Cursor
            self.cursor = self.connection.cursor()
            # self.connection.commit()






if __name__ == "__main__":
    pass



    # ПРОВЕРКА: пОдключение к БД mysql
    
    DB_CONNECTION = MysqlConnection()



    # # ПРОВЕРКА: Подключения к БД

    # DB_BONDS = '/home/lenovo/projects/P19_Bonds_Django/bonds_django_proj/db/bonds.db'
    # sc = SqliteConnection (DB_BONDS)






