

import re
# from time import sleep

# from zmq import NotDone
from noocube.settings import DB_BONDS_, DB_TLH_, DEBUG_
from noocube.sql_syntaxer import SQLSyntaxer

from noocube.sqlite_connection import SqliteConnection
import sqlite3
# from bonds.algorithms_settings import *
from noocube.switch import Switch
import noocube.funcs_general as FG
from noocube.pandas_manager import PandasManager


class SqliteProcessor (SqliteConnection):
    """ 
    OBSOLETED: Класс устарел, так как использует неправильное подсоединение к БД, что сильно замедляет процессы. Использовать его аналог :  SqliteProcessorSpeedup
    Использовать можно только статичные методы пока
    Класс предназначен для реализации sql запросов в виде строки в реальной БД sqlite
    dbName - название БД. Если модуль класса находится не в пространстве проекта, где находится БД, то указывать полный абсолютный путь к БД
    """


    #TODO: con.executescript()


    # # TODO: Проверка возвращения результатов лучше делать примерно так: РЕАЛИЗОВАТЬ ПО НЕОБХОДИМОСТИ В ВИДЕ ОТДЕЛЬНОГО МЕТОДА
    # db = 'bonds.db'
    # db_processor = SqliteProcessor(db)   
    # tbInnIsin = 'bonds_archive'     
    # getFields = ['count(*)']   # [count(*)] - если надо подсчитать ряды полученные
    # conds = {'ONE': ['isin', '=', isin]}
    # cur, sql = db_processor.select_from_table_with_where_condition (tbInnIsin, getFields, conds)
    # flagArch = int(cur.fetchone()[0]) # Возврат по bonds_archive
    # cur.close()

    # tbInnIsin = 'bonds_current'     
    # getFields = ['count(*)']   # [count(*)] - если надо подсчитать ряды полученные
    # cur, sql = db_processor.select_from_table_with_where_condition (tbInnIsin, getFields, conds)            
    # flagCurr = int(cur.fetchone()[0]) # Возврат по bonds_current
    # cur.close()      



    def __init__(self,dbName):
        SqliteConnection.__init__(self,dbName)



    ## -- ДЕКОРАТОРЫ ---
    # https://pythonworld.ru/osnovy/dekoratory.html

    # Дек: Для вывода запросов sql, возвращающих выборки в курсоре, в виде уже готовых массивов (списков)
    def transform_cursor_to_list(func_to_decorate):
        """Трансформирует курсор sql запроса в конечные списки данных"""
        def wrapper(self,*args, **kwargs):
            res = func_to_decorate(self,*args, **kwargs)
            # if DEBUG_:
            #     print(f"res[0] = {res[0]} / sqlite_proccessor.py / transform_cursor_to_list decorator / m35")
            if len(res) > 1: # Значит функция возвращает (cur, sql)
                dsRes = self.get_ds_from_cursor (res[0])
                # res[0].close() # Закрыть курсор

            else: # Значит функция sql возвращает один курсор cur
                dsRes = self.get_ds_from_cursor (res)
                # res.close() # Закрыть курсор
            return dsRes

        return wrapper
    
    
    def execute_select_sql(sql):
        """Декоратор, который выполянет sql select запрос и возвращает список выборки"""
        def wrapper(self,*args, **kwargs):
            res = func_to_decorate(self,*args, **kwargs)
            # if DEBUG_:
            #     print(f"res[0] = {res[0]} / sqlite_proccessor.py / transform_cursor_to_list decorator / m35")
            if len(res) > 1: # Значит функция возвращает (cur, sql)
                dsRes = self.get_ds_from_cursor (res[0])
                res[0].close() # Закрыть курсор

            else: # Значит функция sql возвращает один курсор cur
                dsRes = self.get_ds_from_cursor (res)
                res.close() # Закрыть курсор
            return dsRes

        return wrapper
    


    ## -- END ДЕКОРАТОРЫ ---




    # TODO: !!! СДЕЛАТЬ ЛОГИРОВАНИЕ ЗАПРОСОВ ПРИ РЕАЛИЗАЦИИ КУРСОРОВ !!!
    # https://stackoverflow.com/questions/5266430/how-to-see-the-real-sql-query-in-python-cursor-execute-using-pyodbc-and-ms-acces
    # conn = MySQLdb.connect( read_default_file='~/.my.cnf' )
    # cur = conn.cursor()
    # log_queries(cur)
    # cur.execute('SELECT %s, %s, %s', ('hello','there','world'))      

    def log_queries(cur):
        
        def _query(q):
            print (q) # could also use logging
            return cur._do_query(q)

        cur._query = _query

  


    # SQL-запросы с использованием Pandas dataframe

    def insert_rows_from_dataframe (self, tb, df, fcAssocDic, prKeyField):
        """ Вставка множественных рядов из Pandas Dataframe source 
        
        fcAssocDic - словарь соответствий названий полей таблицы и индекса колонок в dataSet источнике
        Прим:
        df - dataFrame
        fieldsAccordList = {'isin' : 0,  'okpo' : 3} - перечисление всех вставляемых полей, Включая ключевое поле с индексом prKeyInx
        prKeyField - название поля в fieldsAccordList, по которому проверется наичие возможно уже внесенной записи по данному обьекту (проверка UNIQUE) в таюлице для вставкки
        Прим: prKeyField = 'isin'
         """



        insColsVals = {} # Словарь { поле : значение, ...} для записи в таблицу БД, на основании которого формируется sql-запрос
        df = df.reset_index() # make sure indexes pair with number of rows
        for index, dfRow in df.iterrows(): # Цикл по dataFrame

            # Формирование словаря insColsVals для INSERT по текущему ряду dFrame

            for key, val in fcAssocDic.items(): # Цикл по словарю ассоциаций полей и индексов колонок в dataFrame
                insColsVals[key] = dfRow.iloc[val] # формирование 

            pdMngr = PandasManager()
            dictAccordCols = pdMngr.get_accordance_dict_of_df_cols_names_indices(df)
            # print(dictAccordCols)
            # print(f"insColsVals fo SQL  : {insColsVals}")

            # Проверка наличия табличного обьекта БД  по юникам таблицы  
            prColInx =  fcAssocDic[prKeyField]    # индекс ключевой колонки в dataFrame по задаваемому ключевому полю  prKeyField         
            pKeyVal = dfRow.iloc[prColInx] # текущее значение задаваемого  поля UNIQUE prKeyInx для проверки дублирования -  существует ли уже запись в таблице БД
            prKeyName = prKeyField # имя поля, по которому проверяется UNIQUE
            # Pars fo select
            qFields = [prKeyName] # параметр для функции select_from_table - список полей для запроса SELECT. 
            cur = self.select_from_table(tb, qFields) # Курсор результатов запроса
            dsCheck = self.cursor_get_all(cur) # dataSet всех строк курсора
            boolVal = self.if_exist_in_ds(dsCheck, pKeyVal) # Проверка, есть ли в dataSet фрагмент строки val

            if (boolVal) :
                print(pKeyVal + " уже есть в БД ")
            else:
                print (pKeyVal + "  Внести в БД")
                # Вставка полей из текущей строки общего массива данных региона 
                self.insert_row_into_table(tb, insColsVals)     



    # SQL-запросы с использованием Pandas dataframe






    # -- ПРОСТЫЕ МЕТОДЫ ЗАПРОСОВ
    


    def update_rows_from_ds(self , tb, dataSet, fieldsInxAccordList, unqInxColVal):
        """ Обновление значений в таблице БД на основе данных в dataSet (массив общих данных , с множеством разных колонок, в виде списка рядов значений) . Идентификация по ключу uniqueColNames
        ПАРАМЕТРЫ:
        fieldsAcordAbs = {3: 'okpo', 1 : 'reg_year', 7:'comp_name'} - соответствие индексов колонок в dataSet и названий колонок в таблице БД. Индекс в dataSet начинается с 0 \n
        uniqueColNames = [9,'inn'] - список соответствия индекса ключевой колонки в dataSet и ее названия в таблице БД
        """
        # print('TEST')
        # Цикл по dataSet
        uniqColInx = unqInxColVal[0] # индекс ключевой колонки в dataSet
        unqColTbName = unqInxColVal[1] # название ключевой колонки в таблице БД

        for dsRow in dataSet:
            # Формирование словаря {'fieldName':'fieldValue'} по текущему ряду из массива по циклу for rowVals
            updColsVals = {} # Словарь { поле : значение, ...} для внесения обновлений записи в таблицу БД, на основании которого формируется sql-запрос
            for key,value in fieldsInxAccordList.items():
                updColsVals[value] = dsRow[key] # формирование словаря с данными для обновления значений в записи таблицы БД

            uniqExelKeyVal = dsRow[uniqColInx] # значение поля ключевой колонки , по которому будет найдена запись в таблице БД для обновления
            # Подготовка парметров для update_row_in_tb of SqliteProcessor
            unqKeyVal = [unqColTbName, uniqExelKeyVal] # ключевое поле и его значение для поиска записи к обновлению в таблице БД 
            # Обновление записи в таблице БД , найденной по заданному значению ключевого поля
            sql_update = self.update_row_in_tb(tb,  updColsVals, unqKeyVal)
            # print (sql_update)
            


    def update_row_in_tb(self, tbName,  fieldsVals, uniqueKeyVal):
        """ #TODO: Сделать фиксацию ключей, по которым произошло обновление, то есть набор ключей, которые найдены в таблице 
        (так как если ключ не найден, то обновления не происходит и эти данные иногда необходимо знать)
        Обновляет значения в записи, определяемой ключем  uniqueKeyVal\n
        ПРИМЕРЫ ПАРАМЕТРОВ:\n
        tb = 'comps'\n
        uniqueKeyVal = ['inn','2128702350']\n
        fieldsVals = {'okpo' : '111', 'sector' : '333'}"""
        sql_update = ''
        try:
            sql_update = SQLSyntaxer.update_tb_row_with_unique_key_sql(tbName, fieldsVals,uniqueKeyVal)
            # print(f"sql_update = {sql_update} <def update_row_in_tb / sqlite_proccessor.py>")
            cursor = self.connection.cursor()
            cursor.execute(sql_update)
            self.connection.commit()
            cursor.close()   
        
        except sqlite3.Error as error:
            print("ERROR:", error)

            # Обработка ошибок
            if 'UNIQUE constraint failed' in str(error): # Ошибка нарушения уникальности поля 
                # Выполнить поиск записи с уже существующим значением, по которому произошла ошибка нарушения уникальности поля
                errParts = str(error).split('.')
                errTb = errParts[0].split(':')[-1] # Таблица
                errField = errParts[-1] # Поле
                print (f'Найдена ошибка нарушения уникальности поля {errField} при попытке обновить его новым значением {fieldsVals[errField]} в таблице {errTb} (pr: SqliteProcessor.update_row_in_tb )' )
                cur, sql = self.select_from_table_with_where_condition(errTb,[uniqueKeyVal[0]], {'ONE': [errField, '=', fieldsVals[errField]]})
                dsRes = self.get_ds_from_cursor(cur)
                print (f"ERROR!!!: В таблице {errTb} найдена запись : {dsRes[0]} , которая в поле {errField} уже имеет значение {fieldsVals[errField]} (pr: SqliteProcessor.update_row_in_tb )" )

            sql_update = 'SQL не выполнен в результате sqlite3.Error ошибки  (pr: SqliteProcessor.update_row_in_tb )'
            print (sql_update)

        finally:
            return sql_update










    def update_tb1_from_select_tb2_simple_exec(self, tb1,tb2, fieldsTb1, fieldsTb2, condsUpdTb1 = {} , condsSelTb2 = {}, debug = False  ):
        """ Обновление данных полей в первой таблице из соответсвующих полей второй таблицы на основе условий, сочитающих в себе поля из обоих таблиц 
        fieldsTb1 - поля для выборки UPDATE 
        fieldsTb2 - поля для выборки SELECT по каждому полю из fieldsTb1 (размеры списков fieldsTb1 и fieldsTb2 должны быть равны, а типы значений величин - одинаковы для каждого поля выборки SELECT и UPDATE)
        condsSelTb2 - условия WHERE для выборок SELECT для каждого из полей fieldsTb1 (всегда одинаковые для всех полей fieldsTb1 -поэтому и simpe в названии функции Простой вариант функции)
        condsUpdTb1 - условия WHERE для части UPDATE для первой таблицы

        Пример использования внизу класса
            Пример параметров:
            tbCurrent = 'bonds_current'
            tbArchive = 'bonds_archive'
            fieldsTb1 = ['isin'] # список полей  в UPDATE SET первой таблицы
            fieldsTb2 = ['bonds_archive.isin'] # список полей  в SELECT for SET первой таблицы    
            condsUpdTb1 = {} # Условия для UPDATE первой таблицы 
            condsSelTb2 = {'ONE' : ['bonds_current.bond_name','=', '&bonds_archive.bond_name']
                                    } # Условия для SELECT второй таблицы    
         """
        sqlUpd = SQLSyntaxer.update_tb1_from_select_tb2_simple_sql (tb1,tb2, fieldsTb1, fieldsTb2, condsUpdTb1 , condsSelTb2 )
        if DEBUG_:
            print(sqlUpd)

        cursor = self.connection.cursor()
        cursor.execute(sqlUpd)
        self.connection.commit()
        cursor.close()   
        return sqlUpd


    def update_where_in_simple_exec (self, tb, updFields,  updVals, whereConds)   :
        """ Функция простейшего UPDATE с WHERE IN по выборке из SELECT запроса, или по простому списку величин для задаваемого поля. 
            (Для обновления полей updFields заданными updVals константами при выполнении условия whereConds )
            updFields и updVals равны по размерности - параметры для обновления - поля для обновления и их значения соответственно
            conds - стандартный формат для параметра whereConds (хорошо описан в select_from_table_with_where_condition_sql c примером в файле sqlite_processor.py внизу)
                Выборка из таблицы по  условиям WHERE для простого SELECT . В качестве условий могут выступать арифметические условия, а так же IN/NOT IN для для формирования
            условий WHERE IN (...). В последнем случае в качестве значения dsIN условия  могут быть либо sql стринг типа 'SELECT * FROM ...', создающий выборку (типа SELECT * FROM tb WHERE field IN ( SELECT ... ) ).
            Или простой список величин для  осуществления поиска в них заданного поля основного SELECT (типа SELECT * FROM tb WHERE field IN ( 1,2,... ) )
            Если ключ в словаре условий стоит ALL или NO , то выборка -  все записи из таблицы
            getFields - список ['field1','field2' или '*']
            whereConds - список с условиями типа {
                                                'OR' : [['fieldName1', '<', 5], ['fieldName2', '>', 15]], 
                                                'AND' : [['fieldName3', '<', 5], ['fieldName4', '>', 15]], /
                                                'ONE'  : ['fieldName1', '<', 5],/
                                                'ALL or NO'   : None, / <или иначе - без всяких условий>
                                                'STR' : '(fieldName1 > 5 AND fieldName2 < 15) AND (...)'
                                                }
                    Если conds = {} или не заданы вовсе (по умолчанию {}), то SELECT sql формируется без условий WHERE
        """

        sqlUpd = SQLSyntaxer.update_where_in_simple_sql (tb, updFields,  updVals, whereConds )

        cursor = self.connection.cursor()
        cursor.execute(sqlUpd)
        self.connection.commit()
        cursor.close()   
        return sqlUpd        


    def insert_row_into_table (self, tbName, fieldsVals):
        """ Вставляет ряд в талицу sqlite. fieldsVals - данный по одному ряду
        fieldsVals - словарь {'fieldName':'fieldValue'} """
        sql_insert = SQLSyntaxer.insert_row_into_table_sql(tbName, fieldsVals)
        cursor = self.connection.cursor()
        cursor.execute(sql_insert)
        self.connection.commit()
        cursor.close()   
        return sql_insert
    
    
    
    @transform_cursor_to_list
    def last_insert_rowid (self):
        """Возвращает последний rowId (через декоратор - это список, где хранится послений rowID, получать через rowID[0] конечный ID) по вносимым записям через ISERT. 
        Нважно какой был инчер, главное, что возвращает последнее значение rowID после любого INSERT """
        
        sql = 'SELECT last_insert_rowid()'
        cursor = self.execute_sql_with_cursor(sql)
        return cursor,sql
    
    
    @transform_cursor_to_list
    def execute_select_sql (self,sql):
        """Возвращает последний rowId (через декоратор - это список, где хранится послений rowID, получать через rowID[0] конечный ID) по вносимым записям через ISERT. 
        Нважно какой был инчер, главное, что возвращает последнее значение rowID после любого INSERT """
        
        cursor = self.execute_sql_with_cursor(sql)
        return cursor,sql

    

    def insert_general (self, tbIns, fieldsIns, valsIns, onConflicts = '', sqlSelParams = {}, executeSQL = True):
        
        """ Выполняет разные  запросы   INSERT, в том числе со вставкой SELECT, формируемые  синтаксером insert_general_sq
        Виды запросов:
        1. Формирование sql, если нет SELECT парметров  и ввод идет по всем полям равным структуре таблицы / INSERT INTO table VALUES(...)
        2. Формирование sql, если все поля и есть SELECT параметры / INSERT INTO artists_backup  SELECT ArtistId, Name FROM artists;
        3. Формирование sql, если задан список полей и нет SELECT параметров / INSERT INTO table (column1,column2 ,..) VALUES( value1,	value2 ,...)
        4. Формирование sql, если задан список полей и есть SELECT параметры / INSERT INTO table (field1,field2,..fieldN) SELECT f1, f2,...fN FROM ... 

        executeSQL - Флаг выполнения sql-запроса  в БД. Если   = True (по умолчанию), то запустить выполнение . False - просто вернуть sql-запрос для проверки. По умолчанию - выполнять операцию в БД
        fieldsIns - [field1, field2, ... fieldN] or ['*'] - список полей для вставки в части INSERT (f1, f2 ...)... VALUES (v1, v2 ...). Если '*' то все поля, то кол-во полей SELECT д.б. = tb
        valsIns -  [[val1, val2, ... valN], [val1, val2, ... valN]] or ['*'] - список велечин для полей вставки в части INSERT (f1, f2 ...)... VALUES (v1, v2 ...). Д.б. = fields или ['*'], если все поля
                Если спиок в списке, то несколько записей. ['*'] - только, если есть String SELECT. Тогда это обозначает , что все поля из SQLECT, кол-во которых должно быть = всем полям таблицы , в которую идет ISERT и 
                VALUES () вообще не проставляется. Собственно это может вытекать из парсинга SELECT !
        sqlSelParams - парметры SELECT запроса, если он участвует в INSERT
        onConflicts - String, условия по конфликту IGNORE or REPLACE (и еще 5 других) - * https://database.guide/how-on-conflict-works-in-sqlite/
        \nПРИМЕРЫ применения внизу этого файла sql_sintaxer.py
        """
        sql_insert = SQLSyntaxer.insert_general_sql(tbIns, fieldsIns, valsIns, onConflicts, sqlSelParams)
        if  executeSQL: # Если флаг executeSQL = True, то запустить выполнение запроса. В ином случае - просто вернуть sql-запрос для проверки
            cursor = self.connection.cursor()
            cursor.execute(sql_insert)
            self.connection.commit()
            cursor.close()   
        return sql_insert        


    def insert_rows_from_ds (self, tb, dataSet, fieldsAccordList, prKeyInx):
        """ Вставка множественных рядов из общего списка данных (то есть dataSet не отфильтрован и нужно делать соответствие между колонками в ds и поялми таблицы БД), 
        а содержит общие данные по разным полям какой-дибо первичной таблице в экселе или напрямую при парсинге  и т.д.) dataSet 
        в таблицу БД. fieldsAccordList - словарь соответствий названий полей таблицы и индекса колонок в dataSet источнике
        Прим:
        dataSet - ОБЯЗАТЕЛЬНО в форме списка списков (рядов). Даже если одна колонка, то должна быть в ворме [[],[], ... []]
        fieldsAccordList = {0:'isin', 3: 'okpo'} - перечисление всех вставляемых полей, Включая ключевое поле с индексом prKeyInx
        prKeyInx - индекс поля в fieldsAccordList, по которому проверется наичие возможно уже внесенной записи по данному обьекту (проверка UNIQUE) 
        Прим: prKeyInx = 0
        TODO: сделать более продвинутую систему проверки полей UNIQUE таблицы, в которую вносятся данные """

        insColsVals = {} # Словарь { поле : значение, ...} для записи в таблицу БД, на основании которого формируется sql-запрос

        for dsRow in dataSet:


            # Формирование словаря {'fieldName':'fieldValue'} по текущему ряду из массива по циклу for rowVals
            for key,value in fieldsAccordList.items():
                insColsVals[value] = dsRow[key] # формирование 

            # Проверка наличия табличного обьекта БД  по юникам таблицы                
            pKeyVal = dsRow[prKeyInx] # текущее значение задаваемого  поля UNIQUE prKeyInx для проверки дублирования -  существует ли уже запись в таблице БД
            prKeyName = fieldsAccordList[prKeyInx] # имя поля, по которому проверяется UNIQUE
            qFields = [prKeyName] # параметр для функции select_from_table - список полей для запроса SELECT. 
            cur = self.select_from_table(tb, qFields) # Курсор результатов запроса
            dsCheck = self.cursor_get_all(cur) # dataSet всех строк курсора
            boolVal = self.if_exist_in_ds(dsCheck, pKeyVal) # Проверка, есть ли в dataSet фрагмент строки val

            if (boolVal) :
                print(pKeyVal + " уже есть в БД ")
            else:
                print (pKeyVal + "  Внести в БД")
                # Вставка полей из текущей строки общего массива данных региона 
                self.insert_row_into_table(tb, insColsVals)         


    def insert_rows_from_ds_with_multiple_key_check (self, tb, dataSet, fieldsAccordList, prKeyInxs):
        """ Вставка множественных рядов из общего списка данных (то есть dataSet не отфильтрован и нужно делать соответствие между колонками в ds и поялми таблицы БД), 
        а содержит общие данные по разным полям какой-дибо первичной таблице в экселе или напрямую при парсинге  и т.д.) dataSet 
        в таблицу БД. fieldsAccordList - словарь соответствий названий полей таблицы и индекса колонок в dataSet источнике
        Прим:
        dataSet - ОБЯЗАТЕЛЬНО в форме списка списков (рядов). Даже если одна колонка, то должна быть в ворме [[],[], ... []]
        fieldsAccordList = {0:'isin', 3: 'okpo'} - перечисление всех вставляемых полей, Включая ключевое поле с индексом prKeyInx
        prKeyInx - сложный индекс поля в fieldsAccordList, по которому проверется наичие возможно уже внесенной записи по данному обьекту (проверка UNIQUE по сложному ключу) 
        Прим: prKeyInx = [0,3]
        """

        insColsVals = {} # Словарь { поле : значение, ...} для записи в таблицу БД, на основании которого формируется sql-запрос

        # Выборка всех данных из таблицы по набору сложных ключей
        prKeyNames = [fieldsAccordList[x] for x in prKeyInxs]

        for dsRow in dataSet:
            # Формирование словаря {'fieldName':'fieldValue'} по текущему ряду из массива по циклу for rowVals
            for key,value in fieldsAccordList.items():
                insColsVals[value] = dsRow[key] # формирование 

            # Формирование велечин для проверки по ключам
            keysVals = []
            for keyName in prKeyNames:
                keyVal = insColsVals[keyName]
                keysVals.append(keyVal)

            boolRes, messageStr = self.if_exist_in_tb_by_multiple_keys(tb, prKeyNames, keysVals )


            if (boolRes) :
                if DEBUG_:
                    print("\n" + messageStr + f" уже СУЩЕСТВУЕТ в заданных динамически ключевых полях таблицы {tb} -> Не вносим\n")
            else:
                if DEBUG_:
                    print ("\n" + messageStr + f"  НЕТ в заданных динамически ключевых полях таблицы {tb} -> Вносим\n")
                # Вставка полей из текущей строки общего массива данных региона 
                self.insert_row_into_table(tb, insColsVals)           




    def insert_rows_from_ds_with_add_constant_vals_to_other_fields(self, tbIns, dsInp, dsFieldsAccList, fieldsValsConstDict, fieldsKeysToCheckList):
        # TODO: 
        """Внести данные в таблицу из массива основных данных с добавлением маркеров-констант в другие поля таблицы
        dsInp - массив для вноса в таблицу с известными индексами полей и их названиями в таблице (продумать)
        dsFieldsAccList - список названий полей таблицы, в порядковом соответствии с dsInp
        fieldsValsConstDict - словарь с названием полей и значением констан, которые добаляются к каждому ряду в dsInp при внесении в таблицу БД
        dsInp - должен быть !!! ДВУМЕРНЫЙ !!!, даже если одна колонка [[],[], ...[]]. На втором уровне - нет ограничений по кол-ву колонок
        fieldsKeysToCheckLists - список названий полей для проверки
        """
        insFieldsValsFinal = {} # словарь, который содержит в себе все данные для вствки
        for row in dsInp: # цикл по массиву для формирования конечного словаря insFieldsValsFinal для вставки однйо записи в таблицу
            insFieldsValsFinal = { dsFieldsAccList[i] : row[i] for i in range(len(row)) } # формирование части словаря по колонкам в текущем ряду входного массива dsInp
            for key, val in fieldsValsConstDict.items(): # формирование части словаря по добавочным полям - константам и их значениям
                insFieldsValsFinal[key] = val

            # формируем отдельный словарь для проверки UNIQUE
            keyValsToCheckDict = {}
            for keyCheck in fieldsKeysToCheckList:
                keyValsToCheckDict[keyCheck] = insFieldsValsFinal[keyCheck]


            boolRes, messageStr = self.if_exist_in_tb_by_multiple_keys_by_dict(tbIns, keyValsToCheckDict )

            if (boolRes) :
                if DEBUG_:
                    print("\n" + messageStr + f" уже СУЩЕСТВУЕТ в заданных динамически ключевых полях таблицы {tbIns} -> Не вносим\n")
            else:
                if DEBUG_:
                    print ("\n" + messageStr + f"  НЕТ в заданных динамически ключевых полях таблицы {tbIns} -> Вносим\n")
                # Вставка полей из текущей строки общего массива данных региона 
                self.insert_row_into_table (tbIns, insFieldsValsFinal)           

        

    


    def select_from_table(self,tb,fields = ['*']):
        """ Делает выборку из таблицы по указанным полям. Если не указаны поля отдельно, то по умолчанию возвращает выборку по всем полям. 
        Возвращает выборку в  dataSet в виде курсора (cursor) с результатос запроса """

        sql_select = SQLSyntaxer.select_from_table_sql(tb, fields)
        cursor = self.connection.cursor()
        cur = cursor.execute(sql_select)
        return cur




    @transform_cursor_to_list # Декоратор, который трансформирует метод так, что бы возвращался не курсор, а конечный список результатов, готовый к использованию
    def select_from_table_with_where_condition (self,tb, getFields, conds, add = ''):
        """ Conditional SELECT from tb by fields . fields - список полей или *
        Выборка из таблицы по  условиям WHERE для простого SELECT . В качестве условий могут выступать арифметические условия, а так же IN/NOT IN для для формирования
        условий WHERE IN (...). В последнем случае в качестве значения dsIN условия могут быть либо sql стринг типа 'SELECT * FROM ...', создающий выборку (типа SELECT * FROM tb WHERE field IN ( SELECT ... )  ).
        Или простой список величин для  осуществления поиска в них заданного поля основного SELECT (типа SELECT * FROM tb WHERE field IN ( 1,2,... ) )
        Если ключ в словаре условий стоит ALL или NO , то выборка -  все записи из таблицы
        getFields - список ['field1','field2' или '*']
        conds - список с условиями типа {fieldsAccordList
                Если conds = {} или не заданы вовсе (по умолчанию {}), то SELECT sql формируется без условий WHERE
        add - стринговая добавка в ручную, типа, GROUPED BY и т.д.
        """
        # !!! Ввод новой функции на уровне sqlite для поиска по REGEX 
        # https://github.com/thomasnield/oreilly_intermediate_sql_for_data/issues/5  !!!
        def regexp(expr, item):
            reg = re.compile(expr)
            return reg.search(item) is not None
            
        self.connection.create_function("REGEXP", 2, regexp) # Создание новой функции для Regex
        # print (f"5. {conds} in sqliteProcessor module F : select_from_table_with_where_condition")
        sql = SQLSyntaxer.select_from_table_with_where_condition_sql(tb, getFields, conds, add)
        if DEBUG_ :
            print ("select_from_table_with_where_condition -> " + sql)
        cursor = self.connection.cursor()
        cur = cursor.execute(sql)
        return cur, sql     



    @transform_cursor_to_list
    def select_diffr_rows_keys_in_two_tabs_by_key_cols (self, tbSrc, tbTrg, listKeysPair):
        """Найти ключи первой таблицы, которые отсутствуют или присутствуют во второй таблице
        tbSrc - источник поиска ключей
        tbTrg - цель, с которой сравниваются ключи источника
        listKeysPair - спсиок названий ключей в таблице источнике и цели ['fieldKeySrc', 'fieldKeyTrg']
        exept - флаг отсутствуют или присутствуют. По умолчанию - отсуствуют
        """
        
        sql = SQLSyntaxer.select_diffr_rows_keys_in_two_tabs_by_key_cols_sql(tbSrc, tbTrg, listKeysPair)
        if DEBUG_ :
            print ("sql -> " + sql)
        cursor = self.connection.cursor()
        cur = cursor.execute(sql)
        return cur, sql   
        
        





    def select_with_except(self, fullSel1Pars, fullSel2Pars):
        """ Функция SELECT c EXCEPT , для 2х таблиц только
        Выдает записи, которые присутствуют в Dataset1 и их нет в Dataset2      
        fullSel1Pars - полный  стандартный набор параметров для составления SELECT запроса <tb, getFields, conds>   

        Прим:
            selConds1 = {} - условия в части sql SELECT , если наличиствует параметр EXISTS или NOT EXISTS. '&' указывает, что это названия поля
            selFields1 = ['inn']
            fullSelParams1 = {"tb":tbComps,"selFields" : selFields1, "selConds" : selConds1}

            selConds2 = {} - условия в части sql SELECT , если наличиствует параметр EXISTS или NOT EXISTS. '&' указывает, что это названия поля
            selFields2 = ['inn']
            fullSelParams2 = {"tb":tbCompsDescr,"selFields" : selFields2, "selConds" : selConds2}

        """

        sql = SQLSyntaxer.select_with_except_sql(fullSel1Pars, fullSel2Pars)
        cursor = self.connection.cursor()
        cur = cursor.execute(sql)
        return cur, sql     
    
    
    
    @transform_cursor_to_list
    def get_id_from_tb_by_col_val(self, tb, colSrc, colVal, idCol = 'id'):
        """ SqliteProcessor
        НЕ ОТТЕСТИРОВАНО
        Получить id записи по заданному значению в заданнйо колонке (вчастности нужно для определения id из таблицы для вставки по FOREIGN KEY в другую основную таблицу)
        idCol - название идентификатора-ключа-колонки в таблице (по умолчанию равна 'id')
        colSrc - колонка, в которой надо найти значение colVal для получения записи по этому ряду
        colVal - значение в колонке colSrc, которое надо найти для получения записи по этому ряду
        
        """
        
        if isinstance(colVal,str): # Если colVal - string
            sql = f'SELECT {idCol} FROM {tb} WHERE {colSrc}="{colVal}"'
        else:
            sql = f'SELECT {idCol} FROM {tb} WHERE {colSrc}={colVal}'
        
        if DEBUG_ :
            print ("sql -> " + sql)
        cursor = self.connection.cursor()
        cur = cursor.execute(sql)
        return cur, sql   




    @transform_cursor_to_list
    def select_tbs_union (self, listUnionsStructurePars, unionAll, listOrder = None):
        """ SQLSyntaxer
        Создать выражение типа SELECT .... UNION SELECT ... для таблиц и параметров, которые заданы в списке обьектов класса SelectUnionStructure из structures.py,
        который содержит в себе название таблицы, название полей для выборки из этой таблицы и названия типа записей
        В название полей в структурае SelectUnionStructure можно включать разрешенные опреанды, типа  ['isin', 'bond_name AS FIELD2'] (FIELD2 - будет названа колонка результата с bond_name)
        Кроме того, поля в разных таблицах для UNION  могут по названиям не совпадать, главное, что бы совпадали по типу данных (? Возможно работает механизм автоматического приведени. НЕ ИЗУЧЕНО)
        В поля сортирвки listOrder можно так же добавлять стандартные операнды SQLite. НАпример, ['isin ASC'], где ASC  задает порядок сортировки
        
        Условия WHERE для каждой таблицы задаются так же в структуре типа SelectUnionStructure и хранятся в списке listUnionsStructurePars
        
        Пример парметров:
        
        whereCond = { 
            'ONE'  : ['f11', '>', 1687165467]
        }
        
        listUnionsStructurePars = [
            
            SelectUnionStructure(TB_BONDS_CURRENT_, '*', whereCond, 'Corporate'),
            SelectUnionStructure(TB_OFZ_CURRENT_, '*', whereCond, 'OFZ'),
            SelectUnionStructure(TB_MUNICIP_CURRENT_, '*', whereCond, 'Municip'),
        ]
            

        listOrder = [
            'isin DESC',
        ]
        
        Пример использования: 
        
        dsRes = bmm.select_tbs_union(listUnionsStructurePars, unionAll = False, listOrder = listOrder)
        
        """
        
        sql = SQLSyntaxer.select_tbs_union_sql(listUnionsStructurePars, unionAll, listOrder = listOrder )
        cursor = self.connection.cursor()
        cur = cursor.execute(sql)
        if DEBUG_ :
            print ("Executed SQL:  " + sql + " / sqlite_processor.py / select_tbs_union ()")
        return cur, sql  







    def delete_from_table_with_where_condition (self, tb, conds, execSQL = True):
        """ Conditional DELETE from tb with conds . 
        execSQL - Флаг выполнения sql-запроса
        condition - список с условиями типа {
                                            'OR' : [['fieldName1', '<', 5], ['fieldName2', '>', 15]], 
                                            'AND' : [['fieldName3', '<', 5], ['fieldName4', '>', 15]], /
                                            'ONE'  : ['fieldName1', '<', 5],/
                                            'ALL or NO'   : None, / <или иначе - без всяких условий>
                                            'STR' : '(fieldName1 > 5 AND fieldName2 < 15) AND (...)'
                                            }
        Если ключ в словаре условий стоит ALL или NO , то удаляет все записи из таблицы
        STR - вставляется стринговое услови, прописанное в ручную
        ONE - условие только по одному полю
        OR и AND - комплексные  условия по нескольким полям"""

        sql = SQLSyntaxer.delete_from_table_with_where_condition_sql (tb, conds)
        if DEBUG_:
            print (f"sql = {sql}  / sqlite_processor.py / delete_from_table_with_where_condition/M405") 
        # print(f'SqliteProcessor: {sql}')
        if execSQL: # Флаг выполнения sql-запроса
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
        return sql    

    
    def clear_table (self, tb):
        """Отчистить польностью таблицу от всех данных"""
        self.delete_from_table_with_where_condition (tb, {})


    def delete_from_table_by_one_key_vals_in_ds(self, tb, tbKey, dsKeyVals, sqlOperand = '='):
        """
        Удаляет записи в таблице по заданным в массиве  значениям одного ключа (не множественные ключи, а простой один ключ)
        tbKey - название ключевого поля в таблице, по которому ищется значение на удаление записи
        dsKeyVals - одномерный список значений, при нахождении которых в ключевом поле производится удаление записи
        sqlOperand - sql операнд для условия удаления. По умолчанию : '='
        """
        print(f"dsKeyVals = {dsKeyVals}")
        for keyVal in dsKeyVals: # цикл по значением ключевого поля
            conds = {'ONE': [tbKey, sqlOperand, keyVal]}

            self.delete_from_table_with_where_condition (tb, conds)







# -- END ПРОСТЫЕ МЕТОДЫ ЗАПРОСОВ



# ФУНКЦИИ НА ОСНОВЕ SQL без sql-синтаксера

    def delete_from_tb_by_filed_val_proc(self, tb, field, fieldVal):
        """Удалить запись с идентификацией записей по задаваемому значению fieldVal в поле field из любойт таблицы tb"""

        sql = f'DELETE FROM {tb} WHERE {field} ="{fieldVal}"'
        self.execute_sql(sql)

        

# ФУНКЦИИ НА ОСНОВЕ SQL без sql-синтаксера




# -- МЕТОДЫ ВОЗВРАЩЕНИЯ ИЗ КУРСОРА

    def cursor_get_next (self, cur):
        """ Перемещение по результату запроса и возвращение строки результатов из dataSet """
        ds_one_row = cur.fetchone()
        return ds_one_row

    def cursor_get_many(self, cur, n):
        """ Возвращение n-строк из dataSet в виде списка строк со значениями """
        ds_many_rows = cur.fetchmany(n)
        return ds_many_rows


    def cursor_get_all (self, cur):
        """ получение листа всех значений по строкам из dataSet  https://pythonru.com/osnovy/sqlite-v-python """
        ds_full = cur.fetchall()
        return ds_full

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!! РАБОТАЕТ
    def get_ds_from_cursor (self, cur): 
        """ ВОзвращение результатов sql-запроса, хранящемся в курсоре, в виде двумерного или одномерного списков
        Если возвращается одна колонка в курсоре, то результат - простой одномерный список
        Если - несколько колонок, то результат - двумерный список в списке [[col1R0, col2R0], [col1R1, col2R1], ...] (R - ряды)
        RETURN:  Возвращает [ColsN, ds] (ColsN - кол-во колонок в результате)
        Если Ничего не найдено возвращает [-1, -1]
         """
        # TODO: Все работает правильно, кроме пустого результата. СДЕЛАТЬ!!!
        # Проверка, найден ли хотябы один результат
        dsFetchAll = cur.fetchall()
        cur.close()
        fetchN = len(dsFetchAll)
        if DEBUG_:
            print (f"fetchN = {fetchN}")
        if fetchN == 0: # Если не найден ни один результат
            if DEBUG_:
                print ('Не найден ни один результат')
            res = -1
        else: # Если найден хотя бы один результат в cur
            dsFetchFirst = dsFetchAll[0] # Первый элемент из FetchAll
            colN = len(dsFetchFirst)
            cur.close()
            if colN == 1: # Если одна колонка
                # print("Одна колонка")
                ds1Dim = FG.convert_tuple_of_tuples_to_list_of_lists(dsFetchAll)
                res = [x[0] for x in ds1Dim]
            else: # Если несколько колонок
                ds2Dim = FG.convert_tuple_of_tuples_to_list_of_lists(dsFetchAll)
                res = ds2Dim # Возвращает [ColsN, ds]
        return res



# -- АНАЛИТИЧЕСКИЕ МЕТОДЫ

    def if_exist_in_ds(self,dataSet, val):
        """ OBSOLETED : Использовать if_exist_in_tb_by_multiple_keys_by_dict
        Проверяет, есть ли во всех значениях dataSet (считанный список из cursor) по всем рядам числовое значение или фрагмент строки """

        boolVal = any([val in tup for tup in dataSet])
        return boolVal


    def if_exist_in_tb_by_multiple_keys(self, tb, keysNames, keyValsToCheck ):
        """ OBSOLETED : Использовать if_exist_in_tb_by_multiple_keys_by_dict, НО!!! сначала вставить этот код вместо использования ссылки на него в виде этой функции 
        в if_exist_in_tb_by_multiple_keys_by_dict
        Проверка существует ли запись в таблице по множественному ключу"""
        # Выборка всех данных из таблицы по набору сложных ключей
        cur = self.select_from_table(tb, keysNames) # Курсор результатов запроса
        dsAllWithKeyCols = self.cursor_get_all(cur) # dataSet всех строк курсора
        # Формирование списка списков столбцов из полнйо выборке по ключам
        listOfKeyCols = [] # список содержащий одномерные списки по каждой из ключевых колонок в dsAllForCheckKeys
        for iCol in range(len(keysNames)): # Формируем одномерный список из колонки dsAllForCheckKeys с текущим индексом for
            keyColList = FG.convert_list_of_list_to_one_dim_list(dsAllWithKeyCols, iCol)
            listOfKeyCols.append(keyColList)    
         # Проверка налличия записи по сложному ключу
        boolListCheck = [] # Спиок текущих проверок нахождения записей по каждому ключу в соответствующей ключевой колнке 
        messageStr = ''
        i = 0
        for valToCheck in keyValsToCheck:
            messageStr += f" '{str(valToCheck)}' в поле {keysNames[i]} и"
            boolVal = self.if_exist_in_ds(listOfKeyCols[i], valToCheck)
            boolListCheck.append(boolVal)
            i += 1
        messageStr = messageStr.rstrip('и')       
        # Результат перемножения списка булиновых значений в boolListCheck в ктором находятся результаты проверки сверки значений по будущим вносимым значениям в таблицу
        boolRes = True # Результат перемножения буллиновых значений из списка boolListCheck
        for boolVal in boolListCheck:
            boolRes = boolRes * boolVal 
        return boolRes, messageStr



    def if_exist_in_tb_by_multiple_keys_by_dict(self, tb, uniqueCheckDict ):
        """Проверка существует ли запись в таблице по множественному ключу
        uniqueCheckDict - словарь с названиями полей и их значениями, множественную совокупность которых нужно проверить на UNIQU в таблице
        Пример: uniqueCheckDict = {'link': 'http:// ...', 'name' : 'Нейрохирургия'}
        """
        # Подготовка списков из словаря
        keysNames = []
        keyValsToCheck = []
        for key, val in uniqueCheckDict.items():
            keysNames.append(key)
            keyValsToCheck.append(val)

        boolRes, messageStr = self.if_exist_in_tb_by_multiple_keys(tb, keysNames, keyValsToCheck )

        return boolRes, messageStr
    
    
    
    



# -- END АНАЛИТИЧЕСКИЕ МЕТОДЫ


# -- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ

    def execute_sql (self, sql):
        """ Выполняет запрос без возврата курсора с выборкой по результатам запроса"""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close() 
        self.connection.close()   


    def execute_sql_continuing (self, sql):
        """ Выполняет запрос без возврата курсора и без закрытия подключения к БД"""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        # cursor.close() 
        # self.connection.close()   


    def execute_sql_with_cursor (self, sql):
        """ Выполняет запрос с возвратом курсора, содержащего выборку по результатам запроса
        Курсор не закрывается. Его надо закрывать потом вручную"""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        return cursor
    
    @transform_cursor_to_list
    def execute_sql_with_list_result (self, sql):
        """ Выполняет запрос с возвратом курсора, содержащего выборку по результатам запроса
        Курсор не закрывается. Его надо закрывать потом вручную"""
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        
        return cursor, sql
    

    def execute_sql_with_params (self, sql, *args ):
        """ Выполняет запрос с возвратом курсора, содержащего выборку по результатам запроса
        Курсор не закрывается. Его надо закрывать потом вручную"""
        cursor = self.connection.cursor()
        cursor.execute(sql % args)
        self.connection.commit()
        return cursor


    def get_result_from_sql_exec_proc (self, sql):
        """Получить результат из sql-запроса в виде спискоа либо двумерного либо одномерного"""
        cur = self.execute_sql_with_cursor(sql)
        res = self.get_ds_from_cursor(cur)
        return res

    # @transform_cursor_to_list # Декоратор, который трансформирует метод так, что бы возвращался не курсор, а конечный список результатов, готовый к использованию
    # def execute_sql_with_wrap_results (self, sql):
    #     """ Выполняет запрос с возвратом курсора, содержащего выборку по результатам запроса
    #     Курсор не закрывается. Его надо закрывать потом вручную"""
    #     cursor = self.connection.cursor()
    #     cursor.execute(sql)
    #     self.connection.commit()
    #     res = [cursor]
    #     return res


    @staticmethod
    # @SqliteProcessorMacros.transform_cursor_to_list
    def get_funcs_names_from_tb_with_funcs(tbFuncs):
        """ЗАГОТОВКА: Выполнение sql запросов через декораторы только !!!"""
        
        sql = f"SELECT func_name from {tbFuncs}"
        




    def convert_val_list_with_tb_fields_to_val_dictionary (self, tb, vals):
        """ Конвертирует результат выборки из БД в виде списка, а так же в соответствии с полями таблицы в словарь полей,
         в виде ключей, и их полученными в выборке значениями
         vals : ['val1', 'val2' ... 'valN']
         fields : ['tbField1','tbField2' ... 'tbFieldN']
          """
        resDict = {}  
        fields = self.get_tb_fields (tb)
        # resDict = { f: [vals[i] for i in range(len(vals))]  for f in fields }
        resDict = { fields[i]: vals[i] for i in range(len(vals)) }
        


        return resDict


    def convert_list_of_one_tuple_to_list(self, tupArr):
        """ Конвертация данных из запросов , содержащихся в курсоре, в виде  списка из одного тапла [(x1,x2 .. xN)] 
        в обычный список велечин [x1, x2 ...]"""
        listDS = [x for x in tupArr[0]]  # преобразование в список
        return listDS

    def convert_list_of_tuples_to_list(self, tupArr):
        """ Конвертация данных из запросов, содержащихся в курсоре в виде  списка из нескольких таплов [(x1,),(x2,) ...] 
        в обычный список велечин [x1, x2 ...]"""
        listDS = [x[0] for x in tupArr]  # преобразование в список
        return listDS       



    def get_list_from_fetch (self, fetchDS, dsFetchType):
        """ Конвертация массива из cursor.fetch() с данными из запросов , содержащихся в курсоре, в виде  списка тапла или списка таплов (пока два типа)
        в обычный список велечин [x1, x2 ...] 
        fetchDS - результат преобразования курсора после sql-операции через fetch функцию 
        type - вид данных после fetch, которые могут быть в виде списка, содержащего один тапл с величинами результата [(x1,x2 .. xN)]  <type 1>
                или содержащего список из множества таплов в виде [(x1,),(x2,) ...] <type 2>. В зависимости от типа результата после fetch() подключаются 
                разные алгоритмы преобразования в конечный список типа [x1, x2 ...]. Пока type может быть равен 1 или 2 (два типа массива результатов после fetch)
        RET:
        Возвращает список величин в виде [x1, x2 ...]
        """
        if dsFetchType == 1: # Первый тип массива данных после fetch() вида списка из одного тапла, содержащего величины [(x1,x2 .. xN)]
            listDS = self.convert_list_of_one_tuple_to_list(fetchDS)

        elif dsFetchType == 2: # Второй тип массива данных к преобразованию после fetch(), вида множества таплов в списке [(x1,),(x2,) ...] 
            listDS = self.convert_list_of_tuples_to_list(fetchDS)
        return listDS

    
    def get_list_from_cursor(self, cursor, typeFetch = 'all', nForMany = 10):
        """ ОСНОВНАЯ: Возвращает list величин из выборки , находящейся в курсоре
        typeFetch - тип операции fetch() <fetchall(), fetchmany(N), fetchone()>
        nForMany - кол-во из массива fetch. Нужен только для типа fetchmany(N)
         """
        # Считывание выборки в массив fetch в зависимости от типа fetch <fetchall(), fetchmany(N), fetchone()>
        for case in Switch(typeFetch): # Аналог switch ... case
            if case('all'): 
                dsFetch = cursor.fetchall()
                break
            if case('many'): 
                dsFetch = cursor.fetchmany(nForMany)
                break
            if case('one'): 
                dsFetch = cursor.fetchone()
                break

        # Трансформация массива от fetch() в простой список. В зависимости от формата результата fetch(). Пока известно 2 формта : [(x1,x2 .. xN)] и [(x1,),(x2,) ...]
        listDS = ''
        nDsFetch = len(dsFetch)
        if nDsFetch == 1: # Тип формата [(x1,x2 .. xN)]
            listDS = self.convert_list_of_one_tuple_to_list(dsFetch)
        elif nDsFetch > 1: # Тип формата [(x1,),(x2,) ...]
            listDS = self.convert_list_of_tuples_to_list(dsFetch)

        cursor.close()
        return listDS



    def get_cols_full_ds_from_tb(self, tb, cols) :
        """ Получает массив всех значений колонки (колонок) таблицы в виде или одномерного списка, если одна колонка, или двумерный список, если несколько колонок
        cols - список названий колонок Пр: ['inn', 'link2']
        """
        conds = {}
        cur, sql = self.select_from_table_with_where_condition (tb, cols, conds)
        ds = self.get_ds_from_cursor (cur)
        return ds


    def check_wrong_val_in_col_of_2Dim_ds_with_key_col(self, ds, chkCol, chkVal, keyCol):
        """ Проверка на правильность значений в стринговой колонке двумерного массива с несколькими колонками и с колонкой ключевых значений для вывода 
        списка неправильно заполненных рядов путем поиска нужного или ненужного стрингового фрагмента
        ds - двумерный список списков с несколькими (не менее 2х) колонками
        chkCol - индекс колонки, в которой проверяется значение на правильность или на поиск неправильности
        chkVal - стринговый фрагмент, поиск которого определяет правильнсть или неправильность величины
        keyCol - колонка с ключами, которые выводятся в результате. Соответствуют тем рядвам, которые неправильны
        """
        dsWrongKeys = [x[keyCol] for x in ds if chkVal not in x[chkCol]]
        return dsWrongKeys

    def update_set_null_to_col_in_tb (self, tb, col):
        """ 
        OBSOLETED: Название не соответствует. Использовать в этом же классе новый метод  clear_field_in_tb()
        Проставить NULL в каждом ряду записей таблицы в поле col """
        sql = SQLSyntaxer.update_where_in_simple_sql (tb, [col],  ['&NULL'], {})
        self.execute_sql(sql)
        return sql
    
    
    def clear_field_in_tb (self, tb, col):
        """ NEW: Использовать вместо устаревшей update_set_null_to_col_in_tb()
        Проставить NULL в каждом ряду записей таблицы в поле col 
        """
        sql = SQLSyntaxer.update_where_in_simple_sql (tb, [col],  ['&NULL'], {})
        self.execute_sql(sql)
        return sql


    def get_row_id_by_keys_vals_dict(self, tb, keysValsDict):
        """Получение автоинкремнтного ID строки таблицы, если такой предусмотрен в ней
        keysValsDict - словарь {ключ <поле таблицы> : заданное значение поля, ..., N  }
        Прим: keysValsDict = {'name': 'Нейрохирургия СПБ', 'url' : 'http://localhost:51265'} <множественный ключ-значение> OR keysValsDict = {'name': 'Нейрохирургия СПБ'} <одномерный ключ-значение>
        """
        # ПОлучение конечного словаря условий для формаирования запросов SQL из словаря {keyName1 : keyVal1, keyName2 : keyVal2, ...} с заданным операндом '='
        conds = self.get_conds_by_keys_vals_dict_and_by_operands(keysValsDict, 'AND', '=')
        # Получение автоинкрементного ID переменной в системной таблице БД после ее внесения
        # Pars:
        getFields = ['id']
        resID = self.select_from_table_with_where_condition(tb, getFields, conds)        
        return resID[0]



    @staticmethod
    def get_conds_by_keys_vals_dict_and_by_operands(keysValsDict, logicUniteOperand = 'AND', sqlOperand = '='):
        """Получение конечного словаря условий для запросов SQL по словарю keysValsDict пар {keyName1 : keyVal1, keyName2 : keyVal2, ...}
         и заданным операндом для соединения ключей в запросе SQL
         Автоматом создает как для одного ключа, так и для множественных ключей, в чем и сосотоит смысл этой функции
         logicUniteOperand - по умолчанию: AND
         sqlOperand - по умолчанию: '='
         """
        # ПОлучение конечного словаря условий для формаирования запросов SQL из словаря {keyName1 : keyVal1, keyName2 : keyVal2, ...} с заданным операндом '='
        keysValsDictN = len(keysValsDict)
        if keysValsDictN == 1: # Если одно значение ключа-величины
            key = next(iter(keysValsDict))
            val = keysValsDict[key]
            conds = {'ONE' : [key, sqlOperand, val]} # Словарь с Конечными атрибутами выражения для условия SQL по одному ключу
        else: # Если кулючей-значений больше одного
            condsPartList =[] # Список для кончного набора условий по ключам со знаком '='
            for key, val in keysValsDict.items(): # цикл по ключам
                currCond = [key, sqlOperand, val]
                condsPartList.append(currCond)    
                conds = {logicUniteOperand : condsPartList} # Словарь с Конечными множественными атрибутами выражения для условия SQL по множественным ключам
        return conds


# -- END ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ


# Создание сложных условий conds для SQL запростов
    
    @staticmethod
    def formate_conds_OR_with_several_field_and_given_operator (srchCriteriasOR, logic, operator , attrVal):
        """ SqliteProcessor
        Создание множественного условия по нескольким полям , заданным в списке критериев
        logic - логика соединения множественных условий (AND или OR)
        srchCriteriasOR - Список полей критерия conds по логике  OR
        operator - опреатор , второе значение в списке условий. GПо умолчанию operator = '='
        attrVal - значение по условию. Третий компонент условия conds
        """
        condsCreteraaList = [] # Двумерный список условий, если критериев условий поиска болше одного. Логический выбор условий равен OR в этом случае (достаточно найти srchStr в любом поле критериев)
        for fieldCriteria in srchCriteriasOR: # Цикл по списку полей критериев поиска
            cr = [fieldCriteria, operator, attrVal] # текущий критерий по циклу
            condsCreteraaList.append(cr)
        condsOR = {logic : condsCreteraaList} # условия по нескольким критериям
        return condsOR







# END Создание сложных условий conds для SQL запростов


# -- КОМПЛЕКСНЫЕ МЕТОДЫ ИЛИ ПРИКЛАДНЫЕ , НО ОБЩИЕ ДЛЯ  SQL

    def set_same_vals_to_fields_in_all_rows_of_tb (self, tb, setFieldsVals, keyField):
        """ Проставить одни и те же значения во всех рядах таблицы в заданных полях, определенных в параметре setFieldsVals 
        Par:
        setFieldsVals - {field1: val1, field2: val2 ...}
        keyField - поле UNIQUE , по которому будет идти идентификация записи в цикле по выборке и ее UPDATE
         """
        # 1. выборка всех строк в таблице с возвратом одного ключевого поля keyField в записи
        cur = self.select_from_table(tb, [keyField]) # выборка всех строк в таблице с возвратом одного ключевого поля keyField в записи
        dsTup = cur.fetchall()
        ds = self.convert_list_of_tuples_to_list(dsTup) # Перевод данных в формат простого списка. ds - список ключевых полей bond_name со всех строк в таблице
        cur.close()   

        # 2. Цикл по ds (все строки таблицы). Обновление записей - установка значений в рядах таблицы bonds_archive в поле f1 значения 'NOT CONCENCWE'
        for keyVal in ds:
            self.update_row_in_tb(tb,  setFieldsVals, [keyField , keyVal]) # Update строки - установка значения setFieldsVals[1] в поле  setFieldsVals[0] , найденног опо ключу  keyVal

        return ds # Значения ключевого поля в рядах таблицы

    # TODO: 
    def insert_row_to_equal_tb_if_not_exists_by_key_val (self, tb, rowVals, conds):
        # TODO: Не доделана. ТАк как появилась новая общая функция insert_general_sql() Эта функция для более детального управления в циклах, возможно, если необходимо
        # Допутим, если надо добавить поле и его величину и т.д.?
        """ Вставить строку, структура которой идентична структуре таблицы, в таблицу с проверкой наличия подобной записи по ключевому полю
        Если есть, то не вносится. Если нет, то вносится
        Par:
        conds - список с условиями типа {
                                    'OR' : [['fieldName1', '<', 5], ['fieldName2', '>', 15]], 
                                    'AND' : [['fieldName3', '<', 5], ['fieldName4', '>', 15]], /
                                    'ONE'  : ['fieldName1', '<', 5],/
                                    'NO'   : None, /
                                    'STR' : '(fieldName1 > 5 AND fieldName2 < 15) AND (...)'
        row - [val1, val2, ... valN] - структура равна структуре таблицы
        """
        exists = self.check_if_row_exists_by_cond (self, tb, conds)
        if not exists: # если строка с заданным значением условий не найдена
            fieldsVals = '' # TODO
            self.insert_row_into_table (tb, fieldsVals)



    def insert_from_tbsrc_to_tbtrg_with_given_fields_assoc_by_allowed_keys (self, tbSrc, tbTrg, dictAssocFields, listSrcAllowedKeys, tbSrcKey, executeSQL= True):
        """Вставить записи из таблицы -источника из заданных полей в таблицу-цель в заданные соотвтетсвующие поля и в соотвтетствии со списком значений разрешающих вставку ключей 
        из таблицы-источнике. В таблицах названия полей и их кол-во могут не совпадать. Главное, задать  соотвтетсвие полей цели (ключи словаря) и полей источника (значения словаря)
        Можно вставлять в режиме пересечения. то есть вставляются только вколонки, названия которых в обоих таблицах совпадают. Тогда вместо dictAssocFields используется '&'
        tbSrc - источник
        tbTrg - цель
        dictAssocFields - словарь ассоциаций между полями источника и цели. Если поля одигаковы, то ключи и их значения в словаре будут равны. Иначе ключами словаря задаются поля 
        таблицы-цели, а значениями поля таблицы - истоника
        Если вместо словаря ассоциаций dictAssocFields передается '*', то это означает, что все поля в таблице источнике и таблице цели одинаковы по названию и их количеству и 
        записи вставляются дупликатом полностью
        Если надо вставить записи только в те колонки, названия которых идентичны в источнике и цели , то dictAssocFields надо приравнять к '&'
        listSrcAllowedKeys - список разрешенных значений ключей источника для вставки записей по ним в цель
        tbSrcKey - название поля-ключа в источнике
        
        """
        
        if 'str' in str(type(dictAssocFields)) and  '&' in dictAssocFields: # Если надо вставить записи только в те колонки, названия которых идентичны в источнике и цели
            # Получить пересечение названий колонок в таблицах
            tbSrcCols = self.get_tb_fields (tbSrc)
            tbTrgCols = self.get_tb_fields (tbTrg)
            tbTrgColsIntersect = FG.get_intersection_of_two_list(tbTrgCols, tbSrcCols)
            dictAssocFields = FG.convert_two_lists_to_dictionary(tbTrgColsIntersect,tbTrgColsIntersect) # Превращаем два одинаковых листа в словарь
        
        sql = SQLSyntaxer.insert_from_tbsrc_to_tbtrg_with_given_fields_assoc_by_allowed_keys_sql(tbSrc, tbTrg, dictAssocFields, listSrcAllowedKeys, tbSrcKey)
        if  executeSQL: # Если флаг executeSQL = True, то запустить выполнение запроса. В ином случае - просто вернуть sql-запрос для проверки
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            print(f"Executed SQL : {sql} / sqlite_processor.py/ ~ ln 996")
            cursor.close()   
        return sql    
        



    def update_from_tbsrc_to_tbtrg_with_given_fields_assoc_by_allowed_keys (self, tbSrc, tbTrg, dictAssocFields, listSrcAllowedKeys, tbsKeysPair, executeSQL = True):
        """Обновить записи из таблицы -источника из заданных полей в таблице-цели в заданные соотвтетсвующие поля и в соотвтетствии со списком значений разрешающих вставку ключей 
        из таблицы-источника. В таблицах названия полей и их кол-во могут не совпадать. Главное, задать  соотвтетсвие полей цели (ключи словаря) и полей источника (значения словаря)
        tbSrc - источник
        tbTrg - цель
        dictAssocFields - словарь ассоциаций между полями источника и цели. Если поля одигаковы, то ключи и их значения в словаре будут равны. Иначе ключами словаря задаются поля 
        таблицы-цели, а значениями поля таблицы - истоника
        Если вместо словаря ассоциаций dictAssocFields передается '*', то это означает, что все поля в таблице источнике и таблице цели одинаковы по названию и их количеству и 
        записи вставляются дупликатом полностью
        Если надо вставить записи только в те колонки, названия которых идентичны в источнике и цели , то dictAssocFields надо приравнять к '&'
        listSrcAllowedKeys - список разрешенных значений ключей источника для вставки записей по ним в цель
        
        listSrcAllowedKeys - список разрешенных значений ключей источника для вставки записей по ним в цель
        tbsKeysPair - список ключей обоих таблиц [tbKeySrc, tbKeyTrg] (необходимы оба ключа, так как из списка полей  таблиц необходимо удалить ключи, которые
        не могут быть обновлены , так как являются ключами)
        
        """

        if 'str' in str(type(dictAssocFields)) and  '&' in dictAssocFields: # Если надо вставить записи только в те колонки, названия которых идентичны в источнике и цели
            # Получить пересечение названий колонок в таблицах
            tbSrcCols = self.get_tb_fields (tbSrc)
            tbTrgCols = self.get_tb_fields (tbTrg)
            tbTrgColsIntersect = FG.get_intersection_of_two_list(tbTrgCols, tbSrcCols)
            dictAssocFields = FG.convert_two_lists_to_dictionary(tbTrgColsIntersect,tbTrgColsIntersect) # Превращаем два одинаковых листа в словарь
            
        elif 'str' in str(type(dictAssocFields)) and  '*' in dictAssocFields:
            tbSrcCols = self.get_tb_fields (tbSrc)
            dictAssocFields = FG.convert_two_lists_to_dictionary(tbSrcCols,tbSrcCols) # Превращаем два одинаковых листа в словарь
        
        sql = SQLSyntaxer.update_from_tbsrc_to_tbtrg_with_given_fields_assoc_by_allowed_keys_sql(tbSrc, tbTrg, dictAssocFields, listSrcAllowedKeys, tbsKeysPair)
        
        if  executeSQL: # Если флаг executeSQL = True, то запустить выполнение запроса. В ином случае - просто вернуть sql-запрос для проверки
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()   
            
        return sql    



    
    def check_if_row_exists_by_cond (self, tb, conds):
        """ Проверить, существует ли в таблице строка с заданными условиями
            conds - список с условиями типа {
                                                'OR' : [['fieldName1', '<', 5], ['fieldName2', '>', 15]], 
                                                'AND' : [['fieldName3', '<', 5], ['fieldName4', '>', 15]], /
                                                'ONE'  : ['fieldName1', '<', 5],/
                                                'NO'   : None, /
                                                'STR' : '(fieldName1 > 5 AND fieldName2 < 15) AND (...)'
                                                }
         """
        res = self.select_from_table_with_where_condition (tb, ['*'], conds)
        print(f'res = {res}')
        # dsTup = cur.fetchall()
        if type(res) == 'int': # Если нет ни одного значения, то res = -1  type(res) = int
            return False 
        else: # Если есть хоть одна запись, то type(res) = list
            return True


    def copy_row_from_tb_to_equal_tb (self, tbSrc, tbTrg, keyFV, conds, cmnts = False, delSrc = True, delTrg = True):
        """ Копирует строку с заданным значением ключевого поля для поиска в другую таблицу, абсолютно равную ей по структуре
        keyFV - спиок, содержащий название ключевого поля  и его  значение  для поиска строки в таблице-источнике tbSrc
        conds - Условие WHERE  для нахождения строки для переноса в таблице-источнике. Подчиняется правилам параметра функции SQLSyntaxer.select_from_table_with_where_condition_sql
        delSrc - флаг. Если = True,  то строка после копирования удаляется в таблице - источнике. По уvолчанию = True
        tbTrg - флаг. Если = True,  то строка перед копированием удаляется в таблице-цели, если таковая найдена по ключу keyFV. По уvолчанию = True
        cmnts - флаг. Если = True, то выводятся комментарии по процессу переноса строки. По уvолчанию = False

        Пример параметров:
        tbSrc = 'bonds_2022_09_10'
        tbTrg = 'bonds_archive_2022_09_11' 
        keyField = 'bond_name' # Название ключевого поля для поиска строки и переноса 
        keyVal = 'BCS12/24-B' # Значение ключевого поля, по которому будет производится поиск и перенос строки из источника в цель
        keyFV = [keyField, keyVal] # Составляемый параметр: Список с ключевым полем и его значением для поиска строки для переноса в таблице - источнике
        conds = {'ONE' : [keyField,'=', keyVal]} # Условие WHERE  для нахождения строки для переноса в таблице-источнике. Подчиняется правилам параметра функции SQLSyntaxer.select_from_table_with_where_condition_sql
        """
        # keyField = keyFV[0] # Название ключевого поля для поиска строки и переноса 
        keyVal = keyFV[1] # Значение ключевого поля, по которому будет производится поиск и перенос строки из источника в цель
        # conds = {'ONE' : [keyField,'=', keyVal]} # Условие WHERE  для sql
        getFields = ['*'] # перечень полей для запроса в select. '*' - все поля в выборке запросить
        # Проверка наличия записи с ключем  keyField в таблице-источнике
        cur, sql = self.select_from_table_with_where_condition (tbSrc, getFields, conds)
        # print (sql)
        resDS = cur.fetchall()    
        cur.close()  
        # print (resDS)
        nResrc = len(resDS) # кол-во записей с заданным ключем в таблице-источнике
        # print(nResrc)    
        if  nResrc > 0 :   # значит записи  с таким ключем в таблице-источнике есть 
            if cmnts: print (f"Строка с ключем {keyVal} в таблице - источнике {tbSrc} найдена. -> Выполняем проверку в таблице-цели {tbTrg}")
            # Проверка наличия записи в таблице архива с ключем  bond_name = <keyVal>
            cur, sql = self.select_from_table_with_where_condition (tbTrg, getFields, conds)
            # print (sql)
            resDS = cur.fetchall()    
            cur.close()  
            # print (resDS)
            nResTrg = len(resDS) # кол-во записей с заданным ключем в таблице-цели
            # print(nResTrg)
            # Проверка наличия записи в таблице-цели с ключем  bond_name = <keyVal> и удаление ее в случае нахождения, чтобы вставить новую из источника
            if  nResTrg > 0 :   # значит записи  с таким ключем в таблице-цели есть 
                # Если есть, то сначала удаление предыдущей записи архивной и вставка копии
                if cmnts: print(f"В таблице-цели {tbTrg} есть запись с заданным ключем {keyVal}. -> Запись будет удалена для добавления новой из источника")
                if delTrg:
                    sql = self.delete_from_table_with_where_condition (tbTrg, conds) # удаление записи по ключу в таблице-цели (bonds_archive)
                    if cmnts: print (f"Строка в таблице {tbTrg} с ключем {keyVal} удалена")
                    # print (sql)
                else: 
                    if cmnts: print (f"Флаг delTrg = {delTrg} и строка с ключем {keyVal} не будет удалена из таблицы-цели {tbTrg}.-> Скопирована будет подобная строка с таким же ключем, если нет запрета по UNIQUE")
            # Копирование строки из источника и вставка в целевую таблицу
            cur, sql = self.select_from_table_with_where_condition (tbSrc, getFields, conds) # копируем данные строки с ключем в таб bonds
            if cmnts: print(f"В таблице {tbTrg} нет записи с заданным ключем. - > Запись будет скопирована из источника")
            resTups = cur.fetchall()
            cur.close()
            # Составление словаря с ключами в виде названий полей таблицы, и с велечинами в виде значений полей, находящихся в выборке после fetch()
            # Результат fetch() , возможно, может отличатся по форме, поэтому пока анализ формы результата делается в ручную (а не функцией), чтобы получить простой список велечин
            # TODO: Сделать функцию, которая будет автоматом анализировать вариант возвращаемых даынных из выбборки путем fetch() и создавать простой список, а затем и словарь строки на выходе
            resDS = self.convert_list_of_one_tuple_to_list(resTups) # конвертация из [(x1,x2 .. xN)]
            resDic = self.convert_val_list_with_tb_fields_to_val_dictionary (tbSrc, resDS)
            # Вставка данных в архивную таб
            sql = self.insert_row_into_table (tbTrg, resDic)
            if cmnts: print (f"Строка с ключем {keyVal}  скопирована в таблицу {tbTrg}")
            # print (sql)
            # TODO: Удаление строки с заданным ключем из таблицы источника   
            if delSrc:  
                sql = self.delete_from_table_with_where_condition (tbSrc, conds) # удаление записи по ключу в таблице-цели (bonds_archive)
                # print(sql)
                if cmnts: print (f"Строка с ключем {keyVal} в источнике {tbTrg} удалена")
            else:  
                if cmnts: print(f"Флаг delSrc = {delSrc} и строка с ключем {keyVal} не будет удалена из таблицы-источника {tbSrc}")
        else : # Если не найдена в источнике строка с заданным ключе
            if cmnts: print (f"Строка в таблице -источнике {tbSrc} с ключем {keyVal} не найдена")





    def get_dict_from_mono_sql_select_proc(self, tb, sql):
        """Получение записи в виде словаря, которую возвращает полный (*, возвращающий полный набор полей таблицы) моно (возвращающий одну запсиь из таблицы) sql-запрос 
        Ключами служат название полей таблицы, а значениями словаря - значения полей записи, которую возвращает sql-запрос 
        SQL - запрос должен возвращать всё множество полей таблицы ('*')
        RET: 
        Возвращает -1, если не найдена ни одна запись
        или словарь , где ключами являются название полей таблицы, а значениями - значения возвращенной записи sql-запроса
        """

        cols = self.get_tb_fields(tb)
        res = self.get_result_from_sql_exec_proc(sql)   # <!!!!!!!!!!!!!!!>

        if type(res) != int: # Проверка. Если res = -1, то значит не найдено ничего. В ином случае type будет list или tuple

            diffValList = res[0]
            diffDic = FG.convert_two_lists_to_dictionary(cols, diffValList)

        else:
            diffDic = -1

        return diffDic

#  -- END КОМПЛЕКСНЫЕ МЕТОДЫ ИЛИ ПРИКЛАДНЫЕ , НО ОБЩИЕ ДЛЯ  SQL








# -- МЕТОДЫ ПО СТРУКТУРЕ МЕТАДАННЫХ БД

    def get_tb_fields (self, tb):
        """ Получение названий полей таблицы в списке """
        sql = SQLSyntaxer.get_tb_fields_sql(tb)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        arr = cursor.fetchall() # arr в виде списка таплов [(x1,),(x2,) ...]
        dsFields = self.convert_list_of_tuples_to_list(arr)
        # dsFields = [x[0] for x in arr]  # преобразование в список
        cursor.close()   
        return dsFields








        

# -- END МЕТОДЫ ПО СТРУКТУРЕ МЕТАДАННЫХ БД    


# -- МЕТОДЫ СОЗДАНИЯ И ИЗМЕНЕНИЯ МЕТАДАННЫХ

    def create_table (self, tb,fields, rkeys):
        """ Создание таблицы в БД """

        sql_tb_create = SQLSyntaxer.create_tb_sql(tb,fields, rkeys)
        cursor = self.connection.cursor()
        cursor.execute(sql_tb_create)
        self.connection.commit()
        cursor.close()   



    def drop_table_proc(self, tbName):
        """Удалить таблицу, если она существует"""

        sql = SQLSyntaxer.drop_table_sql(tbName)
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()   




# -- END МЕТОДЫ СОЗДАНИЯ И ИЗМЕНЕНИЯ МЕТАДАННЫХ


# -- МЕТОДЫ ДЛЯ ФУНКЦИЙ _ ПАРАМЕТРОВ, КОТОРЫЕ ПЕРЕДАЮТСЯ В ВИДЕ АРГУМЕНТОВ В ДРУГИЕ ФУНКЦИИ, ВООБЩЕ ВСЕ ФУНКЦИИ НАДО СТРОИТЬ С ЭТИМ ПОДХОДОМ АВАНСОМ

    def update_rows_from_ds_PF(self , dataSet, paramsDic):
        """ 
        Class: SqliteProcessor
        Обновление значений в таблице БД на основе данных в dataSet (массив общих данных , с множеством разных колонок, в виде списка рядов значений) . Идентификация по ключу uniqueColNames
        PF - расшифровывается Parameter Function, то есть данная функция может быть передана в виде параметра (значит обладает определенной структурой в своих параметрах
        )
        !!! Функции для подобного подхода должны строится по определенной структуре: В аргументах такой функции-параметра 
        должен сначала идти массив аргументов (тот, который также может быть получен внутри метода и подставлен, а может быть передан и извне),
        а затем словарь с аргументами!!!
        ПАРАМЕТРЫ:
        fieldsAcordAbs = {3: 'okpo', 1 : 'reg_year', 7:'comp_name'} - соответствие индексов колонок в dataSet и названий колонок в таблице БД. Индекс в dataSet начинается с 0 \n
        uniqueColNames = [9,'inn'] - список соответствия индекса ключевой колонки в dataSet и ее названия в таблице БД
        """
        # , tb, dataSet, fieldsInxAccordList, unqInxColVal
        # РАсшифровка параметров:
        tb = paramsDic['tb']
        fieldsInxs = paramsDic['fieldsInxs']
        unqInxCol = paramsDic['unqInxCol']

        # Цикл по dataSet
        uniqColInx = unqInxCol[0] # индекс ключевой колонки в dataSet
        unqColTbName = unqInxCol[1] # название ключевой колонки в таблице БД

        for dsRow in dataSet:
            # Формирование словаря {'fieldName':'fieldValue'} по текущему ряду из массива по циклу for rowVals
            updColsVals = {} # Словарь { поле : значение, ...} для внесения обновлений записи в таблицу БД, на основании которого формируется sql-запрос
            for key,value in fieldsInxs.items():
                updColsVals[value] = dsRow[key] # формирование словаря с данными для обновления значений в записи таблицы БД

            uniqExelKeyVal = dsRow[uniqColInx] # значение поля ключевой колонки , по которому будет найдена запись в таблице БД для обновления
            # Подготовка парметров для update_row_in_tb of SqliteProcessor
            unqKeyVal = [unqColTbName, uniqExelKeyVal] # ключевое поле и его значение для поиска записи к обновлению в таблице БД 
            # Обновление записи в таблице БД , найденной по заданному значению ключевого поля
            self.update_row_in_tb(tb,  updColsVals, unqKeyVal)




# -- END МЕТОДЫ ДЛЯ ФУНКЦИЙ _ ПАРАМЕТРОВ, КОТОРЫЕ ПЕРЕДАЮТСЯ В ВИДЕ АРГУМЕНТОВ В ДРУГИЕ ФУНКЦИИ, ВООБЩЕ ВСЕ ФУНКЦИИ НАДО СТРОИТЬ С ЭТИМ ПОДХОДОМ АВАНСОМ





## МЕТА ФУНКЦИИ  

    def get_create_table_shema_sql_meta(self, tbName):
        """Возвращает sql - запрос с дампом структуры заданной табдлицы (без данныхЮ только структура-схема таблицы)"""

        getFields = ['sql']
        conds = {'AND': [['type','=','table'],['name','=', tbName]]}
        tb = 'sqlite_master'
        resSQL = self.select_from_table_with_where_condition(tb, getFields, conds, add = '')

        return resSQL[0]



    def get_clone_new_tab_sql_of_given_table_structure(self, baseTbName, newTbname):
        """Выдает SQL запрос для создания новой таблицы - клона заданнйо базовой таблицы"""
        createSQL = self.get_create_table_shema_sql_meta(baseTbName)
        # print(createSQL)
        newTbCreateSQL = createSQL[0].replace(baseTbName,newTbname)
        return newTbCreateSQL










## МЕТА ФУНКЦИИ  







if __name__ == "__main__":
    pass



    






    # # ПРОРАБОТКА: SELECT ... UNION из некольких таблиц
    # from bonds.bonds_main_manager import BondsMainManager
    # from bonds.structures import *
    # from bonds.settings import *
    # bmm = BondsMainManager(DB_BONDS_)
    
    # # pars:
    
    # # listUnionsStructurePars = [
        
    # #     SelectUnionStructure(TB_BONDS_ARCIVE_, ['isin', 'bond_name AS FIELD2'], 'Corporate'),
    # #     SelectUnionStructure(TB_OFZ_ARCIVE_, ['isin', 'f2'], 'OFZ'),
    # #     SelectUnionStructure(TB_MUNICIP_ARCIVE_, ['isin', 'f11'], 'Municip'),
    # # ]
    
    # # Единое условие  для всех обьединяемых таблиц
    # whereCond = { 
    #     'ONE'  : ['f11', '>', 1687165467]
    # }
    
    # listUnionsStructurePars = [
        
    #     SelectUnionStructure(TB_BONDS_CURRENT_, '*', whereCond, 'Corporate'),
    #     SelectUnionStructure(TB_OFZ_CURRENT_, '*', whereCond, 'OFZ'),
    #     SelectUnionStructure(TB_MUNICIP_CURRENT_, '*', whereCond, 'Municip'),
    # ]
        

    # listOrder = [
    #     'isin DESC',
    # ]



    # # sql = SQLSyntaxer.select_tbs_union_sql (listUnionsStructurePars, unionAll = True, whereCond = whereCond, listOrder = listOrder, )
    # # print(f"sql = {sql}")
    
    # dsRes = bmm.select_tbs_union(listUnionsStructurePars, unionAll = False, listOrder = listOrder)
    # print(f"dsRes = {dsRes}")




    # # ПРОРАБОТКА: Функции UPDATE двух таблиц по заданным разрешенным ключам с полным совпадением по полям, здаваемым ассоциативно пересечением и естественным пересечением по полям
    # from bonds.settings import *
    # from bonds.bonds_main_manager import BondsMainManager
    
    # bmm = BondsMainManager(DB_BONDS_)
    
    # tbSrc = TB_OFZ_CURRENT_
    # tbTrg = TB_OFZ_ARCIVE_
    
    # listKeysPair = ['isin', 'isin']
    # listSrcAllowedKeys = bmm.select_diffr_rows_keys_in_two_tabs_by_key_cols (tbSrc, tbTrg, listKeysPair)
    # print(f"listSrcAllowedKeys_N = {listSrcAllowedKeys}")
    
    # dictAssocFields = {
    #     'isin': 'isin',
    #     'f5' : 'f5'
    # }
    
    # tbsKeysPair = ['isin', 'isin']
    
    # sql = bmm.update_from_tbsrc_to_tbtrg_with_given_fields_assoc_by_allowed_keys(tbSrc, tbTrg, '&', listSrcAllowedKeys, tbsKeysPair)

    # print(f"{sql}")
    
    
    
    
    
    
    
    



    # ПРИМЕР: Создание FTS таблицы на основе контентной табдицы БД
    # https://stackoverflow.com/questions/55574400/how-to-create-virtual-table-fts-with-external-sqlite-content-table#comment97885135_55577231


    # CREATION:
    # db_processor = SqliteProcessor(DB_TLH_)   
    # sql = 'CREATE VIRTUAL TABLE IF NOT EXISTS infblocks_curr_fts using fts5(content=infblocks_curr, content_rowid=id, id, bl_title, bl_rest, full_path);'
    # cur = db_processor.connection.execute(sql)


    # # SELECT MATCH
    # db_processor = SqliteProcessor(DB_TLH_)   
    # sqlSel = "SELECT * FROM infblocks_curr_fts where infblocks_curr_fts MATCH 'ERROR' ;"
    # cur = db_processor.connection.execute(sqlSel)
    # ds = cur.fetchall()


    # "insert into infblocks_curr_fts(infblocks_curr_fts) VALUES ('rebuild');"





# ПРИМЕРЫ:


    # # ПРИМЕР: Проверка работы select_with_except(self, fullSel1Pars, fullSel2Pars)

    # db = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/bonds.db'
    # db_processor = SqliteProcessor(db)   
    # # db_processor.select_with_except(self, fullSel1Pars, fullSel2Pars)
    # cursor = db_processor.connection.cursor()
    # cur = cursor.execute('SELECT inn FROM comps EXCEPT SELECT inn FROM comps_descr')
    # dsFetch = cur.fetchall()
    # cur.close()


    # # ПРИМЕР: Проверка работы функции get_row_id_by_conds(self, tb, keysValsDict) - получение ID записи в таблице по заданным ключам-значениям


    # dbWebAsseml = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/infor_assembling_center/web_assembl.db'
    # db_processor = SqliteProcessor(dbWebAsseml) 
    # tb = "sessions"

    # # Словарь ключей - значений 
    # keysValsDict = {'name': 'Нейрохирургия СПБ', 'url' : 'http://localhost:51265'}
    # resId = db_processor.get_row_id_by_keys_vals_dict(tb, keysValsDict)

    # print(resId)


    # # ПРИМЕР: Проверка функции select_from_table_with_where_condition
    # db = 'bonds.db'    
    # db_processor = SqliteProcessor(db)    
    # tbCompsDescr = 'comps_descr'
    # getFields = ['inn']
    # linkVal = 'https://fin-plan.org/lk/obligations/company/gruzovichkof-tsentr-ooo/'
    # conds = {'ONE' : ['link2','=',linkVal]}

    # res = db_processor.select_from_table_with_where_condition(tbCompsDescr, getFields, conds)     

    # print(res)



# ------------------

    # # ПРИМЕР:  функция SqliteProcessor.insert_rows_from_ds_with_multiple_key_check внесения данных в таблицу БД с проверкой по сложному ключу из нескольких полей
    # # Out params:
    # tbLinksCurr = 'links_current'
    # tb = tbLinksCurr
    # fieldsAccordList = { # Соответствия индексов в dsInp и полей в таблице
    #     0 : 'link',
    #     1 : 'srch_txt',
    #     2 : 'file_name',
    #     3 : 'directory',
    #     4 : 'theme',
    #     5 : 'time',
    #     6 : 'source'
    # }
    # prKeyInxs = [0,1] # Сложный ключ, по которому идет проверка UNIQUE в таблице до новой записи   

    # dbWebAsseml = 'web_assembl.db'
    # db_processor = SqliteProcessor(dbWebAsseml) 

    # dataSet = [['https://spb.docdoc.ru/clinic/spec/neirohirurgiya',Frame
    #             '22_10_2022_21_45_12',
    #             'Google'],
    #             ['https://www.gosmed.ru/services/statsionarnaya-pomoshch/neyrokhirurgiya/',
    #             'Нейрохирургия СПБ',
    #             'Нейрохирургия.txt',
    #             '~/Yandex.Disk_/MY_MED2',
    #             'MED',
    #             '22_10_2022_21_45_12',
    #             'Google']]

    # db_processor.insert_rows_from_ds_with_multiple_key_check (tb, dataSet, fieldsAccordList, prKeyInxs)






    # # ПРИМЕР: Проверка ошибки в функции
    # db = 'bonds.db'    
    # db_processor = SqliteProcessor(db)   
    # tbCurrent = 'bonds_current'
    # tbArchive = 'bonds_archive'

    # fieldsTb1 = ['isin'] # список полей  в UPDATE SET первой таблицы
    # fieldsTb2 = ['bonds_archive.isin'] # список полей  в SELECT for SET первой таблицы    
    # condsUpdTb1 = {} # Условия для UPDATE первой таблицы 
    # condsSelTb2 = {'ONE' : ['bonds_current.bond_name','=', '&bonds_archive.bond_name']} # Условия для SELECT второй таблицы  
    # sqlUpd = SQLSyntaxer.update_tb1_from_select_tb2_simple_sql (tbCurrent,tbArchive, fieldsTb1, fieldsTb2, condsUpdTb1 , condsSelTb2 )


    # cursor = db_processor.connection.cursor()
    # cursor.execute(sqlUpd)
    # db_processor.connection.commit()
    # cursor.close()   






    # # # ПРИМЕР: Нахождение ISIN по INN компании из таблиц bonds_archive и bonds_current
    # # Парам:
    # db = 'bonds.db'
    # db_processor = SqliteProcessor(db) 
    # inn = 7446031217

    # isins = db_processor.get_isins_by_inn_from_DB (inn)



    # # ПРИМЕР: insert_rows_from_ds
    # db = 'bonds.db'
    # db_processor = SqliteProcessor(db) 
    
    # dsInnOneDim = ['5433158068', '7702070139', '7710170659']
    # # dsInnTwoDim = [[x] for x in dsInnOneDim]
    # dsInnTwoDim = FG.convert_one_dim_list_to_list_of_lists(dsInnOneDim)
    # tb = 'global_A'
    # fieldsAccordList = {0: 'x_str'}
    # prKeyInx = 0
    # # print(f"{dsInnOneDim}")Frame
    # db = 'bonds.db'    
    # tbCurrent = 'bonds_current'
    # tbArchive = 'bonds_archive'
    # fieldsTb1 = ['isin'] # список полей  в UPDATE SET первой таблицы
    # fieldsTb2 = ['bonds_archive.isin'] # список полей  в SELECT for SET первой таблицы    
    # condsUpdTb1 = {} # Условия для UPDATE первой таблицы 
    # condsSelTb2 = {'ONE' : ['bonds_current.bond_name','=', '&bonds_archive.bond_name']} # Условия для SELECT второй таблицы    
    # db_processor = SqliteProcessor(db)
    # db_processor.update_tb1_from_select_tb2_simple_exec(tbCurrent,tbArchive, fieldsTb1, fieldsTb2, condsUpdTb1 , condsSelTb2, True)



    # # ПРИМЕР: Обновление данных в первой таблице из второй таблицы на основе условий, сочитающих в себе поля из обоих таблиц
    # # Парам:
    # db = 'bonds.db'    
    # tbCurrent = 'bonds_current'
    # tbArchive = 'bonds_archive'
    # fieldsTb1 = ['isin'] # список полей  в UPDATE SET первой таблицы
    # fieldsTb2 = ['bonds_archive.isin'] # список полей  в SELECT for SET первой таблицы    
    # # fieldsTb1 = ['bonds_current.isin', 'bonds_current.f2'] # список полей  в UPDATE SET первой таблицы
    # # fieldsTb2 = ['bonds_archive.isin', 'bonds_archive.f2'] # список полей  в SELECT for SET первой таблицы
    # # condsUpdTb1 = {'ONE' : ['bonds_current.f2','>', 5 ]} # условия для UPDATE первой таблицы
    # # condsSelTb2 = {'AND' : [['bonds_current.bond_name','=', '&bonds_archive.bond_name'], 
    # #                         ['bonds_current.bond_name','=', '5'] 
    # #                         ]} # Условия для SELECT второй таблицы
    # condsUpdTb1 = {} # Условия для UPDATE первой таблицы 
    # condsSelTb2 = {'ONE' : ['bonds_current.bond_name','=', '&bonds_archive.bond_name']
    #                         } # Условия для SELECT второй таблицы    
    # db_processor = SqliteProcessor(db)
    # db_processor.update_tb1_from_select_tb2_simple_exec(tbCurrent,tbArchive, fieldsTb1, fieldsTb2, condsUpdTb1 , condsSelTb2, True)



    # # ПРИМЕР: Отработка функции select_from_table_with_where_condition_sql () - получение выражение SELECT с условием WHERE IN
    # db = 'bonds.db'    
    # db_processor = SqliteProcessor(db)
    # tbSel1    = 'bonds_current'    
    # selConds1 = {} # условия в части sql SELECT , если наличиствует параметр EXISTS или NOT EXISTS. '&' указывает, что это названия поля
    # selFields1 = ['bond_name']
    # fullSelParams1 = {"tb":tbSel1,"selFields" : selFields1, "selConds" : selConds1}
    # # Параметры для второго SELECT
    # tbSel2 = 'bonds_archive'    
    # selConds2 = {} # условия в части sql SELECT , если наличиствует параметр EXISTS или NOT EXISTS. '&' указывает, что это названия поля
    # selFields2 = ['bond_name']
    # fullSelParams2 = {"tb":tbSel2,"selFields" : selFields2, "selConds" : selConds2}
    # sqlSelExcept = SQLSyntaxer.select_with_except_sql (fullSelParams1, fullSelParams2) # sql для выявления тех записей, которые присутствуют в bonds_current (обновленной после считывания новой оперативной выборки с сайта smart)
    # # cur = db_processor.execute_sql_with_cursor (sqlSelExcept) # курсор с выпоркой по результатам запроса
    # # dsTupArr = cur.fetchall() # массив данных результата запроса sql в виде списка таплов (которые могут иметь формат двух видов [(x1,x2 .. xN)] <type = 1>) или [(x1,),(x2,) ...]  <type = 2>
    # # dsList = db_processor.get_list_from_cursor (dsTupArr, 2) #  конечный результат выборки sql запроса в виде списка
    # # Параметры:
    # tbIns = 'bonds_archive'
    # fields = ['*']

    # dsIN = sqlSelExcept # dsIN = SELECT string
    # # dsIN = 'SELECT * FROM'
    # # dsIN = ['1','2','3'] # dsIN = список
   
    # conds = {'ONE': ['bond_name', 'IN', dsIN]}  # Условия по одному параметру
    # # conds = {'AND':  [['isin', '>', 5], ['bond_name', 'IN', dsIN]]}  # Условия по нескольким параметрам с AND/OR соединением
 
    # sqlSelIN = SQLSyntaxer.select_from_table_with_where_condition_sql(tbIns, fields, conds)
    # print (sqlSelIN)



    # # ПРИМЕР: Проработка общей функции ISERT / 2.Формирование sql, если все поля и есть SELECT параметры
    # # Par для INSERT: 
    # db = 'bonds.db'
    # sqliteProcessor = SqliteProcessor (db)
    # tbIns = 'bonds_archive' # Таблица для INSERT
    # fields = ['*']
    # vals = ['*']
    # onConflicts = 'IGNORE'
    # # Par для SELECT
    # tbSel = 'bonds_current' # Таблица для SELECT
    # getSelFields = ['*']
    # conds = {'ONE'  : ['bond_name', '=', 'АПРИФП БП5']}
    # sqlSelParams = {'tb' : tbSel, 'getSelFields' : getSelFields, 'conds' : conds} # параметры SELECT  запроса в виде словаря для составления части SELECT внутри функции insert_general_sql
    # sql = sqliteProcessor.insert_general(tbIns, fields, vals, onConflicts, sqlSelParams ) # Конечный INSERT запрос sql
    # print(f'sqlIns = {sql}')Framebond_name
    # db = 'bonds.db'
    # sqliteProcessor = SqliteProcessor (db)
    # # PAR: 
    # tb = 'bonds_archive'
    # getFields = ['*']
    # keyField = 'bond_name'    
    # setFieldsVals = {'f1' : 'NOT MATCHED'} # 'NOT MATCHED' - не найдено совпадений на сайте moex (Моск биржа)
    # db_processor = SqliteProcessor(db)
    # db_processor.set_same_vals_to_fields_in_all_rows_of_tb (tb, setFieldsVals, keyField)


    # # ПРИМЕР: Удаление строки из таблицы
    # db = 'bonds.db'
    # sqliteProcessor = SqliteProcessor (db)
    # tb = 'bonds_archive_2022_09_11'
    # getFields = ['*']
    # keyField = 'bond_name'    

    # keyVal = "BCS12/24-4"
    # conds = {'ONE' : [keyField,'=', keyVal]}

    # db_processor = SqliteProcessor(db)
    # sql = db_processor.delete_from_table_with_where_condition (tb, conds) # удаление записи по ключу в таблице-цели (bonds_archive)
    # print(sql)


    # # ПРИМЕР: Составление словаря из двух равных по размеру списков, в котором один список формирует ключи, другой - величины по ключам
    # # Пример: Ковертации двух видов саисков таплов, которые встречаются в результате fetch() из выборки, хранящейся в курсоре
    # # Пример: Составление словаря на основе двух равных по размеру списка с использованием Comprehance
    # # Par:
    # db = 'bonds.db'
    # tbSrc = 'bonds_2022_09_10'
    # tbTrg = 'bonds_archive_2022_09_11' # Корень в названии таблицы, к которому добавляется дата (для того, что бы не было конфликта с имеющейся возможной таблицей)
    # keyField = 'bond_name'    
    # keyVal = "КАМАЗ БО15"
    # getFields = ['*']
    # conds = {'ONE' : ['bond_name','=', 'КАМАЗ БО15']}  
    # sqliteProcessor = SqliteProcessor (db)
    # dsFields = sqliteProcessor.get_tb_fields (tbSrc) # Конвертация из [(x1,),(x2,) ...] внутри функции get_tb_fields
    # # print ('\n')
    # # print (dsFields)
    # # print(len(dsFields))
    # # print ('\n')
    # cur, sql = sqliteProcessor.select_from_table_with_where_condition (tbSrc, getFields, conds) # копируем данные строки с ключем в таб bonds
    # # print(sql)
    # resTups = cur.fetchall()
    # resDS = sqliteProcessor.convert_list_of_one_tuple_to_list(resTups) # конвертация из [(x1,x2 .. xN)]
    # # print (resDS)    
    # # print(len(resDS))
    # resDict = sqliteProcessor.convert_val_list_with_tb_fields_to_val_dictionary (tbSrc, resDS)Frame
    # # ПРИМЕР: Получение списка полей таблицы
    # db = 'bonds.db'
    # sqliteProcessor = SqliteProcessor (db)
    # tb = 'bonds_2022_09_10'
    # dsFields = sqliteProcessor.get_tb_fields (tb)
    # print (dsFields)

    # # ПРИМЕР
    # # STEP 11. Создание таблицы в БД
    # # ПАРАМЕТРЫ:
    # tb = 'bonds_test'
    # fields = TB_BONDS_11STEP
    # keys =  TB_BONDS_KEYS_1
    # # Получение update sql
    # create_sql = SQLSyntaxer.create_tb_sql(tb, fields, keys)
    # db = 'bonds.db'
    # sqliteProcessor = SqliteProcessor (db)
    # cursor = sqliteProcessor.connection.cursor()
    # cursor.execute(create_sql)
    # sqliteProcessor.connection.commit()
    # cursor.close() 


    # # ПРИМЕР
    # Step 10. Проработка процесса UPDATE тбалиц БД sqlite
    # ПАРАМЕТРЫ:
    # db = 'bonds.db'
    # tb = 'comps'
    # uniqueKeyVal = ['inn','2128702350']
    # fieldsVals = {'okpo' : '111', 'sector' : '333'}
    # sqliteProcessor = SqliteProcessor (db)
    # sqliteProcessor.update_row_in_tb(tb, fieldsVals, uniqueKeyVal)
    # sleep(2)
    # sql_update = sqliteProcessor.update_tb_row_with_unique_key_sql(tb, fieldsVals,uniqueKeyVal)
    # cursor = sqliteProcessor.connection.cursor()
    # cursor.execute(sql_update)
    # sqliteProcessor.connection.commit()
    # cursor.close()   

 # -----------------------------


















