# from asyncio.windows_events import NULL
#from asyncio.windows_events import NULL
# from bonds.algorithms_settings import *
# from bonds.settings import *
# from Switch import *
from noocube.switch import Switch
import noocube.funcs_general as FG
from noocube.funcs_general import strip_by_reg
from noocube.structures import SelectUnionStructure

# import numpy as np

class SQLSyntaxer ():
    """ Класс предназначен для формирования синтаксических запросов, общих для языка  SQL """

    def __init__(self):
        pass


    ## -- ДЕКОРАТОРЫ ---
    # https://pythonworld.ru/osnovy/dekoratory.html

    # Дек: Для вывода запросов sql, возвращающих выборки в курсоре, в виде уже готовых массивов (списков)
    
    def add_sql_order_part(func_to_decorate):
        """Добавляет к SQL- запросу часть с сортировкой типа ORDER BY. Для этого в дкорируемом методе должен быть добавлен именной аргумент с названием listOrder ,
        который содержит спсок названий полей для сортировки и, при необходимости задать направление сортировки, с добавочным операндом направления ASC/DESC
        
        Пример использования декоратора для метода формирования простого SQL-запроса, в который нужно добавить часть ORDER BY :
        
        @add_sql_order_part
        @staticmethod  
        def select_tbs_union_sql (listUnionsStructurePars, unionAll = True, listOrder = None): ...
        
        Пример декорируемого метода:

        sql = SQLSyntaxer.select_tbs_union_sql (listUnionsStructurePars, unionAll = True, listOrder = listOrder)
        
        Пример задания listOrder:
        
        listOrder = [
            'isin ASC',
        ]
        """
        
        @staticmethod  
        def wrapper(*args, **kwargs):
            sql = func_to_decorate(*args, **kwargs)
            
            if 'listOrder' in kwargs: # Проверка наличия ключа
                if kwargs ['listOrder']: # Если kwargs ['listOrder'] не равен None
                    sqlOrder = f"{kwargs ['listOrder']}".replace("\'","").replace('[','').replace(']','')
                    sql += f" ORDER BY {sqlOrder}"
                    

            return sql

        return wrapper



    def add_sql_where_part(func_to_decorate):
        """Добавляет к SQL- запросу часть с условиями типа WHERE. Для этого в дкорируемом методе должен быть добавлен именной аргумент с названием whereCond, который 
        содержит словарь условий, на базе нашего стандарта , описанного в методе select_from_table_with_where_condition_sql() и реализуемом в методе _get_where_clause_sql ()
        в sql_syntaxer.py. whereCond не должен быть равен нулю и должен содержать хотя бы одно условие. В ином случае WHERE часть будет отсутствовать в SQL
        Кроме того, в ЗАГОТОВКАХ недо реализовать так же и через структуру WhereStructure в structures.py TODO: Доработать
        
        Пример использования:
        
        whereCond = {
            'ONE'  : ['fieldName1', '<', 5]
        }

        sql = SQLSyntaxer.select_tbs_union_sql (listUnionsStructurePars, unionAll = True, listOrder = listOrder, whereCond = whereCond)

        """
        
        @staticmethod  
        def wrapper(*args, **kwargs):
            sql = func_to_decorate(*args, **kwargs)
            
            if 'whereCond' in kwargs and kwargs ['whereCond'] != None: # Проверка наличия ключа , что он не равен None
                condsN = len(kwargs ['whereCond'])
                if condsN > 0: # Если заданы условия в параметре whereCond
                    
                    sqlCond = SQLSyntaxer._get_where_clause_sql (kwargs ['whereCond'])
                    sql += f" WHERE " +  sqlCond

            return sql

        return wrapper



    ## -- END ДЕКОРАТОРЫ ---



# -- БАЗОВЫЕ ЗАПРОСЫ SQL

    @staticmethod    
    def update_tb_row_with_unique_key_sql (tb, fieldsVals, uniqueKeyVal):
        """ 
        Update запись (ряд) в таблице БД с уникальным значением в задаваемом поле uniqueKey\n
        <ПРИМЕЧАНИЕ: в методе производится замена одинарной кавычки в значениях TEXT  на бинарные!!! >\n
        fieldsVals - словарь {поле1 - значение1, ...} изменяемых значений\n
        uniqueKeyVal - поле ключа и его значение,  по которому происходит идентификация записи (ряда) в таблице БД. Уникальный индекс \n
        ПРИМЕРЫ ПАРАМЕТРОВ:\n
        uniqueKeyVal = ['inn','2128702350']\n
        fieldsVals = {'float' : 5.76, 'kavych' : 'ООО \'Абис\'', 'int': 56}
        """

        setPartSql = ''
        
        for key, value in fieldsVals.items(): # цикл по полям в одной записи по ряду
            # # проверка на тип данных. В общем все значения можно переводить в стринги, так как при вставке значения будут
            # #  трансформироваться в по типу полей в БД автоматом процессами в самом sqlite 
            if 'str' in str(type(value)): # если str, то заключить значение в кавычки одноразовые
                value = value.replace('\'', '"') # заменить все ' на ", что бы не было неразберихи с кавычками
                setPartSql += f"{key} = '{value}',"
            else: # иначе - просто значение
                setPartSql += f'{key} = {value},'

        setPartSql = setPartSql.rstrip(',') # очищаем от последней запятой

        key = uniqueKeyVal[0] # название ключевого поля
        keyVal = uniqueKeyVal[1] # значение ключа

        if 'str' in str(type(keyVal)):  # если str, то заключить значение в кавычки одноразовые
            kVal = f"'{keyVal}'" # Значение уникального поля, по которому формируется условие WHERE

        udate_sql = f'UPDATE {tb} SET {setPartSql} WHERE {key} = {kVal}'
        print(f"PR_NC_163 --> udate_sql = {udate_sql}")

        return udate_sql
    
    
    @staticmethod    
    def update_tb_row_with_unique_composite_key_sql (tb, fieldsVals, uniqueCompositeKeysVals):
        """ 
        Update запись (ряд) в таблице БД с уникальным значением в задаваемом поле составного ключа uniqueKey\n
        <ПРИМЕЧАНИЕ: в методе производится замена одинарной кавычки в значениях TEXT  на бинарные!!! >\n
        fieldsVals - словарь {поле1 - значение1, ...} изменяемых значений\n
        uniqueCompositeKeysVals - словарь названий ключей и их значений, по которым идентифицируется запись в таблице
        ПРИМ: в словаре fieldsVals не должно быть полей из составного ключа uniqueCompositeKeysVals
        """

        setPartSql = ''
        
        for key, value in fieldsVals.items(): # цикл по полям в одной записи по ряду
            # # проверка на тип данных. В общем все значения можно переводить в стринги, так как при вставке значения будут
            # #  трансформироваться в по типу полей в БД автоматом процессами в самом sqlite 
            if 'str' in str(type(value)): # если str, то заключить значение в кавычки одноразовые
                value = value.replace('\'', '"') # заменить все ' на ", что бы не было неразберихи с кавычками
                setPartSql += f"{key} = '{value}',"
            else: # иначе - просто значение
                setPartSql += f'{key} = {value},'

        setPartSql = setPartSql.rstrip(',') # очищаем от последней запятой

        # Формирууем значения для множественного условия WHERE
        whereStr = ''
        for key, value in uniqueCompositeKeysVals.items():
            
            if isinstance(value, str):  # если str, то заключить значение в кавычки одноразовые
                value = f"'{value}'" # Значение уникального поля, по которому формируется условие WHERE
                
            whereStr += f"{key} = {value} AND "
            
        whereStr = whereStr.rstrip('AND ')



        udate_sql = f'UPDATE {tb} SET {setPartSql} WHERE {whereStr}'
        print(f"PR_NC_164 --> udate_sql = {udate_sql}")

        return udate_sql
    


    @staticmethod    
    def update_where_in_simple_sql (tb, updFields,  updVals, whereConds):
        """ Функция простейшего UPDATE с WHERE IN по выборке из SELECT запроса, или по простому списку величин для задаваемого поля. 
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
        updSQL = f"UPDATE {tb} SET "
        if '*' in updFields[0]: # Если все поля для обновления
            pass
        else: # Если определенные поля, заданные в параметре updFields
            # value = SQLSyntaxer._value_analisis_for_where_conds(updVals[i])
            # создание списка с форматом [field1 = val1, field2 = val2 ...]. Прим. При анализе  формата и типа значения величины, задаваемой в параметре ,  SQLSyntaxer._value_analisis_for_where_conds важно в каких апострофах или двойных кавычках задается  replace('"','') <нужно именно так>

            updSets = ''
            for i in range(len(updFields)): # Анализ полей и значений в цикле и составление части  ... SET
                pass
                field = updFields[i]
                value = SQLSyntaxer._value_analisis_for_where_conds(updVals[i])
                updSets += f'{field} = {value},'

            updSets = updSets[:-1] # удаление последней запятой в конечной части sql для SET

        sql = f"{updSQL} {updSets} WHERE "

        sqlCond = ''
        condsN = len(whereConds)
        if condsN > 0: # Если заданы условия в параметре conds
            sqlCond = SQLSyntaxer._get_where_clause_sql (whereConds) # Обработка для стандартных условий whereConds
        else: # if condN > 0 . Если нет условий conds, то вычитаем WHERE из предложения sql
            sql = sql.rstrip('WHERE')

        sql += sqlCond
        sql = sql.rstrip(' WHERE') # очистка от where, вслучае, если нет никаких условий для удаления (ключ: All или NO)        
        
        return sql



    @staticmethod    
    def update_tb1_from_select_tb2_simple_sql (tb1,tb2, fieldsTb1, fieldsTb2, condsUpdTb1 = {} , condsSelTb2 = {}  ):
        """ Обновление данных полей в первой таблице из соответсвующих полей второй таблицы на основе условий, сочитающих в себе поля из обоих таблиц 
        fieldsTb1 - поля для выборки UPDATE 
        fieldsTb2 - поля для выборки SELECT по каждому полю из fieldsTb1 (размеры списков fieldsTb1 и fieldsTb2 должны быть равны, а типы значений величин - одинаковы для каждого поля выборки SELECT и UPDATE)
        condsSelTb2 - условия WHERE для выборок SELECT для каждого из полей fieldsTb1 (всегда одинаковые для всех полей fieldsTb1 -поэтому и simpe в названии функции Простой вариант функции)
        condsUpdTb1 - условия WHERE для части UPDATE для первой таблицы
        """
        sql = f'UPDATE {tb1} SET '
        for field in fieldsTb1:  # цикл по полям fieldsTb1
            pass
            sql += f' {field} = ('
            selSQL = SQLSyntaxer.select_from_table_with_where_condition_sql (tb2, fieldsTb2, condsSelTb2)
            sql += f' {selSQL} ) ,'
        sql = sql.rstrip(',')
        if len(condsUpdTb1) >0: # Если есть условия в словаре condsUpdTb1 для UPDATE части первой таблицы tb1, то
            # sql += f' WHERE ' # Условие WHERE для части UPDATE tb1
            updWhereSql = SQLSyntaxer._get_where_clause_sql (condsUpdTb1)
            sql += f' WHERE {updWhereSql}'
        return sql








    @staticmethod
    def insert_row_into_table_sql (tb_name, fieldsVals):
        """ Формирует sql -запрос на вставку одного ряда заданных величин в заданную таблицу\n
        <ПРИМЕЧАНИЕ: в методе производится замена одинарной кавычки в значениях TEXT  на бинарные!!! >\n
        fieldsVals - словарь {'fieldName':'fieldValue',  ...} """

        colPartSql = ''
        valPartSql = ''
        
        for key, value in fieldsVals.items(): # цикл по полям в одной записи по ряду
            colPartSql += f'{key},'

            # проверка на тип данных. В общем все значения можно переводить в стринги, так как при вставке значения будут
            #  трансформироваться в по типу полей в БД автоматом процессами в самом sqlite 
            if 'str' in str(type(value)): 
                value = value.replace('\'', '"') # заменить все ' на ", что бы не было неразберихи с кавычками
                valPartSql += f"'{value}',"
            elif 'int' in str(type(value)) or 'float' in str(type(value)):
                valPartSql += f'{value},'
            else:
                valPartSql += f"NULL," # если пустое поле, то вставляем None

        colPartSql = colPartSql.rstrip(',')
        valPartSql = valPartSql.rstrip(',')
        sql =  f"INSERT INTO {tb_name} (" + colPartSql + ") VALUES ( " + valPartSql + ");"
        # print ('\n')
        print (f"PR_NC_226 --> sql = {sql}")
        return sql


    @staticmethod
    def insert_general_sql (tbIns, fieldsIns, valsIns, onConflicts = '', sqlSelParams = {}):
        # TODO: Дорабатывать метод различными прочими вариациями
        """  Формирует разные  запросы   INSERT, в том числе со вставкой SELECT
        Виды запросов:\n
        1. Формирование sql, если нет SELECT парметров  и ввод идет по всем полям равным структуре таблицы / INSERT INTO table VALUES (...),(...),... \n
        2. Формирование sql, если все поля и есть SELECT параметры / INSERT INTO artists  SELECT ArtistId, Name FROM artists\n
        3. Формирование sql, если задан список полей и нет SELECT параметров / INSERT INTO table (column1,column2 ,..) VALUES (...),(...),... \n
        4. Формирование sql, если задан список полей и есть SELECT параметры / INSERT INTO table (field1,field2,..fieldN) SELECT f1, f2,...fN FROM ...\n

        fieldsIns - [field1, field2, ... fieldN] or ['*'] - список полей для вставки в части INSERT (f1, f2 ...)... VALUES (v1, v2 ...). Если '*' то все поля, то кол-во полей SELECT д.б. = tb \n
        valsIns -  [[val1, val2, ... valN], [val1, val2, ... valN]]  - список велечин для полей вставки в части INSERT (f1, f2 ...)... VALUES (v1, v2 ...). Д.б. = fields или ['*'], если все поля
                Если спиок в списке, то несколько записей. ['*'] - только, если есть String SELECT. Тогда это обозначает , что все поля из SQLECT, кол-во которых должно быть = всем полям таблицы , в которую идет ISERT и 
                VALUES () вообще не проставляется. Собственно это может вытекать из парсинга SELECT ! \n
        sqlSelParams - парметры SELECT запроса, если он участвует в INSERT\n
        onConflicts - String, условия по конфликту IGNORE or REPLACE (и еще 5 других) - * https://database.guide/how-on-conflict-works-in-sqlite/\n
        \nПРИМЕРЫ применения внизу этого файла sql_sintaxer.py
        """
        sql = ' INSERT '
        # Анализ парметра по решению конфликту, если он задан
        if len(onConflicts) > 0: # если задано условие по конфликту
            sql += f' OR {onConflicts}'

        sql += f' INTO {tbIns} '

        # Анализ списка задаваемых полей в INSERT. Если стоит * , то - все поля и список полей (f1, f2, ... fN) вообще не нужен. 
        # Но тогда список значений по полям по количеству должен быть равен структуре таблицы по полям
        if '*' in fieldsIns[0]: # Если есть * в первом поле списка, то значит, что должен быть представлен список велечин полей в соответсвии со структурой таблицы
            print (f"\nPR_360 --> В списке полей присутствует *, значит список велечин VALUES() вносимых д.б. = структуре таблицы или из SELECT\n")
            fieldFalg = 0 # Все поля
            # print (f"fieldFalg = {fieldFalg}")
        
        else: # Если нет *, значит идет список полей для INSERT и их значения в списке значений соответственно по количеству
            print (f"\nPR_361 --> В списке полей отсутствует *, значит есть список задаваемых полей (f1, f2, ... fN) и список их значений VALUES()\n")
            fieldFalg = 1 # список полей
            # print (f"fieldFalg = {fieldFalg}")
        
        # Анализ sqlSelParams - есть ли задача сформировать SELECT часть запроса
        selParamsN = len (sqlSelParams) # Кол-во записей в параметрах по SELECT части
        if selParamsN > 0: # Если есть параметры по SELECT запросу, значит необходимо сформировать его в sql для вставки записей оттуда
            print (f"\nPR_362 --> Присутствуют параметры SELECT запроса в sqlSelParams. Д.б. сформирован SELECT для вставки\n")
            selFlag = 1
            # print (f"selFlag = {selFlag}")# -- ЗАПРОСЫ JOIN ------

        else: # Параметры SELECT запроса отсутствуют, значит вносимые ряды формируются за счет чисто INSERT sql
            print("\nPR_363 --> Параметры SELECT запроса отсутствуют, значит вносимые ряды формируются за счет чисто INSERT sql\n")
            selFlag = 0
            
        # Формирование части INSERT по полям и и вносимым значениям
        # 1. Формирование sql, если нет SELECT парметров  и ввод идет по всем полям равным структуре таблицы
        if (fieldFalg == 0 and selFlag ==0):
            print ("PR_364 --> RES: 1.Формирование , если нет SELECT парметров  и ввод идет по всем полям равным структуре таблицы\n")
            valsPart = f" VALUES{valsIns}".replace('[','(').replace(']',')') # часть ISERT VALUES (...) / replace заменяет квадратные скобки списка на круглые
            valsPart = valsPart.replace('((','(').replace('))',')') # Заменяет двойные круглые скобки на одинарные , чтобы получить нужный вид множественной вставки велечин для нескольких строк

            sql += valsPart.replace('((','(').replace('))',')') # Еще раз превратить двойные скобки в одинарные. В некоторых случаях vals передается с трйоным вложением списков #TODO: Проверить в частности функцию SmartlabManager.get_bonds_sorted_with_limit_condition  

        # 2. Формирование sql, если все поля и есть SELECT параметры  
        elif (fieldFalg == 0 and selFlag == 1):
            print ("PR_365 --> RES: 2.Формирование sql, если все поля и есть SELECT параметры\n")
            # Par:
            tbSel = sqlSelParams['tb']
            getSelFields = sqlSelParams['getSelFields']
            conds = sqlSelParams['conds']
            sqlSelect = SQLSyntaxer.select_from_table_with_where_condition_sql (tbSel, getSelFields, conds)
            # print (f'sqlSelect = {sqlSelect}')   
            sql +=  sqlSelect        

        # 3. Формирование sql, если задан список полей и нет SELECT параметров
        elif (fieldFalg == 1 and selFlag == 0):
            print ("PR_366 --> RES: 3.Формирование sql, если задан список полей и нет SELECT параметров. Сисок полей  SELECT д.б. = списку полей INSERT (f1, f2 ..fN)\n")
            fieldsPart = f" {fieldsIns} ".replace('[','(').replace(']',')') # Часть по полям
            valsPart = f" VALUES {valsIns} ".replace('[','(').replace(']',')') # Часть по значениям / replace - заменяет квадратные скобки на крулые
            valsPart = valsPart.replace('((','(').replace('))',')') # Заменяет двойные круглые скобки на одинарные , чтобы получить нужный вид множественной вставки велечин для нескольких строк
            sql += f" {fieldsPart} {valsPart}".replace('((','(').replace('))',')') # Еще раз превратить двойные скобки в одинарные. В некоторых случаях vals передается с трйоным вложением списков #TODO: Проверить в частности функцию SmartlabManager.get_bonds_sorted_with_limit_condition  

        # 4. Формирование sql, если задан список полей и есть SELECT параметры
        elif (fieldFalg == 1 and selFlag == 1):
            print ("PR_367 --> RES: 4.Формирование sql, если задан список полей и есть SELECT параметры. Сисок полей  SELECT д.б. = списку полей INSERT (f1, f2 ..fN)\n")
            # Par:
            tbSel = sqlSelParams['tb']
            getSelFields = sqlSelParams['getSelFields']
            conds = sqlSelParams['conds']
            sqlSelect = SQLSyntaxer.select_from_table_with_where_condition_sql (tbSel, getSelFields, conds) # sql Часть SELECT
            # print (f'sqlSelect = {sqlSelect}')   
            insFields = f"{getSelFields}".replace('[','(').replace(']',')') # sql часть INSERT , отвечающая за поля (f1, f2, ...,fN) / replace заменяет квадратные скобки списка на круглые
            sql +=  f" {insFields} " + sqlSelect  

        return sql


    @staticmethod 
    def insert_with_str_select_sql(tbIns, selSQL):
        """ Формирование  sql - запроса INSERT wuth SELECT , где сформированная конечная SELECT часть передается в виде параметра и из него определяются поля для INSERT.
        """
        sql = f'INSERT INTO {tbIns} '

        # Парсинг selSQL для определения полей. Если '*' в первой SELECT (он может быть комплексным и состоять из нескольких SELECT), то все поля. Или вычислить названия полей для INSERT
        if '*' in selSQL: # Если все поля для вывода в первой части SELECT, то в INSERT вообще не проставляются поля
            fieldsSqlpart = ''
        else: # Если не тзвездочки, то надо вычислить поля при помощи парсинга
            # Парсинг selSQL для вычисления полей для вставки
            selParts = selSQL.split('SELECT') # Рассекаем selSQL по 'SELECT'
            selPartFirst = selParts[1] # СТринг после первой SELECT  и до следующей SELECT, если она есть. Часть откуда надо вычислить поля для вставки INSERT
            # Отделяем первую SELECT от FROM-part# -- ЗАПРОСЫ JOIN ------ часть списка последним словом будет название поля
            fieldsPartsNotCleared = selPartFirstNoFrom.split(',')
            fieldsPartsNotCleared = [x.strip(' ') for x in fieldsPartsNotCleared] # Удаляем все пробелы в начале иконце каждой части в списке частей с полями
            # Вычиляем поля из частей fieldsPartsNotCleared, разделяя сначала каждый элемент по пробелу (если есть слово впереди названия поля) и затем берем последний элемент, который и будет = названию поля
            fields = [] # пустой список для выявленных полей
            for fieldPart in fieldsPartsNotCleared: # Цикл по списку нечистых частей с поялми
                field = fieldPart.split(' ')[-1] # последний элемент при разделении нечистых частей с полями
                # print (field)
                fields.append(field)
            fieldsSqlpart = f" {fields}".replace('[', '(').replace(']',')') # Заменяем квадратные скобки в отпечатанном списке полей на круглые
            fieldsSqlpart = fieldsSqlpart.replace("'", "") # Убираем апострофы в названиях полей в стринге (поля в INSERT идут без апострофов)

        sql += f"{fieldsSqlpart} {selSQL}" # конечный sql-запрос
        return sql
    


    @staticmethod        
    def select_from_table_sql (tb,fields):
        """ SELECT from tb by fields. fields - список полей или * """

        sql = 'SELECT ' 
        felds_part_sql = ''
        for field in fields:
            felds_part_sql  += f'{field},'

        felds_part_sql = felds_part_sql.rstrip(',')

        sql = sql + felds_part_sql + f' FROM {tb}'
        return sql

    @staticmethod        
    def select_from_table_with_where_condition_sql (tb, getFields, conds = {}, add = ''):
        """ Class: SQLSyntaxer
        Conditional SELECT from tb by fields . fields - список полей или *
        Выборка из таблицы по  условиям WHERE для простого SELECT . В качестве условий могут выступать арифметические условия, а так же IN/NOT IN для для формирования
        условий WHERE IN (...). В последнем случае в качестве значения dsIN условия могут быть либо sql стринг типа 'SELECT * FROM ...', создающий выборку (типа SELECT * FROM tb WHERE field IN ( SELECT ... )  ).
        Или простой список величин для  осуществления поиска в них заданного поля основного SELECT (типа SELECT * FROM tb WHERE field IN ( 1,2,... ) )
        
        Если ключ в словаре условий стоит ALL или NO , то выборка -  все записи из таблицы
        getFields - список ['field1','field2' или '*']
        conds - список с условиями типа {
                                            'OR' : [['fieldName1', '<', 5], ['fieldName2', '>', 15]], 
                                            'AND' : [['fieldName3', '<', 5], ['fieldName4', '>', 15]], /
                                            'ONE'  : ['fieldName1', '<', 5],/
                                            'ALL or NO'   : None, / <или иначе - без всяких условий>
                                            'STR' : '(fieldName1 > 5 AND fieldName2 < 15) AND (...)'
                                            }# -- ЗАПРОСЫ JOIN ------
                Если conds = {} или не заданы вовсе (по умолчанию {}), то SELECT sql формируется без условий WHERE

        add - стринговая добавка в ручную, типа, GROUPED BY и т.д.
                """

        # print(f"3. F: select_from_table_with_where_condition_sql")                                     
        sql = 'SELECT ' 
        felds_part_sql = ''
        for field in getFields:
            felds_part_sql  += f'{field},'
        felds_part_sql = felds_part_sql.rstrip(',')
        sql = sql + felds_part_sql + f' FROM {tb} WHERE'
        sqlCond = ''
        condsN = len(conds)
        if condsN > 0: # Если заданы условия в параметре conds
            sqlCond = SQLSyntaxer._get_where_clause_sql (conds)

        else: # if condN > 0 . Если нет условий conds, то вычитаем WHERE из предложения sql
            sql = sql.rstrip('WHERE')

        sql += sqlCond
        sql = sql.rstrip(' WHERE') # очистка от where, вслучае, если нет никаких условий для удаления (ключ: All или NO)

        if len(add) > 0: # Если есть добавка add
            sql += f' {add}'
            
        return sql






    @staticmethod 
    def select_with_except_sql (fullSel1Pars, fullSel2Pars):
        """ Функция SELECT c EXCEPT , для 2х таблиц только
        Выдает записи, которые присутствуют в Dataset1 и их нет в Dataset2
        """
        # Расшифровка параметров:
        tbSel1 = fullSel1Pars['tb']
        selFields1 = fullSel1Pars['selFields'] # Поля для вывода в SELECT
        selConds1 = fullSel1Pars ['selConds'] # Условия для SELECT WHERE
        tbSel2 = fullSel2Pars['tb']
        selFields2 = fullSel2Pars['selFields'] # Поля для вывода в SELECT
        selConds2 = fullSel2Pars ['selConds'] # Условия для SELECT WHERE
        sqlSel1 =  SQLSyntaxer.select_from_table_with_where_condition_sql(tbSel1, selFields1, selConds1)
        sqlSel2 =  SQLSyntaxer.select_from_table_with_where_condition_sql(tbSel2, selFields2, selConds2)
        sql = sqlSel1 + ' EXCEPT ' + sqlSel2
        return sql



    @staticmethod 
    def select_diffr_rows_keys_in_two_tabs_by_key_cols_sql (tbSrc, tbTrg, listKeysPair, exept = True):
        """Найти ключи первой таблицы, которые отсутствуют или присутствуют во второй таблице
        tbSrc - источник поиска ключей
        tbTrg - цель, с которой сравниваются ключи источника
        listKeysPair - спсиок названий ключей в таблице источнике и цели ['fieldKeySrc', 'fieldKeyTrg']
        exept - флаг отсутствуют или присутствуют. По умолчанию - отсуствуют
        """
        if exept:
            logOperand = 'NOT IN'
        else:
            logOperand = 'IN'
        
        sql = f'SELECT {listKeysPair[0]} FROM {tbSrc} WHERE {listKeysPair[0]} {logOperand} (SELECT {listKeysPair[1]} FROM {tbTrg})'
        return sql




    @staticmethod        
    def delete_from_table_with_where_condition_sql (tb, conds):
        """ Conditional DELETE from tb with conds . 
        Если ключ в словаре условий стоит ALL или NO , то удаляет все записи из таблицы
        condition - список с условиями типа {
                                            'OR' : [['fieldName1', '<', 5], ['fieldName2', '>', 15]], 
                                            'AND' : [['fieldName3', '<', 5], ['fieldName4', '>', 15]], /
                                            'ONE'  : ['fieldName1', '<', 5],/
                                            'ALL or NO'   : None, / <или иначе - без всяких условий>
                                            'STR' : '(fieldName1 > 5 AND fieldName2 < 15) AND (...)'
                                            }"""
        sql = f'DELETE FROM {tb} WHERE' 


        sqlCond = ''
        condsN = len(conds)
        if condsN > 0: # Если заданы условия в параметре conds
            sqlCond = SQLSyntaxer._get_where_clause_sql (conds)

        else: # if condN > 0 . Если нет условий conds, то вычитаем WHERE из предложения sql
            sql = sql.rstrip('WHERE')

        sql += sqlCond
        sql = sql.rstrip(' WHERE') # очистка от where, вслучае, если нет никаких условий для удаления (ключ: All или NO)

        # if DEBUG_:
        #     print(f"PR_368 --> sql = {sql} / sql_sintaxer.ru/ delete_from_table_with_where_condition_sql() / M421")

        return sql


    # TODO: CURRENT WORK ON IT
    @staticmethod        
    def delete_with_exists_for_2tb_sql (tbDel, tbSel, condsDel, fullSelParams, exists = ''):
        """ Delete using EXISTS Condition with simple one-field condition 
            exist - параметр из тапла ('', 'EXISTS', 'NOT EXISTS'). Если '' - то его вообще нет
            Если EXISTS, то удаляет все записи, которые соответствуют в таблице SELECT. (ТАк можно искать новые записи в bonds_curr)
            Если NOE EXISTS, то удаляет те записи, которые не присутствуют в таблице  SELECT 
            $TODO: Дорабатывать по необходимости появления новых форматов подобных запросов
            $TODO: Возможно база этой функции может быть использована для вообще универсальнйо функции составления  DELETE запроса
            ПРИМЕР использования внизу класса !!!
        """
        # Проработка DELETE части sql с возможными условиями
        sql = f'DELETE FROM {tbDel} ' 

        delWHERE = SQLSyntaxer._get_where_clause_sql (condsDel) # WHERE часть  DELETE предложения в sql
        sql += f" {delWHERE}"


        # sql = sql.rstrip(' WHERE') # очистка от where в предложении с DELETE, вслучае, если нет никаких условий для удаления (ключ: All или NO) и нет условий EXISTS

        existsN = len(exists) # обьем стринга параметра exists

        if existsN > 0 and 'WHERE' not in delWHERE: # если есть условия по EXISTS и нет других условий WHERE по DELETE (есть ключ: All или NO в словаре условий по DELETE)
            sql += f" WHERE {exists} ( "


            # Проработка SELECT  части sql с условиями (условия точно есть, так как эта часть включается только тогда, когда есть EXISTS)
            
# {"selFields" : selFields, "selConds" : selConds}
            # Расшифровка параметров из fullSelParams
            tb = fullSelParams['tb']
            selFields = fullSelParams['selFields'] # Поля для вывода в SELECT
            selConds = fullSelParams ['selConds'] # Условия для SELECT WHERE
            selSQL = SQLSyntaxer.select_from_table_with_where_condition_sql(tb, selFields, selConds)

            sql += f" {selSQL} )" 
            # TODO: Получение  SELECT запроса из параметров. Продумать передачу параметров по SELECT, что бы пользоваться в полном обьеме универсальнйо функцией select_from_table_with_where_condition_sql
            
            # selWHERE = SQLSyntaxer.get_where_clause_sql (consSel)
            # sql += f" {selWHERE}" 

        return sql



    @staticmethod  
    def insert_from_tbsrc_to_tbtrg_with_given_fields_assoc_by_allowed_keys_sql (tbSrc, tbTrg, dictAssocFields, listSrcAllowedKeys, tbSrcKey):
        """Вставить записи из таблицы -источника из заданных полей в таблицу-цель в заданные соотвтетсвующие поля и в соотвтетствии со списком значений разрешающих вставку ключей 
        из таблицы-источнике. В таблицах названия полей и их кол-во могут не совпадать. Главное, задать  соотвтетсвие полей цели (ключи словаря) и полей источника (значения словаря)
        tbSrc - источник
        tbTrg - цель
        dictAssocFields - словарь ассоциаций между полями источника и цели. Если поля одигаковы, то ключи и их значения в словаре будут равны. Иначе ключами словаря задаются поля 
        таблицы-цели, а значениями поля таблицы - истоника
        Если вместо словаря ассоциаций dictAssocFields передается '*', то это означает, что все поля в таблице источнике и таблице цели одинаковы по названию и их количеству и 
        записи вставляются дупликатом полностью
        
        listSrcAllowedKeys - список разрешенных значений ключей источника для вставки записей по ним в цель
        tbSrcKey - название поля-ключа в источнике
        
        """
        
        if 'str' in str(type(dictAssocFields)) and  '*' in dictAssocFields:
            listTrgFieldsSql = ''
            listSrcFields = '*'
        
        else:
            listTrgFields = list(dictAssocFields.keys())
            listTrgFieldsSql = f"({listTrgFields})" # Вставка со скобками, что бы отделить случай, если вдруг будет '*' (все поля идентичны в таблицах), в котором скобки не нужны
            listSrcFields = list(dictAssocFields.values())
            

        sql1 = f"INSERT INTO {tbTrg} {listTrgFieldsSql} SELECT {listSrcFields}  FROM {tbSrc} WHERE {tbSrcKey} IN "
        sql1 = sql1.replace("\'", "").replace("[", "").replace("]", "")
        
        sql2 = f"({listSrcAllowedKeys})"
        sql2 = sql2.replace("[", "").replace("]", "")
        
        sql = sql1 + sql2
        
        return sql



    @staticmethod  
    def update_from_tbsrc_to_tbtrg_with_given_fields_assoc_by_allowed_keys_sql (tbSrc, tbTrg, dictAssocFields, listSrcAllowedKeys, tbsKeysPair):
        """Обновить записи из таблицы -источника из заданных полей в таблице-цели в заданные соотвтетсвующие поля и в соотвтетствии со списком значений разрешающих вставку ключей 
        из таблицы-источника. В таблицах названия полей и их кол-во могут не совпадать. Главное, задать  соотвтетсвие полей цели (ключи словаря) и полей источника (значения словаря)
        tbSrc - источник
        tbTrg - цель
        dictAssocFields - словарь ассоциаций между полями источника и цели. Если поля одигаковы, то ключи и их значения в словаре будут равны. Иначе ключами словаря задаются поля 
        таблицы-цели, а значениями поля таблицы - истоника { 'trgField1' : 'srcField1'... }
        Так же можно использовать операции над полями в словаре dictAssocFields
        
        listSrcAllowedKeys - список разрешенных значений ключей источника для вставки записей по ним в цель
        tbsKeysPair - список ключей обоих таблиц [tbKeySrc, tbKeyTrg] (необходимы оба ключа, так как из списка полей  таблиц необходимо удалить ключи, которые
        не могут быть обновлены , так как являются ключами)
        
        """
        

        listTrgFields = list(dictAssocFields.keys())
        listTrgFields.remove(tbsKeysPair[1])  # Удаляем ключ, по которому не должно происходить обновлений  ни при каких условиях (иначе ошибка индекса)
        # listTrgFieldsSql = f"({listTrgFields})" # Вставка со скобками, что бы отделить случай, если вдруг будет '*' (все поля идентичны в таблицах), в котором скобки не нужны
        listSrcFields = list(dictAssocFields.values())
        listSrcFields.remove(tbsKeysPair[0])  # Удаляем ключ, по которому не должно происходить обновлений  ни при каких условиях (иначе ошибка индекса)
        listSrcFields = [ f"{tbSrc}." + x for x in listSrcFields]
            
        sql1 = f"UPDATE {tbTrg} SET ({listTrgFields}) = ({listSrcFields}) FROM {tbSrc} WHERE {tbSrc}.{tbsKeysPair[0]} IN  "
        sql1 = sql1.replace("\'", "").replace("[", "").replace("]", "")
        
        sql2 = f"({listSrcAllowedKeys})"
        sql2 = sql2.replace("[", "").replace("]", "")
        
        sql = sql1 + sql2

        return sql




    
    @add_sql_order_part 
    # @add_sql_where_part
    @staticmethod  
    def select_tbs_union_sql (unionSets, unionAll = True, listOrder = None):
        """ SQLSyntaxer
        https://www.sqlitetutorial.net/sqlite-union/
        Создать выражение типа SELECT .... UNION SELECT ... для таблиц и параметров, которые заданы в списке обьектов unionSets класса SelectUnionStructure из structures.py,
        который содержит в себе название таблицы, название полей для выборки из этой таблицы и названия типа записей
        В название полей в структурае SelectUnionStructure можно включать разрешенные опреанды, типа  ['isin', 'bond_name AS FIELD2'] (FIELD2 - будет названа колонка результата с bond_name)
        Кроме того, поля в разных таблицах для UNION  могут по названиям не совпадать, главное, что бы совпадали по типу данных (? Возможно работает механизм автоматического приведени. НЕ ИЗУЧЕНО)
        Что бы присоединить sql-часть для сортировки типа ORDER BY  необходимо добавить в параметры именной параметр listOrder. Если не добавить или прировнять None, то будет приходить
        запрос без ORDER BY
        В поля сортирвки listOrder можно так же добавлять стандартные операнды SQLite. НАпример, ['isin ASC'], где ASC  задает порядок сортировки
        Для подключения  listOrder нужно использовать обязательно их именной формат, так как в декораторы эти параметры передаются через **kwargs
        
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
        
        sql = ""
        for unionPar in unionSets:
            sqlFields = f"{unionPar.selFields}".replace("\'","").replace('[','').replace(']','')
            
            sqlWhere = ''
            if unionPar.whereCond != None and len(unionPar.whereCond) > 0: # WHERE условия
                sqlWhere = f" WHERE " + SQLSyntaxer._get_where_clause_sql(unionPar.whereCond)
            else:
                sqlWhere = ''
                
            sql += f"SELECT {sqlFields}, '{unionPar.type}' AS Type FROM {unionPar.tbName} {sqlWhere} UNION %ALL% " 
            
        
        if  unionAll: # задаем алтернативу между UNION и UNION ALL
            sql = sql.replace('%ALL%','ALL') 
        else:
            sql = sql.replace('%ALL%','') 
            
        sql = sql.rstrip('UNION ALL ').rstrip('UNION ') # Удаляем правую не нужную последнюю вставку UNINO или UNION ALL
            
        return sql        
        
        
        





# -- END БАЗОВЫЕ ЗАПРОСЫ SQL




# -- ЗАПРОСЫ JOIN ------



    def select_two_tables_with_left_join_cond(self, tbLeft, tbRight, fields) :
        """ ЗАГОТОВКА
        Обьеденить 2 таблицы по уловию LEFT JOIN"""
        sql = """SELECT
                    artists.ArtistId, 
                    AlbumId
                    FROM
                    artists
                    LEFT JOIN albums ON
                    albums.ArtistId = artists.ArtistId
                    ORDER BY
                    AlbumId;
                    """








# -- END ЗАПРОСЫ JOIN ------



# -- VIEW --------------------









# -- END VIEW ------------------













# -- СПЕЦИФИЧЕСКИЕ ЗАПРОСЫ 

    @staticmethod        
    def insert_from_list_data_set_with_possible_cols_adds_sql (tbInsTrg, dsSrc, tbFieldsIns, dsClmnsInxs, addColsVals, onConflicts = ''):
        """ Формирование запроса INSERT на основе массива данных в виде списка списков рядов (аналог таблицы) со значениями полей (колонок) с возможностью
        добавления величин-констант в добавоные колонки
        addColsVals - спиок с константами или одномерным списком, равным по длинне длине dsSrc, которые вносятся во все поля всех рядов , после отфильтровки по списку индексов dsClmnsInxs
        dsClmnsInxs - Индексы колонок в  ds , соответствующие полям в tbFieldsIns. Кол-во элементов должно соотвтетсвовать tbFieldsIns
        tbFieldsIns - Названия колонок , отобранных для INSERT, в тбалице tbTrg. Кол-во элементов должно соотвтетсвовать dsClmnsInxs
        """
        # Фильтр массива листов в соответствии с набором индексов колонок в массиве <пока без добавления констант по доп.полям типа 'f2:' >
        dsRes = FG.filter_arr_of_lists_with_col_inxs (dsSrc, dsClmnsInxs) # Массив листов, отфильтрованный по индексам колонок dsClmnsInxs
        addsN = len(addColsVals) # кол-во задаваемых констант для дополнительных полей для добавки в ds
        if addsN >0: # Если заданы величины-константы для проставления в дополнительных полях ds, то выполняем их добавление 
            diffr = len(tbFieldsIns) - len(dsClmnsInxs) # Для проверки соответствия по кол-ву заданных полей в INSERT и кол-ва полей в отфилдьтрованном ds + допюполя
            if len(addColsVals) != diffr: # Если нет соответствия по количеству колонок в tbFieldsIns и сумме кол-ва dsClmnsInxs и добавляемых колонок -констант colsAdds
                print ("PR_369 --> Проверить соответствие (кол-ва доп.полей из списка colsAdds = [addF1, addF2, ... addFN] + кол-во задаваемых колонок из dsClmnsInxs)  и кол-во полей в списке полей для вставки tbFieldsIns <Они должны быть равны>\
                для соответствующего sql INSERT (f1, f2, .. fN) VALUES (v1, v2, ... vN + addF1, addF2, ... addFN) ")
            else: # если все соответствует, проставляем велиу=чины-константы в доп полях всех рядов массива
                # проставляем велиу=чины-константы в доп полях всех рядов массива
                resultDS = FG.add_cols_with_vals_to_list_of_lists (dsRes, addColsVals)
        else: # Добавочные поля и их величины-контанты не заданы, значит оставляем ds неизменным
            resultDS = dsRes
        # 1.Формирование , если нет SELECT парметров  и ввод идет по всем полям равным структуре таблицы
        sqlSelParams = {} # параметры SELECT  запроса в виде словаря для составления части SELECT внутри функции insert_general_sql
        sql = SQLSyntaxer.insert_general_sql (tbInsTrg, tbFieldsIns, resultDS, onConflicts, sqlSelParams ) # Конечный INSERT запрос sql
        # print(f'sqlIns = {sql}')
        # sql = sql.replace('((','(').replace('))',')')        
        return sql




    def drop_duplicates_by_col_sql (self,tb,fieldnNme):
        """ ЗАГОТОВКА
        Удалить дупликаты в таблице по заланному полю
        https://stackoverflow.com/questions/48456131/delete-duplicate-rows-in-large-sqlite-table
        """






# -- END СПЕЦИФИЧЕСКИЕ ЗАПРОСЫ 


# -- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ 

    def _select_sql_parsing (selSql):
        """ NOT COMPLETED. Метод не проработан до конца, потому что появилась идея получать параметры SELECT запроса непосредственно
        из функции формирования SELECT sql, где в параметрах передаются все искомые переменные
        Парсит select sql-запрос с целью определить список полей и таблицу в предложении """
        # Анализ простого (не комплексного ) selSql и парсинг : выяснить список полей и таблицу SELECT

        selParts = selSql.split('SELECT') # Обрубаем по 'SELECT'
        fieldsTabParts = selParts[1].split('FROM') # Остается часть с полями и с таблицей
        fieldsPart = fieldsTabParts[0] # часть SELECT по поялм
        tabWherePart = fieldsTabParts[1]  # Часть SELECT  с таблицей и возможно с  WHERE
        print (fieldsTabParts)

        # Анализ части SELECT по полям
        if '*' in fieldsPart: # Если * в части полей, то значит - все поля запрошены в выборке
            print (f"PR_370 --> Все поля запрошены в выборке SELECT через *")
            # return fieldPart.strip(' '), fieldsTabParts[1].strip(' ') # * в полях и название таблицы в SELECT

        else: # if '*' in fieldsTabParts[0] # Присутствует список полей в выборке SELECT
            print (f"PR_371 --> Присутствует список полей в выборке SELECT")
            selFields = fieldsPart.strip(' ').split(',') # Разделяем поля по запятой
            print (f"PR_372 --> Список полей в SELECT: {selFields}")
            # return selFields, fieldsTabParts[1].strip(' ') # поля и название таблицы в SELECT

        # Анализ части SELECT по таблице и возможными условиями WHERE
        if 'WHERE' in tabWherePart: # есть ли WHERE. Если есть, то вычислить условия WHERE
            print(f"PR_373 --> В части sql с таблицей присутствуют условия WHERE")
            partsTabWhere = tabWherePart.split('WHERE') # Обрубаем по WHERE
            print(partsTabWhere)
            selTab = partsTabWhere[0].strip(' ') # таблица в select
            print (f"PR_374 --> Таблица в SELECT : {selTab}")
            selCondWhere = partsTabWhere[1].strip(' ') # часть SELECT после WHERE
            print (f"PR_375 --> Часть после WHERE : {selCondWhere}")

        else: # если нет WHERE, то условий нет
            print(f"PR_376 --> В части sql с таблицей отсутствует WHERE")

        # Анализ простых однородных условий OR и AND в части SELECT запроса после WHERE
        # Выяснение наличия OR  или AND 
        if 'OR' in selCondWhere : # Наличие OR
            print ("В части WHERE присутствует OR")
            # TODO: ПРорботать , если условия комплексные. Пока просто выводить строку для ручного анализа
        elif 'AND' in selCondWhere: # Наличие AND
            print ("PR_377 --> В части WHERE присутствует AND")
            # TODO: ПРорботать , если условия комплексные. Пока просто выводить строку для ручного анализа
        else: # Если OR и/или AND нет, то условие простое и поле условий одно
            print ("PR_378 --> OR и/или AND нет, условие простое и поле условий одно")

        return 'Словарь с данными SELECT запроса'


    def _get_where_clause_sql (conds):
        """ Вспомогательная функция: Создает часть WHERE для sql запросов с условиями с базовы форматом параметра conds
            conds - список с условиями типа    {
                                                'OR' : [['fieldName1', '<', 5], ['fieldName2', '>', 15]], 
                                                'AND' : [['fieldName3', '<', 5], ['fieldName4', '>', 15]], /
                                                'ONE'  : ['fieldName1', '<', 5],/
                                                'ALL or NO'   : None, / <или иначе - без всяких условий>
                                                'STR' : '(fieldName1 > 5 AND fieldName2 < 15) AND (...)'
                                                }
            Если ключ в словаре условий стоит ALL или NO , то удаляет все записи из таблицы   
            Вместо величин могут стоять имена полей таблиц в любом виде, вкkючая составные типа 'tb1.id'  
            Также названия полей сами могут быть составными, если конечный запрос комплексный и предусматривает использование некольких таблиц   
            Если в величине поля условия перед началом стоит '&', то это значит, что не величина, а названия поля или оператор или фиксированная обозначения NULL. 
        """

        sqlCond = ''
        for key, value in conds.items():  # цикл по словарю условий
            # анализ условий в словаре и составление условной части sql
            for case in Switch(key):  # аналог case .. switch 
                if case('OR'): pass # Если OR или AND условие
                if case('AND'): pass
                if case('_ampers_'): pass # Для запросов в фреймах. Апперсанд тождественен 'AND'
                if case('and'): 
                    # формирование условной части
                    for cond in value: # цикл по параметрам условия (если несколько полей через логику булинову)
                        # анализ типа переменнйо условия в параметре

                        sqlCond += f" {cond[0]} {cond[1]} " # часть предложения по текущему условию без значения value (только имя поля и условие типа =, >, IN и т.д.)

                        sqlVal = SQLSyntaxer._value_analisis_for_where_conds (cond[2]) # анализ структуры и типа величины для текущего условия (внутренняя вспомогательная функция)
                        # if type(cond[2]) == str and '&' not in cond[2]: # если стринг и в нем нет '&', который говорит о том, что это не стринговая величина, а названия поля в условии WHERE
                        #     sqlCond += f"'{cond[2]}' {key}"
                        # elif type(cond[2]) == str and '&' in cond[2]: # если '&' в стринговом значении, значит это не величина, а названия поля в условии
                        #     sqlCond += f"{cond[2]} {key}"
                        # elif type(cond[2]) == int: # если intager
                        #     sqlCond += f"{cond[2]} {key}"

                        if 'IN' in cond[1]: # Если есть в условии IN или NOT IN , то заключаем в скобки это условие, так как это выборка или список в котором ищется совпадение
                            sqlCond += f" ( {cond[2]} )  {key}" # В скобках прописываем список или SELECT sql, который передается в параметре условий последним. 
                            sqlCond = sqlCond.replace("[", "").replace("]", "") # Очищаем стринг от апострофов, если передавался sql SELECT трингом, и от квадратных скобок, если передавался список для проверки в IN

                        else : # иначе - без скобок
                            sqlCond += f" {sqlVal} {key}"

                    sqlCond = sqlCond.rstrip(f'{key}')
                    break
                if case('ONE'): # Если одно условие по одному полю
                    sqlCond += f" {value[0]} {value[1]} " # часть предложения по текущему условию без значения value (только имя поля и условие типа =, >, IN и т.д.)
                    sqlVal = SQLSyntaxer._value_analisis_for_where_conds (value[2]) # анализ структуры и типа величины для текущего условия (внутренняя вспомогательная функция)
                    # if type(value[2]) == str and '&' not in value[2]: # если стринг и в нем нет '&', который говорит о том, что это не стринговая величина, а названия поля в условии WHERE
                    #     sqlCond += f"'{value[2]}'"
                    # elif type(value[2]) == str and '&' in value[2]: # если '&' в стринговом значении, значит это не величина, а названия поля в условии
                    #     sqlCond += f"{value[2]}"
                    # elif type(value[2]) == int: # если intager
                    #     sqlCond += f"{value[2]}"

                if 'IN' in value[1]: # Если есть в условии IN или NOT IN , то заключаем в скобки это условие, так как это выборка или список в котором ищется совпадение
                    sqlCond += f" ( {value[2]} ) " # В скобках прописываем список или SELECT sql, который передается в параметре условий последним. 
                    sqlCond = sqlCond.replace("[", "").replace("]", "") # Очищаем стринг от апострофов, если передавался sql SELECT трингом, и от квадратных скобок, если передавался список для проверки в IN
                else : # иначе - без скобок
                    sqlCond += f" {sqlVal} "                    
                    
                    break
                if case('ALL'): pass
                if case('NO'): 
                    break
                if case('STR'): 
                    sqlCond = f" {value}"
                    break
        sqlCond = sqlCond.replace('&','') # Удаляем возможный '&', который мог быть использован в условиях для обозначения названий полей, а не стринговых величин
        return  sqlCond   


    def _value_analisis_for_where_conds (value):
        """ Вспомогательная внутренняя функция: Качественный анализ стринга величины для поля по условию value в одном условии для sql с WHERE. В зависимости от типа value  и специальных символов в нем,
            делается выбор алгоритма формирования одной строки в условии WHERE с каждым значением value 
            Если в величине поля условия перед началом стоит '&', то это значит, что не величина, а названия поля. 
            """
            # TODO : Изменить аперсанд на другой символ. Этот используется в ссылках!!!
        sqlVal = ''
        if type(value) == str and '&' not in value[:2]: # если стринг и в первых двух символах нет '&' (потому что может встречаться в ссылках, поэтому анализируем первые два символа), который говорит о том, что это не стринговая величина, а названия поля в условии WHERE
            sqlVal = f"'{value}'"
        elif type(value) == str and '&' in value[:2]: # если '&'  в первых двух символах в стринговом значении, значит это не величина, а названия поля в условии
            sqlVal += f"{value}"
            sqlVal = sqlVal.replace('&','')
        elif type(value) == int or type(value) == float: # если intager
            sqlVal += f"{value}"   # Ставится как флаг для раздевания апострофов с обоих сторон выражения в будущем
        return sqlVal
        

# --  END ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ 



# --- МЕТАДАННЫЕ
    @staticmethod   
    def get_tb_fields_sql (tb):
        """ 
        Получение sql запроса для названий полей таблицы 
        """
        sql = f"SELECT name FROM PRAGMA_TABLE_INFO('{tb}');"
        return sql



    @staticmethod   
    def get_tb_fields_mysql_sintax (db, tb):
        """ 
        Получение sql запроса для названий полей таблицы для MySql
        """
        sql = f"SHOW COLUMNS FROM {tb} FROM {db}"
        return sql
    
    


    

    @staticmethod   
    def drop_table_sql (tbName):
        """ 
        Удаление таблицы 
        """

        sql = f'DROP TABLE IF EXISTS {tbName}'
        return sql


    @staticmethod  
    def check_if_table_exists_in_db_stx (tbName):
        """ 
        Проверить наличие таблицы в БД
        """
        
        return f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{tbName}'"



# --- END МЕТАДАННЫЕ



### CREATE STATEMENTS  

    @staticmethod        
    def create_tb_sql (tb,fields, rkeys = None):
        """ Создает текстовый sql запрос для создания таблицы в БД с заданными характеристиками полей в массиве fields """
        #TODO: Сделать подобный метод, но только чтобы автоматом создавал названия колонок (из таблицы эксел) и автоматом анализировал тип поля
        #TODO: Сделать метод в классе работы таблиц эксела для автоматического перевода таблицы эксел в таблицу БД !!! с созданием словаря перевода тайтлов в таблице эксел и названий полей в соответсвии с нумерацией колонок эксела
        
    
        sql = f"CREATE TABLE {tb} ( "

        # --- СОСТАВЛЕНИЕ ЧАСТИ ЗАПРОСА ПО ПОЛЯМ С ИХ АТРИБУТАМИ
        sql_fields_part = ''
        for key, value in fields.items(): # цикл для сохдания части sql,  связанной с перечнем полей

            
            sql_fpart = SQLSyntaxer.create_field_characteristic_part_sql(value) # Создает вставку текста sql для отдельного поля в предложении sql-create
            sql_fields_part += f" {key} {sql_fpart}," # часть запроса отвечающая за поля

        # --- END СОСТАВЛЕНИЕ ЧАСТИ ЗАПРОСА ПО ПОЛЯМ С ИХ АТРИБУТАМИ

        # -- СОСТАВЛЕНИЕ ЧАСТИ ЗАПРОСА  create table , КОТОРАЯ ОТВЕЧАЕТ ЗА КЛЮЧИ ЦЕЛОСТНОСТИ БД
        
        sql += sql_fields_part

        sql_cnstr_part = ''
        if rkeys != None: # Если в параметрах есть референциальные ключи
            sql_cnstr_part = ''
            for rkey in rkeys: # цикл для сохдания части sql,  связанной с перечнем ключей
                sql_cnstr_part += SQLSyntaxer.create_refkeys_part_sql(rkey) # Создает вставку текста sql для отдельного ключа в предложении sql-create для ограничений


        # -- END СОСТАВЛЕНИЕ ЧАСТИ ЗАПРОСА  create table , КОТОРАЯ ОТВЕЧАЕТ ЗА КЛЮЧИ И ПРОЧИЕ ОГРАНИЧЕНИЯ ЦЕЛОСТНОСТИ БД
            
        sql +=  sql_cnstr_part
        sql = sql.rstrip(',') + ')' 

        return sql



    @staticmethod        
    def create_field_characteristic_part_sql (field_attrs):
        """ Вспомогательная F : Создает вставку текста sql для отдельного поля в предложении, где формируется часть запроса по полям для create sql таблицы
            field_attrs: string с разделением '/' для каждого отдельного атрибута поля
        """
        v_parts = field_attrs.split('/') # части параметра поля с заданными характеристиками 
        # print (v_parts)
        n_parts = len(v_parts) # кол-во сегментов характеристики поля Пр: ("ISIN": "str/20/unq",)
        sql_fpart = ''

        for segm in v_parts: # цикл по сегментам параметра, отвечающего за характеристики поля в sql-create

            segm = strip_by_reg(segm) # оставляем только буквенные символы
            # print (len(segm))
            # print (FIELD_ABRIVIATION_STEP11[segm])

            if len(segm) >0: # проверка на пустоту
                v = FIELD_ABRIVIATION_STEP11[segm]
                sql_fpart += f'{v} '

        return sql_fpart
            

    @staticmethod        
    def create_refkeys_part_sql (rkey_attr):
        """ Вспомогательная F : Создает вставку текста sql для референциальных ключей целостности БД для create sql таблицы
            constr_attr: 
                [
                    {
                        'kname': 'fk_inn',
                        'fk' : ['bonds.inn'],
                        'ref' : ['comps.inn_frn'],
                        'del' : 'casc',
                        'upd' : 'casc'

                    },
                ]
        """

        # Проверка есть ли условия удаления или апгрейда в ключе
        if 'del' or 'upd' in rkey_attr: 
            sql_kpart = f" CONSTRAINT {rkey_attr['kname']}"
        else:
            sql_kpart = ''

        
        # Проверка foreign key и составление части запроса
        if 'fk' in rkey_attr:

            sql_kpart += f" FOREIGN KEY ("

            for key in rkey_attr['fk']: # цикл для вставки полей FK создаваемой таблицы

                sql_kpart += f"{key},"

            sql_kpart = sql_kpart.rstrip(",")
            sql_kpart += ')'
            
        # Проверка наличия реферальных полей и составление части запроса
        if 'reffields' in rkey_attr:

            sql_kpart += f" REFERENCES {rkey_attr['reftb']} ("

            for ref in rkey_attr['reffields']: # цикл для вставки полей FK создаваемой таблицы

                sql_kpart += f"{ref},"

            sql_kpart = sql_kpart.rstrip(",")
            sql_kpart += ')'

        # Проверка ON DELETE
        if 'delcasc' in rkey_attr:
            sql_kpart += f" {rkey_attr['delcasc']} "

        # Проверка ON UPDATE 
        if 'updcasc' in rkey_attr:
            sql_kpart += f" {rkey_attr['updcasc']} "            

        return sql_kpart





### END CREATE STATEMENTS  



if __name__ == "__main__":
    pass



    # ПРОРАБОТКА: update_tb_row_with_unique_composite_key_sql (tb, fieldsVals, uniqueCompositeKeysVals)
    
    tb = 'comp_bond_analisys'
    fieldsVals = {
        'comp_bonds_analisys' : 'ООО "СЕЛЛ-Сервис" RU000A104KM0',
        'inx_pckg_decided_id' : 5,
    }
    
    uniqueCompositeKeysVals = {
        'inn' : '5406780551', 
        'isin' : 'RU000A104KM0',
    }
    
    sql = SQLSyntaxer.update_tb_row_with_unique_composite_key_sql (tb, fieldsVals, uniqueCompositeKeysVals)
    
    print(f"PR_925 --> sql = {sql}")




    # # ПРОРАБОТКА: Копировать записи из одной таблицы в другую в тее поля, которые совпадают с источником по заданным коючамв ключевой колонке
    # tbSrc = TB_OFZ_CURRENT_
    # tbTrg = TB_OFZ_ARCIVE_
    
    # sql = "SELECT *FROM INFORMATION_SCHEMA.COLUMNSWHERE TABLE_NAME = N'Customers'"
    






    # # ПРИМЕР: Проработка функции update_where_in_simple_sql с источником в виде списка ИНН
    # # Парам: tb, updFields,  updVals, keyInField, inDS
    # tb = 'global_A'
    # updFields = ['d1']
    # updVals = ['INSERTED']
    # keyInField = ['x_str']
    # # inDS = 'SELECT FROM * '
    # inDS = ['0274051582', '0411137185', '1435133520', '1650032058']

    # whereConds = {'ONE': ['x_str','IN', inDS]}
    # sql = SQLSyntaxer.update_where_in_simple_sql (tb, updFields,  updVals, whereConds)
    # print (sql)










# --- ПРИМЕРЫ ------------



    # # ПРИМЕР: Проработка функции update_where_in_simple_sql с источником в виде списка ИНН
    # # Парам: tb, updFields,  updVals, keyInField, inDS
    # tb = 'global_A'
    # updFields = ['d1']
    # updVals = ['INSERTED']
    # keyInField = ['x_str']
    # # inDS = 'SELECT FROM * '
    # inDS = ['0274051582', '0411137185', '1435133520', '1650032058']

    # whereConds = {'ONE': ['x_str','IN', inDS]}
    # sql = SQLSyntaxer.update_where_in_simple_sql (tb, updFields,  updVals, whereConds)
    # print (sql)



    # # # ПРИМЕР: Обновление данных в первой таблице из второй таблицы на основе условий, сочитающих в себе поля из обоих таблиц
    # # Парам:
    # tbCurrent = 'bonds_current'
    # tbArchive = 'bonds_archive'
    # fieldsTb1 = ['bonds_current.isin'] # список полей  в UPDATE SET первой таблицы
    # fieldsTb2 = ['bonds_archive.isin'] # список полей  в SELECT for SET первой таблицы    
    # # fieldsTb1 = ['bonds_current.isin', 'bonds_current.f2'] # список полей  в UPDATE SET первой таблицы
    # # fieldsTb2 = ['bonds_archive.isin', 'bonds_archive.f2'] # список полей  в SELECT for SET первой таблицы
    # # condsUpdTb1 = {'ONE' : ['bonds_current.f2','>', 5 ]} # условия для UPDATE первой таблицы
    # # condsSelTb2 = {'AND' : [['bonds_current.bond_name','=', '&bonds_archive.bond_name'], 
    # #                         ['bonds_current.bond_name','=', '5'] 
    # #                         ]} # Условия для SELECT второй таблицы
    # condsSelTb2 = {'ONE' : ['bonds_current.bond_name','=', '&bonds_archive.bond_name']
    #                         } # Условия для SELECT второй таблицы    

    
    # sql = SQLSyntaxer.update_tb1_from_select_tb2_simple_sql (tbCurrent,tbArchive, fieldsTb1, fieldsTb2, condsUpdTb1, condsSelTb2)
    # print(sql)


    # # ПРИМЕР: Проработка функции update_where_in_simple_sql
    # # Парам: tb, updFields,  updVals, keyInField, inDS
    # tb = 'bonds_archive'
    # updFields = ['f1']
    # updVals = ['NOT VERIFIED']
    # keyInField = ['bond_name']
    # inDS = 'SELECT FROM * '
    # # inDS = ['1','2']

    # whereConds = {'ONE': ['bond_name','IN', inDS]}
    # sql = SQLSyntaxer.update_where_in_simple_sql (tb, updFields,  updVals, whereConds)
    # print (sql)


    # # ПРИМЕР: Отработка функции insert_with_str_select_sql(tbIns, selSQL) - INSERT with string SELECT как параметр
    # # Параметры:
    # tbIns = 'bonds_archive'
    # selSQL = "SELECT STATUS risposta, DATETIME('now') data_ins FROM   sourceTable"
    # sql = SQLSyntaxer.insert_with_str_select_sql (tbIns, selSQL)
    # print (sql)


    # # ПРИМЕР: Проработка функции SELECT with EXCEPT / Выдает записи, которые присутствуют в Dataset1 и их нет в Dataset2
    # # Параметры для 2х SELECTs
    # tbSel1    = 'bonds_current'    
    # selConds1 = {} # условия в части sql SELECT , если наличиствует параметр EXISTS или NOT EXISTS. '&' указывает, что это названия поля
    # selFields1 = ['bond_name']
    # fullSelParams1 = {"tb":tbSel1,"selFields" : selFields1, "selConds" : selConds1}

    # tbSel2 = 'bonds_archive'    
    # selConds2 = {} # условия в части sql SELECT , если наличиствует параметр EXISTS или NOT EXISTS. '&' указывает, что это названия поля
    # selFields2 = ['bond_name']
    # fullSelParams2 = {"tb":tbSel2,"selFields" : selFields2, "selConds" : selConds2}

    # sql = SQLSyntaxer.select_with_except_sql (fullSelParams1, fullSelParams2)
    # print(sql)


    # # ПРИМЕР: Проработка функции delete_with_exists_for_2tb_sql удаления с условиями, включая EXISTS  для 2х таблиц / Использование функции с  EXISTS с одним условием в части SELECT  и условием EXIST
    # # Параметры для части DELETE
    # tbDel = 'bonds_current'
    # delConds = {} # условия в части sql DELETE
    # # Параметры для части SELECT
    # tbSel = 'bonds_archive'    
    # selConds = {'AND': [['&bonds_current.bond_name', '=', '&bonds_archive.bond_name'], ['bonds_archive.f1','=', 'NOT MATCHED']]} # условия в части sql SELECT , если наличиствует параметр EXISTS или NOT EXISTS. '&' указывает, что это названия поля
    # selFields = ['*']
    # fullSelParams = {"tb":tbSel,"selFields" : selFields, "selConds" : selConds}
    # # параметр определяющий условие EXISTS. Если EXISTS, то удаляет все записи, которые соответствуют в таблице SELECT. (ТАк можно искать новые записи в bonds_curr по остатку)
    # exists = 'EXISTS' # параметр определяющий условие EXISTS
    # sql = SQLSyntaxer.delete_with_exists_for_2tb_sql (tbDel, tbSel, delConds, fullSelParams, exists)
    # print(sql)



    # # ПРИМЕР: Проработка общей функции ISERT / 3. Формирование sql, если задан список полей и нет SELECT параметров
    # # Par для INSERT: 
    # # tbIns = 'bonds_archive' # Таблица для INSERT
    # tbIns = 'cdescript' # Таблица для INSERT
    # fields = ['inn','name', 'descr']
    # vals = [['ddd','АО "TEST1"','descr'],['ddd','АО "TEST2"','descr'],['ddd','АО "TEST3"','descr']]
    # onConflicts = 'IGNORE'
    # # Par для SELECT
    # sqlSelParams = {} # нет SELECT 
    # sql = SQLSyntaxer.insert_general_sql (tbIns, fields, vals, onConflicts, sqlSelParams ) # Конечный INSERT запрос sql
    # print(f'sqlIns = {sql}')


    # # ПРИМЕР: Проработка общей функции ISERT / 1.Формирование , если нет SELECT парметров  и ввод идет по всем полям равным структуре таблицы
    # # Par для INSERT: 
    # # tbIns = 'bonds_archive' # Таблица для INSERT
    # tbIns = 'cdescript' # Таблица для INSERT
    # fields = ['*'] # Все поля запросить
    # vals = [['ddd','АО "TEST1"','descr'],['ddd','АО "TEST2"','descr'],['ddd','АО "TEST3"','descr']]
    # onConflicts = 'IGNORE'
    # # Par для SELECT
    # sqlSelParams = {} # нет SELECT 
    # sql = SQLSyntaxer.insert_general_sql (tbIns, fields, vals, onConflicts, sqlSelParams ) # Конечный INSERT запрос sql
    # print(f'sqlIns = {sql}')



    # # ПРИМЕР: Проработка общей функции ISERT / 4.Формирование sql, если задан список полей и есть SELECT параметры. Сисок полей  SELECT д.б. = списку полей INSERT (f1, f2 ..fN)
    # # Par для INSERT: 
    # tbIns = 'bonds_archive' # Таблица для INSERT
    # fields = ['isin','bond_name', 'qualif']
    # # fields = ['*']    
    # vals = [] # Неважно, что  в списке
    # onConflicts = 'IGNORE'
    # # Par для SELECT
    # tbSel = 'bonds_current' # Таблица для SELECT
    # getSelFields = ['isin','bond_name', 'qualif']
    # conds = {'ONE'  : ['bond_name', '=', 'АПРИФП БП5']}
    # sqlSelParams = {'tb' : tbSel, 'getSelFields' : getSelFields, 'conds' : conds} # параметры SELECT  запроса в виде словаря для составления части SELECT внутри функции insert_general_sql
    # sql = SQLSyntaxer.insert_general_sql (tbIns, fields, vals, onConflicts, sqlSelParams ) # Конечный INSERT запрос sql
    # print(f'sqlIns = {sql}')

    # # ПРИМЕР: Проработка общей функции ISERT / 2.Формирование sql, если все поля и есть SELECT параметры
    # # Par для INSERT: 
    # tbIns = 'bonds_archive' # Таблица для INSERT
    # fields = ['*']
    # vals = [] # Неважно, что  в списке
    # sqlSelect = ''
    # onConflicts = 'IGNORE'
    # # Par для SELECT
    # tbSel = 'bonds_current' # Таблица для SELECT
    # getSelFields = ['*']
    # conds = {'ONE'  : ['bond_name', '=', 'АПРИФП БП5']}
    # sqlSelParams = {'tb' : tbSel, 'getSelFields' : getSelFields, 'conds' : conds} # параметры SELECT  запроса в виде словаря для составления части SELECT внутри функции insert_general_sql
    # sql = SQLSyntaxer.insert_general_sql (tbIns, fields, vals, onConflicts, sqlSelParams ) # Конечный INSERT запрос sql
    # print(f'sqlIns = {sql}')



    # # ПРИМЕР: Проработка составления sql - DELETE с условиями
    # sqlSyntaxer = SQLSyntaxer()
    # tb = 'bonds_2022_09_10'
    # getFields = ['bold_name', 'isin']
    # conds = {
    #     # 'STR': '(fieldName1 > 5 AND fieldName2 < 15) AND (...)'
    #     'ALL': []
    #     # 'ONE': ['bond_name', '=', 'СэтлГрБ1P1']
    #     # 'OR': [['bond_name', '=', 'СэтлГрБ1P1'], ['isin', '=', 'RU000A0ZYEQ9']]
    # }
    # sql = sqlSyntaxer.delete_from_table_with_where_condition_sql(tb,  conds)
    # print (sql)


    # # ПРИМЕР: Проработка составления sql - SELECT с условиями
    # sqlSyntaxer = SQLSyntaxer()
    # tb = 'bonds_2022_09_10'
    # getFields = ['bond_name', 'isin']
    # conds = {
    #     # 'STR': '(fieldName1 > 5 AND fieldName2 < 15) AND (...)'
    #     'ALL': []
    #     # 'ONE': ['bond_name', '=', 'СэтлГрБ1P1']
    #     # 'OR': [['bond_name', '=', 'СэтлГрБ1P1'], ['isin', '=', 'RU000A0ZYEQ9']]
    # }
    # sql = sqlSyntaxer.select_from_table_with_where_condition_sql(tb, getFields, conds)
    # print (sql)




    # ПРИМЕР: Step 11. Проработка CREATE тбалиц БД sqlite
    # sqlSyntaxer = SQLSyntaxer()
    # # ПАРАМЕТРЫ:
    # tb = 'bonds_test'
    # fields = TB_BONDS_11STEP
    # keys =  TB_BONDS_KEYS_1
    # # Получение update sql
    # create_sql = sqlSyntaxer.create_tb_sql(tb, fields, keys)
    # print (create_sql)




# --- END ПРИМЕРЫ ------------


