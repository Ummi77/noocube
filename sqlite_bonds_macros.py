from time import sleep
from noocube.json_manager import JsonManager
from noocube.sql_syntaxer import SQLSyntaxer
from noocube.sqlite_connection import SqliteConnection
import sqlite3
from noocube.algorithms_settings import *
from noocube.sqlite_processor import SqliteProcessor
from noocube.switch import Switch
import noocube.funcs_general as FG
from noocube.settings import ALGORITHM_MESSEGES_, DB_BONDS_, DEBUG_, TB_GLOBAL_A_

class SqliteBondsMacros (SqliteProcessor):
    """ OBSOLETED: Сейчас специализированные проектные макросы выполняет класс BondsMainManager из /home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/bonds_manager.py 
    Прикладные методы для работы с ценными бумагами и sqlite БД """

    def __init__(self,dbName):
        SqliteProcessor.__init__(self,dbName)




# -- КОМПЛЕКСНЫЕ МАКРОСЫ, СПЕЦИФИЧЕСКИЕ ИМЕННО ДЛЯ РАБОТЫ С БД НА ПРЕДМЕТ ЦЕННЫХ БУМАГ ПРОГРАММЫ


    def read_inn_from_tb_globalA_which_null (self, gaFieldCheck)  :
        """ Считывание в таблице global_A тех ИНН компаний, для которых не было произведено внесение маркера по задаваемому полю
        gaFieldCheck - поле, в котором проверяется наличие NULL (т.е. незаполненное маркером)
        return dsInnNotInserted  - [[ ... ]] 
        """
        # Pars: 
        tb = 'global_A'
        conds = {'OR': [[gaFieldCheck, 'IS', '&NULL'], [gaFieldCheck, '=', '']]} # Поле 'l1' соответствуюет маркеру вставление данных в поле 'link1' в таблице comps_descr
        getFields = ['x_str']
        dsRes  = self.select_from_table_with_where_condition (tb, getFields, conds)
        print (f"dsRes = {dsRes}")
        dsInnNotInsertedFetch = dsRes[0].fetchall()
        dsRes[0].close()
        dsInnNotInserted = FG.convert_tuple_of_tuples_to_list_of_lists(dsInnNotInsertedFetch) # Двумерный список [[ ... ]]   тех ИНН, по которым не проставлена метка 'INSERTED'  в таблицк global_A в поле x-str
        return dsInnNotInserted  # [[ ... ]] 


    def get_correspond_list_ISINs_to_INNs (self, dsINN):
        """ Нахождение соотвествующего массива [ISIN, INN], где на входе задается массив INN 
        То есть вычисление хотя бы ISIN одной ценной бумаги, принадлежащей компании с заданными INN. Поиск ISIN производится по обоим таблицам bonds_current и bonds_archive
        """

        # Поиск любой действующей облигации компании по ИНН для нахождения ISIN в табл bonds_current  (текущие, если тут найдены, 
        # то точно есть) или bonds_archive (в этой таблице - возможно есть, не 100%)
        # Pars: 
        tbComps = 'comps'
        tbBondsCurrent = 'bonds_current'
        tbBondsArchive = 'bonds_archive'

        # Нахождение двумерный список [[ INN, ISIN ]] облигаций по массиву ИНН присутствующих в таблицах bonds_current и bonds_archive
        selFields = ['isin','inn_ref']
        selConds = {'ONE' : ['inn_ref', 'IN', dsINN]} # условия в части sql SELECT . '&' указывает, что это названия поля
        add = ' GROUP BY inn_ref' # добавка типа GROUPED BY 

        # sql = SQLSyntaxer.select_from_table_with_where_condition_sql (tbBondsCurrent, selFields, selConds, add) 
        dsGenISIN_INN_bonds_curr = self.select_from_table_with_where_condition (tbBondsCurrent, selFields, selConds, add) # Action: SELECT 
        # dsFetch = cur.fetchall()
        # cur.close()
        # # в bonds_current
        # dsGenISIN_INN_bonds_curr = FG.convert_tuple_of_tuples_to_list_of_lists(dsFetch) # Двумерный список [[ INN, ISIN ]] в bonds_current

        if type(dsGenISIN_INN_bonds_curr).__name__ =='int':
            dsGenISIN_INN_bonds_curr = []

        dsGenISIN_INN_bonds_arch = self.select_from_table_with_where_condition (tbBondsArchive, selFields, selConds, add) # Action: Update 
        if type(dsGenISIN_INN_bonds_arch).__name__ =='int':
            dsGenISIN_INN_bonds_arch = []        
        # dsFetch = cur.fetchall()
        # cur.close()
        # # в bonds_archive
        # dsGenISIN_INN_bonds_arch = FG.convert_tuple_of_tuples_to_list_of_lists(dsFetch) # Двумерный список [[ INN, ISIN ]] в bonds_archive

        dsGenISIN_INN_with_duplicates = dsGenISIN_INN_bonds_curr + dsGenISIN_INN_bonds_arch

        if len(dsGenISIN_INN_with_duplicates) > 0:

            dsGenISIN_INN = FG.remove_duplicates_from_list(dsGenISIN_INN_with_duplicates)

        else:
            dsGenISIN_INN = -1

        return dsGenISIN_INN


    def get_inn_by_isin_from_DB (self, isin):
        """SqliteBondsMacros
        Получение ИНН компании по ISIN ее ценных бумаг на базе существующих в БД данных в таблицах bonds_archive и  bonds_current"""

        # Нахождение ИНН компании по ее ISIN в таблице соответствий (а может надо искать в bonds_archive и bonds_current) 
        # Par:
        tbInnIsin = 'bonds_archive'     
        getFields = ['inn_ref']   # [count(*)] - если надо подсчитать ряды полученные
        conds = {'ONE': ['isin', '=', isin]}
        inn = self.select_from_table_with_where_condition (tbInnIsin, getFields, conds)

        return inn[0]




    def get_isins_by_inn_from_DB (self, inn):
        """ Нахождение ISIN по INN компании из таблиц bonds_archive и bonds_current в БД """
        db = DB_BONDS_
        tbInnIsin = 'bonds_archive'     
        getFields = ['count(*)']   # [count(*)] - если надо подсчитать ряды полученные
        conds = {'ONE': ['inn_ref', '=', inn]}
        cur, sql = self.select_from_table_with_where_condition (tbInnIsin, getFields, conds)
        flagArch = int(cur.fetchone()[0]) # Возврат по bonds_archive
        cur.close()

        tbInnIsin = 'bonds_current'     
        getFields = ['count(*)']   # [count(*)] - если надо подсчитать ряды полученные
        cur, sql = self.select_from_table_with_where_condition (tbInnIsin, getFields, conds)            
        flagCurr = int(cur.fetchone()[0]) # Возврат по bonds_current
        cur.close()  

        # Анализ флагов возврата SELECT count(*) ...
        if flagArch == 1 and flagCurr ==0 : # если найдено совпадение в таблице bonds_archive
            tbInnIsin = 'bonds_archive'     
        elif flagArch == 0 and flagCurr == 1: # если найдено совпадение в таблице bonds_current
            tbInnIsin = 'bonds_current'     
        elif flagArch == 1 and flagCurr == 1 : # Если найдены совпадения в обоих таблицах
            tbInnIsin = 'bonds_archive'     
        elif flagArch == 0 and flagCurr == 0 : # Если не найдены совпадения ни в одной таблице
            print(f"Метод srch_comp_link_by_isin_PF (АИФ) не нашел соответствий между ИСИН и ИНН компании в таблице current_inn_isin.")
            inn = '-1'
            res = [inn]
            # return res

        getFields = ['isin']   # [count(*)] - если надо подсчитать ряды полученные
        cur, sql = self.select_from_table_with_where_condition (tbInnIsin, getFields, conds)
        dsIsinsFetch = cur.fetchall()
        dsIsins2Dim = FG.convert_tuple_of_tuples_to_list_of_lists(dsIsinsFetch)
        dsIsins = FG.convert_list_of_list_to_one_dim_list(dsIsins2Dim,0)
        return dsIsins



    def check_wrong_fill_in_links_fields_of_comps_descr (self, linkField, chkVal):
        """ Проверяет и находит неправильно заполненные поля в колонках с ссылками в таблице comps_descr
        linkField - название поля, в котором проверяется правильность заполнения или неправильность заполнения ссылками
        chkVal - фрагмент, который ищется в значениях полей, что бы подтвердить правильность или неправильность заполнения полей ссылками
        TODO: Может бфть расширена до уровня болшей универсализации. Для поиска в разных таблицах и полях. Потом продумать
        RETURN: Возвращает inn компаний, В которых в поле linkField неправильно заполнены значения
        ИСпользовать для проверки правильности интерактивного заполнения
        TODO: ПОтом продумать реализацию ответа на неправильное заполнения в виде алгоритма
         """
        # Pars:
        tbCompsDescr = 'comps_descr'
        getFields = ['inn', linkField]
        dsInn_Links = self.get_cols_full_ds_from_tb(tbCompsDescr, getFields)
        dsWrongInn = self.check_wrong_val_in_col_of_2Dim_ds_with_key_col(dsInn_Links, 1, chkVal, 0)
        return dsWrongInn


    def get_links_of_comp_pages_from_www_by_inns_from_copms_descr (self, dsINN, linkField):
        """ Получение ссылок на страницы компаний по www ресурсам на основе спсика ИНН из таблицы comps_descr
        dsINN - входной простой список ИНН компаний
        linkField - название поля в таблице comps_descr , где хранятся ссылки по нужному интернет-ресурсу
        """
        tbCompsDescr = 'comps_descr'
        getFields = ['inn', linkField]
        conds = {'ONE': ['inn', 'IN', dsINN]}
        cur, sql = self.select_from_table_with_where_condition (tbCompsDescr, getFields, conds)
        dsLinks = self.get_ds_from_cursor (cur)  
        return  dsLinks     



    # def get_comp_links_from_tb_comps_descr_by_not_marked_vals_from_global_A (self, gaMarkerField, cdlinkField):
    #     """ OBSOLETED/ Разложена на суб-флгоритмы и перенесено все в модуль AlgorithmsSubParts.search_and_fill_to_db_comps_data_universal_PF (Should be Deleted after some time)
    #     Получение ссылок по компаниям на основе анализа немаркированных величин в таблице global_A по той колонке, которая соотвесттвует заданному интернет-ресурсу 
    #     wwwShortname - краткое условное название интернет-ресурса <CHECKO, >
    #     """
    #     # расшифровка параметров по краткому условному названию интернет-ресурса

    #     dsInnNotInserted = self.read_inn_from_tb_globalA_which_null (gaMarkerField) # Массив ИНН из таблицы global_A, в которых не проставлены маркеры в поле 'l1'
    #     dsOneDimNotInserted = FG.convert_list_of_list_to_one_dim_list (dsInnNotInserted, 0) # Конвертация а простой одномерный список
    #     # получить данные с сылками для списка найденных ИИН из comps_descr для не обработанных описаний по CHECKO
    #     dsINNs = dsOneDimNotInserted # Должен быть в таком формате  [inn1,inn2...]
    #     dsLinks = self.get_links_of_comp_pages_from_www_by_inns_from_copms_descr (dsINNs, cdlinkField)
    #     # Оставляем только те ряды в dsLinks, которые по ИНН соответствуют dsInnNotInserted
    #     lN = len(dsLinks) #  Кол-во в изначальном вычесленном отфильтрованном массиве
    #     dsLinksNotInserted = [dsLinks[i] for i in range(lN) if dsLinks[i][0] in dsINNs] # !!! Фильтрация тех рядов в изходном dsLinks , в которых нет метки 'INSERTED'  в таблице global_A в поле x_str (где размещены ИНН всех облигаций описаний которых нет в таблице comps_descr в сравнеии с табдицей comps)
    #     dsLinksOneDim = FG.convert_list_of_list_to_one_dim_list (dsLinksNotInserted, 1) # Оставляем только ссылки на сайт checko.ru (последовательность остается соотвествующей ИНН в главном списке dsLinks)
    #     return dsLinksOneDim



    def get_inn_by_link_in_field_of_tb_comps_descr(self, linkField, linkVal):
        """ Нахождение ИНН компании по ее ссылке в одном из полей link1 ... linkN таблицы comps_descr
        linkField - название поля , В котором хранятся ссылки компаний, в таблице comps_descr. Каждая колонка соответствует одному из заданных 
        вэб-рессурсов
        """
        # Pars:
        tbCompsDescr = 'comps_descr'
        getFields = ['inn']
        conds = {'ONE' : [linkField,'=', linkVal]}
        dsINN= self.select_from_table_with_where_condition(tbCompsDescr, getFields, conds) 
        # print (sql)
        # dsINN = self.get_ds_from_cursor (cur)

        return dsINN
        


    def get_ds_inns_by_link_in_field_of_tb_comps_descr(self, linkField, linkVal):
        """ Нахождение массива ИНН компаний по ее ссылке в одном из полей link1 ... linkN таблицы comps_descr, если ссылки есть одинаковые у нескольких компаний (как ошибки заполнения )
        linkField - название поля , В котором хранятся ссылки компаний, в таблице comps_descr. Каждая колонка соответствует одному из заданных 
        вэб-рессурсов
        """
        # Pars:
        tbCompsDescr = 'comps_descr'
        getFields = ['inn']
        conds = {'ONE' : [linkField,'=', linkVal]}
        cur, sql = self.select_from_table_with_where_condition(tbCompsDescr, getFields, conds) 
        # print (sql)
        dsINN = self.get_ds_from_cursor (cur)

        return dsINN




# -- END КОМПЛЕКСНЫЕ МАКРОСЫ, СПЕЦИФИЧЕСКИЕ ИМЕННО ДЛЯ РАБОТЫ С БД НА ПРЕДМЕТ ЦЕННЫХ БУМАГ ПРОГРАММЫ






if __name__ == "__main__":
    pass


    # TODO: НЕПРАВИЛЬНО РАБОТАЕТ get_ds_from_cursor (cur) !!!!!! с одним результатом по ряду и колонке

    #  ПРИМЕР: Получение ИНН по ссылке в таблице comps_descr
    db = DB_BONDS_
    db_macros = SqliteBondsMacros(db)  
    # Pars;
    linkField = 'link2'
    linkVal = 'https://fin-plan.org/lk/obligations/company/gruzovichkof-tsentr-ooo/'   
    inn = db_macros.get_inn_by_link_in_field_of_tb_comps_descr(linkField, linkVal)




    # # ПРИМЕР: Нахождение массива ISINS  по заданному массиву INNs с использованием универсальной фцнкции через map для обработки всех ISINS атомарной функцией SqliteBondsMacros.get_isins_by_inn_from_DB
    # db = DB_BONDS_
    # db_macros = SqliteBondsMacros(db) 
    # # Pars:
    # linkField = 'link2'
    # chkVal = 'http'
    # dsInnWrong = db_macros.check_wrong_fill_in_links_fields_of_comps_descr (linkField, chkVal)

    # dsISINs2Dim = list(map(db_macros.get_isins_by_inn_from_DB, dsInnWrong)) # Получение двумерного списка ISINs
    # dsISINs1Dim = FG.convert_list_of_list_to_one_dim_list (dsISINs2Dim, 0) # Получение одномерного списка


    # # ПРИМЕР: Получение INNs тех компаний, запись ссылок в таблице comps_descr которых в поле link2 (которая соответствует блоку FINPLAN) не правильная или отсутствует
    # # Парам:
    # db = DB_BONDS_
    # db_macros = SqliteBondsMacros(db) 
    # # 1. ПОлучение массива [inn, link2] из таблицы comps_descr
    # # Pars:
    # tbCompsDescr = 'comps_descr'
    # getFields = ['inn', 'link2']
    # dsInn_Links = db_macros.get_cols_full_ds_from_tb(tbCompsDescr, getFields)

    # dsWrongInn = db_macros.check_wrong_val_in_col_of_2Dim_ds_with_key_col(dsInn_Links, 1, 'http', 0)


    # # ПРИМЕР: Проверка работы метода get_cols_full_ds_from_tb
    # db = 'bonds.db'
    # db_macros = SqliteBondsMacros(db) 

    # # ПОлучение массива [inn, link2] из таблицы comps_descr
    # # Pars:
    # tbCompsDescr = 'comps_descr'
    # getFields = ['inn']
    # dsInn_Links = db_macros.get_cols_full_ds_from_tb(tbCompsDescr, getFields)


    # # # ПРИМЕР: Нахождение ISIN по INN компании из таблиц bonds_archive и bonds_current
    # # Парам:
    # db = 'bonds.db'
    # db_macros = SqliteBondsMacros(db) 
    # inn = 7446031217

    # isins = db_macros.get_isins_by_inn_from_DB (inn)






























