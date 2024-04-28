
from noocube.pandas_manager import PandasManager


# Динамическая настройка на общий settings_bdp_main.py
# import sys
# sys.path.append('/home/ak/projects/P19_Bonds_Django/bonds_django_proj')
# import noocube.settings_bdp_main as ms # общие установки для всех модулей

import numpy as np
import pandas as pd

from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup


class SqlitePandasProcessorSpeedup (): 
    """ 
    Класс для операций с БД через фреймы , ускоренный. Отличается от обычного SqlitePandasProcessor тем, что идет коннекшен к бД
    через константный коннекшен (обысно настраиваемый в settings.py  любокго проекта)
    ПРИМ: Так же отличается тем, что не наследуется ни от какого класса на данный момент
    """

    def __init__(self, dataBaseConnection): 
        
        self.db_uri = f"sqlite:///{dataBaseConnection.dataBase}" # Pandas по умолчанию работает через SQLAlchemy и может создавать сама присоединение к БД по формату адреса URI (см. в документации SQLAlchemy)
        self.db_connection = dataBaseConnection.connection
        self.sps = SqliteProcessorSpeedup(dataBaseConnection) # Обьект класса SqliteProcessorSpeedup
    
    
    
    
    
    

    ##### EXECUTE SQL METHODS ------------
    
    
    def read_sql_to_df_pandas_SPPS(self, sql):
        """
        SqlitePandasProcessorSpeedup
        Считывает результат sql запроса в dataFrame
        
        """    
        df = pd.read_sql(sql, self.db_uri)
        return df
    
    
    
    
    def read_sql_to_df_pandas_mysql_spps(self, sql):
        """
        SqlitePandasProcessorSpeedup
        Считывает результат sql запроса в dataFrame
        
        """    
        print(f"PR_NC_186 --> START: read_sql_to_df_pandas_mysql_spps()")
        df = pd.read_sql(sql, self.db_connection)
        
        
        # print(f"PR_NC_205 --> df = \n{df}")
        
        print(f"PR_NC_187 --> END: read_sql_to_df_pandas_mysql_spps()")

        return df
    
    
    
    
    
    
    
    

    def read_table_by_sql_to_df_pandas_SPPS(self, tb, getFields = ['*']):
        """
        SqlitePandasProcessorSpeedup
        Считывает всю таблицу в фрейм с выбором необходимых колонок в выборке
        getFields - список выводимых колонок. По умолчанию выводятся все колонки
        """
        # Считывание таблицы bonds_archive в фрейм
        sql = f'SELECT * FROM {tb}'
        # print(sql + '  | read_table_by_sql_to_df_pandas() | noocube/sqlite_pandas_processor.py')
        dfTb = self.read_sql_to_df_pandas_SPPS(sql)  
        if '*' in getFields: # если запрашиваются все колонки
            return dfTb
        else : # если выборка колонко
            dfTb = PandasManager.get_sub_df_with_given_cols_static(dfTb, getFields)  
            return  dfTb 






    def read_table_auto_sql_to_df_mysql_spps(self, tb, getFields = ['*']):
        """
        SqlitePandasProcessorSpeedup
        Считывает всю таблицу в фрейм с выбором необходимых колонок в выборке для MySql
        getFields - список выводимых колонок. По умолчанию выводятся все колонки
        """
        # Считывание таблицы bonds_archive в фрейм
        sql = f'SELECT * FROM {tb}'
        # print(sql + '  | read_table_by_sql_to_df_pandas() | noocube/sqlite_pandas_processor.py')
        dfTb = self.read_sql_to_df_pandas_mysql_spps(sql)  
        if '*' in getFields: # если запрашиваются все колонки
            return dfTb
        else : # если выборка колонко
            dfTb = PandasManager.get_sub_df_with_given_cols_static(dfTb, getFields)  
            return  dfTb 





    
    ##### END EXECUTE SQL METHODS ------------


    ##### SELECT 

    def select_full_tb_df_by_name_pandas_spps(self, tbName):
        """Получитиь полную выборку таблицы по ее имни в БД"""
        sql = f"SELECT * FROM {tbName}"
        tbDF = self.read_sql_to_df_pandas_SPPS(sql)
        return tbDF
    
    
    
    
    def update_from_df_by_key_col_pandas_spps (self, tb, df, keyColName):
        """ SqlitePandasProcessor
        Обновление значений в таблице tb БД на основе данных в dataFrame
        Фрейм должен содержать только те колонки, которые будут обновляться в таблице БД и колонку ключа
        keyColName - название ключевой колонки-поля в фрейме и БД  (дожны соотвтетсвовать друг другу, то есть - одинаковы по названию)
        """
        for index, row in df.iterrows():
            uniqueKeyVal = [keyColName,row[keyColName]] # Формирование Ключа идентификации ряда в таблице с названием поля ключа и его значением
            fieldsVals = {} # Словарь с ключами в виде названий полей и значениями в виде величин для этих полей для обновления в таблице
            # Формирования текущих параметров fieldsVals по циклу с названиями полей, Кроме ключевого
            for column in df:
                if column != keyColName: # Исключаем ключевое поле
                    fieldsVals[column] = row[column] 
            self.sps.update_row_in_tb_sps(tb, fieldsVals, uniqueKeyVal) # Обновление ряда в таблице с ключем uniqueKeyVal на основе текущего по циклу ряда фрейма

    
    
    
    
    
    def select_rows_from_data_source_by_values_source_pandas_spps (self, dsBase, dsKeys, dicKeysAssoc = {}, getFields = ['*']):
        """Получение рядов из базового DS dsBase на основе заданного списка ключей dsKeys. 
        dsBase - базовый источник данных (может быть фрейм или название таблицы)
        dsKeys - источник данных с значениями ключей (может быть простой список или фрейм. Если задается таблица или фрейм как источник ключей, то обязательно должен 
        задаваться название колонки в этом источнике для выделения велечин этих ключей из колонки из этих источников)
        dicKeysAssoc - словарь соответствия названия ключа в базе(key) и названия колонки (val) ключей в dsKeys {поле в базовом фрейме : поле в фрейме ключей фильтрации}.
        Если передается простой список ключей, то в dicKeysAssoc должен стоять ключ - название поля ключа dsBase, а величина по ключу может быть любой и неважна
        """
        # Ключи для базового фрейма и соответтсвующий ключ для таблицы для списка ключевых значений для фильтрации , если они беруться из таблиы(если название таблица задана в параметре dsKeys)
        keyBase = list(dicKeysAssoc.keys())[0] # Ключ для базового источника данных
        # keyKeysFrame = list(dicKeysAssoc)[0] # название ключа-колонки в фрейме с ключевыми значениями для фильтрации  !!! PREVIOUS
        keyKeysFrame = list(dicKeysAssoc.values())[0] # название ключа-колонки в фрейме с ключевыми значениями для фильтрации

        # Анализ источников данных и ключей и формирование параметров для филльтрационной функции в зависимости от типа источника  
        if type(dsKeys) == list: # Если источник ключевых значений - простой список
            # keyBase = list(dicKeysAssoc.keys())[0] # названия поля-ключа в dsBase
            listKeysInp = dsKeys # простой список значений для фильтрации
        else: # Если источник ключей - фрейм
            listKeysInp = PandasManager.convert_df_to_list_static( dsKeys, keyKeysFrame) # простой список значений для фильтрации

        # Анализ источника бызовых данных
        if type(dsBase) == str: # Если истоыник ключей - таблица БД с заданным названием колонки-ключа в dicKeysAssoc (величина элемента словаря
            dfBaseInp = self.read_table_by_sql_to_df_pandas_SPPS(dsBase, getFields) # Формирование фрейма на основе названия таблицы в БД и выводимых заданных полей getFields
            # dfBaseInp = dfBaseInp[getFields] PREVIOUS был включен
        else: # Если источник ключей - фрейм
            dfBaseInp = dsBase

        # Получение ссылок по списку ИНН listInn из табл comps_descr
        # Pars:
        logicOper = '|' # Логический оператор AND, для обьединения в логическое И всех частных выражений в query
        kwargs = {keyBase: listKeysInp} # okpo в **kwargs - имя равное названию поля, по которому производится фиьтрация значений по списку listForFilter.  
        qrOper =   '=='    
        dfRes = PandasManager.filter_df_by_multiple_cols_vals_static (dfBaseInp, qrOper, logicOper, **kwargs)

        return dfRes



    
    
    

    ##### END SELECT 
    
    ##### EXECUTE INSERT SQL METHODS ------------
    
    
    
    
    def insert_df_to_tb_no_key_check_pandas_spps(self, df, tb, colsList=['*']):
        """Вставить данные из фрейма в таблицу с возможностью настроить колонки для ввода и с проверкой ключей на уникальность (ряды с неуникальными ключами по сравнению фрейма с 
        таблице - удаляются ряды с неуникалльными рядвами из фрейма)
        Названия колонок в конечном df должно соответствовать названию полей в таблице , в которую будут вставлятся данные
        Если colsList = ['*'] , то идет копирование полногофрейма в таблицу. Поля и колонки должны полностью соответствовать. Поля талицы должны содержать в себе подмножество колонок фрейма
        keyTb - ключ в таблице БД
        https://www.geeksforgeeks.org/how-to-insert-a-pandas-dataframe-to-an-existing-postgresql-table/
        """
        if '*' in colsList : # Значит все колонки
            # tuples = [x  for x in df['x_str']]
            listColumns = PandasManager.get_df_cols_names_list(df) # Все колонки фрейма 
            tuples = df.apply(tuple, axis=1) # Получение значений df в виде тапла тпалов (??) по оси axis=1 (по горизонтали)
            # tuples = [tuple(x) for x in df.to_numpy()]
            # if DEBUG_ :
            print(f"PR_NC_225 --> tuples = {tuples}")
            cols = ','.join(list(df.columns))
            valsQuest = ['?' for  i in range(len(listColumns))] # Массив вопросов для VALUE(?,?) для исполнения cur.executemany(sql , tuples) 
            vals = ','.join(valsQuest)
        else: # или колонки по входному списку colsList
            subDF = PandasManager.get_sub_df_with_given_cols_static(df, colsList)
            # tuples = [tuple(x) for x in subDF.to_numpy()]
            tuples = subDF.apply(tuple, axis=1)
            # print(tuples)
            cols = ','.join(colsList)
            valsQuest = ['?' for  i in range(len(colsList))] # Формирование '?' для SQL , которые потом будут замещаться величиноами при множественной вставке cur.executemany(sql , tuples)
            vals = ','.join(valsQuest)
        
        sql = "INSERT INTO %s(%s) VALUES ( %s )" % (tb, cols, vals)
        
        print (f"PR_NC_222 --> sql = {sql}")
            
        
        cur = self.db_connection.cursor()
        cur.executemany(sql , tuples) # цикл втавок формируемых sql на основе множества tuples (? заменяются значениями из tuples)
        # sleep(.5)
        self.db_connection.commit()
        cur.close()
    
    

    
    




    def insert_df_to_tb_pandas_spps(self, df, tb, colsList, keyTb, db='sqlite'):
        """Вставить данные из фрейма в таблицу с возможностью настроить колонки для ввода и с проверкой ключей на уникальность (ряды фрейма для втавки в таблицу, включевом поле которых
        обнаружены значения , которые уже есть в таблице - удаляются из фрейма и поэтому не будут вставлены в таблицу. Таким образом происходит контроль над возможной вставкой
        неуникального ключа. Запсии в таблице по таким ключам сохраняются прежней, обновления не происходит)
        Названия колонок в конечном df должно соответствовать названию полей в таблице , в которую будут вставлятся данные
        Если colsList = ['*'] , то идет копирование полногофрейма в таблицу. Поля и колонки должны полностью соответствовать. Поля талицы должны содержать в себе подмножество колонок фрейма
        keyTb - ключ в таблице БД
        https://www.geeksforgeeks.org/how-to-insert-a-pandas-dataframe-to-an-existing-postgresql-table/
        """

        # Проверить на уникальность ключи из df в применении к лючам таблицы БД. Если ключ не уникален и уже существует в 
        # таблице tb , то удалить эти ряды из df

        # 1. Получить фрейм ключей keyTb из таблицы -цели tb
        getFields =  [keyTb]
        
        if db=='sqlite':
            dfKeysTb = self.read_table_by_sql_to_df_pandas_SPPS(tb, getFields)
        else:
            dfKeysTb = self.read_table_auto_sql_to_df_mysql_spps(tb, getFields)
            
            
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfKeysTb,True,colsIndxed=True,marker="PR_NC_223 --> df")

        # 2. Удалить из df ряды с ключами из dfKeysTb, если они есть
        keyColAssocDic = {keyTb : keyTb}
        dfUbique = PandasManager.drop_rows_from_df_by_ds_keys_pandas_static (df, dfKeysTb, keyColAssocDic ) # фрейм с уникальными ключами только


        # listColumns = self.get_df_cols_names_list(dfUbique)
        # if DEBUG_ :
        #     print (f"dfColumns = {listColumns}")
        #     print (f"dfColumns_N = {len(listColumns)}")

        if '*' in colsList : # Значит все колонки
            # tuples = [x  for x in df['x_str']]
            listColumns = PandasManager.get_df_cols_names_list(dfUbique) # Все колонки фрейма
            tuples = dfUbique.apply(tuple, axis=1) # Получение значений df в виде тапла тпалов (??) по оси axis=1 (по горизонтали)
            # tuples = [tuple(x) for x in df.to_numpy()]

            cols = ','.join(list(dfUbique.columns))
            valsQuest = ['?' for  i in range(len(listColumns))] # Массив вопросов для VALUE(?,?) для исполнения cur.executemany(sql , tuples) 
            vals = ','.join(valsQuest)
            # print (f"vals = {vals}")

        else: # или колонки по входному списку colsList
            subDF = PandasManager.get_sub_df_with_given_cols_static(dfUbique, colsList)
            # tuples = [tuple(x) for x in subDF.to_numpy()]
            tuples = subDF.apply(tuple, axis=1)
            # print(tuples)
            cols = ','.join(colsList)
            valsQuest = ['?' for  i in range(len(colsList))] # Формирование '?' для SQL , которые потом будут замещаться величиноами при множественной вставке cur.executemany(sql , tuples)
            vals = ','.join(valsQuest)

        sql = "INSERT INTO %s(%s) VALUES ( %s )" % (tb, cols, vals)

        cur = self.db_connection.cursor()
        cur.executemany(sql , tuples) # цикл втавок формируемых sql на основе множества tuples (? заменяются значениями из tuples)
        # sleep(.5)
        self.db_connection.commit()
        cur.close()






    
    
    def insert_df_to_tb_no_key_check_simple_pandas_spps(self, df, tb, colsList=['*']):
        """ 
        df to db mysql table
        colsList -  не проработано
        simple - значит вставка по циклу по фрейму
        """
        
        for index, row in df.iterrows():
            
            fieldsVals = {} # Словарь с ключами в виде названий полей и значениями в виде величин для этих полей для обновления в таблице
            # Формирования текущих параметров fieldsVals по циклу с названиями полей, Кроме ключевого
            for column in df:
                # if column != keyColName: # Исключаем ключевое поле
                fieldsVals[column] = row[column] 

            self.sps.insert_row_into_table_sps (tb, fieldsVals)
                
            

    




    def insert_or_update_df_to_tb_by_given_simple_key_spps(self, df, tb, keyColName):
        """ 
        Вставить или обновить данные таблицы  на основе фрейма с проверкой наличия записей по простому (моно) ключу
        Если запись есть, то проводится обновления ряда таблицы по найденному значению ключа рядом из фрейма с этим же значением по ключевому полю
        Если записи нет, то проводится вставка строки на осное ряда фрейма , ключ которого уэе проерен в таблице
        ПРИМ: Моножество названий колонок фрейма должно быть подмножеством названий полей таблицы.  
        И сохраняем в БД
        """
        
        for index, row in df.iterrows():
            
            uniqueKeyVal = [keyColName,row[keyColName]] # Формирование Ключа идентификации ряда в таблице с названием поля ключа и его значением
            fieldsVals = {} # Словарь с ключами в виде названий полей и значениями в виде величин для этих полей для обновления в таблице
            # Формирования текущих параметров fieldsVals по циклу с названиями полей, Кроме ключевого
            for column in df:
                # if column != keyColName: # Исключаем ключевое поле
                fieldsVals[column] = row[column] 
                        
            # Проверяем сначала наличие записи с ключем , используя запрос
            sql = f"SELECT * FROM {tb} WHERE {keyColName}='{row[keyColName]}'"
            if self.sps.if_select_result_exists_sps(sql): # Если ответ есть, значит запись с ИСИН уже есть и значит делаем UPDATE записи
                print(f"PR_917 --> SYS: Запись {keyColName} = {row[keyColName]} существует в таблице {tb}. Делаем UPDATE")
                # Удалить ключевое поле в словаре, так как при UPDATE  оно нужно лишь для идентификуации записи для изменения. Сам ключ не меняется
                del fieldsVals[keyColName]
                
                self.sps.update_row_in_tb_sps(tb, fieldsVals, uniqueKeyVal) # Обновление ряда в таблице с ключем uniqueKeyVal на основе текущего по циклу ряда фрейма
            
            else: # если записи нет. то делаем INSERT
                print(f"PR_918 --> SYS: Записи с {keyColName} = {row[keyColName]} нет в таблице {tb}. Делаем INSERT")
                self.sps.insert_row_into_table_sps (tb, fieldsVals)
                
            

        
    def insert_or_update_df_to_tb_by_given_composite_key_spps(self, df, tb, keyColsNames):
        """ 
        Вставить или обновить данные таблицы  на основе фрейма с проверкой наличия записей по составному ключу
        Если запись есть, то проводится обновления ряда таблицы по найденному значению ключа рядом из фрейма с этим же значением по ключевому полю
        Если записи нет, то проводится вставка строки на осное ряда фрейма , ключ которого уэе проерен в таблице
        ПРИМ: Моножество названий колонок фрейма должно быть подмножеством названий полей таблицы.  
        И сохраняем в БД
        keyColsNames - название полей композитного ключа в виде списка
        """
        
        for index, row in df.iterrows():
            
            # uniqueKeyVal = [keyColName,row[keyColName]] # Формирование Ключа идентификации ряда в таблице с названием поля ключа и его значением
            fieldsVals = {} # Словарь с ключами в виде названий полей и значениями в виде величин для этих полей для обновления в таблице
            # Формирования текущих параметров fieldsVals по циклу с названиями полей, Кроме ключевого
            for column in df:
                # if column != keyColName: # Исключаем ключевое поле
                fieldsVals[column] = row[column] 
                        
            print(f"PR_929 --> fieldsVals = {fieldsVals}")
                        
            # Формирууем значения для множественного условия WHERE по композитному ключу keyColsNames
            whereStr = ''
            uniqueCompositeKeysVals = {}
            for keyField in keyColsNames:
                
                if isinstance(row[keyField], str):  # если str, то заключить значение в кавычки одноразовые
                    value = f"'{row[keyField]}'" # Значение уникального поля, по которому формируется условие WHERE
                    
                whereStr += f"{keyField} = {value} AND "
                
                # Формирование словаря с ключами и их значениями для составного уникального ключа
                uniqueCompositeKeysVals[keyField] = row[keyField]
                
                
            whereStr = whereStr.rstrip('AND ')
                        
            # Проверяем сначала наличие записи с композитным ключем , используя запрос
            sql = f"SELECT * FROM {tb} WHERE {whereStr}"
            
            print(f"PR_926 --> sql = {sql}")
            
            
            
            if self.sps.if_select_result_exists_sps(sql): # Если ответ есть, значит запись с ИСИН уже есть и значит делаем UPDATE записи
                # print(f"PR_917 --> SYS: Запись {keyColName} = {row[keyColName]} существует в таблице {tb}. Делаем UPDATE")
                # Удалить ключевое поле в словаре, так как при UPDATE  оно нужно лишь для идентификуации записи для изменения. Сам ключ не меняется
                # del fieldsVals[keyColName]
                
                self.sps.update_row_in_tb_by_composite_key_sps(tb, fieldsVals, uniqueCompositeKeysVals) # Обновление ряда в таблице с ключем uniqueKeyVal на основе текущего по циклу ряда фрейма
            
            else: # если записи нет. то делаем INSERT
                # print(f"PR_918 --> SYS: Записи с {keyColName} = {row[keyColName]} нет в таблице {tb}. Делаем INSERT")
                self.sps.insert_row_into_table_sps (tb, fieldsVals)
                
            


        
        







    ##### END EXECUTE INSERT SQL METHODS ------------


    
    ##### КОМПЛЕКСНЫЕ МЕТОДЫ ------------
    
    
    def fill_table_from_another_table_spps(self, tbSource, tbTarget, fieldsAssocDic = {},  keyFieldAssoc = {}, ifClearTb = False, colsList = ['*']):
        """Заполнить таблицу-цель данными из таблицы источника
        fieldsAssocDic - словарь соответствий полей таблиц. По умолчанию словарь не задан и это значит, что названия полей в фрейме, предназначенном  для вставки,
        должны иметь полное совпадение у обоих таблиц
        keyFieldAssoc - словарь соответствий ключей. Если ключи не заданы, то проверка по уникальности по ключам отсутствует. По умолчанию - отсутствует проверка.
                        Если не задан, то значит все поля идентичны, если задан, то необходимо переименовать в inseart-фрейме те поля, которые указаны в словаре keyFieldAssoc,
                        остальные остаются и должны быть равными
        ifClearTb - флаг отчистки таблицы перед наполнением. Если - True, то перед наполнением производится полная очистка таблицы от всех данных. По умолчанию - False
        colList - список колонок таблицы-цели, которые необходимо заполнить из базовой таблицы. Если поля полностью соответствуют, то спсиок соответствий не создается для этих полей.
        """
        # Очистка таблицы , если установлен флаг очистки
        if ifClearTb: # Если флаг очистки таблицы - True - очищаем таблицу цель
            # Отчистиить виртуальную таблицу
            self.sps.clear_table_sps (tbTarget)
        # Считать данные из таблицы comps_descr (БД: bonds) в фрейм
        dfTbSource = self.read_table_by_sql_to_df_pandas_SPPS(tbSource)
        # Анализ списка полей colsList для заполнения (отсев ненужных колонок)
        if len(colsList) < 1 or '*' in colsList: # Значит задан параметр для вывода и заполнения по всем колонкам
            pass # Не удалять pass
        elif len(colsList) > 0 and '*' not in colsList: # Значит задан параметр , ограничивающий полное множество колонок и фрейм должен быть усечен только на допустимые поля
            dfTbSource = dfTbSource[colsList]
            if ms.DEBUG_:
                print (f"PR_132 --->  type of dfCompsDescr = {str(type(dfTbSource))}")
        # Анализ словаря соответствий полей таблиц. Если не задан, то значит все поля идентичны, если задан, то необходимо переименовать в inseart-фрейме те поля, которые указаны в словаре
        fieldsAssocDic_N = len(fieldsAssocDic)
        if fieldsAssocDic_N > 0: # Если есть элементы в словаре, то надо переименовать поля insert-фрейма dfCompsDescr в соотвтетсвии с ними. Если нет, то ничего переименовывать не надо
            # Переименовать поля фрейма в соотвтесвии со словарем соответствий источника и цели
            dfTbSource = PandasManager.rename_cols_by_associate_dic_pandas_static (self, dfTbSource, fieldsAssocDic, False) # False - значит создается копия фрейма с измененными названиями колонок
        keyAssocN = len(keyFieldAssoc) # количество задаваемых ключей проверки на уникальность
        if keyAssocN > 0: # Значит задан как минимум один ключ для проверки уникальности
            # Наполнить виртуалльную таблицу данными из фрейма dfCompsDescr
            keyTb = list(keyFieldAssoc.values())[0] # Ключ для целевой таблицы
            self.insert_df_to_tb_pandas_spps(dfTbSource, tbTarget, colsList, keyTb)
        else: # Если не заданы ключи для проверки уникальности, то не проверяем их
            # Наполнить виртуалльную таблицу данными из фрейма dfCompsDescr
            # keyTb = list(keyFieldAssoc.values())[0] # Ключ для целевой таблицы
            self.insert_df_to_tb_no_key_check_pandas_spps(dfTbSource, tbTarget, colsList)

    
    
    def copy_tb_data_to_another_identical_tb_spps(self, tbSrc, tbTrg):
        "Скопировать данные из одной таблицы в другую идентичную по структуре"
        self.fill_table_from_another_table_spps(tbSrc, tbTrg, fieldsAssocDic = {},  keyFieldAssoc = {}, ifClearTb = False, colsList = ['*'])




    def copy_tb_data_to_another_identical_cleared_tb_sps(self, tbSrc, tbTrg):
        """
        OBSOLETED: название изменено. _sps на _spps ниже
        Скопировать данные из одной таблицы в другую идентичную по структуре с предварительной очисткой целевой таблицы
        """

        # Очищаем табл bonds_curr_prev
        # pandas_db_proc = SqlitePandasProcessor(DB_BONDS_)
        self.sps.clear_table_sps(tbTrg)

        # Копируем данные из табл bonds_curr в табл bonds_curr_prev
        self.copy_tb_data_to_another_identical_tb_spps(tbSrc, tbTrg)
        
        
        

    # def copy_tb_data_to_another_identical_cleared_tb_spps(self, tbSrc, tbTrg):
    #     """
    #     Скопировать данные из одной таблицы в другую идентичную по структуре с предварительной очисткой целевой таблицы
    #     Прим: аналог метода copy_tb_data_to_another_identical_cleared_tb_sps(), устаревшего из-а названия
    #     TODO: Перенести методв в класс SqliteProcessorSpeedup, так как он не свзяан с фреймами, а так же все методв внутри него изменить и перенести
    #     """

    #     # Очищаем табл bonds_curr_prev
    #     # pandas_db_proc = SqlitePandasProcessor(DB_BONDS_)
    #     self.sps.clear_table_sps(tbTrg)

    #     # Копируем данные из табл bonds_curr в табл bonds_curr_prev
    #     self.copy_tb_data_to_another_identical_tb_spps(tbSrc, tbTrg)
        
        
        
        
        
        
        
        
        
        
    def copy_tb_data_to_another_identical_cleared_tb_spps(self, tbSrc, tbTrg):
        """
        Скопировать данные из одной таблицы в другую идентичную по структуре с предварительной очисткой целевой таблицы
        """

        # Очищаем табл bonds_curr_prev
        self.sps.clear_table_sps(tbTrg)

        # Копируем данные из табл bonds_curr в табл bonds_curr_prev
        self.copy_tb_data_to_another_identical_tb_spps(tbSrc, tbTrg)
        
        
        
        
        
    def set_const_marker_in_table_by_keys_spps(self, df, tb, keyColAssocDic, tbFieldConstDic):
        """ 
        
        OBSOLETED: Идентична update_const_vals_with_key_col_in_df_pandas_spps. Просто изменено название иногда более понятное по смыслу
        Проставить маркер в колонке таблице по заданынм ключам
        ПР Pars
        keyColAssocDic = {'dfKeyColName' : 'tbKeyField'}
        tbFieldConstDic = {'tbConstFieldName' : 'constValue'}
        """
        # Расшифровка параметров
        dfKeyColName = list(keyColAssocDic.keys())[0] # название колонки фрейма, где хранятся ключи
        tbKeyField = keyColAssocDic[dfKeyColName] # Название поля таблицы, с которым будет проводится сверка ключей dfKeyColName
        tbConstFieldName = list(tbFieldConstDic.keys())[0] # название поля в таблице, в котором будут проставлятся значения константы 
        constVal = tbFieldConstDic[tbConstFieldName] # Значение константы

        # Формирования текущих параметров  fieldsVals по циклу для функции update

        fieldsVals = {} # Словарь с ключами в виде названий полей и значениями в виде величин для этих полей для обновления в таблице  Пр: {'okpo' : constVal, 'sector' : constVal}
        fieldsVals[tbConstFieldName] = constVal # Этот параметр для Update в данной функции всегда постоянен, так как проставляются одинаковые константы везде

        for index, row in df.iterrows():
            uniqueKeyVal = [tbKeyField,row[dfKeyColName]] # Формирование Ключа идентификации ряда в таблице и его значением из фрейма для функции update  Пр: ['inn','2128702350']
            self.sps.update_row_in_tb_sps(tb, fieldsVals, uniqueKeyVal) # Обновление ряда в таблице с ключем uniqueKeyVal на основе текущего по циклу ряда фрейма

        
        
        
        
        
    def update_const_vals_with_key_col_in_df_pandas_spps(self, df, tb, keyColAssocDic, tbFieldConstDic):
        """ 
        
        Обновить константами поля в таблице на базе ключей из колонки dataFrame
        df - фрейм, с колонокой ключей, по которым находядся записи в таблице, в которых будет проставлено значение константы
        keyColAssocDic - словарь, с ключем в виде названия колонки фрейма с индексами и названием поля-ключа таблицы в виде соотвтетсвенного
        значения словаря по ключу {'dfKeyColName' : 'tbKeyField'}
        tbFieldConstDic - словарь с ключем , в котором хранится название поля таблицы в который будут проставлятся константа , находящаяся 
        в значении словаря {'tbConstFieldName' : 'constValue'}
        ПР Pars
        keyColAssocDic = {'isin' : 'isin'}
        tbFieldConstDic = {'moex' : 'FILEED'}
        """

        # Расшифровка параметров
        dfKeyColName = list(keyColAssocDic.keys())[0] # название колонки фрейма, где хранятся ключи
        tbKeyField = keyColAssocDic[dfKeyColName] # Название поля таблицы, с которым будет проводится сверка ключей dfKeyColName
        tbConstFieldName = list(tbFieldConstDic.keys())[0] # название поля в таблице, в котором будут проставлятся значения константы 
        constVal = tbFieldConstDic[tbConstFieldName] # Значение константы

        # Формирования текущих параметров  fieldsVals по циклу для функции update

        fieldsVals = {} # Словарь с ключами в виде названий полей и значениями в виде величин для этих полей для обновления в таблице  Пр: {'okpo' : constVal, 'sector' : constVal}
        fieldsVals[tbConstFieldName] = constVal # Этот параметр для Update в данной функции всегда постоянен, так как проставляются одинаковые константы везде

        for index, row in df.iterrows():
            uniqueKeyVal = [tbKeyField,row[dfKeyColName]] # Формирование Ключа идентификации ряда в таблице и его значением из фрейма для функции update  Пр: ['inn','2128702350']
            self.sps.update_row_in_tb_sps(tb, fieldsVals, uniqueKeyVal) # Обновление ряда в таблице с ключем uniqueKeyVal на основе текущего по циклу ряда фрейма



        
        
        
        
        
        
    def get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas_spps(self, baseSource, compairSource, assocColsInxDic, getCols= ['*']):
        """ЗАГОТОВКА. 
        baseSource, compairSource - источник данных. Либо сам фрейм, либо название таблицы БД для создания фрейма тут
        Реаkизовать с использованием метода PandasManager.filter_df_by_multiple_cols_vals по шаблону в алгоритме AlgorithmsCalc.a022_update_bonds_archive_and_current_on_base_of_table_comps
        Получить выборку (суб-фрейм) из базового фрейма, ряды которой не принадлежат множеству второго сравниваемого фрейма по величинам заданных ключевых колонок
        assocColsInxDic - словарь сопоставлений полей базового (как ключи) и полей (как значения словаря) сравниваемого фреймов, по совокупности которых идет сравнение и фильтрация в соответствующих фреймах
        (то есть, выборка из базового класса вернет те ряды, которые по значениям в этой совокупности задаваемых колонок и их ассоциаций во втором фрейме не будет присутствовать в стравниваемом фрейме)
        getCols - набор колонок из базового фрейма для результирующего возвращаемого массива 
        !!! Базовым является тот фрейм, в котором есть ряды, значения по индексу-ключу комплексных или пройстой колонок которых нет в стравнительном фрейме
        по тому же комплексному или простому индексу-ключу  и в который (в сравнительный) предположительно эти данные отсутствующие предполагаются
        быть внесенными
        """
        # Анализ  источника базовых данных и создание фрейма, если этот источник задан в виде названия таблицы
        if type(baseSource) == str: # если базовый источник задан названием таблицы
            baseDF = self.read_table_by_sql_to_df_pandas_SPPS(baseSource)
        else:
            baseDF = baseSource

        # Анализ  источника базовых данных и создание фрейма, если этот источник задан в виде названия таблицы
        if type(compairSource) == str: # если базовый источник задан названием таблицы
            compairDF = self.read_table_by_sql_to_df_pandas_SPPS(compairSource)
        else:
            compairDF = compairSource


        qrOper = 'not in' # Оператор сравнения 'не равно', то есть ищутся неравные задаваемым величинам значения в колонках
        logicOper = '&' # Логический оператор AND, для обьединения в логическое И всех частных выражений в query
        # Формирование именных параметров, которые включают в себя именные списки с выборками-векторами по заданным колонкам в комплексном или простом индексе
        #  входного параметра assocColsInxDic из сравниельного фрейма compairDF
        print(f"PR_352 --> baseDF = {baseDF}/ (SqlitePandasProcessor.get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas)")
        print(f"PR_353 --> compairDF = {compairDF}/ (SqlitePandasProcessor.get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas)")
        
        kwargs = {} # словарь для именных параметров для функции филльтрации
        for key, val in assocColsInxDic.items(): # цикл по колонкам в составном индексе колонок assocColsInxDic
            colValsList = PandasManager.convert_df_col_to_list_pm_static(compairDF, val) # получение колокнки-ветора с названием текущего по циклу val во фрейме compairDF в виде простого списка значений (эти значения из списка будут отсеиваться в базовом фрейме по соответствующей колонке с названием текущего ключа key)
            kwargs[key] = colValsList # вставка текущего по циклу именного параметра в словрь kwargs

        dfBaseFiltered = PandasManager.filter_df_by_multiple_cols_vals_static(baseDF, qrOper, logicOper, **kwargs)  #  Базовый фрейм, отфильтрованный по значениям колонок из compairDF совокупного индекса колонок

        # print(f"dfBaseFiltered = {dfBaseFiltered} / (SqlitePandasProcessor.get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas)")

        if '*' in getCols: # То выводятся все колонки
            dfRes =  dfBaseFiltered
        else:
            # !!! CHANGED: WAS return dfBaseFiltered[[getCols]] !!!
            # TODO: Сделать вывод любых колонок по отфидбьолванным ключам из основного базового фрейма
            dfRes =  dfBaseFiltered[getCols] # Иначе вводятся запрашиваемые в списке getCols колонки
            if 'Series' in str(type(dfRes)):
                dfRes = PandasManager.convert_series_to_df_pandas_static(dfRes)

        return dfRes

        
        
        
        
        
    def drop_duplicates_from_table_by_col_spps(self, tb, colSubsetList, tbKey, keepFg = 'last'):
        """
        SqlitePandasProcessor
        Удалить дупликаты в таблице по поиску в одной задаваемой колонке (не наборе колонок)
        colNamesList - набор названий колонок в таблице БД, по ключу которых проверяется дубликаты
        keepFg - настройка, какая запись из дубликатов не удаляется. По умолчанию не удаляется последний из дубликатов
        RET: Возвращает фрейм с дубликатами, которые были удалены, за исключением последнего из дубликатов (тоже можно настроить последний или первый оставляется)
        """
        
        dfTb = self.sps.read_table_to_df_pandas_sps(tb)
        # Выявить дубликаты по значению колонки x_str, в которой к хранятся ИНН
        dfDuplic = PandasManager.get_duplicated_rows_of_column_static (dfTb, colSubsetList)
        if ms.DEBUG_:
            print (f"PR_217 --> dfDuplic = {dfDuplic} / pr: SqlitePandasProcessor.drop_duplicates_from_table_by_cols")\
        
        if len(dfDuplic) > 0: # Если найдены дубликаты
            print(f"PR_218 --> INFO: Найдены дупликаты в таблице {tb} по индексу {colSubsetList}, который должен быть укникальным  и которые будут удалены / SqlitePandasProcessor.drop_duplicates_from_table_by_cols")
            dfTb = PandasManager.drop_duplicates_by_columns_pandas_static (dfTb, colSubsetList, keepFg)
            # Удаляем дупликаты из таблицы(двуступенчатым способомыЫ):
            # 1. очищаем таблицу в БД полностью от всех данных
            self.sps.delete_from_table_with_where_condition_sps(tb, {}) 
            # 2. Вставляем в таблицу данные из фрейма, очищенного от дубликатов
            self.insert_df_to_tb_pandas_spps( dfTb, tb, ['*'], tbKey) 

        else:
            print(f"PR_219 --> INFO: Дупликаты в таблице {tb} по индексу {colSubsetList} НЕ найдены/ SqlitePandasProcessor.drop_duplicates_from_table_by_cols")


        return dfDuplic   
    

        

        
        
    def insert_consts_to_tb_by_df_keys_pandas_spps(self, df, tb, keyColFieldDic, tbFieldsValsDic):
        """
        Вставить значения констант, определенных в словаре tbFieldsValsDic, в поля колонок таблицы tb, определяемых в ключе tbFieldValDic,
        по ключам , заданным в фрейме df в колонке с названием keyCol, которое должно соответствовать , так же, названию ключей в таблице tb
        df может быть любым, главное, что бы он содержал колоку с ключами с одноименным названием с коолонкой в таблице БД. И чтобы названия полей в tbFieldsValsDic
        , в которые будут добавляться константы, тоже были одноименными с таблице в БД
        Кроме того, ключи в df не могут содержать уже существующих в таблице БД, иначе - ошибка. Пока это не реализовано в методе, эту проверку и фильтрацию необходимо 
        делать до запуска метода при подготовке параметров
        keyColFieldDic - словарь соответсттвий между названиями ключей в фрейме и таблицы БД
        ПР параметров:
        tbFieldsValsDic = {
            'moex' : 'FILEED',
            'f1' : 'TEST'
            }
        """
        keyCol = list(keyColFieldDic)[0]
        keyTb = list(keyColFieldDic.values())[0]
        # Получаем фрейм из однйо колонки с ключами
        dfKeys = PandasManager.get_sub_df_with_given_cols_static(df, [keyCol]) 
        # Удаляем возможные пустоты
        dfKeys = PandasManager.filter_df_from_empties_or_any_vals_by_columns_static (dfKeys, [keyCol], ['', ' ', None])
        # Удаляем возможные дубликаты ключей
        dfKeys = PandasManager.drop_duplicates_by_columns_pandas_static (dfKeys, [keyCol])
        # Формируем df с дополнительными колонками констант, задаваемых в tbFieldsValsDic с названиями колонок, соответствующим названию ключей словаря
        PandasManager.add_df_cols_with_constants_pandas_static(dfKeys,  tbFieldsValsDic)
        # Вставляем константы в заданные поля для них по заданным ключам в колонке фрейма keyCol
        
        self.insert_df_to_tb_pandas_spps(dfKeys, tb, ['*'], keyTb)


        
        
        
        
    def check_duplicated_data_in_db_table_with_given_key_fields_spps (self, tb, keyFields):
        """ 
        ПРИМ: Должно работать , но не проверено на 100%
        Найти дублирующие записи в таблице БД по заданным полям ключа
        keyFields - список полей, по котоырм надо проверить дублирующие значения в таблице
        """
        
        sql = f"SELECT {','.join(keyFields)} FROM {tb}"
        
        df = spps.read_sql_to_df_pandas_SPPS(sql)
        
        dfTbFieldsDuplicated = PandasManager.get_duplicated_rows_of_column_static(df, keyFields)
        
        print(f"PR_908 --> dfTbFieldsDuplicated = \n{dfTbFieldsDuplicated}")
        
        return dfTbFieldsDuplicated
            
            
        
        
        
        
        
    def if_value_exists_in_tb_given_column_auto_sql_df_spps (self, tb, colGiven, colVal):
        """ 
        Проверить в таблице в задаваемой колонке наличие искомого значения
        """
        
        df = self.read_table_auto_sql_to_df_mysql_spps (tb)
        
        return PandasManager.if_value_exists_in_df_column_values_static(df, colGiven , colVal)
        
        
        
        
    def check_if_value_exists_in_tb_given_col_and_return_key_val_auto_sql_df_spps (self, tb, colGiven, colVal, colReturn):
        """ 
        Проверить в таблице в задаваемой колонке наличие искомого значения. Вернуть флаг наличия и значение по заданной ключевой колонке для возврата значения
        colGiven - заданная колонка для поиска значения
        colVal - искомое значчение
        colReturn - колонка, знаение которой надо вренуть при нахождении значения

        """
        # Автоматическое создание sql по названию таблицы и на его основе уже создать df
        df = self.read_table_auto_sql_to_df_mysql_spps (tb)
        
        ifExist = PandasManager.if_value_exists_in_df_column_values_static(df, colGiven , colVal)
        
        if ifExist:
            retKeyVal = PandasManager.get_val_of_column_cell_by_val_of_key_column_stat_pandas(df, colGiven, colVal, colReturn)
        else:
            retKeyVal = None

        return ifExist, retKeyVal
        
        
        
        
        
        
    
    ##### END КОМПЛЕКСНЫЕ МЕТОДЫ ------------
    
    ############  ВСЯКИЕ ДЛЯ СОРТИРОВКИ ---------------------------
    
    
    def read_sql_to_dic_like_group_by_spps (self, sql, colPrimeField, colValField):
        """ 
        OBSOLETED: use read_sql_to_dic_like_group_by_mysql_spps()
        Считать sql- запрос в словарь по типу GROUPED BY (с множественными значениями по primeField)
        colPrimeField - первичное поле для формирования ключей по гурппам
        colValField - поле со значениями для формирования списка значений, найденных для групповых ключей
        
        ПРИМ:  primeFields - это не ключи (ключи уникальны). А любые колонки с возможными множественными значениями и не уникальные так же могуь быть
        (источники данных могут быть по типу многие ко многим или один ко многим)
        
        RET: словарь типа 
        {
            colPrimeFieldValue : [valuesOfColValField],
            ...
        }
        """
        
        dfSql = self.read_sql_to_df_pandas_mysql_spps(sql)
        
        # print(f"PR_NC_206 --> dfSql = {dfSql}")
        
        dicRes = PandasManager.read_df_col_as_list_to_diсtionary_by_col_prime (dfSql, colPrimeField, colValField)
        
        return dicRes
    
    
    
    def read_sql_to_dic_like_group_by_mysql_spps (self, sql, colPrimeField, colValField):
        """ 
        Считать sql- запрос в словарь по типу GROUPED BY (с множественными значениями по primeField)
        colPrimeField - первичное поле для формирования ключей по гурппам
        colValField - поле со значениями для формирования списка значений, найденных для групповых ключей
        
        ПРИМ:  primeFields - это не ключи (ключи уникальны). А любые колонки с возможными множественными значениями и не уникальные так же могуь быть
        (источники данных могут быть по типу многие ко многим или один ко многим)
        
        RET: словарь типа 
        {
            colPrimeFieldValue : [valuesOfColValField],
            ...
        }
        """
        
        dfSql = self.read_sql_to_df_pandas_mysql_spps(sql)
        
        # print(f"PR_NC_206 --> dfSql = {dfSql}")
        
        dicRes = PandasManager.read_df_col_as_list_to_diсtionary_by_col_prime (dfSql, colPrimeField, colValField)
        
        return dicRes
    
    
    
    
    
    def read_sql_to_dic_like_one_to_one_tie_spps (self, sql, colPrimeField, colValField, indexDuplicated = False):
        """ 
        Считать sql- запрос в словарь по типу ONE-TO-ONE (с единственным значением искомой колонки по заданному ключу primeField)
        colPrimeField - первичное поле для формирования ключей по гурппам
        colValField - поле со значениями для формирования списка значений, найденных для групповых ключей
        
        indexDuplicated - флаг индексации дублирующих по названию полей в возврате курсора. ПО умолчанию False, нет индексации
        
        ПРИМ: Если запрос возвращает несоклько полей с одинаковым названием (допустим с названеиме 'id') и флаг indexDuplicated = True,
        то метод переименовывает их по принципу : id_1, id_2, ..., id_N
        
        ПРИМ:  primeFields - это не ключи (ключи уникальны). А любые колонки с возможными множественными значениями и не уникальные так же могуь быть
        (источники данных могут быть по типу многие ко многим или один ко многим)
        
        RET: словарь типа 
        {
            colPrimeFieldValue : valuesOfColValField,
            ...
        }
        """
        
        dfSql = self.read_sql_to_df_pandas_mysql_spps(sql)
        
        if indexDuplicated:
            # # переименования (индексации) одинаковых по названию колонок
            dfSql = PandasManager.index_duplicated_name_columns_in_df_universal(dfSql)
            
        
        # print(f"PR_NC_206 --> dfSql = {dfSql}")
        
        # Считать данные в словарь по типу один-к-одному (одному ключу словаря соотвтетсвует одно значение, asList = False)
        dicRes = PandasManager.read_df_cols_by_colPrime_as_diсtionary_for_alternative_ties (dfSql, colPrimeField, colValField, asList = False)
        
        return dicRes
    
    
    
    
    def read_table_given_row_full_data_as_dic_spps (self, tb, dicKeyVal):
        """ 
        Считать одну запись из таблицы , определяемую значением по задаваемому ключу
        dicKeyVal - словарь , определяющий ключ и значение ключа для выдедления в таблице tb
        """
        
        print(f"PR_NC_211 --> START: read_sql_with_one_row_return_to_dic_mysql_spps()")
        
        dfSql = self.read_table_auto_sql_to_df_mysql_spps(tb)
        
        fieldKey = list(dicKeyVal.keys())[0]
        keyFieldVal = dicKeyVal[fieldKey]
        # Фильтрация по значению ключа keyFieldVal  в колонке fieldKey
        dfSql = dfSql[dfSql[fieldKey]==keyFieldVal]
        
        # Считать данные в словарь по типу один-к-одному (одному ключу словаря соотвтетсвует одно значение, asList = False)
        dicRes = PandasManager.read_df_with_one_row_to_dic_stat_pm(dfSql)
        
        print(f"PR_NC_212 --> START: read_sql_with_one_row_return_to_dic_mysql_spps()")
        
        return dicRes
    
    
    
    def read_one_row_return_sql_to_dic_mysql_spps (self, oneRowReturnSql):
        """ 
        Не проверено на практике
        Считать запрос oneRowReturnSql, возвращающий только одну запись по значению в ключе из таблицы, в словарь всех значений по всем полям возварта курсора
        ПРИМ: Если запрос возвращает несоклько полей с одинаковым названием (допустим с названеиме 'id'), то метод переименовывает их 
        по принципу : id_1, id_2, ..., id_N
        """
        
        print(f"PR_NC_214 --> START: read_sql_with_one_row_return_to_dic_mysql_spps()")
        
        # sql, возвращающий только один ряд
        dfSql = self.read_sql_to_df_pandas_mysql_spps(oneRowReturnSql) 
        
        # переименования (индексации) одинаковых по названию колонок
        dfSql = PandasManager.index_duplicated_name_columns_in_df_universal(dfSql)
        
        # Считать данные в словарь по типу один-к-одному (одному ключу словаря соотвтетсвует одно значение, asList = False)
        dicRes = PandasManager.read_df_with_one_row_to_dic_stat_pm(dfSql)
        
        print(f"PR_NC_215 --> START: read_sql_with_one_row_return_to_dic_mysql_spps()")
        
        return dicRes
    
    

    
    
    
    
    
    ############  END ВСЯКИЕ ДЛЯ СОРТИРОВКИ ---------------------------
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    pass


    # # ПРОРАБОТКА: insert_or_update_df_to_tb_by_given_composite_key_spps(df, tb, keyColsNames)
    
    # tb = 'comp_bond_analisys'
    # fieldsVals = {
    #     'inn' : '5406780551', 
    #     'isin' : 'RU000A104KM0',
    #     'comp_bonds_analisys' : 'ООО "СЕЛЛ-Сервис" RU000A104KM0',
    #     'inx_pckg_decided_id' : 6,
    # }
    
    # df = PandasManager.read_df_from_dictionary_static(fieldsVals)
    
    # print(f"PR_928 --> df = \n{df}")
    
    # keyColsNames = ['inn', 'isin']
    
    # # uniqueCompositeKeysVals = {
    # #     'inn' : '5406780551', 
    # #     'isin' : 'RU000A104KM0',
    # # }
    
    
    # spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION)
    
    # spps.insert_or_update_df_to_tb_by_given_composite_key_spps(df, tb, keyColsNames)
    

    
# The above code is calling a function `update_row_in_tb_by_composite_key_sps` with three arguments:
# `tbName`, `fieldsVals`, and `uniqueCompositeKeysVals`. This function is likely used to update a row
# in a database table (`tbName`) based on a composite key (`uniqueCompositeKeysVals`). The
# `fieldsVals` argument is likely a dictionary or list of key-value pairs that represent the fields
# and their updated values for the row being updated.
    # spps.update_row_in_tb_by_composite_key_sps(tbName,  fieldsVals, uniqueCompositeKeysVals)


    # # ПРОРАБОТКА: check_duplicated_data_in_db_table_with_given_key_fields_spps()
    
    # spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION)
    
    # tb = 'inx_packgs_bonds_PREV'
    
    # keyFields = ['inx_pckg_id', 'bond_isin']
    
    # spps.check_duplicated_data_in_db_table_with_given_key_fields_spps (tb, keyFields)
    



    # КОПИРОВАНИЕ ДАННЫХ ТАБЛИЦЫ В ПОДОБНУЮ ИЗМЕНЕННУЮ
    
    # spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION)
    
    # spps.copy_tb_data_to_another_identical_cleared_tb_spps('inx_packgs_bonds_PREV', ms.TB_INX_PACKAGES_BONDS)



    # sql = f"SELECT inx_pckg_id, bond_isin FROM inx_packgs_bonds_PREV"
    
    # df = spps.read_sql_to_df_pandas_SPPS(sql)
    
    # colSubsetList = ['inx_pckg_id', 'bond_isin']
    
    # dfDuplicated = PandasManager.get_duplicated_rows_of_column_static(df, colSubsetList)
    
    # print(f"PR_908 --> dfDuplicated = {dfDuplicated}")













