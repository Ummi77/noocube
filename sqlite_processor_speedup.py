

# Динамическая настройка на общий settings_bdp_main.py
# import sys
# sys.path.append('/home/ak/projects/P19_Bonds_Django/bonds_django_proj')
# import noocube.settings_bdp_main as ms # общие установки для всех модулей

import noocube.funcs_general  as FG

import re

from noocube.sql_syntaxer import SQLSyntaxer

import sqlite3

import pandas as pd


class SqliteProcessorSpeedup ():
    """ 
    Класс предназначен для реализации sql запросов в виде строки в реальной БД sqlite - ускоренный

    """

    def __init__(self, dataBaseConnection): 
        
        self.dbc_set = dataBaseConnection
        self.db_uri = f"sqlite:///{dataBaseConnection.dataBase}" # Pandas по умолчанию работает через SQLAlchemy и может создавать сама присоединение к БД по формату адреса URI (см. в документации SQLAlchemy)
        self.db_connection = dataBaseConnection.connection
        # self.spps = SqlitePandasProcessorSpeedup()



    @staticmethod
    def insert_null_transformation_static_sps (strVariable, stripVals = ''):
        """ 
        Метода проработки и преобразования переменной для стрингового или текстового поля в sql-запросе для того, 
        что бы можно было вставлять в f-стринги величины строкового типа без дополнительных кавычек вокруг в самом sql-запросе
        Это в первую очередь необходимо для того, что бы можно было вставлять в sql-запрос NULL- величины
        Иначе они все получаются окуржены кавычками и воспринимаются как строковые значения типа 'NULL'
        strVariable - стринговая переменная для вставки в активные запросы типа INSERT, Update
        stripFlag - флаг очистки по краям от пустот
        stripVals - набор символов (включая пробел) для очистки с концов. По умолчанию = '', то есть ничего не очищает
        """
        
        strVariable = strVariable.strip(stripVals)
        if not strVariable or strVariable == '':
            strVariable = 'NULL'
        else:
            strVariable = f"'{strVariable}'"
            
        return strVariable



    def insert_null_transformation_sps (self, strVariable, stripVals = ''):
        """ 
        Преобразовать переменнуюдля стрингового поля в sql-запросе для того вставки f-стринг величины  без дополнительных кавычек и 
        оперировать с NULL
        Это в первую очередь необходимо для того, что бы можно было вставлять в sql-запрос NULL- величины
        Иначе они все получаются окуржены кавычками и воспринимаются как строковые значения типа 'NULL'
        strVariable - стринговая переменная для вставки в активные запросы типа INSERT, Update
        stripFlag - флаг очистки по краям от пустот
        stripVals - набор символов (включая пробел) для очистки с концов. По умолчанию = '', то есть ничего не очищает
        """
        
        strVariable = strVariable.strip(stripVals)
        if not strVariable or strVariable == '':
            strVariable = 'NULL'
        else:
            strVariable = f"'{strVariable}'"
            
        return strVariable






    def execute_sql_SPS (self, sql):
        """ 
        SqliteProcessorSpeedup
        Выполняет запрос без возврата курсора с выборкой по результатам запроса
        """
        
        
        cursor = self.db_connection.cursor()
        # print(f"PR_NC_118 --> sql = {sql}")
        cursor.execute(sql)
        self.db_connection.commit()
        cursor.close() 
        # self.connection.close()   
        
        # Если есть команда INSERT в sql-запросе, то получаем последний id, сформулированный в БД
        if 'INSERT' in sql: 
            lastInsertid = self.get_last_inserted_id_in_db_mysql_sps ()
        else:
            lastInsertid = -1
            
        return lastInsertid
        
        
        
        
    def execute_sql_with_cursor_bmms_through_sps (self, dicThrough):
        """ 
        SqliteProcessorSpeedup
        Выполняет запрос с возвратом курсора, содержащего выборку по результатам запроса
        Курсор не закрывается. Его надо закрывать потом вручную
        """
        
        cursor = self.db_connection.cursor()
        cursor.execute(dicThrough['sql'])
        self.db_connection.commit()
        
        
        dicThrough['ds_res'] = self.get_ds_from_cursor_sps(cursor)
        cursor.close()
        
        return dicThrough
    
    
    
    
    def execute_sql_with_cursor_sps(self, sql):
        """ 
        Выполняет запрос с возвратом курсора, содержащего выборку по результатам запроса
        Курсор не закрывается. Его надо закрывать потом вручную
        """
        
        cursor = self.db_connection.cursor()
        cursor.execute(sql)
        self.db_connection.commit()
        return cursor
    
    
    
    

    def get_result_from_sql_exec_proc_sps(self, sql):
        """
        Получить результат из sql-запроса в виде спискоа либо двумерного либо одномерного
        !!! Основной метод получения результата из SQL типа SELECT
        """
        cur = self.execute_sql_with_cursor_sps(sql)
        res = self.get_ds_from_cursor_sps(cur)
        return res
    
    
    
    
    def if_select_result_exists_sps (self, sql):
        """ 
        Содержит ли ответ по SQL-запросу ответ с данными из таблицы. Если запрос возвращает какие-то данные, то True. Если нет - то false 
        """
        
        print(f"PR_NC_184 -->  START: if_select_result_exists_sps()")
        
        
        
        dsRes = self.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(dsRes, int):
            ret = True
            
        else:
            ret = False
            
            
        print(f"PR_NC_185 -->  END: if_select_result_exists_sps()")

            
            
        return ret
    
    
    
    #### SELECT SQLs ---------
    
    def select_rows_with_given_val_in_col_sps(self, tb, getFields, сolName, colVal):
        """
        SqliteProcessorSpeedup
        Получить массив из запрашиваемых полей getFields таблицы, в запиях которых значение поля заданной колонки ColName равна задаваемой велечине colVal
        """
        
        # Найти записи в таблице bonds_archive с помеькой в поле f1= 'NOT MATCHED'
        conds = {'ONE' : [сolName,'=', colVal]}
        dsRes, sql = self.select_from_table_with_where_condition_sps(tb, getFields, conds)     
        return dsRes  
    
    
    
    
    def select_from_table_sps(self,tb,fields = ['*']):
        """ Делает выборку из таблицы по указанным полям. Если не указаны поля отдельно, то по умолчанию возвращает выборку по всем полям. 
        Возвращает выборку в  dataSet в виде курсора (cursor) с результатос запроса """

        sql_select = SQLSyntaxer.select_from_table_sql(tb, fields)
        cursor = self.db_connection.cursor()
        cur = cursor.execute(sql_select)
        
        dsRes = self.get_ds_from_cursor_sps(cur)
        cursor.close()
        
        
        return dsRes, sql_select    
    
    
    
    
    def select_from_table_with_where_condition_sps(self, tb, getFields, conds, add = ''):
        """ 
        SqliteProcessorSpeedup
        Conditional SELECT from tb by fields . fields - список полей или *
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
            
        self.db_connection.create_function("REGEXP", 2, regexp) # Создание новой функции для Regex
        # print (f"5. {conds} in sqliteProcessor module F : select_from_table_with_where_condition")
        sql = SQLSyntaxer.select_from_table_with_where_condition_sql(tb, getFields, conds, add)
        # if ms.DEBUG_ :
        #     print ("PR_129 select_from_table_with_where_condition -> " + sql)
        cursor = self.db_connection.cursor()
        cur = cursor.execute(sql)
        
        dsRes = self.get_ds_from_cursor_sps(cur)
        cursor.close()
        
        
        return dsRes, sql    
    
    
    
    
    
    def select_diffr_rows_keys_in_two_tabs_by_key_cols_sps (self, tbSrc, tbTrg, listKeysPair):
        """Найти ключи первой таблицы, которые отсутствуют или присутствуют во второй таблице
        tbSrc - источник поиска ключей
        tbTrg - цель, с которой сравниваются ключи источника
        listKeysPair - спсиок названий ключей в таблице источнике и цели ['fieldKeySrc', 'fieldKeyTrg']
        exept - флаг отсутствуют или присутствуют. По умолчанию - отсуствуют
        """
        
        sql = SQLSyntaxer.select_diffr_rows_keys_in_two_tabs_by_key_cols_sql(tbSrc, tbTrg, listKeysPair)
        # if ms.DEBUG_ :
        #     print ("PR_288 --> sql -> " + sql)
        cursor = self.db_connection.cursor()
        cur = cursor.execute(sql)
        
        dsRes = self.get_ds_from_cursor_sps(cur)
        cursor.close()
        
        
        return dsRes, sql   
    
    
    

    
    #### END SELECT SQLs ---------
    
    
    #### DELETE SQLs --------
    
    
    def delete_rows_with_col_value_in_ds_sps (self, tb, colName, ds):
        """Удалить записи в таблице ,где величина заданного поля принадлежит множеству значений полей задаваемого одномерного, одноколоночного массива ds
        colName - название колонки, в которой ищется задаваемое значение для удаления
        colValForDel - значение поля колонки, по которому находятся записи для удаления
        """
        # Удалить записииз таблицы bonds_current , isin которых есть в табл bonds_archive
        conds = {'ONE' : [colName, 'IN', ds]}
        self.delete_from_table_with_where_condition_sps( tb, conds)
    
    
    
    
    def delete_from_table_with_where_condition_sps (self, tb, conds, execSQL = True):
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
        # if ms.DEBUG_:
        #     print (f"PR_130 sql = {sql}  / sqlite_processor.py / delete_from_table_with_where_condition/M405") 
        # print(f'SqliteProcessor: {sql}')
        if execSQL: # Флаг выполнения sql-запроса
            cursor = self.db_connection.cursor()
            cursor.execute(sql)
            self.db_connection.commit()
            cursor.close()
            
        return sql    

    
    
    #### END DELETE SQLs --------
    
    
    
    ##### UPDATE SQL ---------
    
    
    def update_where_in_simple_exec_sps (self, tb, updFields,  updVals, whereConds)   :
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

        sqlUpd = SQLSyntaxer.update_where_in_simple_sql(tb, updFields,  updVals, whereConds )

        cursor = self.db_connection.cursor()
        cursor.execute(sqlUpd)
        self.db_connection.commit()
        cursor.close()   
        return sqlUpd 
    
    
    
    ##### END UPDATE SQL ---------
    
    
    
    
    
    ### КОМПЛЕКСНЫЕ МЕТОДЫ ------
    


    def clear_table_sps (self, tb):
        """Отчистить польностью таблицу от всех данных"""
        self.delete_from_table_with_where_condition_sps (tb, {})
        
        

    def truncate_table_mysql_sps (self, tb):
        """
        Отчистить польностью таблицу от всех данных
        ~ https://stackoverflow.com/questions/50383106/cannot-truncate-a-table-referenced-in-a-foreign-key-constraint-in-codeigniter
        """


        
        sql = f"SET foreign_key_checks = 0"
        
        self.execute_sql_SPS(sql)
        
        sql =f"TRUNCATE {tb}"
        
        print(f"PR_NC_194 --> sql = {sql}")
        
        self.execute_sql_SPS(sql)
        
        sql = f"SET foreign_key_checks = 1"
        
        self.execute_sql_SPS(sql)
        
        
        
        
    
    
    def get_rows_difference_between_two_tbs_by_cols_val_sps (self, tb1, tb2, colNameOfTb1, colNameOfTb2):
        """Найти записи в таблице tb1, которых нет в таблице tb2, при сравнении значений колонок с названиями colNameOfTb1 и colNameOfTb2 всоответственных таблицах
        (Если в таблице 2 нет поля со значением , найденным в сравнительном поле таблицы 1, то значит такая запись считается отстствующей в таблице 2 и выводитсяв массиве результата)
        RET: Возвращает одномерный массив ключевого поля colNameOfTb1, тех рядов, которых нет в таблице tb1 по ключу этой колонки
        """

        # Параметры для первого SELECT
        selConds1 = {} # условия в части sql SELECT , если наличиствует параметр EXISTS или NOT EXISTS. '&' указывает, что это названия поля
        selFields1 = [colNameOfTb1]
        fullSelParams1 = {"tb":tb1,"selFields" : selFields1, "selConds" : selConds1}
        # Параметры для второго SELECT
        selConds2 = {} # условия в части sql SELECT , если наличиствует параметр EXISTS или NOT EXISTS. '&' указывает, что это названия поля
        selFields2 = [colNameOfTb2]
        fullSelParams2 = {"tb":tb2,"selFields" : selFields2, "selConds" : selConds2}
        sqlSelExcept = SQLSyntaxer.select_with_except_sql (fullSelParams1, fullSelParams2) # sql для выявления тех записей, которые присутствуют в bonds_current (обновленной после считывания новой оперативной выборки с сайта smart)
        cur = self.execute_sql_with_cursor_sps(sqlSelExcept) # курсор с выпоркой по результатам запроса
        dsTupArr = cur.fetchall() # массив данных результата запроса sql в виде списка таплов (которые могут иметь формат двух видов [(x1,x2 .. xN)] <type = 1>) или [(x1,),(x2,) ...]  <type = 2>
        dsList = self.get_list_from_fetch_sps(dsTupArr, 2) #  конечный результат выборки sql запроса в виде списка
        cur.close()
        return dsList
    
    
    
    def update_given_const_val_for_col_in_all_rows_sps(self, tb, col, val):
        """
        Проставить константное значение val колонки col во всех рядах таблицы
        """
        
        # Парам: 
        updFields = [col]
        updVals = [val]
        whereConds = {}
        sql = SQLSyntaxer.update_where_in_simple_sql (tb, updFields,  updVals, whereConds)
        self.execute_sql_SPS(sql) # Action: Обновить новые скопированные строки в архиве , проставить в поле f1 значение 'NOT VERIFIED'        

    
    
    
    def copy_rows_from_tb1_to_equal_tb2_which_absent_by_key_columns_sps(self, tb1, tb2, keyColName):
        """
        Скопировать те ряды из таблицы1 в !! эквивалентную !! таблицу2 , значений которых нет в ключевых одноименных колонок в тождественных таблицах
        RET: dsKeysRowsVals -  Выборка значений ключевой колонки nf,kbws1 по тем рядам, которых нет в таблице2
        """
        
        # Выборка значений ключевой колонки nf,kbws1 по тем рядам, которых нет в таблице2
        dsKeysRowsVals= self.get_rows_difference_between_two_tbs_by_cols_val_sps(tb1, tb2, keyColName, keyColName) 
        # Составление запроса SELECT IN , для выборки !!полных!! строк записей , появившихся в bonds_current, которые отсутствуют в базовом архиве bonds_archive, на основе списка названий dsList, полученных ранее 
        # Параметры:
        fields = ['*']
        dsIN = dsKeysRowsVals # 
        conds = {'ONE': [keyColName, 'IN', dsIN]}  # Условия по одному параметру
        sqlSelIN = SQLSyntaxer.select_from_table_with_where_condition_sql(tb1, fields, conds) # sql получения полных записей из bonds_current, которые отсутствуют в архиве bonds_archive
        # Копирование выборки полных записей , отсутствующих в архиве, в архив
        selSQL = sqlSelIN # sql выборки отсуствующих в архиве бумаг для вставки в архив
        sqlCopyFinal = SQLSyntaxer.insert_with_str_select_sql(tb2, selSQL) # конечный sql INSERT для копирования (вставки) 
        self.execute_sql_SPS(sqlCopyFinal) # Action: Копировать
        return dsKeysRowsVals
    
    
    
    
    
    
    
    def insert_rows_from_ds_sps (self, tb, dataSet, fieldsAccordList, prKeyInx):
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
            dsResSelect = self.select_from_table_sps(tb, qFields) # Курсор результатов запроса
            # dsCheck = self.cursor_get_all(cur) # dataSet всех строк курсора
            boolVal = self.if_exist_in_ds_sps(dsResSelect, pKeyVal) # Проверка, есть ли в dataSet фрагмент строки val

            if (boolVal) :
                print("PR_348 --> " + pKeyVal + " уже есть в БД ")
            else:
                print ("PR_349 --> " + pKeyVal + "  Внести в БД")
                # Вставка полей из текущей строки общего массива данных региона 
                self.insert_row_into_table_sps(tb, insColsVals)         



    
    def insert_row_into_table_sps (self, tbName, fieldsVals):
        """ 
        Вставляет ряд в талицу sqlite. fieldsVals - данный по одному ряду
        fieldsVals - словарь {'fieldName':'fieldValue'} 
        """
        
        sql_insert = SQLSyntaxer.insert_row_into_table_sql(tbName, fieldsVals)
        cursor = self.db_connection.cursor()
        cursor.execute(sql_insert)
        self.db_connection.commit()
        cursor.close() 
        
        return sql_insert
    
    
    
    
    
    
    def insert_from_tbsrc_to_tbtrg_with_given_fields_assoc_by_allowed_keys_sps (self, tbSrc, tbTrg, dictAssocFields, listSrcAllowedKeys, tbSrcKey, executeSQL= True):
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
            tbSrcCols = self.get_tb_fields_sps (tbSrc)
            tbTrgCols = self.get_tb_fields_sps (tbTrg)
            tbTrgColsIntersect = FG.get_intersection_of_two_list(tbTrgCols, tbSrcCols)
            dictAssocFields = FG.convert_two_lists_to_dictionary(tbTrgColsIntersect,tbTrgColsIntersect) # Превращаем два одинаковых листа в словарь
        
        sql = SQLSyntaxer.insert_from_tbsrc_to_tbtrg_with_given_fields_assoc_by_allowed_keys_sql(tbSrc, tbTrg, dictAssocFields, listSrcAllowedKeys, tbSrcKey)
        if  executeSQL: # Если флаг executeSQL = True, то запустить выполнение запроса. В ином случае - просто вернуть sql-запрос для проверки
            cursor = self.db_connection.cursor()
            cursor.execute(sql)
            self.db_connection.commit()
            print(f"PR_299 --> Executed SQL : {sql} / sqlite_processor.py/ ~ ln 996")
            cursor.close()   
        return sql    
    
    
    
    
    def _execute_sql(self, sql):
        """ 
        Выполнить запрос. Вспомогательный метод
        """
        
        cursor = self.db_connection.cursor()
        cursor.execute(sql)
        self.db_connection.commit()
    
    
    def update_given_const_vals_for_cols_by_dsKeys_sps(self, tb, updFields,  updVals, tbKeyCol, dsKeysIn):
        """Обновить значения полей в колонках заданными константами для тех записей, значения ключей которых принадлежат множеству ключей в dsKeysIn"""
        # db_processor = SqliteProcessor(DB_BONDS_)  
        # updFields = ['f1']
        # updVals = ['MATCHED']
        whereConds = {'ONE': [tbKeyCol, 'IN', dsKeysIn]}
        sqlUpd = self.update_where_in_simple_exec_sps(tb, updFields,  updVals, whereConds)

        return sqlUpd
    
    
    
    def select_all_rows_sps (self, tb, getFields):
        """Сделать выборку заданных полей getFields всех записей из таблицы """
        conds = {}
        dsRes, sql = self.select_from_table_with_where_condition_sps(tb, getFields, conds)     
        return dsRes 
    
    
    
    
    
    
    def update_row_in_tb_sps(self, tbName,  fieldsVals, uniqueKeyVal):
        """ 
        #TODO: Сделать фиксацию ключей, по которым произошло обновление, то есть набор ключей, которые найдены в таблице 
        (так как если ключ не найден, то обновления не происходит и эти данные иногда необходимо знать)
        Обновляет значения в записи, определяемой ключем  uniqueKeyVal\n
        ПРИМЕРЫ ПАРАМЕТРОВ:\n
        tb = 'comps'\n
        uniqueKeyVal = ['inn','2128702350']\n
        fieldsVals = {'okpo' : '111', 'sector' : '333'}
        """
        
        sql_update = ''
        try:
            sql_update = SQLSyntaxer.update_tb_row_with_unique_key_sql(tbName, fieldsVals,uniqueKeyVal)
            # print(f"sql_update = {sql_update} <def update_row_in_tb / sqlite_proccessor.py>")
            cursor = self.db_connection.cursor()
            cursor.execute(sql_update)
            self.db_connection.commit()
            cursor.close()    
            print(f"PR_NC_164 SYS LOG: В БД в таблице {tbName} обновлена запись через следующий SQL-запрос:\n{sql_update}\n")
        
        except sqlite3.Error as error:
            print("ERROR !!!!! PR_NC_165 --> :", error)

            # Обработка ошибок
            if 'UNIQUE constraint failed' in str(error): # Ошибка нарушения уникальности поля 
                # Выполнить поиск записи с уже существующим значением, по которому произошла ошибка нарушения уникальности поля
                errParts = str(error).split('.')
                errTb = errParts[0].split(':')[-1] # Таблица
                errField = errParts[-1] # Поле
                print (f'PR_NC_166 -->  Найдена ошибка нарушения уникальности поля {errField} при попытке обновить его новым значением {fieldsVals[errField]} в таблице {errTb} (pr: SqliteProcessor.update_row_in_tb )' )
                dsRes, sql = self.select_from_table_with_where_condition_sps(errTb,[uniqueKeyVal[0]], {'ONE': [errField, '=', fieldsVals[errField]]})
                # dsRes = self.get_ds_from_cursor(cur)
                print (f"PR_NC_167 -->  !!!! ERROR !!!: В таблице {errTb} найдена запись : {dsRes[0]} , которая в поле {errField} уже имеет значение {fieldsVals[errField]} (pr: SqliteProcessor.update_row_in_tb )" )

            sql_update = 'PR_NC_168 SQL не выполнен в результате sqlite3.Error ошибки  (pr: SqliteProcessor.update_row_in_tb )'
            print (f"PR_NC_169 -->  {sql_update}")

        finally:
            return sql_update
    
    
    
    def update_row_in_tb_by_composite_key_sps(self, tbName,  fieldsVals, uniqueCompositeKeysVals):
        """ 
        #TODO: Сделать фиксацию ключей, по которым произошло обновление, то есть набор ключей, которые найдены в таблице 
        (так как если ключ не найден, то обновления не происходит и эти данные иногда необходимо знать)
        Обновляет значения в записи, определяемой ключем  uniqueKeyVal\n
        ПРИМЕРЫ ПАРАМЕТРОВ:\n
        tb = 'comps'\n
        uniqueKeyVal = ['inn','2128702350']\n
        fieldsVals = {'okpo' : '111', 'sector' : '333'}
        """
        
        sql_update = ''
        try:
            sql_update = SQLSyntaxer.update_tb_row_with_unique_composite_key_sql(tbName, fieldsVals,uniqueCompositeKeysVals)
            print(f"PR_927 --> sql_update = {sql_update} <def update_row_in_tb / sqlite_proccessor.py>")
            cursor = self.db_connection.cursor()
            cursor.execute(sql_update)
            self.db_connection.commit()
            cursor.close()    
        
        except sqlite3.Error as error:
            print("ERROR PR_139 --> :", error)

            # Обработка ошибок
            if 'UNIQUE constraint failed' in str(error): # Ошибка нарушения уникальности поля 
                # Выполнить поиск записи с уже существующим значением, по которому произошла ошибка нарушения уникальности поля
                errParts = str(error).split('.')
                errTb = errParts[0].split(':')[-1] # Таблица
                errField = errParts[-1] # Поле
                print (f'PR_140 -->  Найдена ошибка нарушения уникальности поля {errField} при попытке обновить его новым значением {fieldsVals[errField]} в таблице {errTb} (pr: SqliteProcessor.update_row_in_tb )' )
                dsRes, sql = self.select_from_table_with_where_condition_sps(errTb,[uniqueCompositeKeysVals], {'ONE': [errField, '=', fieldsVals[errField]]})
                # dsRes = self.get_ds_from_cursor(cur)
                print (f"PR_141 -->  ERROR!!!: В таблице {errTb} найдена запись : {dsRes[0]} , которая в поле {errField} уже имеет значение {fieldsVals[errField]} (pr: SqliteProcessor.update_row_in_tb )" )

            sql_update = 'SQL не выполнен в результате sqlite3.Error ошибки  (pr: SqliteProcessor.update_row_in_tb )'
            print (f"PR_142 -->  {sql_update}")

        finally:
            return sql_update

    
    
    
    
    
    
    def set_const_marker_in_table_by_keys_sps(self, df, tb, keyColAssocDic, tbFieldConstDic):
        """ 
        Идентична update_const_vals_with_key_col_in_df_pandas. Просто изменено название иногда более понятное по смыслу
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
            self.update_row_in_tb_sps(tb, fieldsVals, uniqueKeyVal) # Обновление ряда в таблице с ключем uniqueKeyVal на основе текущего по циклу ряда фрейма

    
    
    
    
    
    
    
    
    
    def select_rows_where_col_val_is_not_empty_or_empty_sps(self, tb, getFields, col, notEmpty = True):
        """Получить выборку записей таблицы, в которых в заданном поле значение равны или неравны пустому значению или NULL или 'NOT FOUND'
        getFields - поля выборки
        notEmpty - флаг , который настравивает функцию на поиск пустых или наоборот непустых  значений в заданной колонки. По умолчанию = True,то есть поиск не пустых значений
        """
        # db_processor = SqliteProcessor(DB_BONDS_) 

        if notEmpty:
            sqloperatorNull = 'IS NOT'
            sqlOperatorEmpty = '!='
            logicOperator = 'AND'
        else:
            sqloperatorNull = 'IS'
            sqlOperatorEmpty = '='
            logicOperator = 'OR'

        # getFields = ['isin', 'okpo']
        # conds = {logicOperator:[[col, sqloperatorNull, '&NULL'], [col, sqlOperatorEmpty, ''] ]}
        conds = {logicOperator:[[col, sqloperatorNull, '&NULL'], [col, sqlOperatorEmpty, ''], [col, sqlOperatorEmpty, 'NOT FOUND'] ]}


        dsRes, sql = self.select_from_table_with_where_condition_sps(tb, getFields, conds)
        return dsRes
    
    
    
    
    def update_rows_from_ds_sps(self , tb, dataSet, fieldsInxAccordList, unqInxColVal):
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
            sql_update = self.update_row_in_tb_sps(tb,  updColsVals, unqKeyVal)
            # print (sql_update)
            
        return sql_update
    
    
    
    
    def read_table_to_df_pandas_sps(self, tb):
        """SqlitePandasProcessor
        Считывает данные таблицы из БД и возвращает прообраз таблицы в форме dataFrame
        Прим: Есть проблемы со считыванием числовых колонок , выраженных через стринги. Например Float - '0.0%'.
        Поэтому лучше использовать с теми таблицами, где нет таких форматов. Либо использовать функцию SqlitePandasProcessor.read_sql_to_df_pandas
        """
        dfTb = pd.read_sql_table(tb, self.db_uri)
        return dfTb
    
    
    
    
    def copy_tb_data_to_another_identical_cleared_tb_sps(self, tbSrc, tbTrg):
        """
        НЕ РАБОТАЕТ, Использовать copy_tb_data_to_another_identical_tb_spps() в spps
        Скопировать данные из одной таблицы в другую идентичную по структуре с предварительной очисткой целевой таблицы
        """

        # Очищаем табл bonds_curr_prev
        pandas_db_proc = SqlitePandasProcessor(DB_BONDS_)
        self.clear_table_sps(tbTrg)

        # Копируем данные из табл bonds_curr в табл bonds_curr_prev
        pandas_db_proc.copy_tb_data_to_another_identical_tb(tbSrc, tbTrg)
    
    
    
    
    def clear_column_in_tb_sps (self, tb, cols):
        """ NEW: Использовать вместо устаревшей update_set_null_to_col_in_tb()
        Проставить NULL в каждом ряду записей таблицы в поле col 
        """
        sql = SQLSyntaxer.update_where_in_simple_sql (tb, [cols],  ['&NULL'], {})
        
        print(f"PR_533 --> sql = {sql}")
        
        self._execute_sql(sql)
        return sql
    
    
    
    ### END КОМПЛЕКСНЫЕ МЕТОДЫ ------
    
    
    
    
# -- МЕТОДЫ ДЛЯ ФУНКЦИЙ _ ПАРАМЕТРОВ, КОТОРЫЕ ПЕРЕДАЮТСЯ В ВИДЕ АРГУМЕНТОВ В ДРУГИЕ ФУНКЦИИ, ВООБЩЕ ВСЕ ФУНКЦИИ НАДО СТРОИТЬ С ЭТИМ ПОДХОДОМ АВАНСОМ
# для интерактивных функций aif

    def update_rows_from_ds_PF_sps(self , dataSet, paramsDic):
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
            self.update_row_in_tb_sps(tb,  updColsVals, unqKeyVal)




# -- END МЕТОДЫ ДЛЯ ФУНКЦИЙ _ ПАРАМЕТРОВ, КОТОРЫЕ ПЕРЕДАЮТСЯ В ВИДЕ АРГУМЕНТОВ В ДРУГИЕ ФУНКЦИИ, ВООБЩЕ ВСЕ ФУНКЦИИ НАДО СТРОИТЬ С ЭТИМ ПОДХОДОМ АВАНСОМ

    
    
    
    
    
    
    
    # @transform_cursor_to_list_bmms
    # def execute_select_sql_bmms (self,sql):
    #     """Возвращает последний rowId (через декоратор - это список, где хранится послений rowID, получать через rowID[0] конечный ID) по вносимым записям через ISERT. 
    #     Нважно какой был инчер, главное, что возвращает последнее значение rowID после любого INSERT """
        
    #     cursor = self.execute_sql_with_cursor(sql)
    #     return cursor,sql
    
    
    
    ### ВСПОМОГАТЕЛЬЫНЕ МЕТОДЫ ------
    
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!! РАБОТАЕТ
    def get_ds_from_cursor_sps (self, cur): 
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
        # if ms.DEBUG_:
        #     print (f"PR_350 --> fetchN = {fetchN}")
        if fetchN == 0: # Если не найден ни один результат
            # if ms.DEBUG_:
            #     print ('PR_351 --> Не найден ни один результат')
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
    
    


    def get_list_from_fetch_sps(self, fetchDS, dsFetchType):
        """ 
        Конвертация массива из cursor.fetch() с данными из запросов , содержащихся в курсоре, в виде  списка тапла или списка таплов (пока два типа)
        в обычный список велечин [x1, x2 ...] 
        fetchDS - результат преобразования курсора после sql-операции через fetch функцию 
        type - вид данных после fetch, которые могут быть в виде списка, содержащего один тапл с величинами результата [(x1,x2 .. xN)]  <type 1>
                или содержащего список из множества таплов в виде [(x1,),(x2,) ...] <type 2>. В зависимости от типа результата после fetch() подключаются 
                разные алгоритмы преобразования в конечный список типа [x1, x2 ...]. Пока type может быть равен 1 или 2 (два типа массива результатов после fetch)
        RET:
        Возвращает список величин в виде [x1, x2 ...]
        """
        
        if dsFetchType == 1: # Первый тип массива данных после fetch() вида списка из одного тапла, содержащего величины [(x1,x2 .. xN)]
            listDS = FG.convert_list_of_one_tuple_to_list_fg(fetchDS)

        elif dsFetchType == 2: # Второй тип массива данных к преобразованию после fetch(), вида множества таплов в списке [(x1,),(x2,) ...] 
            listDS = FG.convert_list_of_tuples_to_list_fg(fetchDS)
        return listDS



    def if_exist_in_ds_sps(self,dataSet, val):
        """ OBSOLETED : Использовать if_exist_in_tb_by_multiple_keys_by_dict
        Проверяет, есть ли во всех значениях dataSet (считанный список из cursor) по всем рядам числовое значение или фрагмент строки """

        boolVal = any([val in tup for tup in dataSet])
        return boolVal



    def if_exist_in_tb_by_multiple_keys_sps(self, tb, keysNames, keyValsToCheck ):
        """ OBSOLETED : Использовать if_exist_in_tb_by_multiple_keys_by_dict, НО!!! сначала вставить этот код вместо использования ссылки на него в виде этой функции 
        в if_exist_in_tb_by_multiple_keys_by_dict
        Проверка существует ли запись в таблице по множественному ключу"""
        # Выборка всех данных из таблицы по набору сложных ключей
        cur = self.select_from_table_sps(tb, keysNames) # Курсор результатов запроса
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



    def if_exist_in_tb_by_multiple_keys_by_dict_sps(self, tb, uniqueCheckDict ):
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

        boolRes, messageStr = self.if_exist_in_tb_by_multiple_keys_sps(tb, keysNames, keyValsToCheck )

        return boolRes, messageStr
    
    
    
    



    ### END ВСПОМОГАТЕЛЬЫНЕ МЕТОДЫ ------




# -- МЕТОДЫ ПО СТРУКТУРЕ МЕТАДАННЫХ БД (должны начинатся с meta_)

    def get_tb_fields_sps (self, tb):
        """ 
        OBSOLUTED: Изменения в названии. Теперь - meta_get_tb_fields_sqlite_sps()
        Получение названий полей таблицы в списке 
        """
        sql = SQLSyntaxer.get_tb_fields_sql(tb)
        cursor = self.db_connection.cursor()
        cursor.execute(sql)
        self.db_connection.commit()
        arr = cursor.fetchall() # arr в виде списка таплов [(x1,),(x2,) ...]
        dsFields = FG.convert_list_of_tuples_to_list_fg(arr)
        # dsFields = [x[0] for x in arr]  # преобразование в список
        cursor.close()   
        return dsFields
    
    
    def meta_get_tb_fields_sqlite_sps (self, tb):
        """ Получение названий полей таблицы в списке """
        sql = SQLSyntaxer.get_tb_fields_sql(tb)
        cursor = self.db_connection.cursor()
        cursor.execute(sql)
        self.db_connection.commit()
        arr = cursor.fetchall() # arr в виде списка таплов [(x1,),(x2,) ...]
        dsFields = FG.convert_list_of_tuples_to_list_fg(arr)
        # dsFields = [x[0] for x in arr]  # преобразование в список
        cursor.close()   
        return dsFields
    
    
    
    def meta_get_tb_fields_mysql_sps (self, db, tb):
        """ 
        SqliteProcessorSpeedup
        Получение названий полей таблицы в списке по MySql
        """
        sql = SQLSyntaxer.get_tb_fields_mysql_sintax(db, tb)
        resfields = self.get_result_from_sql_exec_proc_sps(sql)
        
        # # Преобразуем в список только названий полей
        # resfields = [x[0] for x in res]
        
        return resfields
    
    
    
    
    
    
    



    def get_create_table_shema_sql_meta_sps(self, tbName):
        """
        Возвращает sql - запрос с дампом структуры заданной табдлицы (без данныхЮ только структура-схема таблицы)
        """

        getFields = ['sql']
        conds = {'AND': [['type','=','table'],['name','=', tbName]]}
        tb = 'sqlite_master'
        resSQL = self.select_from_table_with_where_condition_sps(tb, getFields, conds, add = '')

        return resSQL[0]
    
    
    




    def get_clone_new_tab_sql_of_given_table_structure_sps(self, baseTbName, newTbname):
        """Выдает SQL запрос для создания новой таблицы - клона заданнйо базовой таблицы"""
        createSQL = self.get_create_table_shema_sql_meta_sps(baseTbName)
        # print(createSQL)
        newTbCreateSQL = createSQL[0].replace(baseTbName,newTbname)
        return newTbCreateSQL




    def if_table_exist_in_db_sps (self, tbName):
        """ 
        Проверить наличие таблицы в БД
        """

        # # check if table exists
        # print('Check if STUDENT table exists in the database:')
        # listOfTables = cur.execute(
        #     """SELECT tableName FROM sqlite_master WHERE type='table'
        #     AND tableName='STUDENT'; """).fetchall()
        
        sql = SQLSyntaxer.check_if_table_exists_in_db_stx(tbName)
        res = self.get_result_from_sql_exec_proc_sps(sql)[0]
        
        # print(f"PR_597 --> res = {type(res[0])}")
            
        if res < 1 :
            print(f'PR_595 --> Table {tbName} not found!')
            ret = False
        else:
            print(f'PR_596 --> Table {tbName} found!')
            ret = True

        return ret




    def get_last_rowid_from_tb_sps (self, tb):
        """ 
        Получить последний row_id для заданнйо таблицы. ТО есть получить последний аутоинкрементный номер ключевого поля таблицы
        """

        # Получить последний ID в таблице tg_messages_proceeded (что бы иметь этот ключ для созданя записи в расширении этой таблицы в tg_message_proceeded_ext)
        sql = f"SELECT rowid from {tb} order by ROWID DESC limit 1"
        res = self.get_result_from_sql_exec_proc_sps(sql)
        lastID = res[0] # Последний ID в таблице tg_messages_proceeded (tgmp)
        # print(f"PR_A116 --> lastId = {tgmpLastId}")
        
        return lastID
    
    
    
    def get_last_inserted_id_in_db_mysql_sps (self): 
        """ 
        Поулчить последний автоинкрементное значение поля по всей БД (неважно, в какой таблице была вставка записи с автоинкрементальным полем в ней)
        """
        
        sql = f"SELECT LAST_INSERT_ID()"
        
        res = self.get_result_from_sql_exec_proc_sps(sql)
        lastID = res[0] # Последний ID в таблице tg_messages_proceeded (tgmp)
        # print(f"PR_A116 --> lastId = {tgmpLastId}")
        
        return lastID
    
    
    
    
    
    def reset_to_zero_autoincrement_key_field_of_table_sps (self, tb):
        """ 
        SqliteProcessorSpeedup
        Обнулить автоинкрементный ключ таблицы
        
        """
        
        sql = f"UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='{tb}'"
        # print(f"PR_NC_170 --> sql = {sql}")
        
        self.execute_sql_SPS(sql)
        print(f"PR_NC_172 --> SYS LOG: Обнулено автоинкрементное поле таблицы {tb}")
    
    
    
    def clear_tb_and_reset_autoincrement_to_zero (self, tb):
        """ 
        Очистить таблицу от записей и обнулить автоинкрементный ключ таблицы
        """
    
        self.clear_table_sps(tb)
        print(f"PR_NC_171 --> SYS LOG: Удалены все записи из таблицы {tb}")
        self.reset_to_zero_autoincrement_key_field_of_table_sps(tb)
        
        

    

    

        

# -- END МЕТОДЫ ПО СТРУКТУРЕ МЕТАДАННЫХ БД    




    def insert_record_to_tb_with_many_to_many_relation (self, tb, dicInsertData):
        """ 
        Вставиь запись в таблицу , которая регестрирует связи многие-ко-многим
        dicInsertData = {
            'field1' : intVal1,
            'field2' : intVal2
        }
        """
        print(f"PR_NC_178 --> START: insert_record_to_tb_with_many_to_many_relation()")

        
        #INI
        keysList = list(dicInsertData.keys())
        valList = list(dicInsertData.values())
        
        sql = f"INSERT INTO {tb} ({keysList[0]}, {keysList[1]})  VALUES ({valList[0]}, {valList[1]})"
        
        # print(f"PR_A248 --> sql = {sql}")
        self.execute_sql_SPS(sql)
        
        print(f"PR_NC_173 -->  SYS DB LOG: внесена запись {dicInsertData} в таблицу многие-ко-многим {tb} ")

        print(f"PR_NC_179 --> END: insert_record_to_tb_with_many_to_many_relation()")
        
        return sql




    @staticmethod
    def transform_list_valuews_to_sql_string_for_tuple_inside_sps (listValues):
        """ 
        Преобразовать список значений в sql-строку для вставки в выражение IN ()
        """

        listValues = [str(x) for x in listValues]
        
        listValuesSql = ",".join(listValues)
        
        return listValuesSql




if __name__ == "__main__":
    pass



    # # ПРОРАБОТКА: update_row_in_tb_by_composite_key_sps(tbName,  fieldsVals, uniqueCompositeKeysVals)
    
    # tb = 'comp_bond_analisys'
    # fieldsVals = {
    #     'comp_bonds_analisys' : 'ООО "СЕЛЛ-Сервис" RU000A104KM0',
    #     'inx_pckg_decided_id' : 5,
    # }
    
    # uniqueCompositeKeysVals = {
    #     'inn' : '5406780551', 
    #     'isin' : 'RU000A104KM0',
    # }
    
    
    # sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)
    
    # sps.update_row_in_tb_by_composite_key_sps(tb,  fieldsVals, uniqueCompositeKeysVals)













