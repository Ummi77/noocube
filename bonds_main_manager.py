

from markupsafe import Markup
# import bonds.funcs_general as FG
import noocube.funcs_general as FG
import numpy as np
import pandas as pd
from .sqlite_pandas_processor import SqlitePandasProcessor
from noocube.settings import *
from noocube.switch import Switch
from noocube.exceptions import *
from noocube.dsource_cube import DSourceCube 
from noocube.settings_date_formats import *  





# from classes.local_manager_BH import LocalManager
# from project_bonds_html.projr.classes.html_manager import HTMLSiteManager
# from settings import TB_PORTFOLIO_HISTORY_
# from settings import TB_BONDS_BOUGHT_



class BondsMainManager(SqlitePandasProcessor):
    """Класс реализующий специализированные  локальные макросы по сущностям , участвующим именно в этом проекте (облигации, компании, процессоры конкретных таблиц и т.д.)
    Относится к надстройкам самого высокого уровня в реализации кода проекта
    Стягивать в этот модуль все специфические конечные методы с конкретными, индивидуальными сущностями 
    Подобный класс путь всегда имеет имя равное общему названию конкретного проекта с добавлением 'Main'
    Ранее его задачи выполнял класс SqliteBondsMacros из файла /home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/sqlite_bonds_macros.py"""

    def __init__(self, dbName): 
        SqlitePandasProcessor.__init__(self, dbName)
        



    
    def get_comp_name_by_inn(self, inn):
        """
        BondsMainManager
        Получить название компании по ее ИНН
        Category: Облигации
        """
        # Pars:
        
        conds = {'ONE':['inn','=',inn]}
        compName = self.select_from_table_with_where_condition(TB_COMPS_, ['comp_name'], conds)
        return compName[0]


    

    def get_bonds_by_comp_inn_bmm(self, inn):
        """
        BondsMainManager
        Получить фрейм с облигациями компании по ее ИНН
        Category: Облигации
        """
        sql = f'SELECT * FROM bonds_current WHERE inn_ref = "{inn}" '
        dfCompBonds = self.read_sql_to_df_pandas(sql)
        return dfCompBonds




    def get_inn_by_bond_isin_bmm(self, isin):
        """
        BondsMainManager
        Получить inn эмитента по любому isin его облигаций в виде списка
        Category: Облигации
        """

        db_proc = SqlitePandasProcessor(DB_BONDS_)
        sql = f"SELECT inn_ref FROM bonds_current WHERE isin = '{isin}'"
        resInn = db_proc.get_result_from_sql_exec_proc (sql)
        return resInn




    def get_df_comps_with_unitar_or_multiple_bonds_from_tb_with_inn(self,specTb, issues = 1):
        """
        BondsMainManager
        Получить выборку компаний из какой-либо специализированной (производной) таблицей specTb, где есть INN эмитентов, которые имеют либо ножесвтенные выпуски бумаг, либо только один выпуск (унитерные) 
        issues - Флаг множественности выпусков облигаций по компании. если = 1, что по умолчанию, то - унитарные. В ином случае - множественные (проставить в параметрах любое другое целочисленное число > 1)
        Category: Облигации
        """

        sql = f"""
            SELECT *,COUNT(*) as bonds_qn FROM {specTb} 
            LEFT JOIN bonds_current 
            ON bonds_current.inn_ref=fapvdo_comp_raitings.inn
            WHERE inn!='NOT FOUND' AND isin IS NOT NULL
            GROUP BY inn_ref
        """

        dfComps = self.read_sql_to_df_pandas(sql)

        if issues != 1: # Если не один выпуск, значит - множественные выпуски 

            # Получить список ИНН компаний с множественными облигациями
            fiE = 'bonds_qn > 1'
            dfCompsFilt = BondsMainManager.filter_df_by_query_pandas(dfComps, fiE)

        else: # Иначе - унитарные (с одни выпуском)

            # Получить список ИНН компаний с унитарным выпуском облигаций
            fiE = 'bonds_qn == 1'
            dfCompsFilt = BondsMainManager.filter_df_by_query_pandas(dfComps, fiE)

        return dfCompsFilt





# ФУНКЦИИ КАЛЬКУЛЯЦИИ ВЫЧИСЛЯЕЫХ ПОЛЕЙ ТАБЛИЦ

    @staticmethod
    def bonds_month_of_cupon_date_t01 (date_t01):
        """
        Вычисление месяц из формата с датой формата YYYY-MM-DD
        t1 - тип 01 ( формат YYYY-MM-DD)
        Category: Облигации
        """
        parts = date_t01.split('-')
        mo = parts[1]
        return mo



    @staticmethod
    def add_col_to_df_for_cupone_date_for_bonds(df, newColName, **kwargs):
        """
        SPEC: BondsMainManager
        Вычисление месяц из формата с датой формата YYYY-MM-DD  для выходной таблицы HTML
        Специализированная функция для добавления колонки с вычисляемым полем месяца из даты выалта купона
        Category: Облигации
        """
        print('START: add_col_to_df_for_cupone_date_for_bonds() ')

        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
        df[newColName] =  df.apply(lambda row: row.coupon_date.split('-')[1] if row.coupon_date else '-1' , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...


        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        # print(f"{df}")

        return newColInx





    @staticmethod
    def add_if_month_in_paym_vector_of_bond_calc_column(df, month, newColName):
        """
        CALC FIELD: BondsMainManager
        Добавление колонки с флагом False или True , который показывает подпадает ли искомый месяц под месяцы выплат по облигациям фрейма, в котором находится их ISIN
        Category: Облигации
        """
        print('START: add_if_month_in_paym_vector_of_bond_calc_field() ')

        bmm = BondsMainManager(DB_BONDS_)
        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
        df[newColName] =  df.apply(lambda row: bmm.if_given_month_belongs_to_month_payment_vector_of_bond_by_isin_v2(month, row['isin']) , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...

        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        return newColInx




    @staticmethod
    def add_bond_name_col_calc_field(df, newColName, **kwargs):
        """
        CALC FIELD: BondsMainManager
        Добавление колонки с кратким названием облигации выисляемому по ее ISIN
        Category: Облигации
        """
        BondsMainManager.print_IF_DEBUG_bmm("\n-- START ->  ",  {
            'module' : 'BondsMainManager',
            'method' : 'add_bond_name_col_calc_field()' 
            })

        bmm = BondsMainManager(DB_BONDS_)

        # print(f"newColName = {newColName}")
        
        

        # Натрйока названия поля, где хранится isin
        if 'add_bond_name_col_calc_field' in kwargs: # Если в kwargs параметрах задано названия колонки фрейма, где хранится isin, то настраиваем его. Если нет, то по умолчанию это 'isin'
            keyField = kwargs['add_bond_name_col_calc_field']
        else:
            keyField = 'isin'
            
        # print(f"keyField= {keyField}")

        # print(f'@@##########&&&&&&&&&& keyField = {keyField}')

        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
        df[newColName] =  df.apply(lambda row: bmm.get_bond_name_by_isin_BMM(row[keyField]) , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...

        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        print('-- END : ')
        BondsMainManager.print_IF_DEBUG_bmm("START: ",  {
            'module' : 'BondsMainManager\n',
            'method' : 'add_bond_name_col_calc_field()' 
            })

        return newColInx




    @staticmethod ## Закаментино 23-06-2023 / Не понадобилось. Можно удалить
    def add_bond_name_col_calc_field_v2(df, newColName, **kwargs):
        """
        CALC FIELD: BondsMainManager
        Добавление колонки с кратким названием облигации выисляемому по ее ISIN
        Category: Облигации
        """
        BondsMainManager.print_IF_DEBUG_bmm("\n-- START ->  ",  {
            'module' : 'BondsMainManager',
            'method' : 'add_bond_name_col_calc_field()' 
            })

        bmm = BondsMainManager(DB_BONDS_)

        # print(f"newColName = {newColName}")
        
        

        # Натрйока названия поля, где хранится isin
        if 'add_bond_name_col_calc_field' in kwargs: # Если в kwargs параметрах задано названия колонки фрейма, где хранится isin, то настраиваем его. Если нет, то по умолчанию это 'isin'
            keyField = kwargs['add_bond_name_col_calc_field']
        else:
            keyField = 'isin'
            
        # print(f"keyField= {keyField}")

        # print(f'@@##########&&&&&&&&&& keyField = {keyField}')

        try:
        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
            df[newColName] =  df.apply(lambda row: bmm.get_bond_name_by_isin_BMM(row[keyField]) , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...
        except Exception:
            raise  exception_factory(AddCalculatedColumnErr, "add_bond_name_col_calc_field_v2 / bonds_main_manager.py / BondsMainManager")

        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        print('-- END : ')
        BondsMainManager.print_IF_DEBUG_bmm("START: ",  {
            'module' : 'BondsMainManager\n',
            'method' : 'add_bond_name_col_calc_field()' 
            })

        return newColInx




    @staticmethod
    def add_inn_by_isin_col_calc_field(df, newColName, **kwargs):
        """
        CALC FIELD: BondsMainManager
        Добавление колонки с ИНН облигации вычисляемому по ее ISIN, если таковой есть(то есть если облигация корпоративная)
        Category: Облигации
        """
        print('START: add_inn_by_isin_col_calc_field() ')

        bmm = BondsMainManager(DB_BONDS_)

        # Натрйока названия поля, где хранится isin
        if 'add_inn_by_isin_col_calc_field' in kwargs: # Если в kwargs параметрах задано названия колонки фрейма, где хранится isin, то настраиваем его. Если нет, то по умолчанию это 'isin'
            keyField = kwargs['add_inn_by_isin_col_calc_field']
        else:
            keyField = 'isin'

        # print(f'@@##########&&&&&&&&&& keyField = {keyField}')

        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
        df[newColName] =  df.apply(lambda row: bmm.get_inn_by_isin_BMM(row[keyField]) , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...

        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        return newColInx



    @staticmethod
    def add_bond_buy_date_calc_col(df, newColName, **kwargs):
        """
        CALC FIELD: BondsMainManager
        Добавление колонки с датой в иномформате, чем дата-ключ в табл bonds_bought
        Category: Облигации
        """
        print('START: add_bond_name_col_calc_field() ')

        bmm = BondsMainManager(DB_BONDS_)
        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
        df[newColName] =  df.apply(lambda row: row['dtime_bought'] , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...

        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        return newColInx










    @staticmethod
    def add_total_qn_bonds_grouped_by_isin(df, newColName, **kwargs):
        """
        CALC FIELD: BondsMainManager
        Добавление колонки с  общим кол-вом облигаций сгруппированных по ISIN 
        Category: Облигации
        """

        print('START: add_total_qn_bonds_grouped_by_isin()')

        bmm = BondsMainManager(DB_BONDS_)
        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
        df[newColName] =  df.apply(lambda row: bmm.get_total_qn_bought_bonds_by_isin(row['isin']) , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...

        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        return newColInx





    @staticmethod
    def add_icons_links(df, newColName, **kwargs):
        """
        CALC FIELD: BondsMainManager
        Добавление колонки с  иконками-ссылками
        Category: Облигации
        """

        print('START: add_icons_links()')

        bmm = BondsMainManager(DB_BONDS_)
        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
        # df[newColName] =  df.apply(lambda row: bmm.get_total_qn_bought_bonds_by_isin(row['isin']) , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...
        df[newColName] =  df.apply(lambda row: 
                                f"""<a id="popover_{row['isin']}" data-bs-toggle="popover" data-bs-trigger="focus" href="" onclick="elPopClick('{row['isin']}')" >
                                <img src="assets/more-app.png" alt="Profile" width="20" height="20">
                                </a>""" 
                                , axis = 1)

        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        return newColInx




    @staticmethod
    def add_icons_del_from_ixpkg(df, newColName, **kwargs):
        """
        CALC FIELD: BondsMainManager
        Удаление записи из индексного пакета
        Category: Облигации
        """

        print('START: add_icons_del_from_ixpkg()')

        bmm = BondsMainManager(DB_BONDS_)
        df[newColName] =  df.apply(lambda row: 
                                f"""<a  href="#" onclick="delFromIxPkg('{row['isin']}')" >
                                <img src="assets/delete.png" alt="Profile" width="20" height="20">
                                </a>""" 
                                , axis = 1)

        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        return newColInx



    @staticmethod
    def add_raex_raiting_calc_col(df, newColName, **kwargs):
        """ 
        CALC FIELD: BondsMainManager
        Калькулируемое поле, проставляет рейтинг эмитента бумаги
        Category: Облигации
        """

        print('START: add_total_qn_bonds_grouped_by_isin()')

        bmm = BondsMainManager(DB_BONDS_)

        # Натрйока названия поля, где хранится isin
        if 'add_raex_raiting_calc_col' in kwargs: # Если в kwargs параметрах задано названия колонки фрейма, где хранится isin, то настраиваем его. Если нет, то по умолчанию это 'isin'
            keyField = kwargs['add_raex_raiting_calc_col']
        else:
            keyField = 'isin'

        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
        df[newColName] =  df.apply(lambda row: bmm.get_bond_raiting_by_isin(row[keyField]) , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...

        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        return newColInx



    @staticmethod
    def add_bonds_bought_qn_calc_col(df, newColName, **kwargs):
        """ 
        CALC FIELD: BondsMainManager
        Калькулируемое поле, проставляет рейтинг эмитента бумаги
        Category: Облигации
        """

        print('START: add_bonds_bought_qn_calc_col()')

        bmm = BondsMainManager(DB_BONDS_)

        # Натрйока названия поля, где хранится isin
        if 'add_bonds_bought_qn_calc_col' in kwargs: # Если в kwargs параметрах задано названия колонки фрейма, где хранится isin, то настраиваем его. Если нет, то по умолчанию это 'isin'
            keyField = kwargs['add_bonds_bought_qn_calc_col']
        else:
            keyField = 'isin'

        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
        df[newColName] =  df.apply(lambda row: bmm.get_bonds_bought_qn_by_isin_BMM(row[keyField]) , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...

        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        return newColInx



    @staticmethod
    def add_row_backgr_color_sys_diff_BMM(df, newColName, **kwargs):
        """ 
        CALC FIELD: BondsMainManager
        Добавляет расчетное системное поле для цвета бэкграунда ряда в таблице на базе задаваемых метрик из таблицы differenciate (ввести в ранг: системного подхода)
        !!! Если задана калькулируемая колонка цветовой дифференциации в словаре соответствий заголовкой, то ОБЯЗАТЕЛЬНО во вьюере, который использует этот словарь
        соотвтетвий должна быть настройка маркеров для dsoc_kwargs параметров в виде :
        calcColorParams['add_row_backgr_color_sys_diff_BMM'] = {} # Словарь с параметрами для настрйоки цветовой дифференциации в функции 'add_row_backgr_color_sys_diff_BMM'
        calcColorParams['add_row_backgr_color_sys_diff_BMM']['markers'] = ['ROW_COLOR_IXPKGS'] # Маркеры, активируемые дял цифровой дифференциации для данного вьюера 
        viewSets['colorColPars'] = calcColorParams
        Category: Цветовые дифференциаторы
        """

        bmm = BondsMainManager(DB_BONDS_)

        # ФОРМИРОВАНИЕ параметров цветовой дифференциации, переданных из вьюера для данной конкретной функции  !!!
        keyField = 'isin' # По умолчанию, до формирвоания параметров из вьюера для этой функции
        diffMarkers = [] # По умолчанию список маркеров пустой (то есть нет никакой цветовой дифференциации вообще)

        # Эти словари должны быть ОБЯЗАТЕЛЬНО заданы во вьюере, использующим словарь соотвтетствий заголовкоы, в котором задана колонка для цветовой дифференциации рядов таблицы из этого вьюера
        if 'colorColPars' in kwargs:
            colorColPars = kwargs['colorColPars'] # Совокупность параметров для цветовых дифференциаций общая

            if 'add_row_backgr_color_sys_diff_BMM' in colorColPars: # Если в kwargs параметрах задано названия колонки фрейма, где хранится isin, то настраиваем его. Если нет, то по умолчанию это 'isin'
                paramsForThisFunc = colorColPars['add_row_backgr_color_sys_diff_BMM']

                print(f"$$$$$$$$$$$$$$$$$^^^^^^^^^^^^^^^^^^^^^^########## paramsForThisFunc = {paramsForThisFunc} <BondsMainManager.add_row_backgr_color_sys_diff_BMM> ")

                # Параметры маркеров
                if 'markers' in paramsForThisFunc:
                    diffMarkers = paramsForThisFunc['markers']

                    print(f"@@@@@@@@@@@@@@@@@@ diffMarkers = {diffMarkers}  <BondsMainManager.add_row_backgr_color_sys_diff_BMM> ")

                # Параметр keyField, по умолчанию равен 'isin'
                if 'keyField' in paramsForThisFunc:
                    keyField = paramsForThisFunc['keyField']

                    print(f"*****************&&&&&&&&&&&&&&&&&  keyField = {keyField}  <BondsMainManager.add_row_backgr_color_sys_diff_BMM> ")


        # Задаваемый список маркеров через **kwargs, по которым должна производится цветовая дифференциация рядов таблицы из источника df
        # diffMarkers = ['ROW_COLOR_IXPKGS'] 

        # A. Получить все записи в таблице fifferenciator с маркерами в списке diffMarkers
        listDictsMarkersTotal = [] # Полный список записей из таблицы differenciator с заданными маркерами в виде списка словарей рядов этой таблицы

        for marker in diffMarkers:

            sqlMarkers = f'SELECT * FROM {TB_DIFFERENCIATOR_} WHERE sys_marker = "{marker}" '

            # listDictsMarkers = bmm.get_diff_dic_by_marker_name(colorMarker)

            dfMarkers = bmm.read_sql_to_df_pandas(sqlMarkers)

            dictsMarkers = BondsMainManager.convert_df_to_list_of_dicts_PM(dfMarkers)

            listDictsMarkersTotal += dictsMarkers
        
        # Получение общего скписка ключей для всех задаваемых в  diffMarkers дифференцирующих маркеров цвета
        # Цикл по списку словарей с полными записями заданных маркеров из табл differenciator
        framesList = [] # общий список фреймов, содержащих значения ключей дял дифференциации по всем источникам от всех заданных маркеров
        for markerDict in listDictsMarkersTotal:

            # дефолтное значение цвета передается в лямбда функцию последнее по циклу, так как они одинаковы для всех однородных маркеров
            colors = [markerDict['quality1'], markerDict['quality2']] 

            # дефолтное значение цвета передается в лямбда функцию последнее по циклу, так как они одинаковы для всех однородных маркеров
            colors = [markerDict['quality1'], markerDict['quality2']] 

            diffTb = markerDict['diff_ds'] # источник значений дифференциальных ключей сверки
            # ключевая колонка в источнике дифференциальных ключей сверки (в лямбда-функцию передается последнее значение по циклу, так как они одинаковы для всех однородных маркеров)
            diffKeyCol = markerDict['key_field'] 

            # Фрейм ключей, по которым производится цветовая дифференциация общего источника данных df
            sql = f'SELECT {diffKeyCol} FROM {diffTb}'

            dfDiffKeys = bmm.read_sql_to_df_pandas(sql)


            # Добавить колонку с цветом для этих ключей
            dfDiffKeys['quality1'] =  dfDiffKeys.apply(lambda row: colors[0] , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...
            # dfDiffKeys['quality2'] =  dfDiffKeys.apply(lambda row: colors[1] , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...

            framesList.append(dfDiffKeys)

        # Общий обьединенный фрейм всех значений дифф-ключей с их цветами выделения
        dfDiffKeysRes = pd.concat(framesList)

        # Добавляем колонку на основе самой колонки coupon_date, вычислив есяц выплат как второй элемент сплита по делиметру '-' от формата даты YYYY-MM-DD
        df[newColName] =  df.apply(lambda row: bmm.if_isin_in_ds_color_diff_BMM(dfDiffKeysRes, diffKeyCol, row[keyField], colors[1]) , axis = 1) # Специализирующее название колонки с датой купона в правлй части row.coupon_date...

        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма

        print(f"%%%%%%%%%%%%%%%^^^^^^^^^^^^^^^   df[newColName] = {df[newColName]}")

        return newColInx





# END ФУНКЦИИ КАЛЬКУЛЯЦИИ ВЫЧИСЛЯЕЫХ ПОЛЕЙ ТАБЛИЦ



# ФУНКЦИИ ДЛЯ РАСЧЕТНЫХ ПОЛЕЙ ВСПОМОГАТЕЛЬНЫЕ  

    @staticmethod
    def if_isin_in_ds_color_diff_BMM(df, diffKeyCol, checkVal, colorDefault = 'White'):
        """
        BondsMainManager
        Проверить находится ли isin в заданном источнике. Если находится, то вернуть цвет с индексом 0 в списке цветов, иначе - с индексом 1
        colorDefault - цвет по умолчанию
        checkVal - значение, которое ищется в ключевой колонке (например, значение isin в главном фрейме)
        diffKeyCol - название ключевой колонки , в которйо осуществляется сверак занчения checkVal
        Category: Цветовые дифференциаторы
        """

        listDictDiff = BondsMainManager.get_list_dicts_from_df_by_col_value_PM(df, diffKeyCol, checkVal)

        if len(listDictDiff) > 0: # Если найдена запись в источнике дифф-ключей, то присваиваем цвет дифф
            color = (listDictDiff[0])['quality1']
        else: # Если не найдено, то цвет - по умолчанию который
            color = 'White'

        return color



# END ФУНКЦИИ ДЛЯ РАСЧЕТНЫХ ПОЛЕЙ ВСПОМОГАТЕЛЬНЫЕ  

# РАСПЕЧАТКИ, ЛОГИ, КОММЕНТАРИИ 

    # Распечатка информации о фрейме
    @staticmethod
    def print_IF_DEBUG_bmm(message, pars, ifPrint = False, timeFlag = False, timeFormat = FORMAT_2_2_, **kwargs):
        """
        BondsMainManager / from bonds.bonds_main_manager import  BondsMainManager
        Распечатки различного рода в зависимости от настройки DEBUG_
        message - сообщение
        ifPrintDF - флаг распечатки, преодолевающий выключенный флаг DEBUG_
        pars -  словарь с координатами источника распечатки {'module': module or class Name, 'method'  : FuncName},  и с другими возможными в будущем прямыми параметрами
        timeFlag - Флаг простановки времени распечатки в сообщении
        timeFormat - формат времени в распечатке
        kwargs - доп параметры, Которые могут понадобится в будущем
        
        ПРИМЕР:
        
        BondsMainManager.print_IF_DEBUG_bmm("\n-- START ->  ",  {
            'method' : 'convert_df_columns_by_set_of_lambda_funcs_pandas()',
            'module' : 'PandasManager',
            })
            
        BondsMainManager.print_IF_DEBUG_bmm("-- END ->  ",  {
            'method' : 'convert_df_columns_by_set_of_lambda_funcs_pandas()',
            'module' : 'PandasManager\n',
            })
        Category: Распечатки
        """
        if (DEBUG_  or ifPrint):
            txt = f"{message} / {pars['method']} / {pars['module']}"
            if timeFlag :
                txt += FG.get_current_time_with_format(timeFormat)
            print(txt)
            
            




    # END Распечатка информации о фрейме


# END РАСПЕЧАТКИ, ЛОГИ, КОММЕНТАРИИ 

# МЕТА ДАННЫЕ БД
    
    def print_indexed_tb_fields(self, tb):
        """
        BondsMainManager
        Распечатать индексированыне поля таблицы из фрейма
        Category: Распечатки
        """
        db_proc  = SqlitePandasProcessor(DB_BONDS_)

        dfFields = db_proc.get_tb_fields_to_df_pandas(tb)
        print(dfFields)
        return dfFields



# END МЕТА ДАННЫЕ БД






    def update_bonds_archive_on_base_of_bonds_current (self):
        """
        BondsMainManager
        Обновить текущие данные в таблице bonds_archive на основе обновленной bonds_current
        Category: Облигации
        """
        db_proc = SqlitePandasProcessor(DB_BONDS_)


        getFields = [
                    'isin',
                    'bond_name',
                    'start_date',
                    'end_date',
                    'years_to_end',
                    'yield',
                    'annual_yield',
                    'last_annual_yield',
                    'curr_price',
                    'volume',
                    'coupon',
                    'frequency',
                    'nkd',
                    'durration',
                    'coupon_date',
                    'oferta'
        ]


        dfBondsCurrent = db_proc.read_table_by_sql_to_df_pandas(TB_BONDS_CURRENT_,getFields)

        print (dfBondsCurrent)
        db_proc.update_from_df_by_key_col_pandas(TB_BONDS_ARCIVE_, dfBondsCurrent, 'isin')




# СПЕЦИАЛИЗИРОВАННЫЕ



    def get_bonds_under_fapvdo_ratings(self):
        """
        BondsMainManager
        Получить общий(свободный от всех манипуляций типа сортировка, фильтрация ит.д.) фрейм с облигациями в разрезе fapvado рейтинга
        С конвертацией всех необходимых колонок с % в float
        Category: Облигации
        """

        # Получение SQL inner join  облигаций и эмитентов
        # TODO: Перенести механизм JOIN-ов в синтаксер !!!
        tb1 = TB_BONDS_CURRENT_
        tb1Key = 'inn_ref'
        tb2 = TB_FAPVDO_COMPS_RAITINGS_
        tb2Key = 'inn'

        ijSQL = f"""
                    SELECT *
                    FROM 
                        {tb1}
                    INNER JOIN {tb2} 
                        ON {tb1}.{tb1Key} = {tb2}.{tb2Key}
            """

        # print(f"ijSQL = {ijSQL}")

        # Получить фрейм на основе ijSQL
        db_proc = SqlitePandasProcessor(DB_BONDS_)
        dfFapvdoBonds = db_proc.read_sql_to_df_pandas(ijSQL)
        # print(f"dfFapvdoBonds = \n{dfFapvdoBonds}")
        # SqlitePandasProcessor.print_indexed_df_cols(dfFapvdoBonds)

        # Очистка и конвертация колонок с действительными числами в стринговом выражении от знака '%' в float
        dfFapvdoBonds = BondsMainManager.clear_format_bonds_fields_to_float(dfFapvdoBonds)

        return dfFapvdoBonds



    def get_bonds_under_fapvdo_and_raex_ratings(self):
        """
        Получить общий(свободный от всех манипуляций типа сортировка, фильтрация ит.д.) фрейм с облигациями в разрезе fapvado & raex рейтинга
        С конвертацией всех необходимых колонок с % в float
        Category: Облигации
        """


        from project_bonds_html.projr.classes.sys_algorithms import SysAlgorithms # НЕ ПЕРЕНОСИТЬ отсюда!!!(этот import д.б. внутри функции)

        # 1. Получение фрейма облигаций в разрезе рейтингов fapvdo

        dsocFapvdoBonds = SysAlgorithms.a_015_get_bonds_under_raiting_fapvdo()
        dfFapvdoBonds = dsocFapvdoBonds.genDf
        # print(f"dfFapvdoBonds_N = {len(dfFapvdoBonds)}")

        # 2. Получение фрейма облигаций в разрезе рейтингов raex

        dsocRaexBonds = SysAlgorithms.a_016_get_bonds_under_raiting_raex()
        dfRaexBonds = dsocRaexBonds.genDf
        # print(f"dfRaexBonds_N = {len(dfRaexBonds)}")


        # 3. Получение пересечения двух фреймов c облигациями по полю isin

        dfIntersect = pd.merge(dfFapvdoBonds, dfRaexBonds, how='inner', on=['isin'])
        # print(f"dfIntersect_N = {len(dfIntersect)}")
        # SqlitePandasProcessor.print_indexed_df_cols(dfIntersect)

        return dfIntersect



    def get_df_comps_inns_under_fapvdo_raitings_with_URI_given_level(self, levelURICond):
        """
        Получить компании в разрезе FAPVDO existing raitings
        levelURICond - Условия по уровню URI - зада.тся списком типа  ['>=', 1]
        Category: Облигации
        """
        # sql- запрос с заданынми условиями по рейтингу и уровню URI
        sql  = f"SELECT * FROM {TB_FAPVDO_COMPS_RAITINGS_} WHERE inn!='NOT FOUND' AND uir {levelURICond[0]} {levelURICond[1]}"
        print(f"sql = {sql}")
        dfCompsFapvdoRait = self.read_sql_to_df_pandas(sql) # isin компаний , подпадающих под условия raitings_sys и уровня levelURI
        return dfCompsFapvdoRait



    def get_df_comps_inns_under_raex_raitings(self):
        """
        ЗАГОТОВКА
        Получить компании в разрезе RAEX existing raitings
        Category: Облигации
        """

        # sql- запрос с заданынми условиями по рейтингу и уровню URI
        sql  = f"SELECT inn FROM {TB_RAEX_COMPS_RAITINGS_} WHERE inn!='NOT FOUND'"
        print(f"sql = {sql}")
        dfCompsRaexRait = self.read_sql_to_df_pandas(sql) # isin компаний , подпадающих под условия raitings_sys и уровня levelURI
        return dfCompsRaexRait












    def get_total_complex_bonds_frame_mv(self):
        """
        NEW: Раньше был в другом модуле  (mv - moved, перенесен из другого модуля по смыслу)
        BondsMainManager
        Получить полную комплексную фрейм всех облигаций из БД (ОФЗ, Муниуцип, корп) с проставленными метками типа облигаций в поле f8
        и цветовой дифференциацией в поле f7 в зависимости от типа облигаций в f8. Колонки annual_yield, last_annual_yield и curr_price прочищены от % и трансформированы в тип float
        Category: Облигации
        """

        # db_proc = SqlitePandasProcessor(DB_BONDS_)
        # Корпоративные облигации из табл bonds_current
        dfCorpBonds = self.read_table_by_sql_to_df_pandas(TB_BONDS_CURRENT_)
        # Государственные облигации ОФЗ из табл ofz_current
        dfOfzBonds = self.read_table_by_sql_to_df_pandas(TB_OFZ_CURRENT_)
        # Субфедеральные или муниципальные облигации из табл municip_current
        dfMunicipBonds = self.read_table_by_sql_to_df_pandas(TB_MUNICIP_CURRENT_)

        # Простановка меток ОФЗ, корпоратвная, муниципальныая в полях колонки 'f8' для будущей  дифференциации по категории облигаций в общем массиве
        # A. Простановка меток в фрейме корпоративных облигаций dfCorpBonds
        colsConstsDic = {'f8': 'КОРП'}
        self.set_const_vals_to_df_cols_pandas(dfCorpBonds,  colsConstsDic)
        # Простановка класса ряда для цветовой дифференциации рядов с облигациями типа 'КОРП'  # НЕ УДАЛЯТЬ - это метка по типу 'КОРП'
        # Поле на дифференцируется по цвету для облигаций типа 'КОРП' 
        colsConstsDic = {'f7': 'White'} # 'table-warning' - класс для ряда в конечной таблице Bootstrap , которые выделяет ряд светло-желтым
        self.set_const_vals_to_df_cols_pandas(dfCorpBonds,  colsConstsDic)

        # B. Простановка меток в фрейме с ОФЗ dfOfzBonds
        colsConstsDic = {'f8': 'ОФЗ'}
        self.set_const_vals_to_df_cols_pandas(dfOfzBonds,  colsConstsDic)
        # Простановка бэкграунда ряда в поле 'f7' для цветовой дифференциации рядов с облигациями типа 'ОФЗ' 
        colsConstsDic = {'f7': 'LemonChiffon'} # 'table-warning' - класс для ряда в конечной таблице Bootstrap , которые выделяет ряд светло-желтым
        self.set_const_vals_to_df_cols_pandas(dfOfzBonds,  colsConstsDic)


        # C. Простановка меток в фрейме муниципальных облигаций dfCorpBonds
        colsConstsDic = {'f8': 'МУНИЦ'}
        self.set_const_vals_to_df_cols_pandas(dfMunicipBonds,  colsConstsDic)
        # Простановка класса ряда в поле 'f7' для цветовой дифференциации рядов с облигациями типа 'ОФЗ' 
        colsConstsDic = {'f7': 'PowderBlue'} # 'table-success' - класс для ряда в конечной таблице Bootstrap , которые выделяет ряд светло-зеленым
        self.set_const_vals_to_df_cols_pandas(dfMunicipBonds,  colsConstsDic)

        # Обьединение 3х фреймлв в один, чтобы поля одинаковых смысловых колонок соотвтетсвовали друг другу
        frames = [dfCorpBonds, dfOfzBonds, dfMunicipBonds]
        dfComplexBonds = pd.concat(frames)

        # Очистка колонок с действительными числами в стринговом выражении от знака '%'
        # dfComplexBonds= PandasManager.clear_str_float_from_persent_simb(dfComplexBonds, 'annual_yield')
        dfComplexBonds = self.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'annual_yield')
        dfComplexBonds = self.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'last_annual_yield')  # !!
        dfComplexBonds  = self.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'curr_price')


        return dfComplexBonds



    def get_complex_bonds_df_with_added_diff_columns(self, tbCorpBonds, tbOfzBonds, tbMunicipBonds, bgColors = ['White', 'LemonChiffon', 'PowderBlue']):
            """
            Сформировать обьединенный комплексный фрейм со смешанными бумагами всех типов с дифференциалльными метками по типу бумаг и цвету в отдельных добавленных колонках фрейма
            BondsMainManager
            bgColors - задает цвета фона рядов для трех видов облигаций для цветовой дифференциации
            Колонки annual_yield, last_annual_yield и curr_price прочищены от % и трансформированы в тип float
            Category: Облигации
            """

            # db_proc = SqlitePandasProcessor(DB_BONDS_)
            # Корпоративные облигации из табл bonds_current
            dfCorpBonds = self.read_table_by_sql_to_df_pandas(tbCorpBonds)
            dfCorpBonds['type'] = 'КОРП'
            dfCorpBonds['bg_color'] = bgColors[0]
            # Государственные облигации ОФЗ из табл ofz_current
            dfOfzBonds = self.read_table_by_sql_to_df_pandas(tbOfzBonds)
            dfOfzBonds['type'] = 'ОФЗ'
            dfOfzBonds['bg_color'] = bgColors[1]
            # Субфедеральные или муниципальные облигации из табл municip_current
            dfMunicipBonds = self.read_table_by_sql_to_df_pandas(tbMunicipBonds)
            dfMunicipBonds['type'] = 'МУНИЦ'
            dfMunicipBonds['bg_color'] = bgColors[2]


            # Обьединение 3х фреймлв в один, чтобы поля одинаковых смысловых колонок соотвтетсвовали друг другу
            frames = [dfCorpBonds, dfOfzBonds, dfMunicipBonds]
            dfComplexBonds = pd.concat(frames, ignore_index=True) # autoreset index after a concatenation

            # Очистка колонок с действительными числами в стринговом выражении от знака '%'
            # dfComplexBonds= PandasManager.clear_str_float_from_persent_simb(dfComplexBonds, 'annual_yield')
            dfComplexBonds = self.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'annual_yield')
            dfComplexBonds = self.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'last_annual_yield')  # !!
            dfComplexBonds  = self.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'curr_price')


            return dfComplexBonds




    def get_bond_month_payment_objects_by_isin(self, isin, keyFieldVal = {'dtime_bought': ''}):
        """
        BondsMainManager
        Получить список названий месяцев выплат по облигации из ее isin
        keyFieldVal - словарь, ключ со значением (либо с пустым значением, которое можно подставить после), по которому находится запись в таблице БД, которую надо арпдейтить данными 
        по календарным выплатам. По умолчанию равен полю в табл bonds_bought 'dtime_bought' и пустому значению, которое после можно заполнить  {'dtime_bought': ''} 
        Ключ необходим для формирования фрейма , на базе которого происходит апдейт полей в таблице, которыую надо будет апдейтить
        
        <ВОЗВРАТ>
        bondMonthInxPayList - список с индексами месяцев выплат купона для облигации
        bondMonthPayList - списка названий полей месяцев из табл bonds_bought соотвтетствующих списку bondMonthPayList
        dfBondMonthPay - одномерный фрейм с колонками в виде названий полей месяцев выплат облигации и с величинами в этих полях равными купонной выплате (на данный момент - константы)
        ПР: [bondMonthInxPayList, bondMonthPayList, dfBondMonthPay] 
        Category: Облигации
        """


        # B. Полный фрейм облигаций
        dfComplexBonds = self.get_total_complex_bonds_frame_mv()

        # C.  Данные по облигации 

        # isin = reqPars['isin'] # isin
        # Все данные оп одной облигации, найденной по ISIN
        dfBondByIsin = self.search_mask_rows_by_col_val_pandas(dfComplexBonds, 'isin', isin) 
        coupon = dfBondByIsin.iloc[0]['coupon'] # купон
        couponDate = dfBondByIsin.iloc[0]['coupon_date']
        # print (f"COUPON = {coupon}")


        # 4. Простановка вектора помесячных выплат в полях Jan...Dec

        # Формула распределения купонов по месяцам в зависимости от астоты выплат и следующего месяца выплат
        
        couponMonthInx = int(couponDate.split('-')[1]) # индекс месяца следующей за ппокупкой выплаты купонов по облигации в целочисленном варианте
        print(couponMonthInx)

        # couponMonthInx = 5

        couponFrequency =  int(dfBondByIsin.iloc[0]['frequency']) # частота выплат купона за год
        print(couponFrequency)

        # Словарь обобщенных нормализованных векторов помесячных выплат в зависимости от частоты выплат в году, где частота выплат в году является ключем словаря
        #TODO: Можно сделать, что бы нормализированные векторы создавались сами только от на базе частоты выплат
        dicOfPossiblePaymentsVectors = {

                2 : np.array([0, 6]),
                4 : np.array([0,3,6,9]),
                6 : np.array([0,2,4,6,8,10]),
                12 : np.array([0,1,2,3,4,5,6,7,8,9,10,11])

        }

        # Нормализованный обобщенный вектор помесячных выплат в году с частотой = 4
        normMonthPayVector = dicOfPossiblePaymentsVectors[couponFrequency]

        # print (f"payMonthVaector = {normMonthPayVector}")

        # Индивидуальный ненормализованный вектор помесячных выплат (ИВПВ) для данной облигации
        bondMonthPayVector = normMonthPayVector  +  couponMonthInx

        # print (f"bondMonthPayVector = {bondMonthPayVector}")  # Res: bondMonthPayVector = [ 3  6  9 12]


        # Приведение индивидуального вектора к нормальному и уже индивидуальному виду
        bondNormMonthPayVector = bondMonthPayVector + np.where(bondMonthPayVector > 12, -12, 0 )

        # print (f"bondNormMonthPayVector = {bondNormMonthPayVector}")
        

        # Имея нормализованный индивидкальный вектор помесячных выплат по облигации легко сделать распределение купонных выплат по месяцам для данной облигации

        # Перевод вектора в список с индексами месяцев выплат купона для облигации
        bondMonthInxPayList = list(bondNormMonthPayVector)
        print (f"bondMonthInxPayList = {bondMonthInxPayList}")


        MONTH_INDEX_ASSCOC_DIC_ = {

                        1 : 'jan',
                        2 : 'feb',
                        3 : 'march',
                        4 : 'apr',
                        5 : 'may',
                        6 : 'june',
                        7 : 'july',
                        8 : 'aug',
                        9 : 'sept',
                        10 : 'oct',
                        11 : 'nov',
                        12 : 'dec',

                    }


        # Получение списка названий полей месяцев из табл bonds_bought соотвтетствующих списку bondMonthPayList
        bondMonthPayList = [MONTH_INDEX_ASSCOC_DIC_[x] for x in bondMonthInxPayList]
        print (f"bondMonthPayList = {bondMonthPayList}")

        # Вставка  выплат купона по полям месяцев в таблицу bonds_bought для данной облигации с известным isin

        # Составление словаря месячных выплат облигации для создания на его основе фрейма
        dicBondMonthPay = {}
        for mo in bondMonthPayList: # Цикл по списку названий полей с месяцами по вектору месяцев выплат
            # print(f"mo = {mo}")
            dicBondMonthPay[mo] = coupon


        # # # Добавление в словарь ключа 
        keyField = list(keyFieldVal.keys())[0]
        keyVal = list(keyFieldVal.values())[0]
        dicBondMonthPay[keyField] = keyVal


        # Составление фрейма на основе составленного словаря dicBondMonthPay
        # Все названия полей должны соотвтетсвовать табличным
        dfBondMonthPay = self.read_df_from_dictionary(dicBondMonthPay)

        # print(f"dfBondMonthPay = \n{dfBondMonthPay}")

        # <RETURN> <ВОЗВРАЩАЕТ>: 
        # bondMonthInxPayList - список с индексами месяцев выплат купона для облигации
        # bondMonthPayList - списка названий полей месяцев из табл bonds_bought соотвтетствующих списку bondMonthPayList
        # dfBondMonthPay - одномерный фрейм с колонками в виде названий полей месяцев выплат облигации и с величинами в этих полях равными купонной выплате (на данный момент - константы)
        res = [bondMonthInxPayList, bondMonthPayList, dfBondMonthPay] 


        return res




    def get_month_payment_vector_by_frequency_and_one_given_pay_month(self, couponFrequency, oneOfPayMonth):
        """
        Получить вектор выплат облигации по ее частоте выплат и одному из месяцев выплат
        Применение: Необходимо в расчетах облигаций которые подпадают по месяцам купонных выплат под искомый месяц, на который мы хотим , что бы пришлись выплаты от покупаемой бумаги
        Category: Облигации
        """
        # Словарь обобщенных нормализованных векторов помесячных выплат в зависимости от частоты выплат в году, где частота выплат в году является ключем словаря
        #TODO: Можно сделать, что бы нормализированные векторы создавались сами только от на базе частоты выплат
        # TODO: Расширить анализ для всех возможных и адекватных частот по облигациям, которые могут встретиться
        dicOfPossiblePaymentsVectors = {

                2 : np.array([0, 6]),
                4 : np.array([0,3,6,9]),
                6 : np.array([0,2,4,6,8,10]),
                12 : np.array([0,1,2,3,4,5,6,7,8,9,10,11])

        }

        # Нормализованный обобщенный вектор помесячных выплат в году с частотой = 4
        normMonthPayVector = dicOfPossiblePaymentsVectors[couponFrequency]

        # print (f"payMonthVaector = {normMonthPayVector}")

        # Индивидуальный ненормализованный вектор помесячных выплат (ИВПВ) для данной облигации
        bondMonthPayVector = normMonthPayVector  +  oneOfPayMonth

        # print (f"bondMonthPayVector = {bondMonthPayVector}")  # Res: bondMonthPayVector = [ 3  6  9 12]

        # Приведение индивидуального вектора к нормальному и уже индивидуальному виду
        bondNormMonthPayVector = bondMonthPayVector + np.where(bondMonthPayVector > 12, -12, 0 )

        return bondNormMonthPayVector



    def if_given_month_belongs_to_month_payment_vector_of_bond_by_isin(self, givenMonth, isin):
        """
        OBSOLETED: Use if_given_month_belongs_to_month_payment_vector_of_bond_by_isin_v2 () 2й версии ниже
        Сделать вывод принадлежит ли задаваемый индексом месяц множеству месяцев, по которым производятся выплаты для задаваемой ISIN  облигации
        Category: Облигации
        """

        # B. Полный фрейм облигаций
        dfComplexBonds = self.get_total_complex_bonds_frame_mv()

        # C.  Данные по облигации 

        # isin = reqPars['isin'] # isin
        # Все данные оп одной облигации, найденной по ISIN
        dfBondByIsin = self.search_mask_rows_by_col_val_pandas(dfComplexBonds, 'isin', isin) 
        # coupon = dfBondByIsin.iloc[0]['coupon'] # купон
        couponDate = dfBondByIsin.iloc[0]['coupon_date']
        # print (f"COUPON = {coupon}")


        # 4. Простановка вектора помесячных выплат в полях Jan...Dec

        # Формула распределения купонов по месяцам в зависимости от астоты выплат и следующего месяца выплат
        
        couponMonthInx = int(couponDate.split('-')[1]) # индекс ближайшей выплаты купонов (или ближайшего месяца выплат после покупки облигации) купонов по облигации в целочисленном варианте
        print(couponMonthInx)

        # couponMonthInx = 5

        couponFrequency =  int(dfBondByIsin.iloc[0]['frequency']) # частота выплат купона за год
        print(couponFrequency)



        bondNormMonthPayVector = self.get_month_payment_vector_by_frequency_and_one_given_pay_month(couponFrequency, couponMonthInx)

        if givenMonth in bondNormMonthPayVector:
            ret = True
        else:
            ret = False


        return ret



    def if_given_month_belongs_to_month_payment_vector_of_bond_by_isin_v2 (self, givenMonth, isin):
        """
        Version 2. Сделать вывод принадлежит ли задаваемый индексом месяц множеству месяцев, по которым производятся выплаты для задаваемой ISIN  облигации
        Category: Облигации
        """
        # Набор данных по облигациям из всех таблиц с облигациями по разным категориЯм
        # givenMonth = 5
        sql = f"""
            SELECT isin, coupon_date, frequency FROM {TB_BONDS_CURRENT_} WHERE isin = '{isin}'
                UNION
            SELECT isin, coupon_date, frequency FROM {TB_OFZ_CURRENT_} WHERE isin = '{isin}'
                UNION
            SELECT isin, coupon_date, frequency FROM {TB_MUNICIP_CURRENT_} WHERE isin = '{isin}'
        """

        cur = self.execute_sql_with_cursor (sql)
        isin, couponDate, couponFrequency = (self.get_ds_from_cursor (cur))[0] # Перевод результата курсовра в список значений полученной выборки по sql-запросу
        couponMonthInx = int(couponDate.split('-')[1]) # Вычисление индекса месяца выплаты по облигации в целочисленном варианте
        couponFrequency = int(couponFrequency) # Целочисленная частота выплат по облигации
        # Формула распределения купонов по месяцам в зависимости от астоты выплат и следующего месяца выплат
        bondNormMonthPayVector = self.get_month_payment_vector_by_frequency_and_one_given_pay_month(couponFrequency, couponMonthInx)

        if givenMonth in bondNormMonthPayVector:
            ret = True
        else:
            ret = False

        return ret





    def get_inn_list_from_raex_comps_withdrawn(self):
        """
        Получить список inn из таблицы raex_comps_withdrawn
        Category: Облигации
        """

        # Получить список ИНН компаний из таблицы
        getFields = ['inn']
        res = self.select_from_table_with_where_condition(TB_RAEX_COMPS_WITHDROWN_, getFields, {})

        return res




    def get_inn_list_from_bunkrupt_bonds(self):
        """
        Получить список inn из таблицы bunkrupt_bonds обанкротившихся эмитентов
        Category: Облигации
        """

        # Получить список ИНН компаний из таблицы
        getFields = ['inn']
        add = f'GROUP BY inn'
        res = self.select_from_table_with_where_condition(TB_BUNKRUPT_BONDS_, getFields, {}, add)

        return res




    def get_index_packages_BMM(self, getFields = ['*']):
        """
        Получить фрейм с индексными пакетами из табл index_packages
        Category: Облигации
        """

        if getFields[0] == '*':
            sql = 'SELECT * FROM index_packages'
        else:
            fields = ','.join(getFields)
            sql = f'SELECT {fields} FROM index_packages'
            # print(f"sql = {sql}")

        dfPackages = self.read_sql_to_df_pandas(sql)

        return dfPackages


    def get_diff_markers_BMM(self, getFields = ['*']):
        """
        Получить фрейм с записями из таблицы differenciator
        Category: Цветовые дифференциаторы
        """

        if getFields[0] == '*':
            sql = 'SELECT * FROM differenciator'
        else:
            fields = ','.join(getFields)
            sql = f'SELECT {fields} FROM differenciator'
            print(f"sql = {sql}")

        dfPackages = self.read_sql_to_df_pandas(sql)

        return dfPackages


    def get_ix_packages_id_list_bmm(self):
        """
        Получить список id индексных пакетов
        Category: Облигации
        """

        sql = f"SELECT id FROM {TB_INDEX_PACKAGES_}"

        ixPkgList = self.get_result_from_sql_exec_proc(sql)

        return ixPkgList


    def get_inx_package_id_by_nickname_bmm(self, nick):
        """
        Получить id индексного пакета по его ник-нейму
        Category: Облигации
        """
        
        sql = f'SELECT id FROM index_packages WHERE nick = "{nick}"'
        res = self.get_result_from_sql_exec_proc(sql)

        return res


    def get_nickname_by_inx_package_id_bmm(self, id):
        """
        Получить ник-нейм индексного пакета по его id
        Category: Облигации
        """
        
        sql = f'SELECT nick FROM index_packages WHERE id = "{id}"'
        res = self.get_result_from_sql_exec_proc(sql)

        return res



        


    def set_curr_datetime_with_format_to_tb_field_by_keys_or_total(self, tbTrg, dsKeys,  tbTrgKey, dateFormat):
        """
        ЗАГОТОВКА, НЕ ДОДЕЛАНО: Проставить текущее время по заданному формату в поле таблицы по заданному источнику ключей
        dsKeys - любой источник ключей (список, фрейм или запрос. Таблица БД - под вопросом , ее надо доработать, не понятно как задается ключ. Это надо смотреть реализацию 
            в DSourceCube классе и доделать)
            Если dsKeys = '*', то проставляется текущее время для всех записей по заданному полю
        tbTrgKey - название ключа в таблице
        dateFormat - Формат для проставления календарного времени в колонку таблицы
        
        Пример параметров:
        Category: Функции времени
        """
        
        # Pars:
        kwargs = {
            'srcListTitles' : [tbTrgKey] # Задаем тайтл для ключевой колонки фрейма, который по идее состоит из одной колонки
        }
        
        
        # Анализируем список или строка '*'
        dfKeys = self.read_df_from_any_source (dsKeys, **kwargs)
        
        keyColAssocDic = {tbTrgKey : tbTrgKey}
        
        currDateTime = FG.get_current_time_with_format(dateFormat)
        
        tbFieldConstDic = {'f2' : currDateTime}
        
        
        self.set_const_marker_in_table_by_keys(dfKeys, tbTrg, keyColAssocDic, tbFieldConstDic)

        # TODO: Сделать метод обновления или добавления колонки во фремй с результатами по калькуляции полями, как из внутреннего фрейма так и с возможностью из другого фрейма!!!
            
        return dfKeys
        
    




    def set_unix_time_based_on_given_date_field_in_tb (self, dsSrc, tbTrg, keyField, dateField, unixField, **kwargs):
        """ 
        BondsMainManager
        Проставить UNIX-время  на основе заданного поля с  календарной датой с определенным форматом
        dsSrc - источник для аргументов лямбда-функции, который задается любым способом (Указанием названия таблицы, или SQL , где можно филльтровать записи по 
        каким-то признакам (ПРОВЕРЕНО), и т.д. Не проверено, можно ли задавать просто фреймом ?)
        tbTrg - название таблицы, цель для поля , которое обновляетя по результату лямбда-функции. Если берется из той же таблицы, то и указывается та же таблица
        dateField - Поле источник даты-времени в таблице tb
        unixField - поле, где надо проставить UNIX-время на основе dateField
        dateFormat - формат календарной даты-времени в поле dateField
        kwargs - параметры для задания формата и флага округдения unix-времени
        
        RET: Возвращает фрейм dfRes, на базе которого произведено обновление поля в таблице
        
        Пример параметров:
        tb = TB_MUNICIP_CURRENT_
        
        keyField = 'isin'
        dateField = 'f2'
        unixField = 'f11'
        kwargs = {
            'format' : FORMAT_2_, 
            'rinteger' : True
            }
        Category: Функции времени
        """

        colUpdTrg = unixField
        lambFunc = FG.convert_from_date_to_unix_universal_with_kwargs
        listLambArgs = [dateField]
        keyFieldsAssoc = [keyField,keyField]
        dfRes = self.update_tb_col_by_lambda_function_with_args_from_any_tb_pandas (dsSrc, tbTrg, keyFieldsAssoc, colUpdTrg, lambFunc, listLambArgs, **kwargs)
        return dfRes






    def convert_data_format_in_data_column_with_given_data (self, dsSrc, tbTrg, keyField, dataCol, listFormats):
        """
        BondsMainManager
        Конвертировать данные в колонке таблицы со значением по датам в каком-то существующем формате в другой заданный формат данных.
        dsSrc - Источник, задаваемый любым способом (Названием таблицы или SQL-запросом с WHERE, ...)
        keyField - ключ таблицы, по которому производится уникальная идентификация записей
        dataCol - колонка, в которой нужно переконвертировать формат данных
        listFormats - список исходного формата и результирующего форматов [formatSrc, formatRes]

        RET: dfRes - фрейм с ключами, на основе которого произведено обновление колонки colUpd в таблице
        Category: Функции времени
        """

        # Pars:
        keyFieldsAssoc = [keyField,keyField]
        colUpdTrg = ['res', dataCol]
        lambFunc = FG.convert_date_format_to_another_date_format
        listLambArgs = [dataCol]
        lambOutArgs = {'formatSrc' : listFormats[0], 'formatRes' : listFormats[1]}
        dfRes = self.update_tb_col_by_lambda_function_with_args_from_any_tb_pandas(dsSrc, tbTrg, keyFieldsAssoc, colUpdTrg, lambFunc, listLambArgs, **lambOutArgs)
        return dfRes



    






    # END СПЕЦИАЛИЗИРОВАННЫЕ








    # СПЕЦ ФУНКЦИИ ПО ОБЛИГАЦИЯМ




    def delete_from_tb_by_isin_BMM(self, tb, field, fieldVal):
        """
        Удалить запись с идентификацией записей п оisin из любойт таблицы, в которой есть колонка isin
        Category: Облигации
        """

        sql = f'DELETE FROM {tb} WHERE {field} ="{fieldVal}"'
        self.execute_sql(sql)
        



    def get_bonds_bought_qn_by_isin_BMM(self, isin):
        """
        BondsMainManager
        Получить кол-во облигаций заданного isin портфолио из таблицы bonds_bought
        Category: Облигации
        """

        sql = f'SELECT SUM(qn) FROM {TB_BONDS_BOUGHT_} WHERE isin = "{isin}"'

        # print(f"@@##$$ sql = {sql}")
        res = self.get_result_from_sql_exec_proc(sql)

        qn = res[0]
        return qn



    def get_bond_field_val_by_isin_BMM(self, isin, field):
        """
        
        BondsMainManager
        Получить значение любого поля field заданной по isin облигации
        Category: Облигации
        """
        res = self.get_field_val_by_isin_from_complex_bonds_proc_BMM (isin, field)
        # print(f"res = {res}")
        
        fieldVal = res[0]
        return fieldVal



    def get_bond_name_by_isin_BMM(self, isin):
        """
        BondsMainManager
        Получить краткое название облигации по ее ISIN
        Category: Облигации
        """
        bondName = self.get_bond_field_val_by_isin_BMM(isin, 'bond_name')
        return bondName


    def get_inn_by_isin_BMM(self, isin):
        """
        Получить значение любого поля field заданной по isin облигации
        Иногда выходит резльтат одномерный, где не надо приводить по мерности res[0] на выходе
        Category: Облигации
        """

        sql = f'SELECT inn_ref FROM bonds_current WHERE isin="{isin}"'
        res = self.get_result_from_sql_exec_proc(sql)
        if type(res) != int: # Проверка. Если res = -1, то значит не найдено ничего. В ином случае type будет list или tuple
            res_N = len(res)
            inn = res[0]
        else:
            inn = 'None'

        return inn


    def get_bond_raiting_by_isin(self,isin):
        """
        RaexManager
        Получить рейтинг эмитента бумаги по ISIN
        Category: Облигации
        """

        # bmm = BondsMainManager(DB_BONDS_)

        inn = self.get_inn_by_isin_BMM(isin) # inn эмитента isin

        print(f"@@@@@@ inn = {inn}")

        if inn:

            if 'None' not in inn: # Если есть результат

                sql = f'SELECT raiting_raex FROM {TB_RAEX_COMPS_RAITINGS_} WHERE inn = {inn}'

                res = self.get_result_from_sql_exec_proc(sql)

                if type(res) != int: # Проверка. Если res = -1, то значит не найдено ничего. В ином случае type будет list или tuple
                    # res_N = len(res)
                    isinRaiting = res[0]
                else: # Если нет результата
                    isinRaiting = '-'

            else:
                isinRaiting = '-'

        else:
            isinRaiting = '-'

        return isinRaiting




    def get_bonds_bought_df_BMM(self):
        """
        Получить фрейм таблицы bonds_bought
        Category: Облигации
        """
        SQLBondsBought = 'SELECT * FROM bonds_bought'
        dfBondsBought = self.read_sql_to_df_pandas(SQLBondsBought)
        return dfBondsBought





    def distribute_lot_real_payments_by_month_in_bonds_bought_BMM(self):
        """
        Распределить реальные выплаты помесячно в рамках матрицы или вектора помесячных выплат по каждому купленному лоту в таблице bonds_bought
        Category: Облигации
        """

        db_proc = BondsMainManager(DB_BONDS_)

        # Получить df  купленных бумаг из таблицы bonds_bought
        dfBondsBought = db_proc.get_bonds_bought_df_BMM()

        # Внести текущие значения купонов по этим бумагам , взятых из таблиц текущих оперативных облигаций
        for index, row in dfBondsBought.iterrows():

            res = db_proc.get_bond_month_payment_objects_by_isin(row['isin'])

            # Кол-во облигаций, купленных и зарегестрированных в таблице bonds_bought
            bondQn = int(row['qn'])

            # cycle isin - часть ключа комплексного
            partKeyIsin = row['isin']

            # cycle dtime_bought - часть ключа комплексного 
            partKeyDateTime = row['dtime_bought']

            # Значение текущего купона по данной облигации 
            bondCoupon = float(row['curr_coupon'])

            # Суммарная выплата по месячному вектору выплат
            sumMonthpay = round(bondCoupon * bondQn,2)
            
            # Умножаем нормальное значение купона для облигации на кол-во этих облигаций купленных
            monthPayDfCols = res[1] # Месяцы выплат по текущей облигации
            for col in monthPayDfCols:
                # Провести update строк в табл bonds_bought по полям, заданным в dfBondMonthPay - проставить реальные выплаты, которые равны величине купона умноженного на кол-во облигаций по каждоу строке в таблице
                # Pars:
                fieldValDic = {col : sumMonthpay}
                compexKeyDic = {'isin' :partKeyIsin, 'dtime_bought' :  partKeyDateTime}
                db_proc.update_bonds_bought_field_proc_BMM(fieldValDic, compexKeyDic)




    def register_bond_lot_bought_in_tb_bonds_bought(self, reqPars):
        """
        BondsMainManager
        Зарегестрировать покупку лота облигаций с заланным isin, с заданным кол-вом купленных бумаг и с заданным на данный момент величины выплачиваемого купона по этой облигации
        При регистрации производится распределение помесячных выплат в соотвтетсвии с получаемым вектором помесячных выплат по той бумаге
        reqPars - словарь request-значений
        Category: Облигации
        """
        # db_proc = BondsMainManager(DB_BONDS_)

        # isin облигации
        isin = reqPars['isin'] 

        # Текущий купон, проставленный вручную в формк регистрации лота покупки облигации данного ISIN
        currCoupon = float(reqPars['curr_coupon']) 

        # кол-во облигаций, купленных в этом лотк данной облигации с данным ISIN
        qn = int(reqPars['qn']) 

        # Суммарная выплата помесячно по вестору месячных выплат для данной облигации
        totalMonthPay = round(currCoupon * qn, 2) 

        # Время регистрации купленного лота в формате типа: 21_11_2022_14_02
        dt = FG.get_current_time_format1_d_m_y_h_m_s() # Время формата 21_11_2022_14_02

        # Получить вектор нормального распределения помесячных выплат для данной олигации с известным ISIN
        monthIsinPayVectors = self.get_bond_month_payment_objects_by_isin(isin)

        # Поля для вставки помесячных выплат на основе полученных веторов распределения помесЯчных выплат
        monthCols = monthIsinPayVectors[1]

        # Получить фрейм из словаря reqPars с зпданными величинами именных парметров. Фрейм дальше вносится в БД и поэтому названия колонок должны соотвтетсвовать названиям полей
        dfBoughtData = self.read_df_from_dictionary(reqPars)

        # 2. Заполнить фрейм всеми необходимыми дополнительными данными : date_time, pdate, распределение купоннымх выплат по месяцам

        # A. Проставление даты-времени в поле ddate_time и pdate
        # Простановка точного времени в фрейме
        dfBoughtData['dtime_bought'] = dt

        # print(f"dfBoughtData = \n{dfBoughtData}")

        # Добавление колонок с суммарными выплатами по месяцам в соотвтетсвии с полученынми векторами распределения выплат для данной облигации
        for monthField in monthCols:
            dfBoughtData[monthField] = totalMonthPay

        print (f"dfBoughtData = \n{dfBoughtData}")

        # Зарегистрировать покупку лота облигаций с  isin в табл bonds_bought
        # <ВСТАВЛЕНИЕ ДАННЫХ В БД табл - > bonds_bought
        # Внести ланные из фрейма в таблицу bonds_bought без проверки ключей (а ключ всегдабудет уникален, так как есть метка по времени в составе комплексного ключча таблицы bonds_bought)
        self.insert_df_to_tb_no_key_check_pandas(dfBoughtData, 'bonds_bought', ['*'])





    def save_and_transfer_sold_bonds_lot_to_history(self, reqPars):
        """
        BondsMainManager
        Сохранить данные о продаже лота бумаг и данные об их изначальной покупки (из табл bonds_bought) в таблице portfolio_history и удаление из таблицы bonds_bought либо 
        полного лота, либо ег очасти, равной проданному кол-ву облигаций
        reqPars - словарь request-значений
        Category: Облигации
        """

        print(f"save_and_transfer_sold_bonds_lot_to_history()")

        bmm = BondsMainManager(DB_BONDS_)

        # A. isin и  дата-время покупки представляют собой комплексный ключ для однозначной идентификации записи в таблице bonds_bought !!!
        isin = reqPars['sold_isin']  # isin облигации
        print(f"ISIN = {isin}")
        dtime_bought = reqPars['buy_date']  # дата-время покупки
        print(f"dtime_bought = {dtime_bought}")


        # B. Получить данные покупки по записи найденой по ключу isin и  dtime_bought из таблицы bonds_bought

        sql = f'SELECT isin, dtime_bought, qn, nkd, gen_comission, total_cost FROM  bonds_bought WHERE isin = "{isin}" AND dtime_bought = "{dtime_bought}" '
        dfBoughtLot = bmm.read_sql_to_df_pandas(sql)

        # print(f"dfBoughtLot = \n{dfBoughtLot}")

        # C. Добавить к фрейму столбцы с данными по регистрации продажи облгаций из этого лота покупки
        dfBoughtLot['sell_qn'] = [reqPars['sold_qn']]
        dfBoughtLot['sell_commisions'] = [reqPars['sold_gen_comission']] # Общая комиссия при продаже 
        dfBoughtLot['sell_total_cost'] = [reqPars['sold_total_cost']] # Общая сумма продажи лота
        dfBoughtLot['sell_nkd'] = [reqPars['sold_nkd']] # НКД на момент продажи (не общий, а для одной облигации)


        # # Время регистрации купленного лота в формате типа: 21_11_2022_14_02
        dt = FG.get_current_time_format1_d_m_y_h_m_s() # Время формата 21_11_2022_14_02
        dfBoughtLot['date_sell'] = [dt] #  дата-время регистрации продажи в БД
        print(f"dfBoughtLot = \n{dfBoughtLot}")

        # D. Вставить запись из фрейма dfBoughtLot с проданным лото в таблицу исторических сделок portfolio_history
        bmm.insert_df_to_tb_no_key_check_pandas(dfBoughtLot, TB_PORTFOLIO_HISTORY_)


        # E. Списывание соответствующего кол-ва бумаг из лота путем update qn или удаление целого лота из таблицы купленных лотов bonds_bought

        # Получить кол-во облигаций на руках в текущем найденном купленном лоте из фрейма dfBoughtLot , в поле qn
        qnAtHand = int(dfBoughtLot.iloc[0]['qn'])
        qnSold = int(reqPars['sold_qn'])
        qnDiff = qnAtHand - qnSold

        # В зависисмости от того нужно ли списать порцию от лота, или весь лот - идет альтернативные алгоритмы
        if qnDiff == 0 : # Если кол-во проданных бумаг равно количеству на руках в лоте, то закрывается целый лот
            pass
            print (f"Удаляем целый лот")
            sql = f"DELETE FROM bonds_bought WHERE isin = '{isin}' AND dtime_bought = '{dtime_bought}' "
            bmm.execute_sql(sql)

        else: # Если продано меньше, чем содержит в себе лот, то списывается часть бумаг из этого лота, путем  update кол-ва в записи в табл bonds_bought
            print (f"Спсиываем часть бумаг из лота путем update qn и не удаляем его")
            sql = f"UPDATE bonds_bought SET qn = {qnDiff} WHERE isin = '{isin}' AND dtime_bought = '{dtime_bought}' "
            bmm.execute_sql(sql)




        # # Получить фрейм из словаря reqPars с зпданными величинами именных парметров. Фрейм дальше вносится в БД и поэтому названия колонок должны соотвтетсвовать названиям полей
        # dfSoldData = self.read_df_from_dictionary(reqPars)


        # # A. Проставление даты-времени в поле ddate_time и pdate
        # # Простановка точного времени в фрейме
        # dfSoldData['dtime_bought'] = dt




    def get_all_bought_lots_by_isin(self, isin):
        """
        Получить все лоты заданной по isin бумаги из таблицы bonds_bought из собственного портфолио
        Возвращает фрейм с лотами и их данными покупки
        Category: Облигации
        """
        
        sql = f"SELECT * FROM bonds_bought WHERE isin = '{isin}' "
        dfBoghtLots = self.read_sql_to_df_pandas(sql)

        return dfBoghtLots






    @staticmethod
    def clear_format_bonds_fields_to_float(df):
        """
        BondsMainManager
        Очистить и привести к float необходимые поля в фрейме, бкрущему свою базу из таблиц bonds_current и подобные таблицы с облигациями, где некоторые поля имеют стринг с %
        и имеющим идентичные колонки с таблицей ('annual_yield', 'last_annual_yield', 'curr_price') 
        Category: Конвертирование
        """

        # Очистка колонок с действительными числами в стринговом выражении от знака '%'
        df = BondsMainManager.convert_str_empty_with_persent_and_empty_str_to_float(df, 'annual_yield')
        df = BondsMainManager.convert_str_empty_with_persent_and_empty_str_to_float(df, 'last_annual_yield')  # !!
        df  = BondsMainManager.convert_str_empty_with_persent_and_empty_str_to_float(df, 'curr_price')

        return df


    @staticmethod
    def clear_format_tb_fields_list_to_float(df, fieldsNameList):
        """ 
        ПОКА НЕ ПРОВЕРЕНО
        Очистить и привести к float необходимые поля в фрейме, заданные именами в списке
        Category: Конвертирование
        """ 
        for fieldName in fieldsNameList:
            df = BondsMainManager.convert_str_empty_with_persent_and_empty_str_to_float(df, fieldName)

        return df





    @staticmethod
    def get_total_qn_bought_bonds_by_isin(isin):
        """
        ЗАГОТОВКА. BondsMainManager
        Получить общеее кол-во купленных облигаций данного ISIN 
        TODO: Слишком долго. Сделать чисто через SQL 
        Category: Облигации
        """


        db_proc = SqlitePandasProcessor(DB_BONDS_)
        SQL = f"SELECT isin, qn FROM bonds_bought WHERE isin='{isin}'"
        dfBondsBought= db_proc.read_sql_to_df_pandas(SQL)

        dfGroupAggBought = dfBondsBought.groupby('isin').agg('sum')

        # print(f"grouAggBought = {dfGroupAggBought}")

        return dfGroupAggBought.iloc[0]['qn']




    # @staticmethod
    def filter_bonds_df_by_given_month_payment_bmm(self, dfBonds, month):
        """
        Отфильтровать фрейм с облигациями, содержащим их ISIN, по заданному месяцу, по которому ищутся совпадения с месячными векторами выплат по облигациям
        Оставить те облигации, у которых вектор месячных выплат содержит искомый задаваемы месяц
        Category: Облигации
        """
        newColName = 'ifMonthIn'
        # Добавить колонку-маску, которая анализирует попадание искомого месяца в множество месяцев выплат по облигации
        self.add_if_month_in_paym_vector_of_bond_calc_column(dfBonds, month, newColName)
        # Удалить строки значение поля в колонке newColInx или newColName = False. Оставить только те облигации, искомый месяц у которых совпадает с вектором помесячных выплат
        dfBonds = self.clear_df_by_mask_column_name_pandas(dfBonds, newColName)
        return dfBonds


    @staticmethod
    def get_top_navigator_by_monthly_payment_bmm(addLis = '', **viewSets):
        """
        Дополнительный верхний горизонтальный навигатор для распределения ссылок фильтрации облигаций по месяцам в рамках расклада по месячным выплатам
        С возможностью добавки любого кода в виде дополнительных тэгов  <li>...</li> через параметр addLi. с Markup выходного кода
        viewName - название обрабатывающего view, на который будут указывать ссылки
        В конечном итоге код должен передаватьбся на jinga темплейт через **kwargs с ключем kwargs['subTopNav']
        pm - активный месяц, выбранный при нажатии на ссылку после перезагрузки страницы. Передается через request
        chosenStyle - стиль выделения активной загруженной страницы в навигаторе
        monthNavFor - тип бумаг для которых производится фильтрация (комплексные, офз, муниципалы и корпоративы)
        reqDic - словарь ,составленный на основе входящего request ()
        addLis - Добаваочные HTML тэги <li>...</li> с содержимым, при необходимости ручной добавки каких-то подразделов в навигаторе
        Пр:
            subTopNav = Markup(subTopNav)
            view_kwargs['subTopNav'] = subTopNav
            return render_template('table_df_type1.html', **view_kwargs) 
        Category: Облигации
        """

        if 'payMonth' in viewSets['reqDic']:
            pm = viewSets['reqDic']['payMonth']
        else:
            pm = ''

        chosenStyle = viewSets['projStyles']['activeMonth']    # Стиль выделенной активной страницы в активном месяце в навигаторе месяцев 
        linkViewName = viewSets['viewForManipLinks'] # Ссылка на вьбер обработки 
        monthNavFor = viewSets['monthNavFor'] # Switch - маркер для обработки фильтрации по месяцу по необходимой таблице 

        if 'ixPkgId' in viewSets['reqDic']:
            ixPkgId = viewSets['reqDic']['ixPkgId'] # ID индексного пакета из параметров словаря request
        else:
            ixPkgId = ''
            
        if 'limDate' in viewSets['reqDic']:
            limDate = viewSets['reqDic']['limDate'] # ID индексного пакета из параметров словаря request
        else:
            limDate = ''


        subTopNav = f""" 
            <nav>
                <ol class="breadcrumb">
                    <li class="breadcrumb-item">Поиск: Выплаты включают месяц </li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='1' else ''}" href="/{linkViewName}?payMonth=1&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">1</a></li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='2' else ''}" href="/{linkViewName}?payMonth=2&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">2</a></li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='3' else ''}" href="/{linkViewName}?payMonth=3&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">3</a></li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='4' else ''}" href="/{linkViewName}?payMonth=4&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">4</a></li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='5' else ''}" href="/{linkViewName}?payMonth=5&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">5</a></li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='6' else ''}" href="/{linkViewName}?payMonth=6&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">6</a></li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='7' else ''}" href="/{linkViewName}?payMonth=7&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">7</a></li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='8' else ''}" href="/{linkViewName}?payMonth=8&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">8</a></li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='9' else ''}" href="/{linkViewName}?payMonth=9&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">9</a></li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='10' else ''}" href="/{linkViewName}?payMonth=10&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">10</a></li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='11' else ''}" href="/{linkViewName}?payMonth=11&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">11</a></li>
                    <li class="breadcrumb-item"><a style="{chosenStyle if pm=='12' else ''}" href="/{linkViewName}?payMonth=12&monthNavFor={monthNavFor}&ixPkgId={ixPkgId}">12</a></li>

                    <li class="breadcrumb-item">
                    <img id="clnd_equal_icon" src = "assets/equal2.png" width = "20px" heigh = "20px" style = "margin-left: 20px; cursor: pointer;"  title = "Равно" onclick="setClndrSign('equal')">
                    <img id="clnd_more_icon" src = "assets/is-greater-than.png" width = "20px" heigh = "20px" style = "margin-left: 20px; cursor: pointer;"  title = "Больше" onclick="setClndrSign('more')">
                    <img id="clnd_less_icon" src = "assets/is-less-than.png" width = "20px" heigh = "20px" style = "margin-left: 20px; cursor: pointer;"  title = "Меньше" onclick="setClndrSign('less')">
                    <img id="clnd_more_equal_icon" src = "assets/more-than-or-equal.png" width = "20px" heigh = "20px" style = "margin-left: 20px; cursor: pointer;"  title = "Больше или равно" onclick="setClndrSign('more_equal')">
                    <img id="clnd_less_equal_icon" src = "assets/is-less-than-or-equal-to.png" width = "20px" heigh = "20px" style = "margin-left: 20px; cursor: pointer;"  title = "Меньше или равно" onclick="setClndrSign('less_equal')">
                    
                    <img id="" src = "assets/calendar.png" width = "20px" heigh = "20px" style = "margin-left: 20px; cursor: pointer;"  title = "Календарная дата: dd-mm-yyyy" >
                    <input id="limCalendDate" value="{limDate}" title = "ex: >10-06-2023 By default if no sign operand equal '>'" >
                    <img id="clnd_delete_icon" src = "assets/multiply.png" width = "20px" heigh = "20px" style = "margin-left: 20px; cursor: pointer;"  title = "Очистить" onclick="setClndrSign('clear_sign')">
                     <img src = "assets/implies2.png" width = "25px" heigh = "25px" style = "margin-left: 10px; cursor: pointer; " title = "Отфильтровать бонды по заданной дате регистрации в БД" onclick="filterBondsByDate()">
                    </li>
                    
                    


                    """

        if addLis: # Вставить добавку
            subTopNav += addLis 

        subTopNav += """
                                </ol>
                            </nav>
                    """

        subTopNav = Markup(subTopNav)


        return subTopNav




    # END СПЕЦ ФУНКЦИИ ПО ОБЛИГАЦИЯМ




    # СПЕЦИАЛИЗИРОВАННЫЙ SINTAXER



    def get_complex_bonds_sql_total_BMM (self):
        """
        SQL запрос для обьединенных запросов для таблиц по всем категориям облигаций
        Category: Облигации
        """
        sql = "SELECT * FROM bonds_current UNION SELECT * FROM ofz_current UNION SELECT * FROM municip_current"
        return sql


    def get_curr_coupon_by_isin_from_complex_bonds_sql_BMM(self, isin, field):
        """
        Запрос получения значения заданного поля из сводной таблицы всех типов облигаций для заданной ISIN облигации
        Category: Облигации
        """
        sql = f"SELECT {field} FROM bonds_archive  WHERE isin = '{isin}' UNION SELECT {field} FROM ofz_archive WHERE  isin = '{isin}' UNION SELECT {field} FROM municip_archive WHERE isin = '{isin}'"
        return sql


    def get_isins_from_tb_sql_BMM(self, tb):
        """
        Получить isins внесенных в заданную тбалицу облигаций
        Category: Облигации
        """
        sql = f'SELECT isin FROM {tb}'
        return sql



    def update_curr_coupon_in_bonds_bought_from_complex_bonds_currents(self):
        """
        Обновить значения текущих купонов купленных облигаций из текущих опреативных таблиц с облигациями
        Category: Облигации
        """

        db_proc = BondsMainManager(DB_BONDS_)

        # Получить isins купленных бумаг из таблицы bonds_bought
        tb = 'bonds_bought'
        isinsBondsBought = db_proc.get_isins_from_tb_proc_BMM(tb)
        print (f"isinsBondsBought = {isinsBondsBought}")

        # Внести текущие значения купонов по этим бумагам , взятых из таблиц текущих оперативных облигаций
        for isin in isinsBondsBought:
            resCoupon = db_proc.get_field_val_by_isin_from_complex_bonds_proc_BMM(isin, 'coupon')
            db_proc.update_coupon_in_bonds_bought_by_isin_proc_BMM(isin, resCoupon[0])


    # END СПЕЦИАЛИЗИРОВАННЫЙ SINTAXER


    # СПЕЦИАЛИЗИРОВАННЫЕ ПРОЦЕССОРЫ 


    @SqlitePandasProcessor.transform_cursor_to_list # Декоратор, который трансформирует метод так, что бы возвращался не курсор, а конечный список результатов, готовый к использованию
    def get_field_val_by_isin_from_complex_bonds_proc_BMM (self, isin, field):
        """
        Получить значение любого поля у заданной через ISIN облигации
        Category: Облигации
        """
        sql = self.get_curr_coupon_by_isin_from_complex_bonds_sql_BMM(isin, field)
        print(sql)
        cursor = self.connection.cursor()
        cur = cursor.execute(sql)
        return cur, sql   


    @SqlitePandasProcessor.transform_cursor_to_list 
    def get_isins_from_tb_proc_BMM(self, tb):
        """
        Получить isins внесенных в заданную тбалицу облигаций
        Category: Облигации
        """
        sql = self.get_isins_from_tb_sql_BMM(tb)
        # print(sql)
        cursor = self.connection.cursor()
        cur = cursor.execute(sql)
        return cur, sql   



    def update_coupon_in_bonds_bought_by_isin_proc_BMM(self, isin, coupon):
        """
        Обновить заданное текущее значение купона coupon в таблице bonds_bought по isin
        Category: Облигации
        """
        sql = f"UPDATE bonds_bought SET curr_coupon = {coupon}  WHERE isin = '{isin}'"
        # print(sql)
        self.execute_sql_with_cursor (sql)
        return sql


    
    def update_bonds_bought_field_proc_BMM(self, fieldValDic, compexKeyDic):
        """
        Произвести update поля field в таблице bonds_bought значением val (задаваемых значением словаря fieldValDic) с комплексным ключем compexKeyDic - словарем {partsKey : partsKeyVal}, 
        который содержит значения коплексного ключа из полей isin и  dtime_bought
        Category: Облигации
        """
        field = list(fieldValDic.keys())[0] # Ключ словаря - название поля, которое нужно обновить
        fieldval = list(fieldValDic.values())[0] # Значение поля в словаре по ключу с названием поля для Update

        isinKeyVal = compexKeyDic['isin']
        dateTimeKeyVal = compexKeyDic['dtime_bought']

        sql = f"UPDATE bonds_bought SET {field} = {fieldval} WHERE  isin = '{isinKeyVal}' and dtime_bought = '{dateTimeKeyVal}'"
        self.execute_sql(sql)
        return sql


    @staticmethod
    def get_complex_bought_bonds_with_full_attrs_BMM():
        """
        BondsMainManager
        Получить комплексный источник с приобретенными облигациями из табл bonds_bought с полными данными по атрибутам из структуры таблиц типа bonds_current ,
        хотя для разных категорий облигаций - разные таблицы, но с идентичной структурой данных
        Category: Облигации
        """


        # 1. SQL LEFT JOIN bonds_bought и bonds_archive и формирование фрейма с прреобретенными облигациями в расширенном атрибутами из табл bonds_archive варианте
        # ПРИМ: В этом варианте SQL для LEFT JOIN не должно быть в таблицах названий полей одинаковых !! Если одинаковые поля, то надо использовать другой вариант LEFT JOIN
        db_proc = SqlitePandasProcessor(DB_BONDS_)
        SQLCorp = 'SELECT * FROM bonds_bought INNER JOIN bonds_archive USING (isin)'
        dfBondsBoughtCorp = db_proc.read_sql_to_df_pandas(SQLCorp)

        # SQL LEFT JOIN bonds_bought и ofz_current
        SQLOFZ = 'SELECT * FROM bonds_bought INNER JOIN ofz_current USING (isin)'
        dfBondsBoughtOFZ = db_proc.read_sql_to_df_pandas(SQLOFZ)

        # SQL LEFT JOIN bonds_bought и municip_current
        SQLMunicip = 'SELECT * FROM bonds_bought INNER JOIN municip_current USING (isin)'
        dfBondsBoughtMunicip = db_proc.read_sql_to_df_pandas(SQLMunicip)

        # Обьединение 3х фреймлв в один, учитывая, что структуры твблиц идентичны
        frames = [dfBondsBoughtCorp, dfBondsBoughtOFZ, dfBondsBoughtMunicip]
        dfBondsBoughtComplex = pd.concat(frames)


        # Очистка колонок с действительными числами в стринговом выражении от знака '%'
        dfBondsBoughtComplex = BondsMainManager.clear_format_bonds_fields_to_float(dfBondsBoughtComplex) # Очистка колонки с конечным названием ГКД


        return dfBondsBoughtComplex





    @staticmethod
    def get_month_payment_vector_by_frequency_and_one_given_pay_month_static(couponFrequency, oneOfPayMonth):
        """
        BondsMainManager
        Получить вектор выплат облигации по ее частоте выплат и одному из месяцев выплат. Статичнный метод. 
        Применение: Необходимо в расчетах облигаций которые подпадают по месяцам купонных выплат под искомый месяц, на который мы хотим , что бы пришлись выплаты от покупаемой бумаги
        """
        # Словарь обобщенных нормализованных векторов помесячных выплат в зависимости от частоты выплат в году, где частота выплат в году является ключем словаря
        #TODO: Можно сделать, что бы нормализированные векторы создавались сами только от на базе частоты выплат
        # TODO: Расширить анализ для всех возможных и адекватных частот по облигациям, которые могут встретиться
        dicOfPossiblePaymentsVectors = {

                2 : np.array([0, 6]),
                4 : np.array([0,3,6,9]),
                6 : np.array([0,2,4,6,8,10]),
                12 : np.array([0,1,2,3,4,5,6,7,8,9,10,11])

        }

        # Нормализованный обобщенный вектор помесячных выплат в году 
        normMonthPayVector = dicOfPossiblePaymentsVectors[couponFrequency]

        # print (f"payMonthVaector = {normMonthPayVector}")

        # Индивидуальный  вектор месяцев выплат (ИВМВ) для данной облигации с заданной частотой выплат и любым известным месяцем выплат oneOfPayMonth, получаемым из bonds_current - месяц выплат купоном 
        bondMonthPayVector = normMonthPayVector  +  oneOfPayMonth

        # print (f"bondMonthPayVector = {bondMonthPayVector}")  # Res: bondMonthPayVector = [ 3  6  9 12]

        # Приведение индивидуального вектора к нормальному и уже индивидуальному виду (получаем конкретный набор месяцев по конкретной облигации, когда будут выплачиваться купоны)
        bondNormMonthPayVector = bondMonthPayVector + np.where(bondMonthPayVector > 12, -12, 0 )

        return bondNormMonthPayVector
    
    




    # END СПЕЦИАЛИЗИРОВАННЫЕ ПРОЦЕССОРЫ 



    # ПО КОМПАНИЯМ


    @staticmethod
    def get_comp_raitings_by_inn(inn):
        """
        BondsMainManager
        ЗАГОТОВКА : Получить рейтинги компании из таблиц с рейтингами по ее ИНН
        Category: Облигации
        """
        bmm = BondsMainManager(DB_BONDS_)

        sqlFabvdo = f'SELECT * FROM fapvdo_comp_raitings WHERE inn = {inn}'
        dfCompFabvdo = bmm.read_sql_to_df_pandas(sqlFabvdo)


        sqlRaex = f'SELECT * FROM raex_comp_ratings WHERE inn = {inn}'
        dfCompRaex = bmm.read_sql_to_df_pandas(sqlRaex)

        print(f"@@#*&T*$  type(dfCompRaex) = {type(dfCompRaex)}")
        print(f"@@#*&T*$  dfCompRaex = \n{dfCompRaex}")

        if dfCompFabvdo.empty:
            fabvdoRait = 'Отсутствует'
        else:
            fabvdoRait = dfCompFabvdo.iloc [0]['raiting_fapvdo']


        if dfCompRaex.empty:
            raexRait = 'Отсутствует'
        else:
            raexRait = dfCompRaex.iloc [0]['raiting_raex']

        
        

        res = [fabvdoRait, raexRait]

        return res
        



   # END ПО КОМПАНИЯМ



        # ФУНКЦИИ ДЛЯ ДИФФЕРЕНЦИАТОРА

    def get_diff_dic_by_marker_name (self, sysMarker):
        """
        HTMLSiteManager
        Получить запись из таблицы differenciator в виде словаря значений полей
        Category: Цветовые дифференциаторы
        """

        sql = f'SELECT * FROM {TB_DIFFERENCIATOR_} WHERE sys_marker = "{sysMarker}"'
        diffDic = self.get_dict_from_mono_sql_select_proc(TB_DIFFERENCIATOR_, sql)

        return diffDic



    # END ФУНКЦИИ ДЛЯ ДИФФЕРЕНЦИАТОРА





    def main():
        pass




if __name__ == '__main__':
    pass



    # # ПРОРАБОТКА: Конвертировать данные в колонке таблицы со значением по датам в каком-то существующем формате в другой заданный формат данных./ convert_data_format_in_data_column_with_given_data
    
    # bmm = BondsMainManager(DB_BONDS_)
    
    
    # dsSrc = f"SELECT * FROM {TB_BONDS_ARCIVE_} WHERE f2 IS NOT NULL"
    
    # # tb = TB_MUNICIP_CURRENT_
    # # tb = TB_OFZ_CURRENT_
    # # tb = TB_OFZ_ARCIVE_
    # # tb = TB_BONDS_CURRENT_
    # tbTrg = TB_BONDS_ARCIVE_
    
    # keyField = 'isin'
    
    # dataCol = 'f2'
    
    # listFormats = [FORMAT_2_1_, FORMAT_2_0_]
    
    # bmm.convert_data_format_in_data_column_with_given_data (dsSrc, tbTrg, keyField, dataCol, listFormats)
    
 
    
    




    # # ПРОРАБОТКА: метода простановки текущего времени в поле таблицы по заданному формату / set_curr_datetime_with_format_to_tb_field_by_keys()
    
    # bmm = BondsMainManager(DB_BONDS_)
    
    # dsKeys = [
    #             'RU000A101T56', 'RU000A105UQ7', 'RU000A106AT1', 'RU000A106AU9', 'RU000A106B51', 'RU000A106BQ5', 'RU000A106C50', 'RU000A106C92', 'RU000A106CA7', 'RU000A106CB5', 
    #             'RU000A106CJ8', 'RU000A106CM2', 'RU000A106CN0', 'RU000A106CR1', 'RU000A106CU5', 'RU000A106D18'
    #         ]
    
    # tbTrg = TB_BONDS_CURRENT_
    
    # # dsKeys = '*'
    
    # tbTrgKey = 'isin'
    
    # dateFormat = FORMAT_2_

    # dfKeys = bmm.set_curr_datetime_with_format_to_tb_field_by_keys_or_total(tbTrg, dsKeys,  tbTrgKey, dateFormat)
    
    # # bmm.print_df_gen_info_pandas_IF_DEBUG(dfKeys, True, colsIndxed = False)

    
    
    
    
    
    
    



    # ПРОРАБОТКА:  Проставить UNIX-время  на основе заданного поля с  календарной датой с определенным форматом / set_unix_time_based_on_given_date_field_in_tb()
    
    bmm = BondsMainManager(DB_BONDS_)

    # tb = TB_MUNICIP_CURRENT_
    # tb = TB_OFZ_CURRENT_
    # tb = TB_OFZ_ARCIVE_
    # tb = TB_BONDS_CURRENT_
    
    dsSrc = f"SELECT * FROM {TB_BONDS_ARCIVE_} WHERE f2 IS NOT NULL"
    
    
    
    tbTrg = TB_BONDS_ARCIVE_
    
    # # Разовая Очистка поля f11 в таблице / Разовое применение / НЕ УДАЛЯТЬ!!!
    # # pars
    # col = 'f11'
    # bmm.clear_field_in_tb (tb, col)
    
    # pars
    keyField = 'isin'
    dateField = 'f2'
    unixField = 'f11'
    kwargs = {
        'format' : FORMAT_2_0_, 
        'rinteger' : True
        }

    # Простановка Unix-времени на базе заданного поля с датой
    dfRes = bmm.set_unix_time_based_on_given_date_field_in_tb (dsSrc, tbTrg, keyField, dateField, unixField, **kwargs)









    # # ПРОРАБОТКА: Проставить текущее время в поля таблицы set_curr_datetime_to_table_fields()
    # bmm = BondsMainManager(DB_BONDS_)
    
    # # Pars: 
    # # Получение фрейма ключей в виде типа DSourceCube на основе входного источника ключей в любом виде (список, таблица, sql-запрос, фрейм)
    # dsKeys = [
    #             'RU000A101T56', 'RU000A105UQ7', 'RU000A106AT1', 'RU000A106AU9', 'RU000A106B51', 'RU000A106BQ5', 'RU000A106C50', 'RU000A106C92', 'RU000A106CA7', 'RU000A106CB5', 
    #             'RU000A106CJ8', 'RU000A106CM2', 'RU000A106CN0', 'RU000A106CR1', 'RU000A106CU5', 'RU000A106D18'
    #           ]
    
    # fieldsDateFormats = {
    #     'f2' : FG.get_current_time_format2(),
    #     'f10' : FG.get_unix_curr_time()
    # }

    # tbKey = 'isin' # ключевая колонка в таблице для идентификации вставок

    # dfKeys = bmm.set_curr_datetime_to_table_fields(dsKeys,  tbKey, fieldsDateFormats) 
    
    


    # # ПРОРАБОТКА: add_row_backgr_color(df, newColName, **kwargs)

    # bmm = BondsMainManager(DB_BONDS_)

    # df = pd.DataFrame()

    # newColName = 'newColName'

    # res = bmm.add_row_backgr_color_sys_diff_BMM(df, newColName)

    # print(f"res = {res}")




    # ПРОРАБОТКА: get_bond_raiting_by_isin

    # raexMngr = RaexManager()






    # # ПРОРАБОТКА:  get_inn_by_isin_BMM():


    # bmm = BondsMainManager(DB_BONDS_)

    # isin = 'RU000A0JXQQ9'

    # inn = bmm.get_inn_by_isin_BMM(isin)

    # # inn = (bmm.get_result_from_sql_exec_proc(isin))[0]
    #         # filtsStr = (bmm.get_result_from_sql_exec_proc(sqlFilt))[0]

    # print(f"inn = {inn}")










    # # ПРОРАБОТКА: 2й версии if_given_month_belongs_to_month_payment_vector_of_bond_by_isin_v2 (self, givenMonth, isin)
    # # from bonds.bonds_main_manager import BondsMainManager

    # bmm = BondsMainManager(DB_BONDS_)

    # givenMonth = 5
    # isin = 'RU000A105DS9'

    # res = bmm.if_given_month_belongs_to_month_payment_vector_of_bond_by_isin_v2 (givenMonth, isin)
    # print (res)

    # # bmm.select_from_table_with_where_condition










        # # ПРОРАБОТКА: СУММЫ ПО ГРУППЕ 
        # from bonds.bonds_main_manager import BondsMainManager

        # isin = 'RU000A1056T2'
        # qn = BondsMainManager.get_total_qn_bought_bonds_by_isin(isin)

        # print(f"qn = {qn}")








        # # ПРОРАБОТКА: if_given_month_belongs_to_month_payment_vector_of_bond_by_isin(self, givenMonth, isin)
        # from bonds.bonds_main_manager import BondsMainManager
        # bmm = BondsMainManager(DB_BONDS_)

        # givenMonth = 6

        # isin = 'SU29008RMFS8'

        # ifMonthIn = bmm.if_given_month_belongs_to_month_payment_vector_of_bond_by_isin(givenMonth, isin)

        # print(f"ifMonthIn = {ifMonthIn}")





        # from bonds.bonds_main_manager import BondsMainManager
        # # ПРОРАБОТКА: получение имени бумаги по ее ISIN

        # print('TEST')

        # bmm = BondsMainManager(DB_BONDS_)

        # name = bmm.get_bond_name_by_isin_BMM('SU26241RMFS8')

        # print (name)

















