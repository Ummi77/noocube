





# from asyncio import sleep
# import sqlite3

# import pysqlite3

from .settings import DB_BONDS_, DEBUG_, TB_BONDS_ARCIVE_, TB_BONDS_CURRENT_, TB_COMPS_, TB_GLOBAL_A_, TB_REG_ISIN_B_
from .sqlite_processor import SqliteProcessor

from .pandas_manager import PandasManager

from .sqlite_processor_macros import SqliteProcessorMacros
import pandas as pd

from .sql_syntaxer import SQLSyntaxer



class SqlitePandasProcessor (SqliteProcessor, PandasManager):
    """ 
    OBSOLETED: Класс устарел, так как использует неправильное подсоединение к БД, что сильно замедляет процессы. Использовать его аналог :  SqlitePandasProcessorSpeedup
    Использовать можно только статичные методы пока
    sqlite_pandas_processor.py
    Класс предназначен для реализации sql запросов в виде строки в реальной БД sqlite сиспользованием фреймов Pandas
    dbName - название БД. Если модуль класса находится не в пространстве проекта, где находится БД, то указывать полный абсолютный путь к БД

    TODO: Подумать целесообразность присоединения еще одного родителя  - PandasManager 
    """

    def __init__(self, dbName):
        SqliteProcessor.__init__(self, dbName)
        PandasManager.__init__(self)
        self.db_uri = f"sqlite:///{self.dataBase}" # Pandas по умолчанию работает через SQLAlchemy и может создавать сама присоединение к БД по формату адреса URI (см. в документации SQLAlchemy)



##  SQL-запросы в реализации через pandas  и фреймы


    def update_from_df_by_key_col_pandas (self, tb, df, keyColName):
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
            self.update_row_in_tb(tb, fieldsVals, uniqueKeyVal) # Обновление ряда в таблице с ключем uniqueKeyVal на основе текущего по циклу ряда фрейма



    def update_const_vals_with_key_col_in_df_pandas(self, df, tb, keyColAssocDic, tbFieldConstDic):
        """ SqlitePandasProcessor
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
            self.update_row_in_tb(tb, fieldsVals, uniqueKeyVal) # Обновление ряда в таблице с ключем uniqueKeyVal на основе текущего по циклу ряда фрейма





    def update_tb_col_by_lambda_function_with_args_from_any_tb_pandas(self, dsSrc, tbTrg, keyFieldsAssoc, colUpdTrg, lambFunc, listLambArgs, **lambOutArgs):
        """О
        Обновление колонки в таблице на основе лямбда-функции с аргументами, берущимися из полей по каждому ряду из этой же таблицы. Колонка обновлять саму себя, например, 
        переконвертировать формат даты самой себя. Для этого надо задать название промежуточной колонки и название конечной колонки опять в виде списка названий.
        Например для колонки 'f2': colUpdTrg = ['res', 'f2']. Если сама колонка не участвует в расчетах, то указывается просто стрингом: colUpdTrg = 'f2'
        dsSrc - источник для аргументов лямбда-функции, который задается любым способом (Указанием названия таблицы, или SQL , где можно филльтровать записи по 
        каким-то признакам (ПРОВЕРЕНО), и т.д. Не проверено, можно ли задавать просто фреймом ?)
        tbTrg - название таблицы, цель для поля , которое обновляетя по результату лямбда-функции. Если берется из той же таблицы, то и указывается та же таблица
        keyFieldsAssoc - Соответствие ключей в таблице-источнике полей аргументов для лямбда-функции  и таблице-цели для обновления поля из результата лямбда-функции [keyFieldSrcTb, keyFieldTrgTb]
        colUpdTrg - Поле, которое обновляется на основе резултата лямбда-функции lambFunc в таблице цели tbTrg. Если этот параметр задается списком из двух названий полей, то
        это означает, что дополнительная колонка для результатов будет названа как-то отлично от поля, которое участвует в операциях. А потом, когда в этой дополнительной
        колонке будет прописан результат, она будет переименована в коненый вариант. Это необходимо, если сама коллонка, которую нужно изменить, участвует в опреациях лямбда-функции
        Например, это используется при конвертации данных в колонке в другой заданный формат , но в этой же самой колонке
        
        listLambArgs - внутренние аргументы лямбда-функции, которые задаются названиями полей таблицы. А порядок должен соотвтетсвовать порядку необходимых аргументов в лямбда-функции
        **lambOutArgs - именованные внешние параметры, по отношению к тем аргументам лямбда-функции, которые беруться из значений полей в записях таблицы. То есть которые не зависят от таблицы,
        но при этом присутствуют в аргументах лямбда-функции
        
        RET: dfRes - фрейм с ключами, на основе которого произведено обновление колонки colUpd в таблице tbTrg
        
        Прим: При реализации lambFunc нужно иметь ввиду, что аргументы на ее вход из данной update_tb_col_by_lambda_pandas подаются в виде списка. Поэтому при ее универсалльной
        реализации для этой функции и для использования вообще, без лямбда-функции, нужно задавать анализ входящих аргументов. И , если они приходят в списке, а не просто, то
        переприсваивать их, вытаскивая из списка внутри функции lambFunc, которая использыется в  виде лямбда тут. Пример: if type(cdate) == list: cdate = cdate[0]
        
        Прим: Метод проверен для обной и той же таблицы как источника, так и цели. Но не проверен, когда таблицы разные
        
        Пример параметров:

        tbSrc = TB_MUNICIP_CURRENT_
        tbTrg = TB_MUNICIP_CURRENT_
        keyFieldsAssoc = ['isin','isin']
        colUpdTrg = 'f11'
        lambFunc = FG.convert_from_date_to_unix_universal
        listLambArgs = ['f2']
        **lambOutArgs = {'format' : '%d-%m-%Y %H:%M:%S'}
        
        Пример лямбда-функции подходящей для этого метода: FG.convert_date_format_to_another_date_format
        
        """
        print('START: update_tb_col_by_lambda_pandas() / sqlite_pandas_processor.py ')
        # Получить исходный фрейм 
        getFields = [keyFieldsAssoc[0]] + listLambArgs # Нужные поля в df состоят из keyFieldSrcTb и listLambArgs источника аргументов для лямбда-функции

        # Считываем источник аргументов для вычислений любым способом (название таблицы, SQL, ...)
        kwargs = {
            'srcListTitles' : [keyFieldsAssoc[0]] # Задаем тайтл для ключевой колонки фрейма, который по идее состоит из одной колонки
        }
        df = self.read_df_from_any_source(dsSrc, **kwargs)
        
        # df = self.read_table_by_sql_to_df_pandas(dsSrc, getFields) # PREVIOUS

        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
        if type(colUpdTrg) == list: # Если необходимо промежуточное переименование колонки
            df[colUpdTrg[0]] =  df.apply(lambda row: lambFunc([row[x] for x in listLambArgs], **lambOutArgs) , axis = 1) 
        else:
            df[colUpdTrg] =  df.apply(lambda row: lambFunc([row[x] for x in listLambArgs], **lambOutArgs) , axis = 1) 
            
        # Оставить в df толькл поля с ключем и с colUpd для совершения UPDATE таблицы через фрейм
        if type(colUpdTrg) == list: # Если необходимо промежуточное переименование колонки
            finalFields = [keyFieldsAssoc[0], colUpdTrg[0]] 
        else:
            finalFields = [keyFieldsAssoc[0], colUpdTrg]
        dfRes = self.slice_df_by_cols_names_pandas(df,finalFields)
        # self.print_df_gen_info_pandas_IF_DEBUG(dfRes, True, colsIndxed = True)
        
        # Переименовать ключевую колонку keyFieldsAssoc[0] в dfRes в соотвтествии с названием ключа keyFieldsAssoc[1] из таблицы-цели
        changNameDic = {keyFieldsAssoc[0] : keyFieldsAssoc[1]}
        dfRes = self.rename_col(dfRes, changNameDic) 
        
        # Переименовать колонку colUpdTrg, если необходимо было промежуточное переименование колонки 
        if type(colUpdTrg) == list:
            changNameDic = {colUpdTrg[0] : colUpdTrg[1]}
            dfRes = self.rename_col(dfRes, changNameDic) 
        
        # Обновить заданную таблицу из фрейма по ключам
        self.update_from_df_by_key_col_pandas(tbTrg, dfRes, keyFieldsAssoc[1])
        print('END: update_tb_col_by_lambda_pandas() / sqlite_pandas_processor.py ')
        
        return dfRes








    def set_const_marker_in_table_by_keys(self, df, tb, keyColAssocDic, tbFieldConstDic):
        """ Идентична update_const_vals_with_key_col_in_df_pandas. Просто изменено название иногда более понятное по смыслу
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
            self.update_row_in_tb(tb, fieldsVals, uniqueKeyVal) # Обновление ряда в таблице с ключем uniqueKeyVal на основе текущего по циклу ряда фрейма






    def select_full_tb_df_by_name_pandas(self, tbName):
        """Получитиь полную выборку таблицы по ее имни в БД"""
        sql = f"SELECT * FROM {tbName}"
        tbDF = self.read_sql_to_df_pandas(sql)
        return tbDF




    def insert_df_to_tb_pandas(self, df, tb, colsList, keyTb):
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
        dfKeysTb = self.read_table_by_sql_to_df_pandas(tb, getFields)

        # 2. Удалить из df ряды с ключами из dfKeysTb, если они есть
        keyColAssocDic = {keyTb : keyTb}
        dfUbique = self.drop_rows_from_df_by_ds_keys_pandas (df, dfKeysTb, keyColAssocDic ) # фрейм с уникальными ключами только


        # listColumns = self.get_df_cols_names_list(dfUbique)
        # if DEBUG_ :
        #     print (f"dfColumns = {listColumns}")
        #     print (f"dfColumns_N = {len(listColumns)}")

        if '*' in colsList : # Значит все колонки
            # tuples = [x  for x in df['x_str']]
            listColumns = self.get_df_cols_names_list(dfUbique) # Все колонки фрейма
            tuples = dfUbique.apply(tuple, axis=1) # Получение значений df в виде тапла тпалов (??) по оси axis=1 (по горизонтали)
            # tuples = [tuple(x) for x in df.to_numpy()]
            if DEBUG_ :
                print(f"PR_124 ---> {tuples}")
            cols = ','.join(list(dfUbique.columns))
            valsQuest = ['?' for  i in range(len(listColumns))] # Массив вопросов для VALUE(?,?) для исполнения cur.executemany(sql , tuples) 
            vals = ','.join(valsQuest)
            # print (f"vals = {vals}")

        else: # или колонки по входному списку colsList
            subDF = self.get_sub_df_with_given_cols(dfUbique, colsList)
            # tuples = [tuple(x) for x in subDF.to_numpy()]
            tuples = subDF.apply(tuple, axis=1)
            # print(tuples)
            cols = ','.join(colsList)
            valsQuest = ['?' for  i in range(len(colsList))] # Формирование '?' для SQL , которые потом будут замещаться величиноами при множественной вставке cur.executemany(sql , tuples)
            vals = ','.join(valsQuest)

        sql = "INSERT INTO %s(%s) VALUES ( %s )" % (tb, cols, vals)
        if DEBUG_:
            print (f"PR_125 ---> sql = {sql}")
        cur = self.connection.cursor()
        cur.executemany(sql , tuples) # цикл втавок формируемых sql на основе множества tuples (? заменяются значениями из tuples)
        # sleep(.5)
        self.connection.commit()
        cur.close()



    def insert_df_to_tb_and_return_no_uniques_keys_val_ignored_pandas(self, df, tb, colsList, keyTb):
        """Вставить данные из фрейма в таблицу с возможностью настроить колонки для ввода и с проверкой ключей на уникальность (ряды фрейма для втавки в таблицу, включевом поле которых
        обнаружены значения , которые уже есть в таблице - удаляются из фрейма и поэтому не будут вставлены в таблицу. Таким образом происходит контроль над возможной вставкой
        неуникального ключа. Запсии в таблице по таким ключам сохраняются прежней, обновления не происходит)
        Проигнорированные значения ключей (то есть которые были уже в таблице и были поэтому проигнорированны, не вставоены)- возвращаются на выходе метода
        Названия колонок в конечном df должно соответствовать названию полей в таблице , в которую будут вставлятся данные
        Если colsList = ['*'] , то идет копирование полногофрейма в таблицу. Поля и колонки должны полностью соответствовать. Поля талицы должны содержать в себе подмножество колонок фрейма
        keyTb - ключ в таблице БД
        https://www.geeksforgeeks.org/how-to-insert-a-pandas-dataframe-to-an-existing-postgresql-table/
        """

        # Проверить на уникальность ключи из df в применении к лючам таблицы БД. Если ключ не уникален и уже существует в 
        # таблице tb , то удалить эти ряды из df

        # 1. Получить фрейм ключей keyTb из таблицы -цели tb
        getFields =  [keyTb]
        dfKeysTb = self.read_table_by_sql_to_df_pandas(tb, getFields)

        # 2. Удалить из df ряды с ключами из dfKeysTb, если они есть
        keyColAssocDic = {keyTb : keyTb}
        dfUbique = self.drop_rows_from_df_by_ds_keys_pandas (df, dfKeysTb, keyColAssocDic ) # фрейм с уникальными ключами только


        # listColumns = self.get_df_cols_names_list(dfUbique)
        # if DEBUG_ :
        #     print (f"dfColumns = {listColumns}")
        #     print (f"dfColumns_N = {len(listColumns)}")

        if '*' in colsList : # Значит все колонки
            # tuples = [x  for x in df['x_str']]
            listColumns = self.get_df_cols_names_list(dfUbique) # Все колонки фрейма
            tuples = dfUbique.apply(tuple, axis=1) # Получение значений df в виде тапла тпалов (??) по оси axis=1 (по горизонтали)
            # tuples = [tuple(x) for x in df.to_numpy()]
            if DEBUG_ :
                print(tuples)
            cols = ','.join(list(dfUbique.columns))
            valsQuest = ['?' for  i in range(len(listColumns))] # Массив вопросов для VALUE(?,?) для исполнения cur.executemany(sql , tuples) 
            vals = ','.join(valsQuest)
            # print (f"vals = {vals}")

        else: # или колонки по входному списку colsList
            subDF = self.get_sub_df_with_given_cols(dfUbique, colsList)
            # tuples = [tuple(x) for x in subDF.to_numpy()]
            tuples = subDF.apply(tuple, axis=1)
            # print(tuples)
            cols = ','.join(colsList)
            valsQuest = ['?' for  i in range(len(colsList))] # Формирование '?' для SQL , которые потом будут замещаться величиноами при множественной вставке cur.executemany(sql , tuples)
            vals = ','.join(valsQuest)

        sql = "INSERT INTO %s(%s) VALUES ( %s )" % (tb, cols, vals)
        if DEBUG_:
            print (f"sql = {sql}")
        cur = self.connection.cursor()
        cur.executemany(sql , tuples) # цикл втавок формируемых sql на основе множества tuples (? заменяются значениями из tuples)
        # sleep(.5)
        self.connection.commit()
        cur.close()









    def insert_df_to_tb_no_key_check_pandas(self, df, tb, colsList=['*']):
        """Вставить данные из фрейма в таблицу с возможностью настроить колонки для ввода и с проверкой ключей на уникальность (ряды с неуникальными ключами по сравнению фрейма с 
        таблице - удаляются ряды с неуникалльными рядвами из фрейма)
        Названия колонок в конечном df должно соответствовать названию полей в таблице , в которую будут вставлятся данные
        Если colsList = ['*'] , то идет копирование полногофрейма в таблицу. Поля и колонки должны полностью соответствовать. Поля талицы должны содержать в себе подмножество колонок фрейма
        keyTb - ключ в таблице БД
        https://www.geeksforgeeks.org/how-to-insert-a-pandas-dataframe-to-an-existing-postgresql-table/
        """
        if '*' in colsList : # Значит все колонки
            # tuples = [x  for x in df['x_str']]
            listColumns = self.get_df_cols_names_list(df) # Все колонки фрейма
            tuples = df.apply(tuple, axis=1) # Получение значений df в виде тапла тпалов (??) по оси axis=1 (по горизонтали)
            # tuples = [tuple(x) for x in df.to_numpy()]
            # if DEBUG_ :
            #     print(tuples)
            cols = ','.join(list(df.columns))
            valsQuest = ['?' for  i in range(len(listColumns))] # Массив вопросов для VALUE(?,?) для исполнения cur.executemany(sql , tuples) 
            vals = ','.join(valsQuest)
        else: # или колонки по входному списку colsList
            subDF = self.get_sub_df_with_given_cols(df, colsList)
            # tuples = [tuple(x) for x in subDF.to_numpy()]
            tuples = subDF.apply(tuple, axis=1)
            # print(tuples)
            cols = ','.join(colsList)
            valsQuest = ['?' for  i in range(len(colsList))] # Формирование '?' для SQL , которые потом будут замещаться величиноами при множественной вставке cur.executemany(sql , tuples)
            vals = ','.join(valsQuest)
        
        sql = "INSERT INTO %s(%s) VALUES ( %s )" % (tb, cols, vals)
        if DEBUG_:
            print (f"sql = {sql}")
        cur = self.connection.cursor()
        cur.executemany(sql , tuples) # цикл втавок формируемых sql на основе множества tuples (? заменяются значениями из tuples)
        # sleep(.5)
        self.connection.commit()
        cur.close()
        # self.connection.close()



    def insert_consts_to_tb_by_df_keys_pandas(self, df, tb, keyColFieldDic, tbFieldsValsDic):
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
        dfKeys = self.get_sub_df_with_given_cols(df, [keyCol]) 
        # Удаляем возможные пустоты
        dfKeys = self.filter_df_from_empties_or_any_vals_by_columns (dfKeys, [keyCol], ['', ' ', None])
        # Удаляем возможные дубликаты ключей
        dfKeys = self.drop_duplicates_by_columns_pandas (dfKeys, [keyCol])
        # Формируем df с дополнительными колонками констант, задаваемых в tbFieldsValsDic с названиями колонок, соответствующим названию ключей словаря
        self.add_df_cols_with_constants_pandas(dfKeys,  tbFieldsValsDic)
        # Вставляем константы в заданные поля для них по заданным ключам в колонке фрейма keyCol
        
        self.insert_df_to_tb_pandas(dfKeys, tb, ['*'], keyTb)









## END  SQL-запросы в реализации через pandas  и фреймы



# АНАЛИТИЧЕКСИЕ МЕТОДЫ

    def if_row_with_given_key_exists_in_tb_return_such_a_row_pandaas(self, tb, dicKysVals):
        """ 
        Если запись с заданным набором ключей и их значениями существует в таблице, то вернуть фрейм с этим рядом. Или пустой фрейм, если не существует.
        dicKysVals - набор ключей с их значениями, наличие записи по которым нужно проверить в таблице tb
        
        RET: Возвращает фрейм с рядом из таблицы, в случае, если запись с такими значениями ключей существует в таблице. и пустой фрейм- если отстуствует
        """
        # 'AND' : [['fieldName3', '<', 5], ['fieldName4', '>', 15]]
        
        # Создать список условий на базе словаря с заданными значениями ключей для формирования запроса SELECT с условиями для WHERE
        
        andondList = []
        for key, val in dicKysVals.items():
            andondList.append([key,'==',val])
            
        conds = {'AND': andondList}
        
        sql = SQLSyntaxer.select_from_table_with_where_condition_sql (tb, ['*'], conds)
        
        df = self.read_sql_to_df_pandas(sql)
        
        # print(f'sql = {sql}')
        
        # df = pd.DataFrame()
        
        return df
        
        


# END АНАЛИТИЧЕКСИЕ МЕТОДЫ


# Считывание данных из БД в фрейм 


    def read_df_from_any_source (self, ds, **kwargs):
        """Создать фрейм на основе любого источника данных (таблицы, запроса, одно- или двумерного списка, фрейма)
        **kwargs - именные параметры, через которые можно задавать развные свойства и совершать обработку DSourceCube - результата, в котором находится и 
        получаемый фрейм. К примеру, задавать названия колонок выходного фрейма, совершать сортирвку по колонке и др (см. в классе DSourceCube)
        Пример:
            bmm = BondsMainManager(DB_BONDS_)
            kwargs = {'srcListTitles' : ['isin']} # Тайтлы для колонок фрейма}
            df = bmm.read_df_from_any_source (dsKeys, **kwargs)
        """
        from project_bonds_html.projr.classes.dsource_cube import DSourceCube # Локальное использование. Не удалять и не переставлять в шапку!!!
        dsc = DSourceCube(self.dataBase, ds, **kwargs)
        df = dsc.genDf
        return df
            


    def read_table_to_df_pandas(self, tb):
        """SqlitePandasProcessor
        Считывает данные таблицы из БД и возвращает прообраз таблицы в форме dataFrame
        Прим: Есть проблемы со считыванием числовых колонок , выраженных через стринги. Например Float - '0.0%'.
        Поэтому лучше использовать с теми таблицами, где нет таких форматов. Либо использовать функцию SqlitePandasProcessor.read_sql_to_df_pandas
        """
        tbDF = pd.read_sql_table(tb, self.db_uri)
        return tbDF



    def read_sql_to_df_pandas(self, sql):
        """
        SqlitePandasProcessor
        Считывает результат sql запроса в dataFrame
        
        """    
        df = pd.read_sql(sql, self.db_uri)
        return df
    

    
    def read_sql_to_df_pandas(self, sql):
        """SqlitePandasProcessor
        Считывает результат sql запроса в dataFrame"""    
        df = pd.read_sql(sql, self.db_uri)
        return df
    


    def read_table_by_sql_to_df_pandas(self, tb, getFields = ['*']):
        """Считывает всю таблицу в фрейм с выбором необходимых колонок в выборке
        getFields - список выводимых колонок. По умолчанию выводятся все колонки
        """
        # Считывание таблицы bonds_archive в фрейм
        sql = f'SELECT * FROM {tb}'
        print(sql + '  | read_table_by_sql_to_df_pandas() | noocube/sqlite_pandas_processor.py')
        dfTb = self.read_sql_to_df_pandas(sql)  
        if '*' in getFields: # если запрашиваются все колонки
            return dfTb
        else : # если выборка колонко
            dfTb = self.get_sub_df_with_given_cols(dfTb, getFields)  
            return  dfTb 



    def read_to_df_from_cursor (self, cursor):
        """SqlitePandasProcessor
        Считать курсор из обычного подсоединения (не через SQLAlchemy) в dataFrame
        https://stackoverflow.com/questions/12047193/how-to-convert-sql-query-result-to-pandas-data-structure
        """
        df = pd.DataFrame(cursor.fetchall())
        df.columns = [description[0] for description in cursor.description] # Получение названий колонок из описания курсора и присвивание их в названия колонок фрейма
        return df



# END Считывание данных из БД в фрейм 




## Специфические комплексные запросы SQL





    def get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas(self, baseSource, compairSource, assocColsInxDic, getCols= ['*']):
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
            baseDF = self.read_table_by_sql_to_df_pandas(baseSource)
        else:
            baseDF = baseSource

        # Анализ  источника базовых данных и создание фрейма, если этот источник задан в виде названия таблицы
        if type(compairSource) == str: # если базовый источник задан названием таблицы
            compairDF = self.read_table_by_sql_to_df_pandas(compairSource)
        else:
            compairDF = compairSource


        qrOper = 'not in' # Оператор сравнения 'не равно', то есть ищутся неравные задаваемым величинам значения в колонках
        logicOper = '&' # Логический оператор AND, для обьединения в логическое И всех частных выражений в query
        # Формирование именных параметров, которые включают в себя именные списки с выборками-векторами по заданным колонкам в комплексном или простом индексе
        #  входного параметра assocColsInxDic из сравниельного фрейма compairDF
        print(f"baseDF = {baseDF}/ (SqlitePandasProcessor.get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas)")
        print(f"compairDF = {compairDF}/ (SqlitePandasProcessor.get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas)")
        
        kwargs = {} # словарь для именных параметров для функции филльтрации
        for key, val in assocColsInxDic.items(): # цикл по колонкам в составном индексе колонок assocColsInxDic
            colValsList = self.convert_df_col_to_list(compairDF, val) # получение колокнки-ветора с названием текущего по циклу val во фрейме compairDF в виде простого списка значений (эти значения из списка будут отсеиваться в базовом фрейме по соответствующей колонке с названием текущего ключа key)
            kwargs[key] = colValsList # вставка текущего по циклу именного параметра в словрь kwargs

        dfBaseFiltered = self.filter_df_by_multiple_cols_vals(baseDF, qrOper, logicOper, **kwargs)  #  Базовый фрейм, отфильтрованный по значениям колонок из compairDF совокупного индекса колонок

        # print(f"dfBaseFiltered = {dfBaseFiltered} / (SqlitePandasProcessor.get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas)")

        if '*' in getCols: # То выводятся все колонки
            dfRes =  dfBaseFiltered
        else:
            # !!! CHANGED: WAS return dfBaseFiltered[[getCols]] !!!
            # TODO: Сделать вывод любых колонок по отфидбьолванным ключам из основного базового фрейма
            dfRes =  dfBaseFiltered[getCols] # Иначе вводятся запрашиваемые в списке getCols колонки
            if 'Series' in str(type(dfRes)):
                dfRes = self.convert_series_to_df_pandas(dfRes)

        return dfRes


    def select_rows_from_data_source_by_values_source_pandas (self, dsBase, dsKeys, dicKeysAssoc = {}, getFields = ['*']):
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
            listKeysInp = self.convert_df_to_list( dsKeys, keyKeysFrame) # простой список значений для фильтрации

        # Анализ источника бызовых данных
        if type(dsBase) == str: # Если истоыник ключей - таблица БД с заданным названием колонки-ключа в dicKeysAssoc (величина элемента словаря
            dfBaseInp = self.read_table_by_sql_to_df_pandas(dsBase, getFields) # Формирование фрейма на основе названия таблицы в БД и выводимых заданных полей getFields
            # dfBaseInp = dfBaseInp[getFields] PREVIOUS был включен
        else: # Если источник ключей - фрейм
            dfBaseInp = dsBase

        # Получение ссылок по списку ИНН listInn из табл comps_descr
        # Pars:
        logicOper = '|' # Логический оператор AND, для обьединения в логическое И всех частных выражений в query
        kwargs = {keyBase: listKeysInp} # okpo в **kwargs - имя равное названию поля, по которому производится фиьтрация значений по списку listForFilter.  
        qrOper =   '=='    
        dfRes = self.filter_df_by_multiple_cols_vals (dfBaseInp, qrOper, logicOper, **kwargs)

        return dfRes



        


    def drop_duplicates_from_table_by_col(self, tb, colSubsetList, tbKey, keepFg = 'last'):
        """
        SqlitePandasProcessor
        Удалить дупликаты в таблице по поиску в одной задаваемой колонке (не наборе колонок)
        colNamesList - набор названий колонок в таблице БД, по ключу которых проверяется дубликаты
        keepFg - настройка, какая запись из дубликатов не удаляется. По умолчанию не удаляется последний из дубликатов
        RET: Возвращает фрейм с дубликатами, которые были удалены, за исключением последнего из дубликатов (тоже можно настроить последний или первый оставляется)
        """
        
        dfTb = self.read_table_to_df_pandas(tb)
        # Выявить дубликаты по значению колонки x_str, в которой к хранятся ИНН
        dfDuplic = self.get_duplicated_rows_of_column (dfTb, colSubsetList)
        if DEBUG_:
            print (f"dfDuplic = {dfDuplic} / pr: SqlitePandasProcessor.drop_duplicates_from_table_by_cols")\
        
        if len(dfDuplic) > 0: # Если найдены дубликаты
            print(f"INFO: Найдены дупликаты в таблице {tb} по индексу {colSubsetList}, который должен быть укникальным  и которые будут удалены / SqlitePandasProcessor.drop_duplicates_from_table_by_cols")
            dfTb = self.drop_duplicates_by_columns_pandas (dfTb, colSubsetList, keepFg)
            # Удаляем дупликаты из таблицы(двуступенчатым способомыЫ):
            # 1. очищаем таблицу в БД полностью от всех данных
            self.delete_from_table_with_where_condition(tb, {}) 
            # 2. Вставляем в таблицу данные из фрейма, очищенного от дубликатов
            self.insert_df_to_tb_pandas( dfTb, tb, ['*'], tbKey) 

        else:
            print(f"INFO: Дупликаты в таблице {tb} по индексу {colSubsetList} НЕ найдены/ SqlitePandasProcessor.drop_duplicates_from_table_by_cols")


        return dfDuplic     




## END Специфические комплексные запросы SQL


### ФУНКЦИИ СОЗДАНИЯ КЛОНОВ ТАБЛИЦ (ОБЫЧНЫХ, НЕ ВИРТУАЛЬНЫХ. ) И ИХ НАПОЛНЕНИЕ ИЗ БАЗОВЫХ

#TODO: Сделать по алгоритмам, которые реализованы для виртуальных таблиц ниже

    def get_table_create_sql_meta(self, baseTbName, cloneTbName):
        """ ЗАГОТОВКА : Сделать по алгоритмам, которые реализованы для виртуальных таблиц ниже
        Получение SQL-скрипта для создания таблицы  cloneTbName на основе заанной базовой  таблицы baseTbName из БД """


    def create_clone_table_meta(self, baseTbName, cloneTbName):
        """ ЗАГОТОВКА : Сделать по алгоритмам, которые реализованы для виртуальных таблиц ниже
        Создать структуру клонируемой  таблицы на основе базовой обычной из БД"""


    def fill_table_from_another_table(self, tbSource, tbTarget, fieldsAssocDic = {},  keyFieldAssoc = {}, ifClearTb = False, colsList = ['*']):
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
            self.clear_table (tbTarget)
        # Считать данные из таблицы comps_descr (БД: bonds) в фрейм
        dfTbSource = self.read_table_by_sql_to_df_pandas(tbSource)
        # Анализ списка полей colsList для заполнения (отсев ненужных колонок)
        if len(colsList) < 1 or '*' in colsList: # Значит задан параметр для вывода и заполнения по всем колонкам
            pass # Не удалять pass
        elif len(colsList) > 0 and '*' not in colsList: # Значит задан параметр , ограничивающий полное множество колонок и фрейм должен быть усечен только на допустимые поля
            dfTbSource = dfTbSource[colsList]
            if DEBUG_:
                print (f"type of dfCompsDescr = {str(type(dfTbSource))}")
        # Анализ словаря соответствий полей таблиц. Если не задан, то значит все поля идентичны, если задан, то необходимо переименовать в inseart-фрейме те поля, которые указаны в словаре
        fieldsAssocDic_N = len(fieldsAssocDic)
        if fieldsAssocDic_N > 0: # Если есть элементы в словаре, то надо переименовать поля insert-фрейма dfCompsDescr в соотвтетсвии с ними. Если нет, то ничего переименовывать не надо
            # Переименовать поля фрейма в соотвтесвии со словарем соответствий источника и цели
            dfTbSource = self.rename_cols_by_associate_dic_pandas (self, dfTbSource, fieldsAssocDic, False) # False - значит создается копия фрейма с измененными названиями колонок
        keyAssocN = len(keyFieldAssoc) # количество задаваемых ключей проверки на уникальность
        if keyAssocN > 0: # Значит задан как минимум один ключ для проверки уникальности
            # Наполнить виртуалльную таблицу данными из фрейма dfCompsDescr
            keyTb = list(keyFieldAssoc.values())[0] # Ключ для целевой таблицы
            self.insert_df_to_tb_pandas(dfTbSource, tbTarget, colsList, keyTb)
        else: # Если не заданы ключи для проверки уникальности, то не проверяем их
            # Наполнить виртуалльную таблицу данными из фрейма dfCompsDescr
            # keyTb = list(keyFieldAssoc.values())[0] # Ключ для целевой таблицы
            self.insert_df_to_tb_no_key_check_pandas(dfTbSource, tbTarget, colsList)



    def copy_tb_data_to_another_identical_tb(self, tbSrc, tbTrg):
        "Скопировать данные из одной таблицы в другую идентичную по структуре"
        self.fill_table_from_another_table(tbSrc, tbTrg, fieldsAssocDic = {},  keyFieldAssoc = {}, ifClearTb = False, colsList = ['*'])



    def copy_tb_data_to_another_identical_cleared_tb(self, tbSrc, tbTrg):
        """
        Скопировать данные из одной таблицы в другую идентичную по структуре с предварительной очисткой целевой таблицы
        """

        # Очищаем табл bonds_curr_prev
        pandas_db_proc = SqlitePandasProcessor(DB_BONDS_)
        pandas_db_proc.clear_table(tbTrg)

        # Копируем данные из табл bonds_curr в табл bonds_curr_prev
        pandas_db_proc.copy_tb_data_to_another_identical_tb(tbSrc, tbTrg)



    def create_and_fill_clone_table (self, baseTbName, virtTbName, fieldsAssocDic = {},  keyFieldAssoc = {}, ifClearTb = False, colsList = ['*']):
        """ ЗАГОТОВКА : Сделать по алгоритмам, которые реализованы для виртуальных таблиц ниже
        Создать виртуальную таблицу на основе базовой  и наполнить ее данными из базовой
        fieldsAssocDic - словарь соответствий полей таблиц. По умолчанию словарь не задан и это значит, что названия полей в фрейме, предназначенном  для вставки,
        будут иметь полное совпадение у обоих таблиц. Если заданы, то названия полей изменятся в соотвтетсвии со словарем
        keyFieldAssoc - словарь соответствий ключей. Если ключи не заданы, то проверка по уникальности по ключам отсутствует. По умолчанию - отсутствует проверка.
                        Если не задан, то значит все поля идентичны, если задан, то необходимо переименовать в inseart-фрейме те поля, которые указаны в словаре keyFieldAssoc,
                        остальные остаются и должны быть равными
        ifClearTb - флаг отчистки таблицы перед наполнением. Если - True, то перед наполнением производится полная очистка таблицы от всех данных. По умолчанию - False
        colList - список колонок таблицы-цели, которые необходимо заполнить из базовой таблицы. Если поля полностью соответствуют, то спсиок соответствий не создается для этих полей.
        """



### END ФУНКЦИИ СОЗДАНИЯ КЛОНОВ ТАБЛИЦ (ОБЫЧНЫХ, НЕ ВИРТУАЛЬНЫХ. ) И ИХ НАПОЛНЕНИЕ ИЗ БАЗОВЫХ



## ФУНКЦИИ С ВИРТУАЛЬНЫМИ ТАБЛИЦАМИ  ДЛЯ  FTS или для таблиц в оперативной памяти RAM таблицы

    def get_fts_virt_table_create_sql_ram(self, baseTbName, virtTbName):
        """Получение SQL-скрипта для создания виртуальной таблицы FTS virtTbName на основе заанной базовой обычной таблицы baseTbName из БД """
        createSQL = self.get_create_table_shema_sql_meta(baseTbName)
        sqlLines = createSQL.split('\n')
        fields = [x.split(' ')[0].replace('\t','') for x in sqlLines if ',' in x] # Получение списка названий полей из общего SQL (парсинг)
        fildsPartSQL = ','.join(fields) # Часть sql с полями
        virtTbSQLCreate = f'CREATE VIRTUAL TABLE {virtTbName} USING fts5 ({fildsPartSQL})'
        return virtTbSQLCreate




    def create_virtual_table_ram(self, baseTbName, virtTbName):
        """Создать виртуальную таблицу на основе базовой обычной из БД"""
        virtTbSQLCreate = self.get_fts_virt_table_create_sql_ram(baseTbName, virtTbName)
        # Создать виртуальную таблицу virtTbName в БД с использованием технологии FTS5
        self.execute_sql(virtTbSQLCreate)
        return virtTbSQLCreate






    def create_and_fill_virt_table_ram(self, baseTbName, virtTbName, fieldsAssocDic = {},  keyFieldAssoc = {}, ifClearTb = False, colsList = ['*']):
        """Создать виртуальную таблицу на основе базовой  и наполнить ее данными из базовой
        fieldsAssocDic - словарь соответствий полей таблиц. По умолчанию словарь не задан и это значит, что названия полей в фрейме, предназначенном  для вставки,
        будут иметь полное совпадение у обоих таблиц. Если заданы, то названия полей изменятся в соотвтетсвии со словарем
        keyFieldAssoc - словарь соответствий ключей. Если ключи не заданы, то проверка по уникальности по ключам отсутствует. По умолчанию - отсутствует проверка.
                        Если не задан, то значит все поля идентичны, если задан, то необходимо переименовать в inseart-фрейме те поля, которые указаны в словаре keyFieldAssoc,
                        остальные остаются и должны быть равными
        ifClearTb - флаг отчистки таблицы перед наполнением. Если - True, то перед наполнением производится полная очистка таблицы от всех данных. По умолчанию - False
        colList - список колонок таблицы-цели, которые необходимо заполнить из базовой таблицы. Если поля полностью соответствуют, то спсиок соответствий не создается для этих полей.
        """
        # Создать виртуальную таблицу
        self.create_virtual_table_ram(baseTbName, virtTbName) 
        # Наполнить созданную виртуальную таблицу данными из базовой таблицы\
        self.fill_table_from_another_table(baseTbName, virtTbName, fieldsAssocDic = {},  keyFieldAssoc = {}, ifClearTb = False, colsList = ['*'])





## END ФУНКЦИИ С ВИРТУАЛЬНЫМИ ТАБЛИЦАМИ  ДЛЯ  FTS или для таблиц в оперативной памяти RAM таблицы





    # МАТА-ФУНКЦИИ и  данные БД

    def get_tb_fields_to_df_pandas(self, tb):
        """SqlitePandasProcessor
        Полуение фрейма названий полей таблицы БД"""
        sql = SQLSyntaxer.get_tb_fields_sql(tb)
        dfTbFiels = self.read_sql_to_df_pandas(sql)
        return dfTbFiels




    # END МАТА данные БД




    #  SEARCH EXPRESSIONS 

    def search_mask_rows_by_col_val_pandas(self, df, colName, val):
        """
        OBSOLETED: Перенесена в модуль PandasManager с переводом в статичный метод
        Найти строки в фрейме по значению в поле через query"""
        dfFound = df.loc[df[colName] == val]
        return dfFound




    #  END SEARCH EXPRESSIONS  







if __name__ == "__main__":
    pass






    # # ПРОРАБОТКА: Обновление полей в таблице на основе заданных функций для операции над полями / update_tb_col_by_lambda_inside_cols_pandas() / sqlite_pandas_processor.py

    # from bonds.bonds_main_manager import BondsMainManager
    # from bonds.structures import *
    # from bonds.settings import *
    # import bonds.funcs_general as FG
    
    # bmm = BondsMainManager(DB_BONDS_)
    
    # tbSrc = TB_MUNICIP_CURRENT_
    # tbTrg = TB_MUNICIP_CURRENT_
    
    # lambOutArgs = {
        
    #     'format' : '%d-%m-%Y %H:%M:%S'
    # }
    # # pars
    # colUpdTrg = 'f11'
    # lambFunc = FG.convert_from_date_to_unix_universal
    # listLambArgs = ['f2']
    
    # #pars
    # keyFieldsAssoc = ['isin','isin']
    
    # dfRes = bmm.update_tb_col_by_lambda_function_with_args_from_any_tb_pandas (tbSrc, tbTrg, keyFieldsAssoc, colUpdTrg, lambFunc, listLambArgs, **lambOutArgs)
    
    # bmm.print_df_gen_info_pandas_IF_DEBUG(dfRes, True, colsIndxed = True)
    







    # # ПРОРБОТКА: read_sql_to_df_pandas(self, sql)
    
    # db_panda_proc = SqlitePandasProcessor(DB_BONDS_)
    
    # sql = 'SELECT * FROM ofz_current'
    
    # res = db_panda_proc.read_sql_to_df_pandas(sql)
    
    
    


    # # ПРОРАБОТКА: insert_consts_to_tb_by_df_keys_pandas  <138>
    # # Pars:
    # db_panda_proc = SqlitePandasProcessor(DB_BONDS_)
    # getFields = ['isin']
    # dfISINs = db_panda_proc.read_table_by_sql_to_df_pandas(TB_BONDS_ARCIVE_, getFields)
    # # Pars:
    # tbFieldsValsDic = {
    #     'moex' : 'FILEED',
    #     'f1' : 'TEST'
    #     }
    # keyCol = 'isin'
    # db_panda_proc.insert_consts_to_tb_by_df_keys_pandas(dfISINs, TB_REG_ISIN_B_, keyCol, tbFieldsValsDic)






    # # ПРИМЕР: Вставка через executemany

    # db_panda_proc = SqlitePandasProcessor(DB_BONDS_)
    
    # playlists={'user1':{'Karma Police':3.0,'Roxanne':4.0,'Sonnet':5.0,
    #                     'We Will Rock You':1.0,'Song 1': 1.0},
    #         'user2':{'Karma Police':2.0,'Roxanne':3.0,'Sonnet':2.0,
    #                     'We Will Rock You':3.0,'Song 2': 1.0},
    #         'user3':{'Karma Police':8.0,'Roxanne':1.0,'Sonnet':6.0,
    #                     'We Will Rock You':4.0,'Song 3': 1.0},
    #         'user4':{'Karma Police':5.0,'Roxanne':2.0,'Sonnet':1.0,
    #                     'We Will Rock You':6.0,'Song 4': 1.0},
    #         'user5':{'Karma Police':9.0,'Roxanne':4.0,'Sonnet':7.0,
    #                     'We Will Rock You':9.0,'Song 4': 1.0}}

    # print (f"playlists = {playlists}")

    # sqltuples = [(k1, k2, v2) for k1, v1 in playlists.items() for k2, v2 in v1.items()]

    # print (f"sqltuples = {sqltuples}")

    # cur = db_panda_proc.connection.cursor()

    # cur.execute('''
    #     CREATE TABLE playlists(
    #     id INTEGER PRIMARY KEY,
    #     user TEXT,
    #     track_names TEXT,  
    #     count INTEGER)
    # ''')
    # db_panda_proc.connection.commit()

    # cur.executemany('INSERT INTO playlists (user, track_names, count) VALUES (%s)' , sqltuples)
    # db_panda_proc.connection.commit()



    # # ПРИМЕР: Проработка insert_df_to_tb_pandas(self, df, tb, colsList)

    # db_panda_proc = SqlitePandasProcessor(DB_BONDS_)
    # df = db_panda_proc.read_table_to_df_pandas(TB_COMPS_)

    # colsList = ['*']
    # db_panda_proc.insert_dinsert_df_to_tb_pandasf_to_tb(df, TB_GLOBAL_A_, colsList)



    # # ПРИМЕР: Проверка работы функции read_to_df_from_cursor (self, cursor)
    # db_panda_proc = SqlitePandasProcessor(DB_BONDS_)
    # # db_processor = SqliteProcessor(DB_BONDS_)   
    # # db_processor.select_with_except(self, fullSel1Pars, fullSel2Pars)
    # cursor = db_panda_proc.connection.cursor()
    # cur = cursor.execute('SELECT * FROM bonds_archive')
    # df = db_panda_proc.read_to_df_from_cursor (cur)
    # # dsFetch = cur.fetchall()
    
    # cur.close()    




    # # ПРИМЕР: Проработка read_sql_to_df_pandas

    # db_panda_proc = SqlitePandasProcessor(DB_BONDS_)
    # # db_panda_proc.read_sql_table_to_df_pandas(TB_BONDS_ARCIVE_)

    # sql = 'SELECT * FROM bonds_archive'
    # df = db_panda_proc.read_sql_to_df_pandas(sql)





    # # ПРИМЕР: Проработка update_rows_from_df(self , tb, df, fieldsInxAccordList, unqInxColVal)

    # db_panda_proc = SqlitePandasProcessor(DB_BONDS_)
    # # db_proc = SqliteProcessor = (DB_BONDS_)
    # # pars:

    # dfOkpoInn = AlgorithmsSubParts.a022_1_()

    # keyCol = 'okpo'

    # for index, row in dfOkpoInn.iterrows():

    #     uniqueKeyVal = [keyCol,row[keyCol]] # Ключ идентификации ряда в таблице с названием поля ключа и его значением
    #     fieldsVals = {} # Словарь с ключами в виде названий полей и значениями в виде величин для этих полей для обновления в таблице
    #     for column in dfOkpoInn:
    #         # print(column)
    #         # print (row[column])
    #         if column != keyCol:
    #             fieldsVals[column] = row[column] 
            


    #         # db_panda_proc.update_row_in_tb(TB_BONDS_CURRENT_,  fieldsVals, uniqueKeyVal)


        










