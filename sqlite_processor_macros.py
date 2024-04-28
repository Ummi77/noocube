
from noocube.sql_syntaxer import SQLSyntaxer
from noocube.sqlite_processor import SqliteProcessor
from noocube.settings import *
import noocube.funcs_general as FG

class SqliteProcessorMacros ():
    """ 
    OBSOLETED: Класс устарел, так как использует неправильное подсоединение к БД, что сильно замедляет процессы. Его методы разнесены 
    в классы с окончанием-маркером 'Speedup'
    Класс предназначен для реализации макросов (комплексных специфических функций) sql запросов на основе методов sql-процедур более низкого 
    уровня
    """

    def __init__(self,dbName):

        self.db_proc = SqliteProcessor(dbName)  # Собственный процессор БД




    def delete_rows_with_given_col_value_macr (self, tb, colName, colValForDel):
        """Удалить записи в таблице ,где величина поля заданной колонки colName равна задаваемой величине colValForDel
        colName - название колонки, в которой ищется задаваемое значение для удаления
        colValForDel - значение поля колонки, по которому находятся записи для удаления
        """
        conds = {'ONE' : [colName,'=', colValForDel]}
        self.db_proc.delete_from_table_with_where_condition( tb, conds)



    def delete_rows_with_col_value_in_ds_macr (self, tb, colName, ds):
        """Удалить записи в таблице ,где величина заданного поля принадлежит множеству значений полей задаваемого одномерного, одноколоночного массива ds
        colName - название колонки, в которой ищется задаваемое значение для удаления
        colValForDel - значение поля колонки, по которому находятся записи для удаления
        """
        # Удалить записииз таблицы bonds_current , isin которых есть в табл bonds_archive
        conds = {'ONE' : [colName, 'IN', ds]}
        self.db_proc.delete_from_table_with_where_condition( tb, conds)



    def get_rows_difference_between_two_tbs_by_cols_val_macr (self, tb1, tb2, colNameOfTb1, colNameOfTb2):
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
        cur = self.db_proc.execute_sql_with_cursor (sqlSelExcept) # курсор с выпоркой по результатам запроса
        dsTupArr = cur.fetchall() # массив данных результата запроса sql в виде списка таплов (которые могут иметь формат двух видов [(x1,x2 .. xN)] <type = 1>) или [(x1,),(x2,) ...]  <type = 2>
        dsList = self.db_proc.get_list_from_fetch (dsTupArr, 2) #  конечный результат выборки sql запроса в виде списка
        cur.close()
        return dsList



    def select_all_rows_macr (self, tb, getFields):
        """Сделать выборку заданных полей getFields всех записей из таблицы """
        conds = {}
        dsRes = self.db_proc.select_from_table_with_where_condition(tb, getFields, conds)     
        return dsRes             


    def select_rows_with_given_val_in_col_macr (self, tb, getFields, сolName, colVal):
        """Получить массив из запрашиваемых полей getFields таблицы, в запиях которых значение поля заданной колонки ColName равна задаваемой велечине colVal"""
        # Найти записи в таблице bonds_archive с помеькой в поле f1= 'NOT MATCHED'
        conds = {'ONE' : [сolName,'=', colVal]}
        dsRes = self.db_proc.select_from_table_with_where_condition(tb, getFields, conds)     
        return dsRes     



    def select_rows_where_col_val_with_str_fragment_conditioned_macr(self, tb, getFields, col, strFragm, strOperator = 'LIKE'):
        """Получить выборку записей из таблицы, если значение стрингового поля заданной колонки содержит один вариант стрингового фрагмента (простой текстовый поиск)
        getFields - поля запрашиваемой выборки
        col - название колонки, в которой производится поиск
        strFragm - поисковый стринговый фрагмент,который в зависисмости от цели может быть ограничен символами % '%strFragm%', 'strFragm%', '%strFragm' или вообще не ограничен
        strOperator - вид оператора LIKE или NOT LIKE (могут быть и любые другие SQL опреаторы со стрингами).  По умолчанию 'LIKE'
        
        Прим: Отредактировано 21-06-2023. Добавлено условие на поиск по ОКПО, если проставлено 'NOT FOUND' (не найдены ранее оп каким-то причинам). Добавлено [col, sqlOperatorEmpty, 'NOT FOUND'] 
        в выражении conds = {logicOperator:[[col, sqloperatorNull, '&NULL'], [col, sqlOperatorEmpty, ''], [col, sqlOperatorEmpty, 'NOT FOUND'] ]} ниже
        """
        conds = {'ONE' : [col,'LIKE', strFragm]}
        dsRes = self.db_proc.select_from_table_with_where_condition(tb, getFields, conds)       
        return dsRes


    def select_rows_where_col_val_is_not_empty_or_empty_macr(self, tb, getFields, col, notEmpty = True):
        """Получить выборку записей таблицы, в которых в заданном поле значение равны или неравны пустому значению или NULL или 'NOT FOUND'
        getFields - поля выборки
        notEmpty - флаг , который настравивает функцию на поиск пустых или наоборот непустых  значений в заданной колонки. По умолчанию = True,то есть поиск не пустых значений
        """
        db_processor = SqliteProcessor(DB_BONDS_) 

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


        dsRes = db_processor.select_from_table_with_where_condition(tb, getFields, conds)
        return dsRes



    def update_given_const_val_for_col_in_all_rows (self, tb, col, val):
        """Проставить константное значение val колонки col во всех рядах таблицы"""
        # Парам: 
        updFields = [col]
        updVals = [val]
        whereConds = {}
        sql = SQLSyntaxer.update_where_in_simple_sql (tb, updFields,  updVals, whereConds)
        self.db_proc.execute_sql (sql) # Action: Обновить новые скопированные строки в архиве , проставить в поле f1 значение 'NOT VERIFIED'        



    def update_given_const_vals_for_cols_by_dsKeys_macr(self, tb, updFields,  updVals, tbKeyCol, dsKeysIn):
        """Обновить значения полей в колонках заданными константами для тех записей, значения ключей которых принадлежат множеству ключей в dsKeysIn"""
        db_processor = SqliteProcessor(DB_BONDS_)  
        # updFields = ['f1']
        # updVals = ['MATCHED']
        whereConds = {'ONE': [tbKeyCol, 'IN', dsKeysIn]}
        sqlUpd = db_processor.update_where_in_simple_exec (tb, updFields,  updVals, whereConds)

        return sqlUpd




    def copy_rows_from_tb1_to_equal_tb2_which_absent_by_key_columns_macr(self, tb1, tb2, keyColName):
        """Скопировать те ряды из таблицы1 в !! эквивалентную !! таблицу2 , значений которых нет в ключевых одноименных колонок в тождественных таблицах
        RET: dsKeysRowsVals -  Выборка значений ключевой колонки nf,kbws1 по тем рядам, которых нет в таблице2
        """
        # Выборка значений ключевой колонки nf,kbws1 по тем рядам, которых нет в таблице2
        dsKeysRowsVals= self.get_rows_difference_between_two_tbs_by_cols_val_macr(tb1, tb2, keyColName, keyColName) 
        # Составление запроса SELECT IN , для выборки !!полных!! строк записей , появившихся в bonds_current, которые отсутствуют в базовом архиве bonds_archive, на основе списка названий dsList, полученных ранее 
        # Параметры:
        fields = ['*']
        dsIN = dsKeysRowsVals # 
        conds = {'ONE': [keyColName, 'IN', dsIN]}  # Условия по одному параметру
        sqlSelIN = SQLSyntaxer.select_from_table_with_where_condition_sql(tb1, fields, conds) # sql получения полных записей из bonds_current, которые отсутствуют в архиве bonds_archive
        # Копирование выборки полных записей , отсутствующих в архиве, в архив
        selSQL = sqlSelIN # sql выборки отсуствующих в архиве бумаг для вставки в архив
        sqlCopyFinal = SQLSyntaxer.insert_with_str_select_sql(tb2, selSQL) # конечный sql INSERT для копирования (вставки) 
        self.db_proc.execute_sql (sqlCopyFinal) # Action: Копировать
        return dsKeysRowsVals






if __name__ == "__main__":
    pass



    # ПРОРАБОТКА: Простановка в заданном поле для unix-времени велечин, соотвтетсвующих какой-то календарной дате в поле для дат в этой же таблице
    
    sql = 'UPDATE '



    # # ПРИМЕР: Проработка функции ere_col_val_contain_str_fragment


    # db_proc_macros = SqliteProcessorMacros(DB_BONDS_)

    # conds = {'OR' : [['isin','LIKE', 'XS%'],['isin','LIKE', 'RU%']]}
    # dsRes = db_proc_macros.db_proc.select_from_table_with_where_condition(TB_BONDS_CURRENT_, ['isin'], conds)     


















