

# from markupsafe import Markup
# import bonds.funcs_general as FG
# import numpy as np
# import pandas as pd
# from .sqlite_pandas_processor import SqlitePandasProcessor
# from bonds.settings import *
# from bonds.switch import Switch
# from bonds.exceptions import *
# from project_bonds_html.projr.classes.dsource_cube import DSourceCube 
# from bonds.settings_date_formats import *  
# from classes.local_manager_BH import LocalManager
# from project_bonds_html.projr.classes.html_manager import HTMLSiteManager
# from settings import TB_PORTFOLIO_HISTORY_
# from settings import TB_BONDS_BOUGHT_

from noocube.sqlite_connection import SqliteConnection
from noocube.pandas_manager import PandasManager
import pandas as pd
import noocube.funcs_general  as FG

# # Динамическая настройка на общий settings_bdp_main.py
# import sys
# sys.path.append('/home/ak/projects/P19_Bonds_Django/bonds_django_proj')
# import noocube.settings_bdp_main as ms # общие установки для всех модулей

from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup

import numpy as np

from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup

from pytictoc import TicToc # https://pypi.org/project/pytictoc/

class BondsMainManagerSpeedup():
    """
    Методы для быстрого выполнения. 
    dataBaseConnection - открытый connection к БД
    """

    def __init__(self, dataBaseConnection): 
        
        self.db_uri = f"sqlite:///{dataBaseConnection.dataBase}" # Pandas по умолчанию работает через SQLAlchemy и может создавать сама присоединение к БД по формату адреса URI (см. в документации SQLAlchemy)
        self.db_connection = dataBaseConnection
        self.spps = SqlitePandasProcessorSpeedup(self.db_connection) # Обьект класса SqlitePandasProcessorSpeedup
        self.sps = SqliteProcessorSpeedup(self.db_connection) # Обьект класса SqliteProcessorSpeedup
        
        
    def read_sql_to_df_pandas_BMMS(self, sql):
        """
        OBSOLETED: Перенесен в класс SqlitePandasProcessorSpeedup по смыслу класса с названием read_sql_to_df_pandas_SPPS
        BondsMainManagerSpeedup
        Считывает результат sql запроса в dataFrame
        
        """    
        df = pd.read_sql(sql, self.db_uri)
        return df
    
    
    def read_table_by_sql_to_df_pandas_BMMS(self, tb, getFields = ['*']):
        """ OBSOLETED: Перенесен в класс SqlitePandasProcessorSpeedup по смыслу класса с названием read_table_by_sql_to_df_pandas_SPPS
        Считывает всю таблицу в фрейм с выбором необходимых колонок в выборке
        getFields - список выводимых колонок. По умолчанию выводятся все колонки
        """
        # Считывание таблицы bonds_archive в фрейм
        sql = f'SELECT * FROM {tb}'
        # print(sql + '  | read_table_by_sql_to_df_pandas() | noocube/sqlite_pandas_processor.py')
        dfTb = self.read_sql_to_df_pandas_BMMS(sql)  
        if '*' in getFields: # если запрашиваются все колонки
            return dfTb
        else : # если выборка колонко
            dfTb = PandasManager.get_sub_df_with_given_cols_static(dfTb, getFields)  
            return  dfTb 
    


    def get_index_packages_df_BMMS(self, getFields = ['*']):
        """
        Получить фрейм с индексными пакетами из табл index_packages
        """

        if getFields[0] == '*':
            sql = 'SELECT * FROM index_packages'
        else:
            fields = ','.join(getFields)
            sql = f'SELECT {fields} FROM index_packages'
            # print(f"sql = {sql}")

        dfPackages = self.read_sql_to_df_pandas_BMMS(sql)
        
        # print (f'PR_895 --> dfPackages = \n{dfPackages}')

        return dfPackages
    
    
    
    
    def get_inx_package_id_by_nickname_BMMS(self, nick):
        """
        OBSOLETED: Переведен в класс ProjectBondsFunctions проектного уровня 
        ~ /home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/project_bonds_funcs.py
        Получить id индексного пакета по его ник-нейму
        Category: Облигации
        """
        
        sql = f'SELECT id FROM index_packages WHERE nick = "{nick}"'
        dfRes = self.read_sql_to_df_pandas_BMMS(sql)
        res = PandasManager.get_cell_val_by_row_inx_and_col_name(dfRes, 0, 'id')

        return res
    
    
    
    def get_nickname_by_inx_package_id_BMMS(self, id):
        """
        Получить ник-нейм индексного пакета по его id
        Category: Облигации
        """
        
        sql = f'SELECT nick FROM index_packages WHERE id = "{id}"'
        dfRes = self.read_sql_to_df_pandas_BMMS(sql)
        res = PandasManager.get_cell_val_by_row_inx_and_col_name(dfRes, 0, 'nick')

        return res
    
    
    
    def get_isins_from_inx_pkg_its_id_BMMS (self, inxPkgId):
        """ 
        BondsMainManagerSpeedup
        Считать в фрейм isins из таблицы индексных пакетов по ID индексного пакета
        Category: Облигации
        """
        
        sql = f'SELECT * FROM inx_package_{inxPkgId}'
        # print(f"PR_593 --> sql = {sql}")
        dfRes = self.read_sql_to_df_pandas_BMMS(sql)
        # print(f"PR_594 --> dfRes = {dfRes}")
        
        
        return dfRes
    
    
    
    
    def get_isins_from_inx_pkg_bonds_by_pckg_id_BMMS (self, inxPkgId):
        """ 
        BondsMainManagerSpeedup
        Считать в фрейм isins из таблицы индексных пакетов по ID индексного пакета
        Category: Облигации
        """
        
        sql = f'SELECT * FROM {ms.TB_INX_PACKAGES_BONDS} WHERE inx_pckg_id={inxPkgId}'
        dfRes = self.read_sql_to_df_pandas_BMMS(sql)
        
        return dfRes
    
    
    
    
    def get_isins_list_from_inx_pkg_with_given_id_bmms (self, inxPkgId):
        """ 
        BondsMainManagerSpeedup
        Получить список isins из таблицы индексных пакетов по ID индексного пакета
        Category: Облигации
        """
        
        dfRes = self.get_isins_from_inx_pkg_its_id_BMMS (inxPkgId)
        
        listIsins = dfRes['isin_ixp'].tolist()
        
        return listIsins
    
    
    
    def get_isins_list_from_inx_pkg_bonds_tb_with_given_pckg_id_bmms (self, inxPkgId):
        """ 
        BondsMainManagerSpeedup
        Получить список isins из таблицы индексных пакетов по ID индексного пакета
        Category: Облигации
        """
        
        sql = f'SELECT * FROM {ms.TB_INX_PACKAGES_BONDS} WHERE inx_pckg_id={inxPkgId}'
        print(f"PR_581 --> sql={sql}")
        dfRes = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # print(f"PR_582 --> dfRes = \n{dfRes}")
        
        # dfRes = self.get_isins_from_inx_pkg_its_id_BMMS (inxPkgId)
        
        listIsins = dfRes['bond_isin'].tolist()
        
        return listIsins




    def get_bought_bonds_df_with_added_diff_columns(self, bgColors = ['White', 'LemonChiffon', 'PowderBlue']):
            """
            BondsMainManagerSpeedup
            Получить общий фрейм приобретенных облигаций, расширенных данными по аргументам табблицы bonds_archive и добавить колонки дифференциации по типу облигаций и 
            цветовой подсветки
            Колонки annual_yield, last_annual_yield и curr_price прочищены от % и трансформированы в тип float
            Category: Облигации
            """

            # Корпоративные облигации из табл bonds_current
            sqlCorp = 'SELECT * FROM bonds_bought INNER JOIN bonds_archive USING (isin)'
            dfCorpBonds = self.read_sql_to_df_pandas_BMMS(sqlCorp)
            dfCorpBonds['type'] = 'КОРП'
            dfCorpBonds['bg_color'] = bgColors[0]
            # Государственные облигации ОФЗ из табл ofz_current
            sqlOFZ = 'SELECT * FROM bonds_bought INNER JOIN ofz_archive USING (isin)'
            dfOfzBonds = self.read_sql_to_df_pandas_BMMS(sqlOFZ)
            dfOfzBonds['type'] = 'ОФЗ'
            dfOfzBonds['bg_color'] = bgColors[1]
            # Субфедеральные или муниципальные облигации из табл municip_current
            sqlMunicip = 'SELECT * FROM bonds_bought INNER JOIN municip_archive USING (isin)'
            dfMunicipBonds = self.read_sql_to_df_pandas_BMMS(sqlMunicip)
            dfMunicipBonds['type'] = 'МУНИЦ'
            dfMunicipBonds['bg_color'] = bgColors[2]


            # Обьединение 3х фреймлв в один, чтобы поля одинаковых смысловых колонок соотвтетсвовали друг другу
            frames = [dfCorpBonds, dfOfzBonds, dfMunicipBonds]
            frames = [x for x in frames if len(x)>0] # Фильтруем пустые фреймы, если есть
            dfCBoughtBonds = pd.concat(frames, ignore_index=True) # autoreset index after a concatenation

            # Очистка колонок с действительными числами в стринговом выражении от знака '%'
            dfCBoughtBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfCBoughtBonds, 'annual_yield')
            dfCBoughtBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfCBoughtBonds, 'last_annual_yield')  # !!
            dfCBoughtBonds  = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfCBoughtBonds, 'curr_price')
            
            
            # Конвертировать необходимые столбцы в тип float (а именно столбцы с помесячными выплатами)
            
            colsToConvertList = [
                    'jan',
                    'feb',
                    'march',
                    'apr',
                    'may',
                    'june',
                    'july',
                    'aug',
                    'sept',
                    'oct',
                    'nov',
                    'dec',
                ]
            
            dfCBoughtBonds = PandasManager.convert_df_cols_to_float_pandas(dfCBoughtBonds, colsToConvertList)


            return dfCBoughtBonds



    def get_complex_bonds_df_with_added_diff_columns_BMMS(self, tbCorpBonds, tbOfzBonds, tbMunicipBonds, bgColors = ['White', 'LemonChiffon', 'PowderBlue']):
            """
            Сформировать обьединенный комплексный фрейм со смешанными бумагами всех типов с дифференциалльными метками по типу бумаг и цвету в отдельных добавленных колонках фрейма
            BondsMainManagerSpeedup
            bgColors - задает цвета фона рядов для трех видов облигаций для цветовой дифференциации
            Колонки annual_yield, last_annual_yield и curr_price прочищены от % и трансформированы в тип float
            Category: Облигации
            """

            # db_proc = SqlitePandasProcessor(DB_BONDS_)
            # Корпоративные облигации из табл bonds_current
            dfCorpBonds = self.read_table_by_sql_to_df_pandas_BMMS(tbCorpBonds)
            dfCorpBonds['type'] = 'КОРП'
            dfCorpBonds['bg_color'] = bgColors[0]
            # Государственные облигации ОФЗ из табл ofz_current
            dfOfzBonds = self.read_table_by_sql_to_df_pandas_BMMS(tbOfzBonds)
            dfOfzBonds['type'] = 'ОФЗ'
            dfOfzBonds['bg_color'] = bgColors[1]
            # Субфедеральные или муниципальные облигации из табл municip_current
            dfMunicipBonds = self.read_table_by_sql_to_df_pandas_BMMS(tbMunicipBonds)
            dfMunicipBonds['type'] = 'МУНИЦ'
            dfMunicipBonds['bg_color'] = bgColors[2]


            # Обьединение 3х фреймлв в один, чтобы поля одинаковых смысловых колонок соотвтетсвовали друг другу
            frames = [dfCorpBonds, dfOfzBonds, dfMunicipBonds]
            dfComplexBonds = pd.concat(frames, ignore_index=True) # autoreset index after a concatenation

            # Очистка колонок с действительными числами в стринговом выражении от знака '%'
            # dfComplexBonds= PandasManager.clear_str_float_from_persent_simb(dfComplexBonds, 'annual_yield')
            dfComplexBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'annual_yield')
            dfComplexBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'last_annual_yield')  # !!
            dfComplexBonds  = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'curr_price')


            return dfComplexBonds



    def get_complex_bonds_df_with_added_diff_columns_BMMS_v2(self, bgColors = ['White', 'LemonChiffon', 'PowderBlue']):
            """
            Сформировать обьединенный комплексный фрейм со смешанными бумагами всех типов с дифференциалльными метками по типу бумаг и цвету в отдельных добавленных колонках фрейма
            Версия 2: Таблицы задаются внутри метода и не нужно их передавать в параметрах
            BondsMainManagerSpeedup
            bgColors - задает цвета фона рядов для трех видов облигаций для цветовой дифференциации
            Колонки annual_yield, last_annual_yield и curr_price прочищены от % и трансформированы в тип float
            Category: Облигации
            """

            # db_proc = SqlitePandasProcessor(DB_BONDS_)
            # Корпоративные облигации из табл bonds_current
            dfCorpBonds = self.read_table_by_sql_to_df_pandas_BMMS('bonds_current')
            dfCorpBonds['type'] = 'КОРП'
            dfCorpBonds['bg_color'] = bgColors[0]
            # Государственные облигации ОФЗ из табл ofz_current
            dfOfzBonds = self.read_table_by_sql_to_df_pandas_BMMS('ofz_current')
            dfOfzBonds['type'] = 'ОФЗ'
            dfOfzBonds['bg_color'] = bgColors[1]
            # Субфедеральные или муниципальные облигации из табл municip_current
            dfMunicipBonds = self.read_table_by_sql_to_df_pandas_BMMS('municip_current')
            dfMunicipBonds['type'] = 'МУНИЦ'
            dfMunicipBonds['bg_color'] = bgColors[2]


            # Обьединение 3х фреймлв в один, чтобы поля одинаковых смысловых колонок соотвтетсвовали друг другу
            frames = [dfCorpBonds, dfOfzBonds, dfMunicipBonds]
            dfComplexBonds = pd.concat(frames, ignore_index=True) # autoreset index after a concatenation

            # Очистка колонок с действительными числами в стринговом выражении от знака '%'
            # dfComplexBonds= PandasManager.clear_str_float_from_persent_simb(dfComplexBonds, 'annual_yield')
            dfComplexBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'annual_yield')
            dfComplexBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'last_annual_yield')  # !!
            dfComplexBonds  = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'curr_price')


            return dfComplexBonds





    def get_complex_bonds_archive_df_with_added_diff_columns_bmms(self, bgColors = ['White', 'LemonChiffon', 'PowderBlue']):
            """
            Сформировать обьединенный комплексный фрейм со смешанными бумагами всех типов с дифференциалльными метками по типу бумаг и цвету в отдельных добавленных колонках фрейма
            на основе облигаций из таблиц '..._archive' (то есть все возможные облигации исторические)
            BondsMainManagerSpeedup
            bgColors - задает цвета фона рядов для трех видов облигаций для цветовой дифференциации
            Колонки annual_yield, last_annual_yield и curr_price прочищены от % и трансформированы в тип float
            Category: Облигации
            """
            
            # db_proc = SqlitePandasProcessor(DB_BONDS_)
            # Корпоративные облигации из табл bonds_current
            dfCorpBonds = self.read_table_by_sql_to_df_pandas_BMMS(ms.TB_BONDS_ARCHIVE)
            dfCorpBonds['type'] = 'КОРП'
            dfCorpBonds['bg_color'] = bgColors[0]
            # Государственные облигации ОФЗ из табл ofz_current
            dfOfzBonds = self.read_table_by_sql_to_df_pandas_BMMS(ms.TB_OFZ_ARCHIVE)
            dfOfzBonds['type'] = 'ОФЗ'
            dfOfzBonds['bg_color'] = bgColors[1]
            # Субфедеральные или муниципальные облигации из табл municip_current
            dfMunicipBonds = self.read_table_by_sql_to_df_pandas_BMMS(ms.TB_MUNICIP_ARCHIVE)
            dfMunicipBonds['type'] = 'МУНИЦ'
            dfMunicipBonds['bg_color'] = bgColors[2]


            # Обьединение 3х фреймлв в один, чтобы поля одинаковых смысловых колонок соотвтетсвовали друг другу
            frames = [dfCorpBonds, dfOfzBonds, dfMunicipBonds]
            dfComplexBonds = pd.concat(frames, ignore_index=True) # autoreset index after a concatenation

            # Очистка колонок с действительными числами в стринговом выражении от знака '%'
            # dfComplexBonds= PandasManager.clear_str_float_from_persent_simb(dfComplexBonds, 'annual_yield')
            dfComplexBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'annual_yield')
            dfComplexBonds = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'last_annual_yield')  # !!
            dfComplexBonds  = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dfComplexBonds, 'curr_price')


            return dfComplexBonds







    def get_full_attrs_of_inx_pkg_bonds_by_its_id_BMMS(self, inxPkgId):
        """ 
        BondsMainManagerSpeedup
        Получить фрейм со всеми атрибутами  облигаций в индексном пакете по его ID
        Category: Облигации
        """

        dfTotalCmplxBonds = self.get_complex_bonds_df_with_added_diff_columns_BMMS(ms.TB_BONDS_CURRENT, ms.TB_OFZ_CURRENT, ms.TB_MUNICIP_CURRENT)

        # Проверить, есть ли таблица с индексным пакетом 
        inxTbName = f"inx_package_{inxPkgId}"
        # Если существует, проводим необхожимые процедуры
        if self.sps.if_table_exist_in_db_sps(inxTbName):
            dfPkgIsins = self.get_isins_from_inx_pkg_its_id_BMMS (inxPkgId)
            listPkgIsins = PandasManager.get_unique_col_vals_as_list_static(dfPkgIsins,'isin_ixp') # Список исинов облигаций в индексном пакете
            # Отфильтрованные облигации по исинам индекного пакета
            dfPkgBonds = PandasManager.filter_df_by_field_vals_list(dfTotalCmplxBonds, 'isin', listPkgIsins)
            
        else:
            dfPkgBonds = -1
        
        return dfPkgBonds




    def get_inx_packages_id_bmms(self):
        """
        BondsMainManagerSpeedup
        Получить список id индексных пакетов
        Category: Облигации
        """

        sql = f"SELECT id FROM {ms.TB_INDEX_PACKAGES_}"
        
        dfInxPkgs = self.read_sql_to_df_pandas_BMMS(sql)

        ixPkgList = PandasManager.get_columns_vals_as_list_static(dfInxPkgs, 'id')

        return ixPkgList




    def get_bound_bought_consolidated_by_on_hand_qn(self):
        """ 
        BondsMainManagerSpeedup
        Получить фрейм со всеми атрибутами с купленными блигациями, консолидированными (сгруппированными) по количеству купленных бумаг на руках
        """
        
        dfBoughtBonds = self.get_bought_bonds_df_with_added_diff_columns()
        # Индексировать названия колонок в фрейме с одинаковыми названиями (в данном случае nkd имеет две колонки с одним и тем же названием)
        dfBoughtBonds = PandasManager.index_duplicated_name_columns_in_df(dfBoughtBonds)
        # Удаляем дупликаты по ISIN
        dfUniqueIsins = dfBoughtBonds.drop_duplicates(['isin'], keep = 'first')
        # Удаляем колонку qn, что бы при merge не было дополнительной колонки с таким же названием
        dfUniqueIsins = dfUniqueIsins.drop(['qn'], axis=1)
        # Группируем фрейм по isin  и находим сумму в колонке qn (всех бумаг данного исина на руках, то есть купленных)
        dfResConsolidated = dfBoughtBonds.groupby('isin').agg({'qn': 'sum'}).reset_index()
        # Консолидированные купленные облигации по количеству по граппе isin
        dfBondsBoughtConsolidatedByIsinQn = dfUniqueIsins.merge(dfResConsolidated, on='isin')
        # Переместить последнюю колонку qn на место ее предыдущего нахождения, что бы соотвтетсвовало ассоц словарю
        # TODO: Найти способ сразу вставлять конслодириованное значение в колонку qn. Искать в группировке и агрегировании
        dfBondsBoughtConsolidatedByIsinQn = PandasManager.shift_col_by_name_in_df (dfBondsBoughtConsolidatedByIsinQn, 'qn', 2)

        return dfBondsBoughtConsolidatedByIsinQn


    @staticmethod
    def get_bound_bought_matrix_payment_consolidated(dfBoughtBonds):
        """ 
        BondsMainManagerSpeedup
        Получить фрейм со всеми атрибутами с купленными блигациями, консолидированными (сгруппированными) по количеству купленных бумаг на руках
        """
        
        # dfBoughtBonds = self.get_bought_bonds_df_with_added_diff_columns()
        # # Индексировать названия колонок в фрейме с одинаковыми названиями (в данном случае nkd имеет две колонки с одним и тем же названием)
        # dfBoughtBonds = PandasManager.index_duplicated_name_columns_in_df(dfBoughtBonds)
        # Удаляем дупликаты по ISIN
        dfUniqueIsins = dfBoughtBonds.drop_duplicates(['isin'], keep = 'first')
        
        # # Удаляем колонку qn, что бы при merge не было дополнительной колонки с таким же названием
        # dfUniqueIsins = dfUniqueIsins.drop(['qn'], axis=1)
        dfUniqueIsins = dfUniqueIsins.drop([
            'qn', 
            'jan',
            'feb',
            'march',
            'apr',
            'may',
            'june',
            'july',
            'aug',
            'sept',
            'oct',
            'nov',
            'dec'
            ], axis=1)
        
        # Группируем фрейм по isin  и находим сумму в колонке qn (всех бумаг данного исина на руках, то есть купленных)
        dfResConsolidated = dfBoughtBonds.groupby('isin').agg({
            'qn': 'sum', 
            'jan': 'sum', 
            'feb': 'sum', 
            'march': 'sum', 
            'apr': 'sum', 
            'may': 'sum', 
            'june': 'sum', 
            'july': 'sum', 
            'aug': 'sum', 
            'sept': 'sum', 
            'oct': 'sum', 
            'nov': 'sum', 
            'dec': 'sum', 
            }).reset_index()
        
        # Консолидированные купленные облигации по количеству по граппе isin
        dfBondsBoughtConsolidatedByIsinQn = dfUniqueIsins.merge(dfResConsolidated, on='isin').round(2)
        
        
        # окуруглить суммы в ячейках до второго знака после запятой
        
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfBondsBoughtConsolidatedByIsinQn, False, colsIndxed = True)
        
        # Переместить последнюю колонку qn на место ее предыдущего нахождения, что бы соотвтетсвовало ассоц словарю
        # TODO: Найти способ сразу вставлять конслодириованное значение в колонку qn. Искать в группировке и агрегировании
        dfBondsBoughtConsolidatedByIsinQn = PandasManager.shift_col_by_name_in_df (dfBondsBoughtConsolidatedByIsinQn, 'qn', 2)
        
        # Переместить список колонок в указанный индекс позиции
        
        colsNamesConsicList = [
            'jan',
            'feb',
            'march',
            'apr',
            'may',
            'june',
            'july',
            'aug',
            'sept',
            'oct',
            'nov',
            'dec'
        ]
        
        dfBondsBoughtConsolidatedByIsinQn = PandasManager.shift_consicutive_cols_list_to_inx_position_in_df(dfBondsBoughtConsolidatedByIsinQn, colsNamesConsicList, 9)

        return dfBondsBoughtConsolidatedByIsinQn







    def register_bond_lot_bought_in_tb_bonds_bought_BMMS(self, requestDic):
        """
        BondsMainManagerSpeedup
        Зарегестрировать покупку лота облигаций с заданным isin, с заданным кол-вом купленных бумаг и с заданным на данный момент величины выплачиваемого купона по этой облигации
        При регистрации производится распределение помесячных выплат в соотвтетсвии с получаемым вектором помесячных выплат по той бумаге
        reqPars - словарь request-значений
        """
        # db_proc = BondsMainManager(DB_BONDS_)

        # isin облигации
        isin = requestDic['isin'] 

        # Текущий купон, проставленный вручную в формк регистрации лота покупки облигации данного ISIN
        currCoupon = float(requestDic['curr_coupon']) 
        
        # # Текущий НКД, проставленный вручную в формк регистрации лота покупки облигации данного ISIN
        # nkd = float(requestDic['nkd']) 

        # кол-во облигаций, купленных в этом лотк данной облигации с данным ISIN
        qn = int(requestDic['qn']) 

        # Суммарная выплата помесячно по вектору месячных выплат для данной облигации
        totalMonthPay = round(currCoupon * qn, 2) 

        # Время регистрации купленного лота в формате типа: 21_11_2022_14_02
        dt = FG.get_current_time_format1_d_m_y_h_m_s() # Время формата 21_11_2022_14_02

        # Получить вектор нормального распределения помесячных выплат для данной олигации с известным ISIN
        monthIsinPayVectors = self.get_bond_month_payment_objects_by_isin_BMMS(isin)

        # Поля для вставки помесячных выплат на основе полученных веторов распределения помесЯчных выплат : like ['dec', 'march', 'june', 'sept']
        monthCols = monthIsinPayVectors[1]

        # TODO: Получить нужные аргументы из общего словаря аргументов url
        # Получить фрейм из словаря reqPars с зпданными величинами именных парметров. Фрейм дальше вносится в БД и поэтому названия колонок должны соотвтетсвовать названиям полей
        dfBoughtData = PandasManager.read_df_from_dictionary_static(requestDic)

        # 2. Заполнить фрейм всеми необходимыми дополнительными данными : date_time, pdate, распределение купоннымх выплат по месяцам

        # A. Проставление даты-времени в поле ddate_time и pdate
        # Простановка точного времени в фрейме
        dfBoughtData['dtime_bought'] = dt
        # Простановка UNIX-времени
        dfBoughtData['time_reg_unix'] = FG.get_unix_curr_time()

        # print(f"dfBoughtData = \n{dfBoughtData}")

        # Добавление колонок с суммарными выплатами по месяцам в соотвтетсвии с полученынми векторами распределения выплат для данной облигации
        for monthField in monthCols:
            dfBoughtData[monthField] = totalMonthPay

        print (f"PR_563 --> dfBoughtData = \n{dfBoughtData}")

        # Зарегистрировать покупку лота облигаций с  isin в табл bonds_bought
        # <ВСТАВЛЕНИЕ ДАННЫХ В БД табл - > bonds_bought
        # Внести ланные из фрейма в таблицу bonds_bought без проверки ключей (а ключ всегдабудет уникален, так как есть метка по времени в составе комплексного ключча таблицы bonds_bought)
        self.spps.insert_df_to_tb_no_key_check_pandas_spps(dfBoughtData, 'bonds_bought', ['*'])













    def get_bond_month_payment_objects_by_isin_BMMS(self, isin, keyFieldVal = {'dtime_bought': ''}):
        """
        BondsMainManagerSpeedup
        Получить список названий месяцев выплат по облигации из ее isin
        keyFieldVal - словарь, ключ со значением (либо с пустым значением, которое можно подставить после), по которому находится запись в таблице БД, которую надо арпдейтить данными 
        по календарным выплатам. По умолчанию равен полю в табл bonds_bought 'dtime_bought' и пустому значению, которое после можно заполнить  {'dtime_bought': ''} 
        Ключ необходим для формирования фрейма , на базе которого происходит апдейт полей в таблице, которыую надо будет апдейтить
        
        <ВОЗВРАТ>
        bondMonthInxPayList - список с индексами месяцев выплат купона для облигации
        bondMonthPayList - списка названий полей месяцев из табл bonds_bought соотвтетствующих списку bondMonthPayList
        dfBondMonthPay - одномерный фрейм с колонками в виде названий полей месяцев выплат облигации и с величинами в этих полях равными купонной выплате (на данный момент - константы)
        ПР: [bondMonthInxPayList, bondMonthPayList, dfBondMonthPay] 
        """


        # B. Полный фрейм облигаций (из архивных таблиц)
        dfComplexBonds = self.get_complex_bonds_archive_df_with_added_diff_columns_bmms()

        # C.  Данные по облигации 

        # isin = reqPars['isin'] # isin
        # Все данные об одной облигации, найденной по ISIN
        dfBondByIsin = PandasManager.search_mask_rows_by_col_val_pandas(dfComplexBonds, 'isin', isin) 
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfBondByIsin, True, colsIndxed=True, marker="PR_996 --> dfBondByIsin")
        
        coupon = dfBondByIsin.iloc[0]['coupon'] # купон
        couponDate = dfBondByIsin.iloc[0]['coupon_date']
        couponDate = couponDate.replace('-','.')
        # print (f"COUPON = {coupon}")


        # 4. Простановка вектора помесячных выплат в полях Jan...Dec

        # Формула распределения купонов по месяцам в зависимости от астоты выплат и следующего месяца выплат
        # print(f"PR_A018 --> couponDate = {couponDate}")
        couponMonthInx = int(couponDate.split('.')[1]) # индекс месяца следующей за ппокупкой выплаты купонов по облигации в целочисленном варианте
        # print(f"PR_A016 --> couponMonthInx = {couponMonthInx}")

        # couponMonthInx = 5

        couponFrequency =  int(dfBondByIsin.iloc[0]['frequency']) # частота выплат купона за год
        # print(f"PR_A017 --> couponFrequency = {couponFrequency}")

        # Словарь обобщенных нормализованных векторов помесячных выплат в зависимости от частоты выплат в году, где частота выплат в году является ключем словаря
        #TODO: Можно сделать, что бы нормализированные векторы создавались сами только от на базе частоты выплат
        dicOfPossiblePaymentsVectors = {

                2 : np.array([0, 6]),
                3: np.array([0, 4, 8]),
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
        # print (f"PR_354 --> bondMonthInxPayList = {bondMonthInxPayList}")


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
        # print (f"PR_355 --> bondMonthPayList = {bondMonthPayList}")

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
        dfBondMonthPay = PandasManager.read_df_from_dictionary_static(dicBondMonthPay)

        # print(f"dfBondMonthPay = \n{dfBondMonthPay}")

        # <RETURN> <ВОЗВРАЩАЕТ>: 
        # bondMonthInxPayList - список с индексами месяцев выплат купона для облигации
        # bondMonthPayList - списка названий полей месяцев из табл bonds_bought соотвтетствующих списку bondMonthPayList
        # dfBondMonthPay - одномерный фрейм с колонками в виде названий полей месяцев выплат облигации и с величинами в этих полях равными купонной выплате (на данный момент - константы)
        res = [bondMonthInxPayList, bondMonthPayList, dfBondMonthPay] 


        return res







    def get_all_bought_lots_by_isin_BMMS(self, isin):
        """
        BondsMainManagerSpeedup
        Получить все лоты заданной по isin бумаги из таблицы bonds_bought из собственного портфолио
        Возвращает фрейм с лотами и их данными покупки
        Category: Облигации
        """
        
        sql = f"SELECT * FROM bonds_bought WHERE isin = '{isin}' "
        dfBoghtLots = self.read_sql_to_df_pandas_BMMS(sql)

        return dfBoghtLots






    def save_and_transfer_sold_bonds_lot_to_history_BMMS(self, requestDic):
        """BondsMainManagerSpeedup
        Сохранить данные о продаже лота бумаг и данные об их изначальной покупки (из табл bonds_bought) в таблице portfolio_history и удаление из таблицы bonds_bought либо 
        полного лота, либо ег очасти, равной проданному кол-ву облигаций
        reqPars - словарь request-значений
        """

        print(f"PR_356 --> save_and_transfer_sold_bonds_lot_to_history()")

        # bmm = BondsMainManager(DB_BONDS_)

        # A. isin и  дата-время покупки представляют собой комплексный ключ для однозначной идентификации записи в таблице bonds_bought !!!
        isin = requestDic['sold_isin']  # isin облигации
        # print(f"ISIN = {isin}")
        dtime_bought = requestDic['prch_date']  # дата-время покупки
        # print(f"dtime_bought = {dtime_bought}")


        # B. Получить данные покупки по записи найденой по ключу isin и  dtime_bought из таблицы bonds_bought

        sql = f'SELECT isin, dtime_bought, qn, nkd, gen_comission, total_cost FROM  bonds_bought WHERE isin = "{isin}" AND dtime_bought = "{dtime_bought}" '
        
        print(f"PR_995 --> sql = {sql}")
        
        dfBoughtLot = self.read_sql_to_df_pandas_BMMS(sql)

        print(f"PR_994 --> dfBoughtLot = \n{dfBoughtLot}")

        # C. Добавить к фрейму столбцы с данными по регистрации продажи облгаций из этого лота покупки
        dfBoughtLot['sell_qn'] = [requestDic['sold_qn']]
        dfBoughtLot['sell_commisions'] = [requestDic['sold_gen_comission']] # Общая комиссия при продаже 
        dfBoughtLot['sell_total_cost'] = [requestDic['sold_total_cost']] # Общая сумма продажи лота
        dfBoughtLot['sell_nkd'] = [requestDic['sold_nkd']] # НКД на момент продажи (не общий, а для одной облигации)


        # # Время регистрации купленного лота в формате типа: 21_11_2022_14_02
        dt = FG.get_current_time_format1_d_m_y_h_m_s() # Время формата 21_11_2022_14_02
        dfBoughtLot['date_sell'] = [dt] #  дата-время регистрации продажи в БД
        print(f"PR_357 --> dfBoughtLot = \n{dfBoughtLot}")

        # D. Вставить запись из фрейма dfBoughtLot с проданным лото в таблицу исторических сделок portfolio_history
        self.spps.insert_df_to_tb_no_key_check_pandas_spps(dfBoughtLot, ms.TB_PORTFOLIO_HISTORY_)


        # E. Списывание соответствующего кол-ва бумаг из лота путем update qn или удаление целого лота из таблицы купленных лотов bonds_bought

        # Получить кол-во облигаций на руках в текущем найденном купленном лоте из фрейма dfBoughtLot , в поле qn
        qnAtHand = int(dfBoughtLot.iloc[0]['qn'])
        qnSold = int(requestDic['sold_qn'])
        qnDiff = qnAtHand - qnSold

        # В зависисмости от того нужно ли списать порцию от лота, или весь лот - идет альтернативные алгоритмы
        if qnDiff == 0 : # Если кол-во проданных бумаг равно количеству на руках в лоте, то закрывается целый лот
            pass
            print (f"PR_358 --> Удаляем целый лот")
            sql = f"DELETE FROM bonds_bought WHERE isin = '{isin}' AND dtime_bought = '{dtime_bought}' "
            self.sps.execute_sql_SPS(sql)

        else: # Если продано меньше, чем содержит в себе лот, то списывается часть бумаг из этого лота, путем  update кол-ва в записи в табл bonds_bought
            print (f"PR_359 --> Спсиываем часть бумаг из лота путем update qn и не удаляем его")
            sql = f"UPDATE bonds_bought SET qn = {qnDiff} WHERE isin = '{isin}' AND dtime_bought = '{dtime_bought}' "
            self.sps.execute_sql_SPS(sql)





    def get_inn_by_isin_from_DB_bmms (self, isin):
        """BondsMainManagerSpeedup
        Получение ИНН компании по ISIN ее ценных бумаг на базе существующих в БД данных в таблицах bonds_archive и  bonds_current"""

        # Нахождение ИНН компании по ее ISIN в таблице соответствий (а может надо искать в bonds_archive и bonds_current) 
        # Par:
        tbInnIsin = 'bonds_archive'     
        getFields = ['inn_ref']   # [count(*)] - если надо подсчитать ряды полученные
        conds = {'ONE': ['isin', '=', isin]}
        inn = self.sps.select_from_table_with_where_condition_sps (tbInnIsin, getFields, conds)

        return inn[0]




    @staticmethod
    def get_comp_raitings_by_inn_bmms(inn):
        """
        BondsMainManagerSpeedup
        ЗАГОТОВКА : Получить рейтинги компании из таблиц с рейтингами по ее ИНН
        """
        
        bmms = BondsMainManagerSpeedup(ms.DB_CONNECTION)

        sqlFabvdo = f'SELECT * FROM fapvdo_comp_raitings WHERE inn = {inn}'
        dfCompFabvdo = bmms.spps.read_sql_to_df_pandas_SPPS(sqlFabvdo)


        sqlRaex = f'SELECT * FROM raex_comp_ratings WHERE inn = {inn}'
        dfCompRaex = bmms.spps.read_sql_to_df_pandas_SPPS(sqlRaex)

        # print(f"PR_548 --> @@#*&T*$  type(dfCompRaex) = {type(dfCompRaex)}")
        # print(f"PR_549 --> @@#*&T*$  dfCompRaex = \n{dfCompRaex}")

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






    ## -- ДЕКОРАТОРЫ ---
    # https://pythonworld.ru/osnovy/dekoratory.html

    # # Дек: Для вывода запросов sql, возвращающих выборки в курсоре, в виде уже готовых массивов (списков)
    # def transform_cursor_to_list_bmms(func_to_decorate):
    #     """Трансформирует курсор sql запроса в конечные списки данных"""
    #     def wrapper(self,*args, **kwargs):
    #         res = func_to_decorate(self,*args, **kwargs)
    #         # if DEBUG_:
    #         #     print(f"res[0] = {res[0]} / sqlite_proccessor.py / transform_cursor_to_list decorator / m35")
    #         if len(res) > 1: # Значит функция возвращает (cur, sql)
    #             dsRes = self.get_ds_from_cursor (res[0])
    #             # res[0].close() # Закрыть курсор

    #         else: # Значит функция sql возвращает один курсор cur
    #             dsRes = self.get_ds_from_cursor (res)
    #             # res.close() # Закрыть курсор
    #         return dsRes

    #     return wrapper
    


    ## -- END ДЕКОРАТОРЫ ---






#### 













if __name__ == '__main__':
    pass
















