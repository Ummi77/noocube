

# SELF: from noocube.pandas_manager import PandasManager

from noocube.sql_syntaxer import SQLSyntaxer
import noocube.funcs_general as FG
import sys
import pandas as pd

from noocube.class_ini import ClassIni
# 
from noocube.settings import *
from noocube.sql_syntaxer import SQLSyntaxer

# from bonds.algorithms_subparts import AlgorithmsSubParts

from noocube.settings import DEBUG_
# from algorithms_subparts import AlgorithmsSubParts
# from settings import DB_BONDS_
# from sqlite_pandas_processor import SqlitePandasProcessor
# sys.path.append('/home/ak/projects/3_Proj_Bonds_HTML_Center/project_bonds_html') # Прописываем path в системную переменную Python, что бы можно было запускать функции из данного модуля напрямую

import noocube.local_gen_func as LGF
from noocube.re_manager import ReManager
from noocube.settings import DB_BONDS_
import numpy as np
from .switch import Switch

from noocube.exceptions import *

from noocube.python_sys_manager import PythonSysManager




class PandasManager (ClassIni): 
    """ 
    Класс для работы с Pandas
    """

    def __init__(self):
        ClassIni.__init__(self)







    def get_pandas_data_frame(self, list2Dim, titleList= []):
        """ 
        OBSOLETED: Имя перетало соотвтетствовать нюансам . Копия метода ниже, но с новым именем
        Получение dataFtame из входного списка (и из одномерного списка тоже) с заголовками столбцов или без них
        titleList - должен соответствовать по кол-ву столбцов в списке. По умолчанию идет пустой список заголовков , тогда dataFrame просто индексируется
        Category: Фреймы
        """
        if len(titleList) > 0:
            df = pd.DataFrame(list2Dim,  columns = titleList) 
        else:
            df = pd.DataFrame(list2Dim)
        return df


    @staticmethod
    def get_pandas_data_frame_static(list2Dim, titleList= []):
        """ 
        OBSOLETED: Имя перетало соотвтетствовать нюансам . Копия метода ниже, но с новым именем
        Получение dataFtame из входного списка (и из одномерного списка тоже) с заголовками столбцов или без них
        titleList - должен соответствовать по кол-ву столбцов в списке. По умолчанию идет пустой список заголовков , тогда dataFrame просто индексируется
        Category: Фреймы
        """
        if len(titleList) > 0:
            df = pd.DataFrame(list2Dim,  columns = titleList) 
        else:
            df = pd.DataFrame(list2Dim)
        return df


    def get_data_frame_from_2dim_list_pandas (self, list2Dim, titleList= []):
        """ 
        NEW: Заменил предыдущий метод . Идентичный , но с новым названием
        Получение dataFtame из входного списка (и из одномерного списка тоже) с заголовками столбцов или без них
        titleList - должен соответствовать по кол-ву столбцов в списке. По умолчанию идет пустой список заголовков , тогда dataFrame просто индексируется
        Category: Фреймы
        """
        if len(titleList) > 0:
            df = pd.DataFrame(list2Dim,  columns = titleList) 
        else:
            df = pd.DataFrame(list2Dim)
        return df


    def read_df_from_2dim_list_pandas (self, list2Dim, titleList= []):
        """ 
        OBSOLETED: изменено просто название на read_df_from_any_dim_list_pandas по смыслу (можно считывать df со списка любой размерности)
        NEW: Заменил предыдущий метод . Идентичный , но с новым названием
        Получение dataFtame из входного списка (и из одномерного списка тоже) с заголовками столбцов или без них
        titleList - должен соответствовать по кол-ву столбцов в списке. По умолчанию идет пустой список заголовков , тогда dataFrame просто индексируется
        Category: Фреймы
        """
        if len(titleList) > 0:
            df = pd.DataFrame(list2Dim,  columns = titleList) 
        else:
            df = pd.DataFrame(list2Dim)
        return df
    
    
    def read_df_from_any_dim_list_pandas (self, list2Dim, titleList= []):
        """ 
        NEW: Заменил предыдущий метод read_df_from_2dim_list_pandas и get_data_frame_from_2dim_list_pandas. Идентичный , но с новым названием
        Получение dataFtame из входного списка (и из одномерного списка тоже) с заголовками столбцов или без них
        titleList - должен соответствовать по кол-ву столбцов в списке. По умолчанию идет пустой список заголовков , тогда dataFrame просто индексируется
        Category: Фреймы
        """
        if len(titleList) > 0:
            df = pd.DataFrame(list2Dim,  columns = titleList) 
        else:
            df = pd.DataFrame(list2Dim)
        return df


    def get_columns_vals_as_list(self, df, colName):
        """
        Получить значения в заданной колонки из фрейма в качестве списка
        Category: Фреймы
        """
        colValsList = df[colName].tolist()
        return colValsList


    @staticmethod
    def get_columns_vals_as_list_static(df, colName):
        """
        PandasManager
        Получить значения в заданной колонки из фрейма в качестве списка
        Category: Фреймы
        """
        colValsList = df[colName].tolist()
        return colValsList



    def get_unique_col_vals_as_list (self, df, colName):
        """
        Получить списко уникальных значений по колонке с названием colName из фрейма df
        Category: Фреймы
        """
        uniqueColVals = list(set(df[colName].tolist()))
        
        return uniqueColVals
    
    @staticmethod
    def get_unique_col_vals_as_list_static(df, colName):
        """
        PandasManager
        Получить списко уникальных значений по колонке с названием colName из фрейма df
        Category: Фреймы
        """
        uniqueColVals = list(set(df[colName].tolist()))
        
        return uniqueColVals
        


    @staticmethod
    def filter_df_by_field_vals_list(df, fieldName, listVals):
        """ 
        PandasManager
        Отфильтровать фрейм df по совпадению ключа fieldName со списком фильтрации listVals по значению ключа
        Category: Фреймы
        """
        dfRes = df.query(f'{fieldName} in @listVals')
        
        return dfRes



    @staticmethod
    def filter_df_with_algebraic_expr_for_one_field (dfSrc, fieldName, operand, compairedVal):
        """ 
        PandasManager
        ПРИМ: Не проверен
        Отфильтровать фрейм df по одному полю алгебраичеким выражением с одним операндом и заданынм значением сравнения
        Category: Фреймы
        """
        
        dfFiltered = dfSrc.query(f"@fieldName {operand} @compairedVal")
        
        return dfFiltered





    @staticmethod
    def filter_df_by_field_vals_not_in_list(df, fieldName, listVals):
        """ 
        PandasManager
        Отфильтровать фрейм df по НЕсовпадению ключа fieldName со списком фильтрации listVals по значению ключа 
        Оставить только те записи, значений которых по ключевому полю нет в списке фильтрации listVals
        Category: Фреймы
        """
        dfRes = df.query(f'{fieldName} not in @listVals')
        
        return dfRes






    @staticmethod
    def get_cell_val_by_row_inx_and_col_name(df, inx, colName):
        """
        PandasManager
        Получить значение ячейки фрейма оп индексу строки и названию колонки
        Category: Фреймы
        """
        cellVal = df[colName].iloc[inx]
        
        return cellVal





    @staticmethod
    def add_or_update_df_col_by_lambda_func_with_args_of_same_df_pandas(df, colTrg, lambFunc, listLambArgs, **lambOutArgs):
        """PandasManager
        OBSOLTED: Изменено название функции. Новое название - convert_or_add_calc_col_in_df_by_lambda_func_with_args_pandas()
        Обновление (или создание новой) и наполнение колонки в целевом фрейме на основе колонок-аргументов этого же фрейма с использованием лямбда-функции
        colTrg - Колонка, в которую нужно записать вычисляемые результаты по каждому ряду. Если нужно обновить колонку, то тогда listLambArgs = ['f2', ...] (как аргумент) 
        и colTrg = 'f2' (как целевая колонка). А если colTrg будет отлична от колонок в фрейме, то эта колонка добавиться и в нее проставятся результирующие значения
        lambFunc - лямбда функция
        listLambArgs - аргументы для лямбда вункции в виде списка названий колонок, в соотвтетсвии с последовательностью аргументов лямбда функции
        **lambOutArgs - аргументы, которые не исходят из полей фрейма, а задаются извне. Они так же могут присутствовать в лямбда функции. Для этого лямбда-функция должна 
        учитывать, что аргументы будут передаваться в виде списка. И там должны анализироваться и переприсваиваться в конечные внутренние переменные используемой функции
        
        Пример параметров:
        colTrg = 'f2'
        lambFunc = FG.convert_date_format_to_another_date_format
        listLambArgs = ['f2']
        lambOutArgs ={
            'formatSrc' : FORMAT_2_0_,
            'formatRes' : FORMAT_2_1_
            
        Пример лямбда-функции подходящей для этого метода: FG.convert_date_format_to_another_date_format
        }
        Category: Фреймы
        """
        print('START PR_419 --> : update_df_col_by_lambda_function_with_args_from_any_df_pandas() ')
        # listLambArgs = ['yield']
        df[colTrg] =  df.apply(lambda row: lambFunc([row[x] for x in listLambArgs], **lambOutArgs) , axis = 1)
        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма
        print('END PR_420 --> : update_df_col_by_lambda_function_with_args_from_any_df_pandas() ')
        return df
    
    
    @staticmethod
    def convert_or_add_calc_col_in_df_by_lambda_func_with_args_pandas(df, colTrg, lambFunc, listLambArgs, **lambOutArgs):
        """
        PandasManager
        NEW: Изменение названия функции, более понятное. Старая функция - add_or_update_df_col_by_lambda_func_with_args_of_same_df_pandas()
        Обновление (или создание новой) и наполнение колонки в целевом фрейме на основе колонок-аргументов этого же фрейма с использованием лямбда-функции
        colTrg - Колонка, в которую нужно записать вычисляемые результаты по каждому ряду. Если нужно обновить колонку, то тогда listLambArgs = ['f2', ...] (как аргумент) 
        и colTrg = 'f2' (как целевая колонка). А если colTrg будет отлична от колонок в фрейме, то эта колонка добавиться и в нее проставятся результирующие значения
        lambFunc - лямбда функция
        listLambArgs - аргументы для лямбда вункции в виде списка названий колонок, в соотвтетсвии с последовательностью аргументов лямбда функции
        **lambOutArgs - аргументы, которые не исходят из полей фрейма, а задаются извне. Они так же могут присутствовать в лямбда функции. Для этого лямбда-функция должна 
        учитывать, что аргументы будут передаваться в виде списка. И там должны анализироваться и переприсваиваться в конечные внутренние переменные используемой функции
        
        Пример параметров:
        colTrg = 'f2'
        lambFunc = FG.convert_date_format_to_another_date_format
        listLambArgs = ['f2']
        lambOutArgs ={
            'formatSrc' : FORMAT_2_0_,
            'formatRes' : FORMAT_2_1_
            
        Пример лямбда-функции (ее формат аргументов и RET) подходящей для этого метода: FG.convert_date_format_to_another_date_format
        }
        Category: Фреймы
        """
        print('START PR_421 --> : update_df_col_by_lambda_function_with_args_from_any_df_pandas() ')
        # from noocube.calc_fields import CalcFields
        # listLambArgs = ['yield']
        df[colTrg] =  df.apply(lambda row: lambFunc([row[x] for x in listLambArgs], **lambOutArgs) , axis = 1)
        cols = list(df) # Список колонок
        newColInx = len(cols)-1 # Последний индекс добавленнйо колонки равен длинне фрейма
        print('END PR_422 --> : update_df_col_by_lambda_function_with_args_from_any_df_pandas() ')
        return df
    
    
    @staticmethod
    def convert_or_add_calc_col_in_df_by_lambda_func_with_args_pandas_v2(df, colTrg, lambFunc, listLambArgs, **lambOutArgs):
        """
        PandasManager
        NEW: Изменение названия функции, более понятное. Старая функция - add_or_update_df_col_by_lambda_func_with_args_of_same_df_pandas()
        Обновление (или создание новой) и наполнение колонки в целевом фрейме на основе колонок-аргументов этого же фрейма с использованием лямбда-функции
        colTrg - Колонка, в которую нужно записать вычисляемые результаты по каждому ряду. Если нужно обновить колонку, то тогда listLambArgs = ['f2', ...] (как аргумент) 
        и colTrg = 'f2' (как целевая колонка). А если colTrg будет отлична от колонок в фрейме, то эта колонка добавиться и в нее проставятся результирующие значения
        lambFunc - лямбда функция
        listLambArgs - аргументы для лямбда вункции в виде списка названий колонок, в соотвтетсвии с последовательностью аргументов лямбда функции
        **lambOutArgs - аргументы, которые не исходят из полей фрейма, а задаются извне. Они так же могут присутствовать в лямбда функции. Для этого лямбда-функция должна 
        учитывать, что аргументы будут передаваться в виде списка. И там должны анализироваться и переприсваиваться в конечные внутренние переменные используемой функции
        
        Пример параметров:
        colTrg = 'f2'
        lambFunc = FG.convert_date_format_to_another_date_format
        listLambArgs = ['f2']
        lambOutArgs ={
            'formatSrc' : FORMAT_2_0_,
            'formatRes' : FORMAT_2_1_
            
        Пример лямбда-функции (ее формат аргументов и RET) подходящей для этого метода: FG.convert_date_format_to_another_date_format
        }
        Category: Фреймы
        """
        print('--------START PR_423 --> : convert_or_add_calc_col_in_df_by_lambda_func_with_args_pandas_v2() |noocube/pandas_manager.py')
        
        # Ограничение фрейма для тестов
        # df = df[:5]
        
        # pm = PandasManager()
        # pm.print_df_gen_info_pandas_IF_DEBUG(df, True, printFull = True)
        
        # print(f"%%%%$$$$ colTrg = {colTrg}")
        
        df[colTrg] =  df.apply(lambda row: lambFunc([row[x] for x in listLambArgs], **lambOutArgs) , axis = 1)
        
		# * https://stackoverflow.com/questions/47749018/why-is-pandas-apply-lambda-slower-than-loop-here
		# * https://stackoverflow.com/questions/38938318/why-apply-sometimes-isnt-faster-than-for-loop-in-a-pandas-dataframe
        # for row in df.index:
        #     if df.ix[row,'Lower'] <= df.ix[row, 'Mid'] <= df.ix[row,'Upper']:
        #         qualified_actions.append(True)
        #     else:
        #         qualified_actions.append(False)

        print('--------END PR_424 --> : convert_or_add_calc_col_in_df_by_lambda_func_with_args_pandas_v2() |noocube/pandas_manager.py')
        return df





    def get_df_sorted_by_col_name(self, df, sortDict, na_position = 'first'):
        """
        OBSOLETED: используются запутанные параметры. ниже копия, изменены названия ключей именованных параметров
        Сортирует dataFrame по колонке с именем. Входной dataFrame должен иметь установленные имена колонок
        na_position - устанавливает NaN элементы вначале при сотрирове.  По умолчанию - вверху
        sortDict - словрь с входнымипараметрами для сортировки : с ключами ['desc'] - порядок сортировки, ['sortColName'] - название сортируемой колонки в dFrame
        ascending - именновананя переменная ниже - False или True
        Category: Фреймы
        """
        # Расшифровка параметров сортировки
        desc = sortDict['desc'] # Порядок сортировки
        if DEBUG_:
            print (f"PR_425 --> descFlag = {desc} / PandasManager.get_df_sorted_by_col_name <pandas_manager.py>")
            
        sortColName = sortDict['sortColName'] # Название поля по которому происводится сортировка. Соотвтествует по номеру индексу в названии полей в таблице bonds_current
            
        dfSorted = df.sort_values(by=[sortColName], ascending = desc , na_position = na_position) # ascending - False или True, na_position - first, last и еще что-то там
        return dfSorted

    
    def get_df_sorted_by_col_name_v02 (self, df, sortColName, ascTrue = True,  na_position = 'first'):
        """ 
        NEW: 26.12.2022  - изменены названия ключей именованных параметров
        Сортирует dataFrame по колонке с именем. Входной dataFrame должен иметь установленные имена колонок
        na_position - устанавливает NaN элементы вначале при сотрирове.  По умолчанию - вверху
        sortDict - словрь с входнымипараметрами для сортировки : с ключами ['desc'] - порядок сортировки, ['sortColName'] - название сортируемой колонки в dFrame
        ascending - именновананя переменная ниже - False или True
        Category: Фреймы
        """
        # Расшифровка параметров сортировки
        if DEBUG_:
            print (f"PR_426 --> ascTrue = {ascTrue} / PandasManager.get_df_sorted_by_col_name <pandas_manager.py>")
        dfSorted = df.sort_values(by=[sortColName], ascending = ascTrue , na_position = na_position) # ascending - False или True, na_position - first, last и еще что-то там
        return dfSorted


    def get_df_sorted_by_col_index(self, df, sortColIndx, ascTrue = True, na_position = 'first'):
        """
        Сортирует dataFrame по индексу колонки. Входной dataFrame должен (???) иметь установленные имена колонок
        na_position - устанавливает NaN элементы вначале при сотрирове.  По умолчанию - вверху
        colIndx - индекс сортируемой колонки в dFrame
        ascTrue -  Порядок сорьтроовки (ascending = True - по увеличению , False - в сторону уменьшения)
        Category: Фреймы
        """
        sortColName = df.columns[sortColIndx]
        dfSorted = self.get_df_sorted_by_col_name_v02(df, sortColName, ascTrue, na_position)
        return dfSorted
        


    def get_df_sorted_by_sys_index(self, df):
        """
        Сортировка по системному индексу фрейма
        Category: Фреймы
        """
        df = df.sort_index(ascending=True)
        return df
    
    @staticmethod
    def get_col_inx_by_col_name(df, colName):
        """
        PandasManager
        Получить индекс колонки по имени в фрейме
        Category: Фреймы
        """
        
        colInx = df.columns.get_loc(colName)
        return colInx


    def get_df_sorted_from_site_request(self, df, tbFields, request):
        """
        Получение отсортированного массива dataFrame из параметров в получаемом с сайта request
        request - параметры GET - запроса со страницы сайта
        list2Dim - общий входной двумерный список данных с поялми и рядами
        titleList - спсиок  соответствующих названий заголовков для организации dataFrame, который соответствует колонкам входного двумерного списка list2Dim
        Category: Фреймы
        """
        ## Входные Параметры сортировки , запрашиваемые со страницы сайта
        desc = request.args.get('desc') # Получение значения флага сортировки по заданному полю
        sort = request.args.get('sort') # Получение значения флага сортировки по заданному полю
        sortCol = request.args.get('sortcol') # Индекс колонки ддля сортировки

        # Словарь  выбора sortFlag в зависимости от поступающей переменной desc, Если не установлен sort = 1.
        #  Служит для присваивания порядка сортировки, если не было смены порядка при нажатии на заголовок
        sortFlagByDescDict = { 
            '1' : True,
            '0' : False,
            'None' : True,
            None : True
        }

        if sort == '1': # Если флаг сортировки  = 1, то запускаем бинарное переключение порядка сортировки. Если  = 0, то не запускаем и порядок сортировки остается такм же, как был
            # Бинарное переключение переменной в зависимости от собственного ее значения
            biRes = LGF.binary_switch_str_var(desc) # Бинарный переключатель задаваемой бинарной переменной
            desc = biRes[0] # бинарное значение переменной
            sortFlag = biRes [1]
        else: # Если  = 0, то не запускаем и порядок сортировки остается такм же, как был
            sortFlag = sortFlagByDescDict[desc]

        # Передаваемое из сайта значение индекса сортируемой колонки
        if sortCol =='' or sortCol == None:
            sortCol = 1
        ## END Параметры сортировки 

        # Состсавление словаря параметров сортировки
        sortDict = {}
        sortDict['desc'] = sortFlag # Порядок сортировки
        sortDict['inxSortCol'] = sortCol # Индекс колонки сортировки
        sortDict['sortColName'] = tbFields[int(sortCol)] # Название поля по которому происводится сортировка. Соотвтествует по номеру индексу в названии полей в таблице bonds_current

        dfSorted = self.get_df_sorted_by_col_name(df, sortDict)

        return dfSorted, desc,  sortCol



    def get_df_sorted_with_switch_sort_dir_pandas(self, df, sortColsList, sortParams={}):
        """
        NEW по сравнению с get_df_sorted_from_site_request()
        sortColsList - список названий колонок фрейма для сортировки (последовательность должна быть важна возможно ??!!)

        Получение отсортированного массива dataFrame из параметров в получаемом с сайта request
        request - параметры GET - запроса со страницы сайта
        list2Dim - общий\входной двумерный список данных с поялми и рядами
        titleList - спсиок  соответствующих названий заголовков для организации dataFrame, который соответствует колонкам входного двумерного списка list2Dim
        Category: Фреймы
        """
        ## Входные Параметры сортировки , запрашиваемые со страницы сайта
        desc = sortParams ['desc'] # Получение значения флага сортировки по заданному полю
        # desc = '0'

        sort = sortParams ['sort'] # Получение значения флага сортировки по заданному полю
        sortCol = sortParams ['sortCol'] # индекс колонки для сортировки, если задана. По умолчанию сортировки нет. Пока по одной колонке

        # Словарь  выбора sortFlag в зависимости от поступающей переменной desc, Если не установлен sort = 1.
        #  Служит для присваивания порядка сортировки, если не было смены порядка при нажатии на заголовок
        sortFlagByDescDict = { 
            '1' : True,
            '0' : False,
            'None' : True,
            None : True
        }

        if sort == '1': # Если флаг сортировки  = 1, то запускаем бинарное переключение порядка сортировки. Если  = 0, то не запускаем и порядок сортировки остается такм же, как был
            # Бинарное переключение переменной в зависимости от собственного ее значения
            biRes = LGF.binary_switch_str_var(desc) # Бинарный переключатель задаваемой бинарной переменной
            desc = biRes[0] # бинарное значение переменной
            sortFlag = biRes [1]
        else: # Если  = 0, то не запускаем и порядок сортировки остается такм же, как был
            sortFlag = sortFlagByDescDict[desc]

        # Передаваемое из сайта значение индекса сортируемой колонки
        if sortCol =='' or sortCol == None:
            sortCol = 1
        ## END Параметры сортировки 

        # Состсавление словаря параметров сортировки
        sortDict = {}
        sortDict['desc'] = sortFlag # Порядок сортировки
        sortDict['inxSortCol'] = sortCol # Индекс колонки сортировки
        sortDict['sortColName'] = sortColsList # Раньше было по одной колонке. Но тут мы делаем по списку колонок сортирвку !!! (для теста пока пусть одна колонка)

        dfSorted = self.get_df_sorted_by_col_name(df, sortDict)

        return dfSorted, desc,  sortCol



    @staticmethod
    def get_intersect_of_two_df_by_key_col(df1, df2, intersectColName, how = 'inner'):
        """
        ПОКА ЗАГОТОВКА
        Получение пересечения кросс двух фреймов по заданной колонке
        Category: Фреймы
        """
        dfIntersect = pd.merge(df1, df2, on = [intersectColName], how = how)
        return dfIntersect
    
    
    
    @staticmethod
    def get_intersect_rows_are_not_in_other_frame_pm(dfValidation, dfBase, intersectColName):
        """
        ПРМИ: Проверять. иногда метод глючит
        Получить ряды, которых нет в другом фрейме по заданной колонке-ключе
        dfBase - Фрейм, в котором ищаться те ряды, которых нет в сравниваемом фрейме dfValidation
        Возвращаются dfBase с теми рядами, которые отсутствуют в dfValidation при сравнении по заданной колонке -ключу intersectColName
        ПРИМ: Можно сравнивать по нескольким или по всем колонкам фреймов. Тогда intersectColName - должен быть список названий
        колонок. Или вообще отсуствовать, тогда сравниваются все колонки вообще.
        
        ~ https://stackoverflow.com/questions/71558316/check-if-a-row-in-one-data-frame-exist-in-another-data-frame-but-do-not-merge-bo
        ~ https://stackoverflow.com/questions/28901683/pandas-get-rows-which-are-not-in-other-dataframe
        """
    
        # Создать колонку с результатом сравнения одинаковости колонок по лефому join. Резудбтат в виде булиинового False/True (False - если 
        # величины в обоих фреймах совпадают. True - если не совпадают)
        dfBase['Pass_validation?'] = dfBase.merge(dfValidation, 
                                            indicator=True, 
                                            on = [intersectColName],
                                            how='left')['_merge'].ne('both')
        
        

        
        #  Применить булиновую маску-фильтрацию по вспомогательной колонке 'Pass_validation?'
        dfBase = PandasManager.clear_df_by_mask_column_name_bool_pandas(dfBase, 'Pass_validation?')
        

        
        # Удалить ненужную вспомогательную  колонку после фильтрации
        dfBase = dfBase[dfBase.columns[:-1]]
        
        PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfBase, True, colsIndxed=True, 
                                                            marker=f"PR_479 --> dfBase =")
        

        return dfBase



    @staticmethod
    def replace_col_name_by_last_col_in_df (df, colToReplaceName):
        """
        PandasManager
        Переместить последнюю колонку сназванием  lastColName на место заданной colToReplace, удалить замещенную colToReplace и переименовать перемещкнную именем замещенной колонки 
        Другими словами, замещение заданной колонки по имени последней колонкой с заданынм именем. И удаление исходной замещаеой колонки из фрейма
        Category: Фреймы
        """
        
        cols = df.columns.tolist() # Список колонок фрейма изначальный
        srcColInx = PandasManager.get_col_inx_by_col_name(df, colToReplaceName) # Получить индекс колонки - источника
        newColsOrder = cols[:srcColInx] +  cols[-1:]  + cols[srcColInx+1:-1] # Новый порядок колонок в фрейме
        df = df[newColsOrder]
        df.rename(columns = {cols[-1]:colToReplaceName}, inplace = True) # Переименовать колонку в источниковую
        
        return df




    @staticmethod
    def shift_col_by_name_in_df (df, colNameToShift, newInx):
        """
        PandasManager
        Переместить колонку с заданным именем на заданное индексом положение в фрейме
        Category: Фреймы
        """

        cols = df.columns.tolist() # Список колонок фрейма изначальный
        
        # Удалить название перемещаемой колонки
        colInxToShift = PandasManager.get_col_inx_by_col_name(df, colNameToShift) # Получить индекс колонки , которую надо переместить
        cols.pop(colInxToShift) # Удалить из списка порядка колонок название перемещаемой колонки
        l1 = cols[:newInx] #
        l1.append(colNameToShift) # добавляем в список порядка колонок название перемещаемой колонки
        l2 = cols[newInx:]
        newColsOrder = l1 + l2 # Опять обьединяем
        
        df = df[newColsOrder]
        
        return df
    
    
    @staticmethod
    def shift_consicutive_cols_list_to_inx_position_in_df (df, colsNamesConsicList, newInx):
        """
        PandasManager
        Переместить список последовательных колонок с заданным именем colsNamesConsicList на заданное индексом newStartInx положение в фрейме
        Category: Фреймы
        """
        
        # Список колонок фрейма изначальный
        cols = df.columns.tolist() 
        
        # Удалить название перемещаемой колонки
        cols = PandasManager.delete_sublist_from_list(cols, colsNamesConsicList)
        
        # print(f'###########   $$$$$$$$$$$$$$$$   cols = {cols}')
        
        l1 = cols[:newInx] #
        l1 += colsNamesConsicList # добавляем в список порядка колонок название перемещаемой колонки
        l2 = cols[newInx:]
        newColsOrder = l1 + l2 # Опять обьединяем

        # print(f'###########   $$$$$$$$$$$$$$$$   newColsOrder = {newColsOrder}')
        
        df = df[newColsOrder]
        
        return df



    @staticmethod
    def drop_col_by_index_pandas (df, colInxDel):
        """
        PandasManager
        Удалить колонку по индексу из фрейма
        Category: Фреймы
        """
        
        df = df.drop(df.columns[colInxDel], axis=1)
        
        return df
    
    
    def delete_sublist_from_list(clist, sublist):
        """ 
        PandasManager
        Удалить из списка подсписок
        ~ https://stackoverflow.com/questions/49737657/remove-sublist-from-list
        Category: Фреймы
        
        """
        
        filter_set = set(sublist)
        clist = [x for x in clist if x not in filter_set]
        
        return clist



    @staticmethod
    def drop_col_by_name_pandas (df, columnsList):
        """
        ~ https://stackoverflow.com/questions/13411544/delete-a-column-from-a-pandas-dataframe
        PandasManager
        Удалить колонки по названию или списку названий
        Category: Фреймы
        """
        
        df = df.drop(columnsList, axis=1)
        
        return df




    # Обработка данных фрейма


    @staticmethod
    def read_df_from_list_of_dics(listOfDics):
        """ 
        PandasManager
        Формирование фрейма на базе списка словарей, представляющих услловно ряды 
        """
        
        df = pd.DataFrame.from_dict(listOfDics)
        return df



    @staticmethod
    def get_list_dicts_from_df_by_col_value_PM(df, keyCol, val):
        """
        PandasManager
        Получить список словарей-проекций рядов фрейма в результате поиска по заданному значению в заданной колонке
        Category: Фреймы
        """

        dfRes = PandasManager.filter_df_by_col_val_PM(df, keyCol, val)
        dictsList = PandasManager.convert_df_to_list_of_dicts_PM(dfRes)
        return dictsList


    @staticmethod
    def get_dict_from_df_with_key_col_name_and_val_col_name_pbf (df, keyColName, keyValName):
        """ 
        PandasManager
        Получить словарь из фрейма с ключами по заданной ключевой колонке и со значениями в виде значений заданной колонке значений
        ПРИМ: Может быть проработан более глубоко.
        """
        dict = {}
        for index, row in df.iterrows():
            dict[row[keyColName]] = row[keyValName]

        return dict
    
    
    
    
    
    @staticmethod
    def get_dict_from_df_of_class_objects_with_key_col_name_and_cols_vals_names_pm (df, objClassFullData, keyColName, listColsValsNames = []):
        """ 
        PandasManager
        Получить словарь из фрейма с ключами по заданной ключевой колонке keyColName и со значениями в виде значений заданных колонках значений listColsValsNames
        Присвоить эти значения в обьект класса objClassName
        По умолчанию названия колонок задаются в атрибутах класса-структуры индексированным названием  атрибута 'field' (field1, field2, ...)
        В этих полях с префиксом 'field' хранятся значения названий колонок фрейма (или, что то же самое - полей в таблице источнике фрейма). То есть те поля,
        по которым должны быть заполнены значения из фрейма. эти значения присваиваются автоматически в динамически создаваемые атрибуты обьекта с названиями
        равными названию полей в атрибутах класса с префиксом 'field'
        EXPLAIN: clsObj.field1 = <название колонки фрейма>  ---> 
                --->  динамически создаваемый атрибут clsObj.<название колонки фрейма> = <значение в фрейме по колонке field1>
        
        обьекту присвоить соотвтетсвующие названия атрибутов автоматически с префиксом 'obj_'. Если заданы поля в списке listColsValsNames, то они обладают
        более высоким приоритетом и поиск значений в фрейме осуществляется по ним
        
        objClassFullData - Путь к классу и название класса
        
        Notes:
        listOfAttributesInTuple = [('field1', 'volume_file_name'), ('field2', 'volume_title'), ('table', 'lib_book_audio_volumes'), 
        ('volumeFileName', ''), ('volumeTitle', '')]
        """
        # Локальный импорт, не переносить
        from noocube.funcs_general_class import FunctionsGeneralClass
        # import pandas as pd 
        
        
        # ПРИМ: Возможно нужно заменить пустые значения в коолнке 'volume_title' стрринговой пустотой (иначе идут потом глюки со словарем и темплейтингов в Джаного, 
        # где вместо путоты Джанго выдает 'None' для пустых значений в ловаре)
        # https://www.geeksforgeeks.org/python-pandas-dataframe-fillna-to-replace-null-values-in-dataframe/
    
        classObj = FunctionsGeneralClass.load_class_obj_from_file(objClassFullData['classFullPath'], objClassFullData['className'],) # В  случае , если модуль задается полным путем файла
    
        # Получить атрибуты обьекта класса
        listOfAttributesInTuple = PythonSysManager.obtain_all_attributes_of_class_object(classObj)
        
        # Если не задан список полей
        if not len(listColsValsNames) > 0: 
        
            # получить названия полей . по которым нужно считать информацию из фрейма (те, названия которых начинаются с 'field')
            listFields = [x[1] for x in listOfAttributesInTuple if x[0].startswith('field')]
                
            dict = {}
            # Цикл по рядам фрейма
            for index, row in df.iterrows():
                
                # print(f"PR_A835 --> index = {index}")
                
                classObj = FunctionsGeneralClass.load_class_obj_from_file(objClassFullData['classFullPath'], objClassFullData['className'],) # В  случае , если модуль задается полным путем файла
                
                # Цикл по полям фрейма
                for field in listFields:
                    
                    # Присвоить обьекту класса в заданный атрибут текущее значение по циклу  iterrows() [по фрейму]
                    setattr(classObj, field, row[field])
                
                dict[row[keyColName]] = classObj
                
        # TODO: Не реализован else: -> для случаев, когда задан список полей в listColsValsNames

        # print(f"PR_A832 --> dict = {dict}")

        return dict

    

    
    
    
    
    @staticmethod
    def get_dict_from_df_with_only_one_row_stat_pm (oneRowDf): 
        """ 
        OBSOLETED: rename to  read_df_with_one_row_to_dic_stat_pm
        PandasManager
        Получить словарь из фрейма только с одним рядом
        oneRowDf - фрейм только с одним рядом
        """
        
        dic = oneRowDf.loc[0].to_dict()
        
        return dic
    
    
    

    
    
    
    @staticmethod
    def get_dict_from_df_by_row_index_stat_pm (df, rowInx):
        """ 
        PandasManager
        Получить словарь из фрейма по заданному индексу ряда
        НЕ ПРОВЕРЕНО
        """
        
        dic = df.loc[rowInx].to_dict()
        
        return dic




    @staticmethod
    def filter_df_by_col_val_PM(df, keyCol, val):
        """
        PandasManager
        Отфильтровать фрейм по заданному знаению в заданной колонке
        Category: Фреймы
        """

        dfRes = df.loc[df[keyCol] == val]
        return dfRes




    def filter_df_rows_by_str_col_values(self, df, col, listValues, inverse = False):
        """ 
        PandasManager
        Фильтрация рядов фрейма по значениям в списке values (multiple values and str dtype)
        
        Фильтрация данных по значениям величин в заданной колонке
        https://stackoverflow.com/questions/18172851/deleting-dataframe-row-in-pandas-based-on-column-value

        Пример:
        df = pd.DataFrame({"colName": ["a","a","a","a","b","b","c"], "other": [1,2,3,4,5,6,7]})
        filter_rows_by_values(df, "colName", ["b","c"])
        Category: Фреймы
        """
        return df[df[col].isin(listValues) == inverse]
        #return df[~df[col].isin(listValues)] # Было до ввода флага инверсии inverse



    @staticmethod
    def filter_df_rows_by_str_col_values_pm_static(df, col, listValues, inverse = False):
        """ 
        PandasManager
        Фильтрация рядов фрейма по значениям в списке values (multiple values and str dtype)
        
        Фильтрация данных по значениям величин в заданной колонке
        https://stackoverflow.com/questions/18172851/deleting-dataframe-row-in-pandas-based-on-column-value

        Пример:
        df = pd.DataFrame({"colName": ["a","a","a","a","b","b","c"], "other": [1,2,3,4,5,6,7]})
        filter_rows_by_values(df, "colName", ["b","c"])
        Category: Фреймы
        """
        return df[df[col].isin(listValues) == inverse]
        #return df[~df[col].isin(listValues)] # Было до ввода флага инверсии inverse





    def filter_df_by_multiple_cols_vals (self, df, qrOper, logicOper, **kwargs):
        """ 
        PandasManager
        Фильтрация фрейма по значениям в нескольких колонках с настраиваемыми операторам сравнения , общим для каждого частного query, и логическим опреатором обьединения всех частных queries
        Для всех типов величин аргументов. None величины тоже допускаются, они просто пропускаются и не обрабатываются фильтратором
        qrOper - Опреатор сравнения внутри каждого выражения query
        logicOper - логический Оператор обьединения выражений в общем query для его под-частей
        **kwargs - именованные списки величин, где ключем (именем параметра) является название колонки, а величинами в списках - величины, которые нужно отфильтровать в каждой колонке (туда могут быть добавлены значения пустот '' и пр)
        Will remove None values so can be directly incoperated to functions with some values defaulting to None also the previous one would not work if the value was not string ,
        this will work on any type of arguments

        Пример использования: 
            qrOper = '!=' # Оператор сравнения 'не равно', то есть ищутся неравные задаваемым величинам значения в колонках
            logicOper = '&' # Логический оператор AND, для обьединения в логическое И всех частных выражений в query
            kwargs = {"okpo": listForFilter} # okpo в **kwargs - имя равное названию поля, по которому производится фиьтрация значений по списку listForFilter.
            dfFiltered = db_panda_proc.filter_df_by_multiple_cols_vals(dfToFilter, qrOper, logicOper, **kwargs)  

        https://stackoverflow.com/questions/22086116/how-do-you-filter-pandas-dataframes-by-multiple-columns
        https://habr.com/ru/company/ruvds/blog/482464/

        для фильтрации пустот можно использовать спсиок для **kwargs = listNones = ['', ' ', '-', '—', None]
        Category: Фреймы
        """
        # print (f"df = {df} / PandasManager.filter_df_by_multiple_cols_vals")
        query_list = []
        for key, value in kwargs.items():
            if value is not None:

                kwList = value
                query_list.append(f"{key} {qrOper} @kwList")
                # query_list.append(f"{key} {qrOper} @kwargs['{str(key)}']")
        query = f' {logicOper} '.join(query_list)
        # if DEBUG_:
            # print(f"query = {query} / pr: PandasManager.filter_df_by_multiple_cols_vals") # не удалять !!
            # print(f"kwargs = {kwargs} / pr: PandasManager.filter_df_by_multiple_cols_vals")
            # print(f"colsNames = {list(df)} / pr: PandasManager.filter_df_by_multiple_cols_vals")
        dfFiltered = df.query(query)   

        # Проверка. Если тип Serries (обычно если одна колонка), то преобразуем в фрейм с одной колонкой
        
        # print(f"Type of dfFiltered = {type(dfFiltered)}")

        if 'Series' in str(type(dfFiltered)):
            dfFiltered = self.convert_series_to_df_pandas(dfFiltered)

        return dfFiltered       


    @staticmethod
    def filter_df_by_multiple_cols_vals_static (df, qrOper, logicOper, **kwargs):
        """ 
        PandasManager
        Фильтрация фрейма по значениям в нескольких колонках с настраиваемыми операторам сравнения , общим для каждого частного query, и логическим опреатором обьединения всех частных queries
        Для всех типов величин аргументов. None величины тоже допускаются, они просто пропускаются и не обрабатываются фильтратором
        qrOper - Опреатор сравнения внутри каждого выражения query
        logicOper - логический Оператор обьединения выражений в общем query для его под-частей
        **kwargs - именованные списки величин, где ключем (именем параметра) является название колонки, а величинами в списках - величины, которые нужно отфильтровать в каждой колонке (туда могут быть добавлены значения пустот '' и пр)
        Will remove None values so can be directly incoperated to functions with some values defaulting to None also the previous one would not work if the value was not string ,
        this will work on any type of arguments

        Пример использования: 
            qrOper = '!=' # Оператор сравнения 'не равно', то есть ищутся неравные задаваемым величинам значения в колонках
            logicOper = '&' # Логический оператор AND, для обьединения в логическое И всех частных выражений в query
            kwargs = {"okpo": listForFilter} # okpo в **kwargs - имя равное названию поля, по которому производится фиьтрация значений по списку listForFilter.
            dfFiltered = db_panda_proc.filter_df_by_multiple_cols_vals(dfToFilter, qrOper, logicOper, **kwargs)  

        https://stackoverflow.com/questions/22086116/how-do-you-filter-pandas-dataframes-by-multiple-columns
        https://habr.com/ru/company/ruvds/blog/482464/

        для фильтрации пустот можно использовать спсиок для **kwargs = listNones = ['', ' ', '-', '—', None]
        Category: Фреймы
        """
        # print (f"df = {df} / PandasManager.filter_df_by_multiple_cols_vals")
        query_list = []
        for key, value in kwargs.items():
            if value is not None:

                kwList = value
                query_list.append(f"{key} {qrOper} @kwList")
                # query_list.append(f"{key} {qrOper} @kwargs['{str(key)}']")
        query = f' {logicOper} '.join(query_list)
        # if DEBUG_:
            # print(f"query = {query} / pr: PandasManager.filter_df_by_multiple_cols_vals") # не удалять !!
            # print(f"kwargs = {kwargs} / pr: PandasManager.filter_df_by_multiple_cols_vals")
            # print(f"colsNames = {list(df)} / pr: PandasManager.filter_df_by_multiple_cols_vals")
        dfFiltered = df.query(query)   

        # Проверка. Если тип Serries (обычно если одна колонка), то преобразуем в фрейм с одной колонкой
        
        # print(f"Type of dfFiltered = {type(dfFiltered)}")

        if 'Series' in str(type(dfFiltered)):
            dfFiltered = PandasManager.convert_series_to_df_pandas_static(dfFiltered)

        return dfFiltered     




    def filter_df_from_empties_or_any_vals_by_columns (self, df, colFiltList, listOfEmpties =  ['', ' ', '-', '—', None], inverse = False):
        """
        Очистка удаление рядов фрейма в которых находятся пустоты (или другие символы/величины/стринги) из заданного списка по задаваемым полям
        colFiltList - список названий колонок в которых проверяются пустоты 
        listOfEmpties - список фильрационных символов. По  умолчанию - ['', ' ', '-', '—', None]. Но можно задать любые символы и списки
        inverse - флаг инверсии. По умолчанию False (нет инверсии). Если true, то применяется инверсия и смысл фильтрации меняется на противоположный:
        "Очистка удаление рядов фрейма в которых НЕ находятся пустоты (или другие символы/величины/стринги) из заданного списка по задаваемым полям
        Category: Фреймы
        """
        # Отфильтровать NULL и пустоты (или другие символы/величины/стринги) в заданных колонках colFiltList
        if not inverse: # Если флаг инверсии = False (инверсия НЕ включена. Это default по умолчанию)
            qrOper = '!='
            logicOper = '&'
            kwargs = {}
            for col in colFiltList:
                kwargs[col] = listOfEmpties

        if inverse: # Если флаг инверсии = True (инверсия включена)
            qrOper = '=='
            logicOper = '|'
            kwargs = {}
            for col in colFiltList:
                kwargs[col] = listOfEmpties


        dfCleared = self.filter_df_by_multiple_cols_vals (df, qrOper, logicOper, **kwargs)     
        return  dfCleared  


    def filter_df_from_empties_or_any_vals_by_columns_static (df, colFiltList, listOfEmpties =  ['', ' ', '-', '—', None], inverse = False):
        """
        PandasManager
        Очистка удаление рядов фрейма в которых находятся пустоты (или другие символы/величины/стринги) из заданного списка по задаваемым полям
        colFiltList - список названий колонок в которых проверяются пустоты 
        listOfEmpties - список фильрационных символов. По  умолчанию - ['', ' ', '-', '—', None]. Но можно задать любые символы и списки
        inverse - флаг инверсии. По умолчанию False (нет инверсии). Если true, то применяется инверсия и смысл фильтрации меняется на противоположный:
        "Очистка удаление рядов фрейма в которых НЕ находятся пустоты (или другие символы/величины/стринги) из заданного списка по задаваемым полям
        Category: Фреймы
        """
        # Отфильтровать NULL и пустоты (или другие символы/величины/стринги) в заданных колонках colFiltList
        if not inverse: # Если флаг инверсии = False (инверсия НЕ включена. Это default по умолчанию)
            qrOper = '!='
            logicOper = '&'
            kwargs = {}
            for col in colFiltList:
                kwargs[col] = listOfEmpties

        if inverse: # Если флаг инверсии = True (инверсия включена)
            qrOper = '=='
            logicOper = '|'
            kwargs = {}
            for col in colFiltList:
                kwargs[col] = listOfEmpties


        dfCleared = PandasManager.filter_df_by_multiple_cols_vals_static (df, qrOper, logicOper, **kwargs)     
        return  dfCleared 




    def filter_df_get_rows_with_empty_by_columns (self, df, colFiltList, listOfEmpties =  ['', ' ', None]):
        """
        Получение рядов из фрейма с пустотами  по заданным колонкам
        colNamesList - список названий колонок в которых проверяются пустоты 
        listOfEmpties - список  символов пустот. По  умолчанию -  ['', ' ', None]. Но можно задать любые символы и списки
        Category: Фреймы
        """
        # Получение рядов из фрейма с пустотами  по заданным колонкам
        qrOper = '=='
        logicOper = '|'
        kwargs = {}
        for col in colFiltList:
            kwargs[col] = listOfEmpties

        dfCleared = self.filter_df_by_multiple_cols_vals (df, qrOper, logicOper, **kwargs)     
        return  dfCleared  



    

    @staticmethod
    def filter_df_get_rows_with_empty_by_columns_pandas_static (df, colFiltList, listOfEmpties =  ['', ' ', None]):
        """
        Получение рядов из фрейма с пустотами  по заданным колонкам
        colNamesList - список названий колонок в которых проверяются пустоты 
        listOfEmpties - список  символов пустот. По  умолчанию -  ['', ' ', None]. Но можно задать любые символы и списки
        Category: Фреймы
        """
        # Получение рядов из фрейма с пустотами  по заданным колонкам
        qrOper = '=='
        logicOper = '|'
        kwargs = {}
        for col in colFiltList:
            kwargs[col] = listOfEmpties

        dfCleared = PandasManager.filter_df_by_multiple_cols_vals_static (df, qrOper, logicOper, **kwargs)     
        return  dfCleared  






    def filter_df_with_str_fragm_by_one_col_and_one_cond (self, df, colName, strFragm, flagDiff = 'contain', invert = False, nap = False):
        """
        Фильтрация рядов фрейма по содержанию стрингового фрагмента в поле заданной одной колонки и пока по одному условию
        Аналог LIKE. Либо содержание либо start with .
        flagDiff - флаг диференциации либо ищется по содержанию, либо по StartWith (Можно еще добавить endWith) (contain, startwith, endwith)
        invert - флаг инверсии. По умолчанию - False (means - not inverted). If True , то инвертируется. (То есть - not contain, not startwith ...)
        nap - флаг игнорирования NULL и прочие not applicable значения в полях, к примеру, если разныого типа данные, которые не подпадают под символику филтрации
            По умолчанию = False (значит - игнорируюются). if True, то not applicable - не игнорируются   
        Можно добавить флаги дифференциации по fillna(False)]  ( if your problem with the pandas str methods was that your column wasn't entirely of string type)
        и и по case=False) - case sencitive <см в ссылке ниже>
        
        https://stackoverflow.com/questions/31391275/using-like-inside-pandas-query
        Category: Фреймы
        """
        for case in Switch(flagDiff):
            if case('contain'): 
                dfFilt = df[~df[colName].str.contains(strFragm, na = nap) == invert]
                break
            if case('startwith'): 
                dfFilt = df[~df[colName].str.startswith(strFragm, na = nap) == invert]
                break
            if case('endwith'): 
                dfFilt = df[~df[colName].str.endswith(strFragm, na = nap) == invert]
                break

            if case(): # default
                print(f'PR_427 --> Нет такого флага дифференциации {flagDiff}')
                break        
        return dfFilt



    @staticmethod
    def filter_df_with_str_fragm_by_one_col_and_one_cond_static (df, colName, strFragm, flagDiff = 'contain', invert = False, nap = False):
        """
        Фильтрация рядов фрейма по содержанию стрингового фрагмента в поле заданной одной колонки и пока по одному условию
        Аналог LIKE. Либо содержание либо start with .
        flagDiff - флаг диференциации либо ищется по содержанию, либо по StartWith (Можно еще добавить endWith) (contain, startwith, endwith)
        invert - флаг инверсии. По умолчанию - False (means - not inverted). If True , то инвертируется. (То есть - not contain, not startwith ...)
        nap - флаг игнорирования NULL и прочие not applicable значения в полях, к примеру, если разныого типа данные, которые не подпадают под символику филтрации
            По умолчанию = False (значит - игнорируюются). if True, то not applicable - не игнорируются   
        Можно добавить флаги дифференциации по fillna(False)]  ( if your problem with the pandas str methods was that your column wasn't entirely of string type)
        и и по case=False) - case sencitive <см в ссылке ниже>
        
        https://stackoverflow.com/questions/31391275/using-like-inside-pandas-query
        Category: Фреймы
        """
        for case in Switch(flagDiff):
            if case('contain'): 
                dfFilt = df[~df[colName].str.contains(strFragm, na = nap) == invert]
                break
            if case('startwith'): 
                dfFilt = df[~df[colName].str.startswith(strFragm, na = nap) == invert]
                break
            if case('endwith'): 
                dfFilt = df[~df[colName].str.endswith(strFragm, na = nap) == invert]
                break

            if case(): # default
                print(f'PR_428 --> Нет такого флага дифференциации {flagDiff}')
                break        
        return dfFilt




    def filter_df_by_regex_pandas (self, df, colName, regExPar):
        """
        Фильтрация df по патерну по задаваемой колонке
        na = False  / Отсекает все NULL NaN в значениях полей 
        regExPar - регулярное выражение, по которому фильтруется df в заданной колонке colName
        ReManager.regex_filter - функция, которая применяется ко всем значениям в задаваемой колонке через встроенный метод обьекта .apply
        Category: Фреймы
        """
        dfFiltBool = df[colName].apply(ReManager.regex_filter, rExpr = regExPar)
        dfFiltered = df[dfFiltBool]
        return dfFiltered


    @staticmethod
    def filter_df_by_regex_pandas_static (df, colName, regExPar):
        """
        Фильтрация df по патерну по задаваемой колонке
        na = False  / Отсекает все NULL NaN в значениях полей 
        regExPar - регулярное выражение, по которому фильтруется df в заданной колонке colName
        ReManager.regex_filter - функция, которая применяется ко всем значениям в задаваемой колонке через встроенный метод обьекта .apply
        Category: Фреймы
        """
        dfFiltBool = df[colName].apply(ReManager.regex_filter, rExpr = regExPar)
        dfFiltered = df[dfFiltBool]
        return dfFiltered



    def search_frame_by_col_val_simple(self, df, col, val):
        """
        Поиск по фрейму
        Category: Фреймы
        """
        dfFound = df.query(f"{col} == '{val}'")
        return dfFound


    def filter_frame_by_col_val_simple(self, df, col, oper, val):
        """
        Поиск - фильрация фрейма по заданному значению поля, значения и математического оператора
        Category: Фреймы
        """
        dfFound = df.query(f"{col} {oper} '{val}'")
        return dfFound



    def filter_frame_by_multiple_conds_sintaxer (self, df, condsDic):
        """
        Поиск-фильтрация фрейма  по множественным условиям с использзованием SQL-синтаксера для БД
        condsDic - словарь с условиями на подобие условий для запросов по SQL
        {'ONE':['colName','oper','val']}
        {'AND':[['colName'1,'oper1','val1'], ['colName2','oper2','val2'] ...]}
        Апперсанд тождественен 'AND', но система его не видит, поэтому в словаре условий вместо него ставим  '_ampers_',
        который после обработки синтаксером SQLSyntaxer замещается необходимым '&'
        ПР: conds = {'_apers_' : [[colName, '>', 8], [colName, '<', 10]]}  OR  conds = {'ONE' : [colName, '==', 'SU52002RMFS1']}
        Можно использовать и прочие операнды и операторы вместо ONE, AND, _apers_ и <, >, =, ==, IN ...
        Если вместо val использовать &val, то метод будет рассмтаивать это не как величину, а как название переменной или NULL, etc. и не будет заключать это название в кавычки, как
        это будет, если потавить стринговую переменную без & перед ней ПР: conds = {'ONE' : [colName, '==', '&NULL']}
        Category: Фреймы
        """
        condQuery = SQLSyntaxer._get_where_clause_sql(condsDic).replace('_ampers_', '&')
        # <PRINT>
        if DEBUG_: print (f"PR_429 --> condQuery = {condQuery}")
        
        dfFiltered = df.query(f"{condQuery}")
        # <PRINT>
        if DEBUG_: print(f"PR_430 --> dfFiltered_N = {len(dfFiltered)}")

        return dfFiltered


    @staticmethod
    def filter_df_by_query_pandas (df, qrExpress):
        """
        Отфильтровать фрейм через выражение query
        Category: Фреймы
        """

        df = df.query(f"{qrExpress}", engine='python')

        return df

    @staticmethod
    def ifColumnExistsInDf (df, col):
        """
        PandasManager
        Вернуть наличие колонки в фрейме в виде True or False
        """
        columns = list(df)
        # print (f"columns = {columns}")
        if col in columns:
            return True
        else:
            return False




    def drop_rows_from_df_by_ds_keys_pandas (self, dfBase, dsDropKeys, keyColAssocDic, inverse = False ):
        """
        Удаление рядов из фрейма df по заданным ключам 
        Если источником ключей для удаления является фрейм, то ключи соотвтетсвий для обоих фреймов задаются в словре соответсий keyColAssocDic {'keyDfBaseName' : 'keyDsDropKeys'}
        Если источником ключей для удаления является простой список, то в словаре  keyColAssocDic важен толлько значение ключа, который определяет ключевую колонку в dfBase
        dfBase - базовый фрейм, который фильтруется 
        dsDropKeys - массив с ключами. Можкт быть фреймом или простым списком
        inverse - флаг инверсии. По умолчанию False (нет инверсии). Если true, то применяется инверсия и смысл фильтрации метода меняется на противоположный:
        ПР: 
        keyColAssocDic = {'isin' : 'isin'}
        Category: Фреймы
        """
        # print(f"type of dsDropKeys = {type(dsDropKeys)}")
        if 'DataFrame' in str(type(dsDropKeys)) : # Если источник ключей для удаления dsDropKeys - колонка из фрейма 
            keyDsDropCol = list(keyColAssocDic.values())[0] # ключевая колонка в фрейме с ключами для удаления в dsDropKeys (если источник ключей на удаление - фрейм)
            dropKeysList = self.convert_df_to_list(dsDropKeys, keyDsDropCol)  # список ISINs, которые уже присутствуют в табл reg_isins_B , то есть уже были внесены данные по этим бумагам из MOEX
        elif 'list' in str(type(dsDropKeys)):  # Если источник ключей для удаления dsDropKeys - простой список
            dropKeysList = dsDropKeys  # список ключей, которые уже присутствуют в табл reg_isins_B
        else:
            print (f"PR_431 --> Тип данных {type(dsDropKeys)} в dsDropKeys неприемлем / PandasManager.drop_rows_from_df_by_ds_keys_pandas")

        keyCol = list(keyColAssocDic)[0] # ключевая колонка в фрейме
        colFiltList = [keyCol] # Список колонок для фильтрации ( isin)
        dfFiltered = self.filter_df_from_empties_or_any_vals_by_columns (dfBase, colFiltList, dropKeysList, inverse = inverse)
        return dfFiltered
    
    
    
    
    @staticmethod
    def drop_rows_from_df_by_ds_keys_pandas_static (dfBase, dsDropKeys, keyColAssocDic, inverse = False ):
        """
        PandasManager
        Удаление рядов из фрейма df по заданным ключам 
        Если источником ключей для удаления является фрейм, то ключи соотвтетсвий для обоих фреймов задаются в словре соответсий keyColAssocDic {'keyDfBaseName' : 'keyDsDropKeys'}
        Если источником ключей для удаления является простой список, то в словаре  keyColAssocDic важен толлько значение ключа, который определяет ключевую колонку в dfBase
        dfBase - базовый фрейм, который фильтруется 
        dsDropKeys - массив с ключами. Можкт быть фреймом или простым списком
        inverse - флаг инверсии. По умолчанию False (нет инверсии). Если true, то применяется инверсия и смысл фильтрации метода меняется на противоположный:
        ПР: 
        keyColAssocDic = {'isin' : 'isin'}
        Category: Фреймы
        """
        # print(f"type of dsDropKeys = {type(dsDropKeys)}")
        if 'DataFrame' in str(type(dsDropKeys)) : # Если источник ключей для удаления dsDropKeys - колонка из фрейма 
            keyDsDropCol = list(keyColAssocDic.values())[0] # ключевая колонка в фрейме с ключами для удаления в dsDropKeys (если источник ключей на удаление - фрейм)
            dropKeysList = PandasManager.convert_df_to_list_static(dsDropKeys, keyDsDropCol)  # список ISINs, которые уже присутствуют в табл reg_isins_B , то есть уже были внесены данные по этим бумагам из MOEX
        elif 'list' in str(type(dsDropKeys)):  # Если источник ключей для удаления dsDropKeys - простой список
            dropKeysList = dsDropKeys  # список ключей, которые уже присутствуют в табл reg_isins_B
        else:
            print (f"PR_432 --> Тип данных {type(dsDropKeys)} в dsDropKeys неприемлем / PandasManager.drop_rows_from_df_by_ds_keys_pandas")

        keyCol = list(keyColAssocDic)[0] # ключевая колонка в фрейме
        colFiltList = [keyCol] # Список колонок для фильтрации ( isin)
        dfFiltered = PandasManager.filter_df_from_empties_or_any_vals_by_columns_static (dfBase, colFiltList, dropKeysList, inverse = inverse)
        return dfFiltered
    
    
    



    def convert_series_to_df_pandas(self, ser):
        """
        PandasManager
        Трансформирует вектор или серию в fFrame
        Category: Фреймы
        """
        df = ser.to_frame()
        return df


    def convert_series_to_df_pandas_static(ser):
        """
        PandasManager
        Трансформирует вектор или серию в fFrame
        Category: Фреймы
        """
        df = ser.to_frame()
        return df

    # END Обработка данных фрейма


## МОДИФИКАЦИЯ ФРЕЙМА




    @staticmethod
    def clear_df_by_mask_column_name_pandas(df, maskColName):
        """
        OBSOLETED: by its name. Use clear_df_by_mask_column_name_bool_pandas()
        Очистить ряды фрейма на базе колонки-маски со значениями True-False
        Category: Фреймы
        """
        df = df.loc[df[maskColName], :]
        return df



    @staticmethod
    def clear_df_by_mask_column_name_bool_pandas(df, maskColName):
        """
        Очистить ряды фрейма на базе колонки-маски со значениями True-False
        Category: Фреймы
        """
        df = df.loc[df[maskColName], :]
        return df



## END МОДИФИКАЦИЯ ФРЕЙМА


    # Аналитика

    def get_duplicated_rows_of_column (self, df, colSubsetList = None) -> pd.DataFrame:
        """
        Получить ряды с дупликатами значенпий по заданной колонке
        colSubsetList - список колонок. по  коосплексу которых проверяются дупликаты. 
        Если их нет, то дупликаты проверяются по всей совокупности колонок фрейма (как бы логическое умножение)
        RET: Возвращается отсортированный по сабсету колонок фрейм с дупликатами
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.duplicated.html#pandas.DataFrame.duplicated
        Category: Фреймы
        """
        serDuplicatedRows = df[df.duplicated(subset = colSubsetList)].sort_values(by=colSubsetList)
        return serDuplicatedRows
    
    
    @staticmethod
    def get_duplicated_rows_of_column_static (df, colSubsetList = None) -> pd.DataFrame:
        """
        Получить ряды с дупликатами значенпий по заданной колонке
        colSubsetList - список колонок. по  коосплексу которых проверяются дупликаты. 
        Если их нет, то дупликаты проверяются по всей совокупности колонок фрейма (как бы логическое умножение)
        RET: Возвращается отсортированный по сабсету колонок фрейм с дупликатами
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.duplicated.html#pandas.DataFrame.duplicated
        Category: Фреймы
        """
        serDuplicatedRows = df[df.duplicated(subset = colSubsetList)].sort_values(by=colSubsetList)
        return serDuplicatedRows
    
    
    


    @staticmethod
    def get_df_cols_names_list(df):
        """
        PandasManager
        Получить список названий колонок в dataFrame
        Прим. Если колонка не имеет имени, то ее на будет в списке
        Category: Фреймы
        """
        # TODO: Сделать проверку на то, что df = None или пустой
        colsnamesList = list(filter(None, df.index.names + df.columns.values.tolist()))
        return colsnamesList

    @staticmethod
    def print_df_cols_names_pandas(df):
        """
        PandasManager
        Распечатать колонки фрейма
        Category: Фреймы
        """
        dfCols = PandasManager.get_df_cols_names_list(df)
        print (f"PR_433 --> dfColsNames = {dfCols}")
        return dfCols


    def get_accordance_dict_of_df_cols_names_indices(self, df):
        """
        Получить словарь соответствия названий колонок в dataFrame и их индексов
        Category: Фреймы
        """
        dictAccordCols = dict(enumerate(df))
        return dictAccordCols


    def get_df_type_of_datas_pandas(self, df):
        """
        Получить перечень типов данных, содержащихся в колонка фрейма
        Category: Фреймы
        """
        dataType = df.dtypes
        return dataType


    # END Аналитика


    # операции с данными dataFrame

    def duplicate_col_in_df(self, df, colNameToDupl, newColName):
        """
        Дублировать колонку в фрейме и присвоить название
        Category: Фреймы
        """
        df[newColName] = df.loc[:, colNameToDupl]



    def drop_rows_by_duplicates_vals_in_col(self, df, colSubsetList):
        """ 
        OBSOLETED
        Удалить ряды со вторым дупликатом (если такие есть) по проверяемой  колонке
        Category: Фреймы
        """
        df.drop_duplicates(subset=[colSubsetList])
        # df.drop_duplicates(subset=[colToCheck], inplace=True)
        
    @staticmethod
    def drop_rows_by_duplicates_vals_in_col_static(df, colSubsetList):
        """ 
        OBSOLETED
        Удалить ряды со вторым дупликатом (если такие есть) по проверяемой  колонке
        Category: Фреймы
        """
        df.drop_duplicates(subset=[colSubsetList])
        # df.drop_duplicates(subset=[colToCheck], inplace=True)
        
        


    def drop_duplicates_by_columns_pandas (self, df, colSubsetList, keepFg = 'last'):
        """
        Удалить дупликаты по нескольким колонкам listColNames для проверки 
        colSubsetList - сабсет колонок, по совокупности которых ищются дупликаты и удаляются, кроме заданных флагом keepFg
        keepFg - настройка, какая запись из дубликатов не удаляется. По умолчанию не удаляется последний из дубликатов. Может не удалятся первый. Или удалятся все (?)
        Category: Фреймы
        """
        dfDroped = df.drop_duplicates(colSubsetList, keep = keepFg)
        return dfDroped
    
    
    def drop_duplicates_by_columns_pandas_static (df, colSubsetList, keepFg = 'last'):
        """
        Удалить дупликаты по нескольким колонкам listColNames для проверки 
        colSubsetList - сабсет колонок, по совокупности которых ищются дупликаты и удаляются, кроме заданных флагом keepFg
        keepFg - настройка, какая запись из дубликатов не удаляется. По умолчанию не удаляется последний из дубликатов. Может не удалятся первый. Или удалятся все (?)
        Category: Фреймы
        """
        dfDroped = df.drop_duplicates(colSubsetList, keep = keepFg)
        return dfDroped


    def get_rows_by_col_name_val(self, df, colName, colVal):
        """
        Получить ряды, в заданной по наванию колонке которых находится поисковая величина ячейки
        Category: Фреймы
        """
        dfRows = df.loc[df[colName] == colVal]
        return dfRows
    
    
    @staticmethod
    def get_row_indices_by_col_val (df, colName, colVal):
        """
        PandasManager
        Получить индексы рядов фрейма df, в котором значения в ячейках по заданной колонке colName равно заданнйо величине colVal
        Возвращает именно лейбловые индексы , которые могут быть стрингами или int, а не порядковый индекс, который только int
        Category: Фреймы
        """
        
        rowIndices = df.index[df[colName]==colVal].tolist()
        return rowIndices
    
    
    
    @staticmethod
    def set_value_in_df_by_col_name_and_row_lebel_index(df, rowLabelIndex, colName, val):
        """ 
        PandasManager
        Установить значение в ячейке фрейма по названию колонки и лейбовому индексу ряда
        Category: Фреймы
        """
        
        df.at[rowLabelIndex, colName] = val
        return df
    
    
    
    
    @staticmethod
    def set_value_in_col_with_given_key_col_val_pandas (df, colKeyName, keyVal, colSetName, colSetVal):
        """ 
        PandasManager
        Установить значение colSetVal в ячейке с заданной колонкой colSetName в ряду, в котором находится искомое значение keyVal колонки- ключа colKeyName 
        (то есть, любой колонке с уникальными значениями в ячейках)
        Category: Фреймы
        """
        
        rowLabelIndex = PandasManager.get_row_indices_by_col_val (df, colKeyName, keyVal)
        df.at[rowLabelIndex[0], colSetName] = colSetVal
        return df
    
    
    @staticmethod
    def if_val_exists_in_col_pandas (df, colName, val):
        """ 
        PandasManager
        Подтвердить есть ли в заданнйо колонке colName ячейка, значение которой равно заданнйо величине val
        ПРИМ: Можно оптимизировать так: len(row['filter']) > 0  или подумать
        Category: Фреймы
        """
        
        colValsList = df[colName].tolist()
        
        if val in colValsList:
            return True
        else:
            return False
        
    
    
    
    
    
    @staticmethod
    def get_col_name_val_by_key_col_name_val_pandas (df, keyColName = '', keyColVal = -1, resColName = '', **kwargs):
        """
        PandasManager
        OBSOLETED: новое название метода ->> get_val_of_column_cell_by_val_of_key_column_stat_pandas()
        TODO: переименовать правильно: get_val_of_column_cell_by_val_of_key_column_stat_pandas()
        Найти значение в задаваемой колонке resColName по заданному значению keyColVal в ключевой колонке keyColName фрейма df
        Значения велечин в ключевой колонке должны быть уникальны
        Параметры могут задаваться через **kwargs
        Category: Фреймы
        """
        if 'keyColName' in kwargs:
            keyColName = kwargs['keyColName']
        if 'keyColVal' in kwargs:
            keyColVal = kwargs['keyColVal']
        if 'resColName' in kwargs:
            resColName = kwargs['resColName']
        
        print(f"PR_706 --> keyColName = {keyColName}")
        print(f"PR_707 --> keyColVal = {keyColVal}")
        print(f"PR_708 --> resColName = {resColName}")
        
        # Если нет inn в таблице comps_descr, то возникает ошибка. Обрабатываем
        try:
            val = df.loc[df[keyColName] == keyColVal, resColName].iloc[0]
        except:
            pass
            val = f'В фрейме нет значения keyColVal: {keyColVal} по ключевой колонке {keyColName} (PR_713)'
            print(f"!!! ERROR !!! PR_709 --> : В фрейме нет значения keyColVal: {keyColVal} по ключевой колонке {keyColName}")
        return val




    @staticmethod
    def get_val_of_column_cell_by_val_of_key_column_stat_pandas (df, keyColName = '', keyColVal = -1, resColName = '', **kwargs):
        """
        PandasManager
        NEW: старое название метода ->> get_col_name_val_by_key_col_name_val_pandas(...)
        Найти значение в задаваемой колонке resColName по заданному значению keyColVal в ключевой колонке keyColName фрейма df
        Значения велечин в ключевой колонке должны быть уникальны
        Параметры могут задаваться через **kwargs
        Category: Фреймы
        """
        if 'keyColName' in kwargs:
            keyColName = kwargs['keyColName']
        if 'keyColVal' in kwargs:
            keyColVal = kwargs['keyColVal']
        if 'resColName' in kwargs:
            resColName = kwargs['resColName']
        
        print(f"PR_706 --> keyColName = {keyColName}")
        print(f"PR_707 --> keyColVal = {keyColVal}")
        print(f"PR_708 --> resColName = {resColName}")
        
        # Если нет inn в таблице comps_descr, то возникает ошибка. Обрабатываем
        try:
            val = df.loc[df[keyColName] == keyColVal, resColName].iloc[0]
        except:
            pass
            val = f'В фрейме нет значения keyColVal: {keyColVal} по ключевой колонке {keyColName} (PR_713)'
            print(f"!!! ERROR !!! PR_709 --> : В фрейме нет значения keyColVal: {keyColVal} по ключевой колонке {keyColName}")
        return val



    def concatinate_two_frames_non_duplicates(a, b, col=None):
        """ 
        Обьединяет два смежных (одинаковых по полям) фрейма в один с фильтрацией дубликатов. Можно задать колонку для анализа дубликата или анализируются дупликаты по всем полям
        https://stackoverflow.com/questions/21317384/how-to-concatenate-two-dataframes-without-duplicates
        Category: Фреймы
        """
        if ((a is not None and type(a) is not pd.core.frame.DataFrame) or (b is not None and type(b) is not pd.core.frame.DataFrame)):
            raise ValueError('a and b must be of type pandas.core.frame.DataFrame.')
        if (a is None):
            return(b)
        if (b is None):
            return(a)
        if(col is not None):
            aind = a.iloc[:,col].values
            bind = b.iloc[:,col].values
        else:
            aind = a.index.values
            bind = b.index.values
        take_rows = list(set(bind)-set(aind))
        take_rows = [i in take_rows for i in bind]
        return(a.append( b.iloc[take_rows,:] ))



    def replace_value_in_col_by_cond_pandas(self, df, col, srchVal, newValue, alternValue):
        """
        Изменить df значение в ячейках заданной колонки col в соответствии с задаваемыми условиями srchVal на новое заданнйо значение newValue
        https://www.geeksforgeeks.org/how-to-replace-values-in-column-based-on-condition-in-pandas/
        Category: Фреймы
        """

        df[col] = np.where(df[col] == srchVal, newValue, alternValue)


        return df


    @staticmethod
    def replace_value_in_col_by_cond_pandas_static(df, col, srchVal, newValue, alternValue):
        """
        Изменить df значение в ячейках заданной колонки col в соответствии с задаваемыми условиями srchVal на новое заданнйо значение newValue
        https://www.geeksforgeeks.org/how-to-replace-values-in-column-based-on-condition-in-pandas/
        Category: Фреймы
        """

        df[col] = np.where(df[col] == srchVal, newValue, alternValue)


        return df




    def add_df_cols_with_constants_pandas(self, df,  colsConstsDic):
        """
        OBSOLETED: Плохое название метода. Изменено на add_const_val_to_df_pandas()
        Добавить задаваемые колонки с зададанынми константами из словаря colsConstsDic в фрейм df
        RET: Возвращает сам себя, так что можно не пользоваться возвратом, так как входной df изменяется сам по себе
        Category: Фреймы
        """
        for key, val in colsConstsDic.items():
            df[key] = val
        return df
    
    
    @staticmethod
    def add_df_cols_with_constants_pandas_static(df,  colsConstsDic):
        """
        OBSOLETED: Плохое название метода. Изменено на add_const_val_to_df_pandas() (или не oBSOLeTED)
        Добавить задаваемые колонки с зададанынми константами из словаря colsConstsDic в фрейм df
        RET: Возвращает сам себя, так что можно не пользоваться возвратом, так как входной df изменяется сам по себе
        Category: Фреймы
        """
        for key, val in colsConstsDic.items():
            df[key] = val
        return df
    
    
    



    def set_const_vals_to_df_cols_pandas(self, df,  colsConstsDic):
        """
        OBSOLETED: по названию не подходит. Изменено на update_const_vals_to_df_cols_pandas(self, df,  colsConstsDic):
        Добавить задаваемые колонки с зададанынми константами из словаря colsConstsDic в фрейм df
        colsConstsDic - пр: {'f7':'White'}
        RET: Возвращает сам себя, так что можно не пользоваться возвратом, так как входной df изменяется сам по себе
        Category: Фреймы
        """
        for key, val in colsConstsDic.items():
            df[key] = val
        return df


    def update_const_vals_to_df_cols_pandas(self, df,  colsConstsDic):
        """
        PandasManager
        Добавить задаваемые колонки с зададанынми константами из словаря colsConstsDic в фрейм df
        colsConstsDic - пр: {'f7':'White'}
        RET: Возвращает сам себя, так что можно не пользоваться возвратом, так как входной df изменяется сам по себе
        Category: Фреймы
        """
        for key, val in colsConstsDic.items():
            df[key] = val
        return df









# END операции с данными dataFrame


# Аналитические функции

    @staticmethod
    def if_value_exists_in_df_column_values_static(df, colCheckName, checkVal):
        """ 
        Проверить наличие в значениях заданной колонки colCheckName фрейма df заданного проверяемого значения checkVal
        """
        
        # Список велечин из колонки фрейма с заданным названием colCheckName
        listColVals = list(df[colCheckName])
        
        if checkVal in listColVals:
            print(f"PR_937 --> SYS: Значение {checkVal} существует в значениях по колонке фрейма с названием '{colCheckName}'")
            return True
        else:
            print(f"PR_938 --> SYS: Значение {checkVal} НЕ существует в значениях по колонке фрейма с названием '{colCheckName}'")
            return False
        
        




# END Аналитические функции


# Сохранение фреймов на носители


    def save_df_to_zip_file_with(self, df: pd, filePath):
        """
        Сохраняет содержимое фрейма в архивированный файл
        Category: Фреймы
        """
        df.to_pickle(filePath)




    def read_df_from_txt_file(self, filePath, delimiter = ' '):
        """
        считать фрейм из текстового файла
        Category: Фреймы
        """
        df = pd.read_table(filePath, delimiter)
        return df


    def read_from_zip_file(self, filePath):
        """
        Считать фрейм с из архивированного файла
        Category: Фреймы
        """

        # reading from the zip file
        df = pd.read_pickle(filePath)
        return df


    def read_df_from_dictionary(self, dicInp : dict):
        """
        Считать фрейм из словаря dicInp
        index=[0]  - > https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi
        Category: Фреймы
        """
        # df = pd.DataFrame.from_dict(dicInp)
        df = pd.DataFrame(dicInp, index=[0])
        return df
    
    
    @staticmethod
    def read_df_from_dictionary_static(dicInp : dict):
        """
        OBSOLETED: По названиб. Использовать тоэжественный  read_dict_to_df_simpe_static() 
        Считать фрейм из словаря dicInp
        index=[0]  - > https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi
        Category: Фреймы
        """
        # df = pd.DataFrame.from_dict(dicInp)
        df = pd.DataFrame(dicInp, index=[0])
        return df
    
    
    
    
    
    @staticmethod
    def read_dict_to_df_simpe_static(dicInp : dict):
        """
        Считать фрейм из словаря dicInp
        index=[0]  - > https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi
        Category: Фреймы
        """
        # df = pd.DataFrame.from_dict(dicInp)
        df = pd.DataFrame(dicInp, index=[0])
        return df
    
    
    @staticmethod
    def read_data_from_dict_to_two_columns_frame_pm_static (dicInp : dict, columnslist):
        """
        Считать  данные из словаря dicInp в фрейм с двумя колонками
        index=[0]  - > https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi
        Category: Фреймы
        """
        # df = pd.DataFrame.from_dict(dicInp)
        df = pd.DataFrame(dicInp.items(), columns=columnslist)
        return df
    
    
    

    # def read_df_for_given_keys_from_dictionary_static(dicInp : dict):
    #     """
    #     Считать фрейм из словаря dicInp
    #     index=[0]  - > https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi
    #     Category: Фреймы
    #     """
    #     # df = pd.DataFrame.from_dict(dicInp)
    #     df = pd.DataFrame(dicInp, index=[0])
    #     return df


    @staticmethod
    def read_df_from_list_of_structure_objs(listObjs, colsName =[]):
        """
        Считать список обьектов какой-то структуры в фрейм
        Класс обьектов долен иметь метод to_dict(). 
        Пример: /home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/structures.py / class FunctionStructure
        Category: Фреймы
        """
        
        df = pd.DataFrame.from_records([s.to_dict(colsName) for s in listObjs])
        return df
        
        
        
        
        
        
        






    def save_df_to_excel_file (self, df, dirPath, fileName, open = False):
        """
        Сохраняет данные из фрейма в эксел-файл
        df - фрейм
        dirPath - директорий сохранения файла (без косой черты в конце)
        fileName - название создаваемого файла
        open - опция открытия файла в конце (по умолчанию False)
        Category: Фреймы
        """
        from bonds.lo_calc_pandas_db import LibreCalcPandasDB # Не удалять. локальный импорт тут идет
        loSheetsPd = LibreCalcPandasDB() # обьект sheets класса LibreCalcPandasDB 

        # формирование полного названия файла с учетом времени создания в имени
        currTime = FG.get_current_time_format1_d_m_y_h_m_s()
        fName = fileName + f'_{currTime}.ods' # имф файла , связанное с временем создания
        fullPath = dirPath + '/' + fName

        # Открываем пустой эксел-файл
        loSheetsPd.open_document ('') # Создаем и открываем новый документ Calc Spreadsheet
        loSheetsPd._save_doc_as_new_file(fullPath) # Сохраняем созданный файл по заданному пути
        print(f"PR_434 --> INFO: Создан файл {fullPath}")
        loSheetsPd.close() # Закрытие документа
        
        # Записываем таблицу из фрейма dfIsinNotQualifed с облигациями с неквалифицированными инвесторами в созданный эксел файл (не открывая его)
        startCell = [3,2] # Стартовая  ячейка, с которой начинается левый верххний угол таблицы
        LibreCalcPandasDB.write_from_df_to_exel_pandas (df, fullPath, startCell = startCell, indxFlag = True)
        
        if open: # Открываем заполненный эксел-файл, если open = True
            loSheetsPd.open_document (fullPath)

        # loSheetsPd._save() # Сохраняем снова НЕ УДАЛЯТЬ!!
        print(f"PR_435 --> INFO: Данные из фрейма сохранены в файле {fullPath}")









# END Сохранение фреймов на носители


# Конвертирование

    def convert_df_col_to_list(self, df, colName):
        """ 
        OBSOLETED : Использовать более универсальную функцию convert_df_to_list
        Конвертировать серию-вектор колонки фрейма в простой список
        Category: Фреймы
        """
        colList =  list(df[colName])
        return colList
    
    
    @staticmethod
    def convert_df_col_to_list_pm_static(df, colName):
        """ 
        OBSOLETED : Использовать более универсальную функцию convert_df_to_list
        Конвертировать серию-вектор колонки фрейма в простой список
        Category: Фреймы
        """
        colList =  list(df[colName])
        return colList
    


    def convert_df_to_list(self, df, colsNamesList = []):
        """
        Конвертировать dataFrame или заданные его колонки в список
        colsNamesList - список коллонок для конвертирования в список. Если не заданы коллонки, то в список конвертируется весь фрейм (по умолчанию - весь фрейм в список)
        Если задана всего одна колонка в списке, то получается двумерный список , но с одной колонкой [[],[]...[]].
        А если вместо списка задается просто стринговое имя колонки, то выводится простой одномерный список!!! в виде [val1, val2 ... valN]
        Поэтому эта функция моет быть универсальной и функция convert_df_col_to_list - можно считать OBSOLETED
        Прим:
        listIsinKeysDated = bmm.convert_df_to_list(dfIsinKeysDated, 'isin'), если задана одна колонка из фрейма и ддля получения простого списка [val1, val2 ... valN]
        Category: Фреймы
        """
        if len(colsNamesList) > 0: # Если задан список колонок для конвертирования, то конвертируем только их
            listDF = df[colsNamesList].values.tolist()
        else: # Если не задан список колонок, то конвертируем весь фрейм
            listDF = df.values.tolist()
        return listDF
    
    
    @staticmethod
    def convert_df_to_list_static(df, colsNamesList = []):
        """
        Конвертировать dataFrame или заданные его колонки в список
        colsNamesList - список коллонок для конвертирования в список. Если не заданы коллонки, то в список конвертируется весь фрейм (по умолчанию - весь фрейм в список)
        Если задана всего одна колонка в списке, то получается двумерный список , но с одной колонкой [[],[]...[]].
        А если вместо списка задается просто стринговое имя колонки, то выводится простой одномерный список!!! в виде [val1, val2 ... valN]
        Поэтому эта функция моет быть универсальной и функция convert_df_col_to_list - можно считать OBSOLETED
        Прим:
        listIsinKeysDated = bmm.convert_df_to_list(dfIsinKeysDated, 'isin'), если задана одна колонка из фрейма и ддля получения простого списка [val1, val2 ... valN]
        Category: Фреймы
        """
        if len(colsNamesList) > 0: # Если задан список колонок для конвертирования, то конвертируем только их
            listDF = df[colsNamesList].values.tolist()
        else: # Если не задан список колонок, то конвертируем весь фрейм
            listDF = df.values.tolist()
        return listDF



    @staticmethod
    def convert_df_to_list_static(df, colsNamesList = []):
        """
        PandasManager
        Конвертировать dataFrame или заданные его колонки в список
        colsNamesList - список коллонок для конвертирования в список. Если не заданы коллонки, то в список конвертируется весь фрейм (по умолчанию - весь фрейм в список)
        Если задана всего одна колонка в списке, то получается двумерный список , но с одной колонкой [[],[]...[]].
        А если вместо списка задается просто стринговое имя колонки, то выводится простой одномерный список!!! в виде [val1, val2 ... valN]
        Поэтому эта функция моет быть универсальной и функция convert_df_col_to_list - можно считать OBSOLETED
        Прим:
        listIsinKeysDated = bmm.convert_df_to_list(dfIsinKeysDated, 'isin'), если задана одна колонка из фрейма и ддля получения простого списка [val1, val2 ... valN]
        Category: Фреймы
        """
        if len(colsNamesList) > 0: # Если задан список колонок для конвертирования, то конвертируем только их
            listDF = df[colsNamesList].values.tolist()
        else: # Если не задан список колонок, то конвертируем весь фрейм
            listDF = df.values.tolist()
        return listDF




    def get_sub_df_with_given_cols(self, df, colNamesList):
        """
        Получить суб-фрейм подмножество из фрейма с заданными колонками
        Category: Фреймы
        """
        subDF = df.loc[:,colNamesList] 
        # subDF = df[colNamesList]
        # subDF = pd.DataFrame(df, columns=colNamesList)
        return subDF

    @staticmethod
    def get_sub_df_with_given_cols_static(df, colNamesList):
        """
        PandasManager
        Получить суб-фрейм подмножество из фрейма с заданными колонками
        Category: Фреймы
        """
        subDF = df.loc[:,colNamesList] 
        # subDF = df[colNamesList]
        # subDF = pd.DataFrame(df, columns=colNamesList)
        return subDF



    def rename_col(self, df, changNameDic):
        """
        Переименгвть колонку
        changNameDic : {"inn": "inn_ref"}
        Category: Фреймы
        """
        dfChanged = df.rename(columns=changNameDic)
        return dfChanged
    
    @staticmethod
    def rename_col_pandas_static(df, changNameDic):
        """
        ПРИМ: Какя-то ошибка (или все норм?)
        Переименгвть колонки (именно множество колонок) в соотвтетсвии со словарем названий
        changNameDic : {"inn": "inn_ref", "isin_ref" : "isin", ...}
        Category: Фреймы
        """
        dfChanged = df.rename(columns=changNameDic)
        return dfChanged
    

    
    def rename_columns_by_lebel_list(self, df, leblist):
        """
        Переименовать в df название колонок по порядку в соответствии со списком названий колонок leblist
        Category: Фреймы
        """
        dfRes = df.set_axis(leblist, axis=1)
        return dfRes
    
    
    
    # def rename_df_titles_for_general_columns_tb_static (df, colsExcept, titleLetter):
    #     """ 
    #     Переименовать колонки фрейма для полей таблицы, которые имеют универсальные нейтральные газвания типа t1, t2, f1, ...
    #     colsExcept - те названия колонок. которые должны сохранить свои имена как в фрейме. Остальные все колонки будут переименованы
    #     """
    
    
    
    
    
    @staticmethod
    def rename_columns_by_lebel_list_static(df, leblist):
        """
        Переименовать в df название колонок по порядку в соответствии со списком названий колонок leblist
        Category: Фреймы
        """
        dfRes = df.set_axis(leblist, axis=1)
        return dfRes
    


    def rename_cols_by_associate_dic_pandas(self, df, assocDic, inplace = False):
        """
        PandasManager <??? Не работает коректно. По индексам не переименовывает. Словарь соотвтествий должен содержать соответствие между именами>
        <#TODO: Переписать функцию . Используя функцию трансформации индексов в словаре в имена оригинальных названий колонок в фрейме !!!>
        Переименовать те колонки фрейма, соотвтествие которых задано в словаре соотвтествий. Ключами в словаре являются искомые колонки в фрейме, которые нужно переименовать
        в соотвтествии со значениями из словаря по этим ключам
        inplace - если стоит True, то словарь не перезаписывается, а колонки переименовываются в существующем фремй.
        Если - False, то создается копия словаря с переименнованными колонками
        По умолчанию inplace = False
        https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas
        Category: Фреймы
        """
        # Переименование колонок, заданных словарем соответствий
        dfRenamed = df.rename(columns= assocDic, inplace=inplace) 
        return dfRenamed




    def rename_cols_by_associate_dic_pandas_static(df, assocDic, inplace = False):
        """
        PandasManager 
        <??? Не работает коректно. По индексам не переименовывает. Словарь соотвтествий должен содержать соответствие между именами>
        <#TODO: Переписать функцию . Используя функцию трансформации индексов в словаре в имена оригинальных названий колонок в фрейме !!!>
        Переименовать те колонки фрейма, соотвтествие которых задано в словаре соотвтествий. Ключами в словаре являются искомые колонки в фрейме, которые нужно переименовать
        в соотвтествии со значениями из словаря по этим ключам
        inplace - если стоит True, то словарь не перезаписывается, а колонки переименовываются в существующем фремй.
        Если - False, то создается копия словаря с переименнованными колонками
        По умолчанию inplace = False
        https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas
        Category: Фреймы
        """
        # Переименование колонок, заданных словарем соответствий
        dfRenamed = df.rename(columns= assocDic, inplace=inplace) 
        return dfRenamed




    def rename_cols_by_associate_dic_type2_pandas(self, df, assocDicType2, inplace = True):
        """PandasManager / ОТТЕСТИРОВАНА !!!
        Переименовать те колонки фрейма, соотвтествие которых задано в словаре соотвтествий. Ключами в словаре являются индексы колонок фрейма, которые нужно переименовать
        в соотвтествии со значениями из словаря по этим ключам
        assocDicType2 - словарь ассоциаций 2го типа / type2 { dfColinx : 'tbColТame'} , где dfColinx - индекс колонки в фрейме, tbColТame - 
        соотвтетсвующее этой колонке название поля в таблице, для которой предназначен словарь ассоциаций
        inplace - если стоит True, то словарь не перезаписывается, а колонки переименовываются в существующем фремй.
        Если - False, то создается копия словаря с переименнованными колонками
        https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas
        """
        
        colinxs = list(assocDicType2.keys()) # Индексы колонок в фрейме df
        
        print(f"\nPR_436 --> Print Source: rename_cols_by_associate_dic_type2_pandas() | /home/ak/projects/3_Proj_Bonds_HTML_Center/project_bonds_html/projr/classes/pandas_manager.py")
        print (f"PR_437 --> colinxs = {colinxs}")
        
        try:
            new_names_map = {df.columns[i]:assocDicType2[i] for i in colinxs}
        except Exception as err:
            raise  exception_factory(AssocDicToRenameNotEqualByStructure, "rename_cols_by_associate_dic_type2_pandas() | PandasManager | pandas_manager.py | 3_Bonds_HTML_Center")
                
            
        # Переименование колонок, заданных словарем соответствий
        df.rename(new_names_map, axis=1, inplace = inplace)
        return df



    def rename_cols_by_associate_dic_type2_pandas_static(df, assocDicType2, inplace = True):
        """PandasManager / ОТТЕСТИРОВАНА !!!
        Прим: Работает некорректно. Переделать на примере метода rename_cols_by_assoc_dic_inx_name_and_slice_pandas() 
        Переименовать те колонки фрейма, соотвтествие которых задано в словаре соотвтествий. Ключами в словаре являются индексы колонок фрейма, которые нужно переименовать
        в соотвтествии со значениями из словаря по этим ключам
        assocDicType2 - словарь ассоциаций 2го типа / type2 { dfColinx : 'tbColТame'} , где dfColinx - индекс колонки в фрейме, tbColТame - 
        соотвтетсвующее этой колонке название поля в таблице, для которой предназначен словарь ассоциаций
        inplace - если стоит True, то словарь не перезаписывается, а колонки переименовываются в существующем фремй.
        Если - False, то создается копия словаря с переименнованными колонками
        https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas
        """
        
        colinxs = list(assocDicType2.keys()) # Индексы колонок в фрейме df
        
        print(f"\nPR_337 --> Print Source: rename_cols_by_associate_dic_type2_pandas() | /home/ak/projects/3_Proj_Bonds_HTML_Center/project_bonds_html/projr/classes/pandas_manager.py")
        print (f"PR_338 --> colinxs = {colinxs}")
        
        try:
            new_names_map = {df.columns[i]:assocDicType2[i] for i in colinxs}
        except Exception as err:
            raise  exception_factory(AssocDicToRenameNotEqualByStructure, "rename_cols_by_associate_dic_type2_pandas() | PandasManager | pandas_manager.py | 3_Bonds_HTML_Center")
                
            
        # Переименование колонок, заданных словарем соответствий
        df.rename(new_names_map, axis=1, inplace = inplace)
        return df




    def rename_cols_by_assoc_dic_inx_name_pandas(self, df, assocDicInxName, inplace = False):
        """
        PandasManager
        Переименование колонок в фрейме на базе словаря ассоциаций вида {inx : 'colNewName', ...}, то есть, где в виде ключей заданы индексы колонок фрейма, 
        а значения словаря - новые имена колонок фрейма
        Category: Фреймы
        """

        for key, val in assocDicInxName.items(): # Цикл по словарю ассоциаций
            df = df.rename(columns={df.columns[key]: val}, inplace = inplace)

        return df



    def rename_cols_by_assoc_dic_inx_name_and_slice_pandas(self, df, assocDicInxName):
        """
        Переименование колонок в фрейме на базе словаря ассоциаций вида {inx : 'colNewName', ...}, то есть, где в виде ключей заданы индексы колонок фрейма, 
        а значения словаря - новые имена колонок фрейма. А так же вырезать ненужные колонки в фрейме, оставив лишь те, переименование по которым задано в словаре 
        ассоциаций assocDicInxName
        Category: Фреймы
        """

        dfRenamed = self.rename_cols_by_assoc_dic_inx_name_pandas(df, assocDicInxName) # Переименовать

        keysList = list(assocDicInxName.keys())
        dfSliced = self.slice_df_by_cols_indices_pandas (dfRenamed, keysList) # Вырезать



        return dfSliced
    
    
    
    
    def rename_frame_columns_and_slice_by_dic_with_cols_names_stat_pandas (df, dicColsAssosiate):
        """ 
        NEW: 28-01-2024
        PandasManager
        
        Переименование колонок фрейма и обрезание ненужных колонок в соответтсвии со словарем старых-новых имен dicColsAssosiate
        Порядок коллонок в конечном фрейме соотвтетсвует порядку названий колонок в словаре
        В фрейме остаются только те колонки, которые присутствуют в словаре
        Ключи словаря - должны соотвтетсвовать названиям колонок фрейма
        
        ПРИМ: 
        COLS_ASSOC_FOR_BOOKS_DOWNLOADED_ = {   
            'message_own_id' : 'Mssg_ID', 
            'message_text' : 'Текст_сообщения',
        } 
        Category: Фреймы
        """
        
        # Переименовываем в соотвтетсвии со словарем ассоциаций dicColsAssosiate
        df = df.rename(columns = dicColsAssosiate)
        
        # Оставляем только те колонки, которые есть в занчениях словаря ассоциаций
        listColsSlice = list(dicColsAssosiate.values())
        df = df.loc[:, listColsSlice]
        
        return df
        
        
        
        
        
        
        
        
        
        
        
        
    
    @staticmethod
    def read_df_row_to_dic_by_key_val_stat_pm(df, keyVal):
        """
        PandasManager
        Конвертировать один ряд фрейма , взятый по значению в поле-ключе, в словрь, где ключи - названия колонок фрейма, значения - значения 
        # в колонках фрейма
        keyVal - словарь { 'key' : keyField, 'val' : keyFieldVal}
        Category: Фреймы
        """
    
        print(f"PR_NC_176 --> START: read_df_row_to_dic_by_key_val_stat_pm()")

    
        keyField = keyVal['key'] # название ключевого поля
        keyFieldVal = keyVal['val'] # значение поля-ключа
        
        # print(f"PR_NC_175 --> DEBUG LOG: keyVal = {keyVal}")
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(df, True, colsIndxed=True, marker=f"PR_A289 --> DEBUG LOG: df")
        
        dfFilt = df.query(f'{keyField} == {keyFieldVal}')
        
        qnDfFilt = len(dfFilt)
        
        if qnDfFilt > 0:
            
            # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(df, True, marker='PR_NC_174 --> ')
            
            # Фильтр-строка
            fStr = f"{keyField} == {keyFieldVal}"
            
            dic = df.query(fStr).to_dict('records')[0]
            
            print(f"PR_NC_183 --> dic = {dic}")
            
        else:
            dic = -1
        
        
        print(f"PR_NC_177 --> END: read_df_row_to_dic_by_key_val_stat_pm()")
        
        return dic
    
    
    



    # {CURRENT 08-02-2024 14-00}
    @staticmethod
    def read_df_row_to_dic_by_multiple_key_val_stat_pm(df, listOfKeyVals):
        """
        PandasManager
        Конвертировать один ряд фрейма , взятый по значению в поле-ключе, в словрь, где ключи - названия колонок фрейма, значения - значения 
        # в колонках фрейма
        keyVal - словарь { 'key' : keyField, 'val' : keyFieldVal}
        Category: Фреймы
        """
    
        print(f"PR_NC_176 --> START: read_df_row_to_dic_by_key_val_stat_pm()")


        # A. сформировать фильтр-выражение для query для фрейма
        
        fqExpr =""
        
        for keyVal in listOfKeyVals:
        
            keyField = keyVal['key'] # название ключевого поля
            keyFieldVal = keyVal['val'] # значение поля-ключа
            
            
            fqExpr += f"{keyField} == {keyFieldVal}" + " & "
            
            
        fqExpr = fqExpr.strip(' &')
            
        # print(f"PR_NC_175 --> DEBUG LOG: fqExpr = {fqExpr}")    

            
        dfFilt = df.query(fqExpr)
        
        qnDfFilt = len(dfFilt)
        
        if qnDfFilt > 0:


            
            dic = dfFilt.to_dict('records')[0]
            
            # print(f"PR_NC_183 --> dic = {dic}")
            
        else:
            dic = -1
        
        
        print(f"PR_NC_177 --> END: read_df_row_to_dic_by_key_val_stat_pm()")
        
        return dic
    



    @staticmethod
    def read_df_with_one_row_to_dic_stat_pm (oneRowDf): 
        """ 
        PandasManager
        Получить словарь из фрейма только с одним рядом
        oneRowDf - фрейм только с одним рядом
        """
        
        dic = oneRowDf.loc[0].to_dict()
        
        return dic
    



    @staticmethod
    def read_multiple_rows_df_to_list_of_row_dictionaries_stat_pm (df):
        """ 
        Получить список словарей, соотыеттсвующих каждому ряду заданного фрейма, где ключами являются названия полей фрейма (которые тождественны названию полей исходной 
        # таблицы)
        """
        listDfRowsDicts = []
        
        for index, row in df.iterrows():
            
            dicCurr = row.to_dict()
            
            listDfRowsDicts.append(dicCurr)
            
        return listDfRowsDicts





    


    @staticmethod
    def convert_df_to_list_of_dicts_PM(df):
        """
        PandasManager
        Конвертировать фрейм с список словарей с элементами в виде значений по полям ряда фрейма
        Category: Фреймы
        """

        dictsList = df.to_dict(orient='records')
        return dictsList




    def convert_key_col_and_val_col_of_df_to_dic_pm_static(df, colKeyName, colValName):
        """ 
        PandasManager
        Конвертировать задаваемую колонку с ключевыми значениями из фрейма и задаваемую колонку с соотвтетсвующими значениями из фрейма
        в словарь
        ПРим: в фрейме не должно быть колонок с одинаковыми названиями, иначе будет глюк при выводе результата в словаре
        Category: Фреймы
        """

        # print(f"PR_974 --> colKeyName = {colKeyName}")
        # print(f"PR_975 --> colValName = {colValName}")
        listKeys = list(df[colKeyName])
        # print(f"PR_973 --> listKeys = {listKeys}")
        listVals = list(df[colValName])
        # print(f"PR_971 --> listVals = {listVals}")
        dicRes = FG.convert_two_lists_to_dictionary(listKeys, listVals)
        # print(f"PR_972 --> dicRes = {dicRes}")
        
        
        
        return dicRes


    @staticmethod
    def drop_empty_name_columns_static(df):
        """ 
        PandasManager
        Удалить колонки из ырейма, которые не имеют тайтла , названия
        Category: Фреймы
        """
        
        df = df[[x for x in df.columns if len(x)>=1]]
        return df




# END Конвертирование



    ### Конвертирование данны в колонках / рядах

    @staticmethod
    def clear_str_float_from_persent_simb (df, colName):
        """
        PandasManager
        OBSOLETED: new one ->  convert_str_empty_with_persent_and_empty_str_to_float () !!!
        Удалить символы % в колонке с действительными  числами в стринговой колонке фрейма
        Category: Фреймы
        """
        # Конверация колонки в float с предварительным удалением знака '%'
        df[colName] = df[colName].astype(str).str.rstrip('%').astype(float)

        return df



    @staticmethod
    def convert_str_empty_with_persent_and_empty_str_to_float (df, colName):
        """
        PandasManager
        Переводит (Только пустоты) пустоты в колонке в -1 и потом конвертирует всю колонку в float. Необходимо, так как когда присутствуют пустоты в виде стрингов, то не выходит сортировка, пока
        не провести данную операцию. Переводит пропуск '-'(тире) в -2. 
        Category: Фреймы
        """
        df[colName] = df[colName].apply(lambda x: x.replace('', '-1') if (isinstance(x, str) and len(x)<1) else x) # Перевести стринговые пустоты в '-1' 
        df[colName] = df[colName].apply(lambda x: x.replace('-', '-2') if (isinstance(x, str) and x=='-') else x) # Перевести прочерк '-' в '-2' 

        df[colName] = df[colName].apply(lambda x: x.replace('%', '') if (isinstance(x, str) ) else x) # Очистить от %
        df[colName] = df[colName].apply(lambda x: x.replace(' ', '') if (isinstance(x, str) ) else x) # Удалить пропуски
        df[colName] = df[colName].apply(lambda x: float(x)) # Конвертировать в float()
        return df
    
    


    def convert_list_of_df_columns_clear_from_str_empty_with_persent_and_empty_str_to_float_pm (df, colList):
        """ 
        Переводит (Только пустоты) пустоты в списке колонок colList в -1 и потом конвертирует все колонки в float для списка колонок в фрейме df
        """

        for colName in colList:
            pass
            df = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(df, colName)
            
            
        return df



    @staticmethod
    def convert_df_columns_by_set_of_lambda_funcs_pandas (df, colsTrg, dicFuncsPars):
        """
        PandasManager
        Конвертирует список заданных колонок в нужный формат за счет заданной последовательности функций-параметров
        colsTrg - список необходимых колонок, по отношению к которым последовательно будут применен последовательный набор лямбда-функций из словаря dicFuncsPars
        
        dicFuncsPars - словарь , где ключем служит название функции, Которая будет применена через лямбда, а значением служит словарь с аргументами и параметрами
        соответствующей в ключе функции. Словарь с аргументами и параметрами ,В свою очередь, содержит:
        valuePars['listLambArgs'] - список названий полей-аргументов фрейма
        valuePars['kwargs'] - **kwargs параметры для функции-лябмда, не связанные с полями фрейма (это могут быть различные настройки, параметры и пр.)
        
        Если в списке аргументов valuePars['listLambArgs']  вместо списка полей, поле ['_selfCol_'], то это означает, что сами колонки из списка колонок -целей  colsTrg
        будет переконвертирована в соотвтетсвии с последовательным набором динамических функций из dicFuncsPars
        
        ПРИМЕР параметров: 
        
        colsTrg = [
            'annual_yield', 
            'yield', 
            'last_annual_yield'
            ]
        dicFuncsPars = {
            'FunctionsGeneralClass.convert_str_with_persent_and_empty_str_to_float' : {
                                                                                        'kwargs': {},
                                                                                        'listLambArgs' : ['_selfCol_']
                                                                                    }
        Category: Фреймы
        """
        from bonds.bonds_main_manager import BondsMainManager
        BondsMainManager.print_IF_DEBUG_bmm("\n-- START ->  ",  {
            'method' : 'convert_df_columns_by_set_of_lambda_funcs_pandas()',
            'module' : 'PandasManager',
            })
        for funcName, valuePars in dicFuncsPars.items():
            
            funcDynParts = funcName.split('.') # Вычисление названий класса в которой находится АИФП и  имени атомарной поисковой функции
            clsName = funcDynParts[0] # названий класса в которой находится АИФП 
            funcDynName = funcDynParts[1] # название атомарной поисковой функции
            classProc = globals()[clsName] # Нахождение класса в глобальных переменных
            oClassProc = classProc()
            funcDynamic = getattr(oClassProc, funcDynName) # Динамическая функция
            listLambArgs = valuePars['listLambArgs']
            kwargs = valuePars['kwargs']
            for colTrg in colsTrg:
                if listLambArgs[0] == '_selfCol_':
                    listLambArgs = [colTrg]
                df = PandasManager.add_or_update_df_col_by_lambda_func_with_args_of_same_df_pandas( df, colTrg, funcDynamic, listLambArgs, **kwargs)
                
        BondsMainManager.print_IF_DEBUG_bmm("-- END ->  ",  {
            'method' : 'convert_df_columns_by_set_of_lambda_funcs_pandas()',
            'module' : 'PandasManager\n',
            })
        return df




    @staticmethod
    def convert_df_cols_to_float_pandas(df, colsToConvertList):
        """
        Конвертировать заданные колоки фрейма в float . Поля могут содержать None и NaN
        Category: Фреймы
        """

        df[colsToConvertList] = df[colsToConvertList].astype(float)
        return df



    ### END Конвертирование данны в колонках / рядах


    # Распечатка информации о фрейме
    
    def print_df_gen_info_pandas_IF_DEBUG(self, df, ifPrintDF = False, dfId = '', srcId = '', colsIndxed = False, getFields = ['*'], printFull = False, marker = ''):
        """
        Вывод общей информации о фрейме и самого фрейма
        ifPrintDF - распечатывать или нет фрейм
        srcId - модуль из которого идет распечатка
        dfId - 
        Category: Фреймы
        """
        # print(marker)
        if DEBUG_:
            
            # Распечатка маркера
            if len(marker)>0:
                print(marker)
            
            if printFull: # ПОлная распечатка фрейма в консоли без сокращений
                pd.set_option('display.max_columns', None)
            
            listDFCols = self.get_df_cols_names_list(df)
            if colsIndxed:
                self.print_indexed_df_cols(df)
            else:
                print (f"PR_NC_160 --> dfCols{dfId} = {listDFCols} {srcId}") # Колонки


            # Slice by columnnames
            if getFields[0] == '*':
                pass
            else:
                self.slice_df_by_cols_names_pandas(df, getFields)

            print(f"PR_NC_161 --> dataFrame_N = {len(df)}")
            if ifPrintDF:
                print(f'PR_NC_162 --> dataFrame = \n{df}' )
                
            
                
    @staticmethod            
    def print_df_gen_info_pandas_IF_DEBUG_static(df, ifPrintDF = False, dfId = '', srcId = '', colsIndxed = False, getFields = ['*'], printFull = False, marker = ''):
        """
        OBSOLETED: use print_df_gen_info_pandas_static_NEW
        PandasManager
        Вывод общей информации о фрейме и самого фрейма
        ifPrintDF - распечатывать или нет фрейм
        srcId - модуль из которого идет распечатка
        dfId - 
        Category: Фреймы
        """
        
        if DEBUG_:
            
            # Распечатка маркера
            if len(marker)>0:
                print(marker)
            
            if printFull: # ПОлная распечатка фрейма в консоли без сокращений
                pd.set_option('display.max_columns', None)
            
            listDFCols = PandasManager.get_df_cols_names_list(df)
            if colsIndxed:
                PandasManager.print_indexed_df_cols(df)
            else:
                print (f"PR_NC_159 --> dfCols{dfId} = {listDFCols} {srcId}") # Колонки


            # Slice by columnnames
            if getFields[0] == '*':
                pass
            else:
                PandasManager.slice_df_by_cols_names_pandas_static(df, getFields)

            print(f"PR_NC_157 --> dataFrame_N = {len(df)}")
            if ifPrintDF:
                print(f'PR_NC_158 --> dataFrame = \n{df}' )
                
                


    # END Распечатка информации о фрейме




    @staticmethod            
    def print_df_gen_info_pandas_static_NEW(df, ifPrintDF = False, dfId = '', srcId = '', colsIndxed = False, getFields = ['*'], printFull = False, marker = ''):
        """
        PandasManager
        Вывод общей информации о фрейме и самого фрейма
        ifPrintDF - распечатывать или нет фрейм
        srcId - модуль из которого идет распечатка
        dfId - 
        Category: Фреймы
        """
        
        if isinstance(df, int):
        
            print(f"{marker}--> Фрейм либо пустой , либо вообще None. df = {df}")
            
        else:
            
            # Распечатка маркера
            if len(marker)>0:
                print(marker)
            
            if printFull: # ПОлная распечатка фрейма в консоли без сокращений
                pd.set_option('display.max_columns', None)
            
            listDFCols = PandasManager.get_df_cols_names_list(df)
            if colsIndxed:
                PandasManager.print_indexed_df_cols(df)
            else:
                print (f"PR_NC_159 --> dfCols{dfId} = {listDFCols} {srcId}") # Колонки


            # Slice by columnnames
            if getFields[0] == '*':
                pass
            else:
                PandasManager.slice_df_by_cols_names_pandas_static(df, getFields)

            print(f"PR_NC_157 --> dataFrame_N = {len(df)}")
            if ifPrintDF:
                print(f'PR_NC_195 --> dataFrame = \n{df}' )
                
            


    # END Распечатка информации о фрейме























# МЕТА-ФУНКЦИИ или функции со структурой фрейма



    @staticmethod
    def index_duplicated_name_columns_in_df (df):
        """
        OBSOLETED: Использовать теперь index_duplicated_name_columns_in_df_universal ()
        PandasManager
        ~ https://stackoverflow.com/questions/39986925/multiple-columns-with-the-same-name-in-pandas
        Индексировать названия колонок в фрейме с одинаковыми названиями, что бы их названия различались. Иначе обработка фрейма будет происходить с глюками, 
        если будут одинаковые названия колонок. 
        ПРИМ: Работает на данный момент только для таких случаях, когда совпадений в названиях колонок могут быть только 2. ТО есть не мжет быть колонок с одинаковым именем 
        более двух. 
        ПРИМ: Первая колонка должна сохранить начальное название, так как по ней могут выполнятся разные функцинальные форматирования, и если
        изменить все названия колонок, то будет ошибка, если эта колонка использовалась в форматировании фрейма при подготовке к выводу на страницу сайта 
        Прим: На выходе вторая колонка будет проименована как column + '_1', а первая не изменит своего названия
        Category: Фреймы
        """
        duplicated_columns_list = []
        list_of_all_columns = list(df.columns)
        for column in list_of_all_columns:
            if list_of_all_columns.count(column) > 1 and not column in duplicated_columns_list:
                duplicated_columns_list.append(column)
                
                
        for column in duplicated_columns_list:
            list_of_all_columns[list_of_all_columns.index(column)] = column + '_2'
            list_of_all_columns[list_of_all_columns.index(column)] = column + '_1'
            list_of_all_columns[list_of_all_columns.index(column + '_2')] = column # Обратно переименовать первую колонку в изначальное название
            
        df.columns = list_of_all_columns
        
        return df



    @staticmethod
    def index_duplicated_name_columns_in_df_universal (df, delimSign = '_'):
        """ 
        Универсальный метод переименования (индексации) одинаковых по названию колонок, независимо от их колличества
        ~ https://stackoverflow.com/questions/24685012/pandas-dataframe-renaming-multiple-identically-named-columns
        delimSign - разделитель между названием колонки и ее индексом по одноименным названиям
        """

        cols=pd.Series(df.columns)

        for dup in cols[cols.duplicated()].unique(): 
            cols[cols[cols == dup].index.values.tolist()] = [dup + delimSign + str(i) if i != 0 else dup for i in range(sum(cols == dup))]

        # rename the columns with the cols list.
        df.columns=cols

        # print(df)
        
        return df






    def slice_df_by_cols_indices_pandas (self, df, indicesList):
        """
        Вырезка из фрейма по списку индексов колонок
        Category: Фреймы
        """
        dfSliced = 	 df.iloc[:,indicesList] 
        return dfSliced


    def slice_df_by_cols_names_pandas (self, df, namesList):
        """
        Вырезка из фрейма по списку названий колонок
        Category: Фреймы
        """
        dfSliced = 	 df.loc[:,namesList] 
        return dfSliced
    
    @staticmethod
    def slice_df_by_cols_names_pandas_static (df, namesList):
        """
        Вырезка из фрейма по списку названий колонок статичный метод
        Category: Фреймы
        """
        dfSliced = 	 df.loc[:,namesList] 
        return dfSliced




    @staticmethod
    def get_indexed_df_cols_pandas(df):
        """
        PandasManager
        Получить индексированные названия колонок фрейма в виде словаря
        Category: Фреймы
        """
        # iterating the columns
        inx_col_dict = {}
        for index,col in enumerate(df.columns):

            inx_col_dict[index] = col

        return inx_col_dict


    @staticmethod
    def print_indexed_df_cols(df):
        """
        PandasManager
        Распечатать индексированные названия колонок
        Category: Фреймы
        """

        inx_col_dict = {}
        for index,col in enumerate(df.columns):

            print(f"{index} {col}")

        return inx_col_dict




    @staticmethod
    def get_indexed_df_cols_dict(df):
        """
        PandasManager
        Получить словарь индексированных названий колонок
        Category: Фреймы
        """

        inx_col_dict = {}
        for index,col in enumerate(df.columns):
            # print(f"{index} {col}")
            inx_col_dict[index] = col
            
        return inx_col_dict



    def print_cols_type(df):
        """
        Распечатать типы колонок фрейма
        Category: Фреймы
        """
        print(df.dtypes)
        return df.dtypes


# END МЕТА-ФУНКЦИИ или функции со структурой фрейма






    #  АГРЕГАТОРЫ
    @staticmethod
    def get_aggregate_by_cols_and_agg_func(df, colslist, strAggFunc):
        """
        PandasManager
        Получить агрегаторы фрейма по задаваемым колонкам и функцией агрегирования
        Category: Фреймы
        """
        res = df[colslist].aggregate(strAggFunc)
        return res





    #  END АГРЕГАТОРЫ



    #  SEARCH EXPRESSIONS 

    @staticmethod
    def search_mask_rows_by_col_val_pandas(df, colName, val):
        """
        NEW: Перенесена из млдуля SqlitePandasProcessor с переводом в статичный метод
        Найти строки в фрейме по значению в поле через query"""
        dfFound = df.loc[df[colName] == val]
        return dfFound




    #  END SEARCH EXPRESSIONS  



    @staticmethod
    def read_df_col_as_list_to_diсtionary_by_col_prime (df, colPrime, colVal, asList = True):
        """ 
        OBSOLETED; устарел по названию. теперь использовать read_df_cols_by_colPrime_as_diсtionary_for_alternative_ties()
        PandasManager
        Считать значения по колонке из фрейма в словарь в виде списка по заданной первичной колонке (если значения по первичной колонке повторяются, то значения в 
        словаре добавлятся как список)
        По аналогии : GROUP BY
        
        colPrime - Название колонки, которая будет являтся ключем в словаре
        colVal - Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
        asList - флаг вывода результатов в виде списка. Если много значений у ключа (если  один-ко-многим , к примеру). Если asList = False, то
        результат выводится не как список, а как значение (для тех случаяев, когда не один-ко-многим, а когда один-к-одному), то есть когда одному значению ключа
        соотвтетсвует только одно значение величины в заданной колонке Y (Y = F(X)  ). 
        По умолчанию метод работает для типа массива один-ко-многим, а asList = True
            
        Типа:
        {
            key1: value1-1,value1-2,value1-3....value100-1
            key2: value2-1,value2-2,value2-3....value100-2
            key3: value3-1,value3-2,value3-2....value100-3
        }
        
        На выходе - словарь, где ключами служат значения по како-то заданной первичной колонке в фрейме, а в его значениях находятся списки со значениями
        по соответствующей колонке colVal фрейма. 
        ПРИМ: Если значения исходной колонки в фрейме повторяются, то словрь по этомк ключу в список добавляется значение по заданнйо колонке
        По аналогии выходит словарь типа  GROUP BY
        
        """
        
        dicRes = {}
                
        for index, row in df.iterrows():
            
            colPrimeKey = row[colPrime]
            
            colValRes = row[colVal]
            
            
            # Дифференциация записи в словарь в зависимлости от флага типа результата asList
            # Для массива данных со связью ключа к искомым данным типа один-ко-многим
            if asList: 
                if colPrimeKey in dicRes:
                    dicRes[colPrimeKey].append(colValRes)
                else:
                    dicRes[colPrimeKey] = [colValRes]
                    
            # Для массива данных со связью ключа к искомым данным типа один-к-одному        
            else: 
                dicRes[colPrimeKey] = colValRes
                    
        return dicRes





    @staticmethod
    def read_df_cols_by_colPrime_as_diсtionary_for_alternative_ties (df, colPrime, colVal, asList = True):
        """ 
        PandasManager
        Считать значения по колонке из фрейма в словарь в виде списка по заданной первичной колонке (если значения по первичной колонке повторяются, то значения в 
        словаре добавлятся как список)
        По аналогии : GROUP BY
        
        colPrime - Название колонки, которая будет являтся ключем в словаре
        colVal - Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
        asList - флаг вывода результатов в виде списка. Если много значений у ключа (если  один-ко-многим , к примеру). Если asList = False, то
        результат выводится не как список, а как значение (для тех случаяев, когда не один-ко-многим, а когда один-к-одному), то есть когда одному значению ключа
        соотвтетсвует только одно значение величины в заданной колонке Y (Y = F(X)  ). 
        По умолчанию метод работает для типа массива один-ко-многим, а asList = True
            

        На выходе - словарь, где ключами служат значения по како-то заданной первичной колонке в фрейме, а в его значениях находятся списки со значениями
        по соответствующей колонке colVal фрейма. СВязь типа многие -ко-многим
                Типа:
        {
            key1: [value1-1,value1-2,value1-3....value100-1]
            key2: [value2-1,value2-2,value2-3....value100-2]
            key3: [value3-1,value3-2,value3-2....value100-3]
        }
        
        для типа один-к-одному при asList = False на выходе словарь типа
        
        {
            key1: value1
            key2: value2
            key3: value3
        }
        
        
        
        ПРИМ: Если значения исходной колонки в фрейме повторяются, то словрь по этомк ключу в список добавляется значение по заданнйо колонке
        По аналогии выходит словарь типа  GROUP BY
        
        """
        
        dicRes = {}
                
        for index, row in df.iterrows():
            
            colPrimeKey = row[colPrime]
            
            colValRes = row[colVal]
            
            
            # Дифференциация записи в словарь в зависимлости от флага типа результата asList
            # Для массива данных со связью ключа к искомым данным типа один-ко-многим
            if asList: 
                if colPrimeKey in dicRes:
                    dicRes[colPrimeKey].append(colValRes)
                else:
                    dicRes[colPrimeKey] = [colValRes]
                    
            # Для массива данных со связью ключа к искомым данным типа один-к-одному        
            else: 
                dicRes[colPrimeKey] = colValRes
                    
        return dicRes
















if __name__ == '__main__':
    pass





    # # ПРОРАБОТКА: Обновление (или создание новой) и наполнение колонки в целевом фрейме на основе колонок-аргументов этого же или другого фрейма с использованием лямбда-функции
    # # update_df_col_by_lambda_function_with_args_from_any_df_pandas()
    # from bonds.bonds_main_manager import BondsMainManager
    # from bonds.settings_date_formats import *
    
    # pm = PandasManager()
    
    # # Pars:
    # bmm = BondsMainManager(DB_BONDS_)

    # df = bmm.read_sql_to_df_pandas(f'SELECT isin, f2 FROM {TB_OFZ_CURRENT_}')
    # colTrg = 'f11'
    # keyFieldsAssoc = {'isin' : 'isin'}
    # lambFunc = FG.convert_date_format_to_another_date_format
    # listLambArgs = ['f2']
    # lambOutArgs ={
    #     'formatSrc' : FORMAT_2_0_,
    #     'formatRes' : FORMAT_2_1_
    #     }
    
    # pm.add_or_update_df_col_by_lambda_func_with_args_of_same_df_pandas(df, colTrg, lambFunc, listLambArgs, **lambOutArgs)
    # bmm.print_df_gen_info_pandas_IF_DEBUG(df,True, colsIndxed = True)

    
    
    
    
    



    # # ПРИМЕР: Сохранение df в эксел-файл Либре
    
    # pm = PandasManager()
    # # pars
    # dirPath = '/home/ak/projects/3_Proj_Bonds_HTML_Center/project_bonds_html/projr/proj_docs'  # полный путь и название файла эксел для вывода данных      
    # fileName = 'bonds_bought_qn' # Название файла    
    
    # # Фрейм приобретенных бондов с общим кол-вом
    # from project_bonds_html.projr.classes.bonds_html_main_manager import BondsHTMLMainManager # Не удалять. локальный импорт тут идет
    # dfBondsBoughtTotalQn = BondsHTMLMainManager.get_bonds_qn_bought_grouped_by_isin_df(['isin','bond_name'],'isin','SUM(qn)')
    
    # pm.save_df_to_excel_file (dfBondsBoughtTotalQn, dirPath, fileName, True)
    
    


    # # ПРИМЕР: Проработка поиска -фиьтрации в фрейме по множественным условиям

    # # sqlSintaxer = SQLSyntaxer()

    # #Pars:
    # # conds = {'ONE' : ['ГКД', '>', '10']}

    # conds = {'_ampers_' : [['ГКД', '>', '5'], ['ГКД', '<', '10']]}

    # queryStr = ''

    # condQuery = SQLSyntaxer._get_where_clause_sql(conds).replace('_ampers_', '&')

    # print (f"condQuery = {condQuery}")










    # ПРОРАБОТКА:  функции filter_df_by_regex
    
    # db_panda_proc = SqlitePandasProcessor(DB_BONDS_)

    # # db_panda_proc = SqlitePandasProcessor(DB_BONDS_)
    # # pMangr = PandasManager()

    # # # ПРИМЕР: Проработка функции filter_df_by_multiple_cols_vals

    # dfOkpoInnComps = AlgorithmsSubParts.a022_1_() 
    # dfTbGlobalAInnCleared = AlgorithmsSubParts.a022_8_() 
    # # print (f"dfBondsCurrInnOkpoFromCompsNotSet = {dfTbGlobalAInnCleared}")       
    # print (f"dfBondsCurrInnOkpoFromCompsNotSet = {len(dfTbGlobalAInnCleared)}") 

    # baseDF = dfOkpoInnComps
    # compairDF = dfTbGlobalAInnCleared


    # db_panda_proc = SqlitePandasProcessor(DB_BONDS_)
    # assocColsInxDic = {'inn':'x_str'}
    # getCols = 'inn' # набор колонок из базового фрейма для результирующего массива 
    # # dfNewInn = db_panda_proc.get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas(baseDF, compairDF, assocColsInxDic, getCols )
    # # print (f"dfNewInn = {dfNewInn} / (AlgorithmsSubParts.a022_9_)")
    # # return dfNewInn


    # qrOper = 'not in' # Оператор сравнения 'не равно', то есть ищутся неравные задаваемым величинам значения в колонках
    # logicOper = '&' # Логический оператор AND, для обьединения в логическое И всех частных выражений в query
    # # Формирование именных параметров, которые включают в себя именные списки с выборками-векторами по заданным колонкам в комплексном или простом индексе
    # #  входного параметра assocColsInxDic из сравниельного фрейма compairDF
    # print(f"baseDF = {baseDF}/ (SqlitePandasProcessor.get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas)")
    # print(f"compairDF = {compairDF}/ (SqlitePandasProcessor.get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas)")
    
    # kwargs = {} # словарь для именных параметров для функции филльтрации
    # for key, val in assocColsInxDic.items(): # цикл по колонкам в составном индексе колонок assocColsInxDic
    #     colValsList = db_panda_proc.convert_df_col_to_list(compairDF, val) # получение колокнки-ветора с названием текущего по циклу val во фрейме compairDF в виде простого списка значений (эти значения из списка будут отсеиваться в базовом фрейме по соответствующей колонке с названием текущего ключа key)
    #     kwargs[key] = colValsList # вставка текущего по циклу именного параметра в словрь kwargs

    # dfBaseFiltered = db_panda_proc.filter_df_by_multiple_cols_vals(baseDF, qrOper, logicOper, **kwargs)  #  Базовый фрейм, отфильтрованный по значениям колонок из compairDF совокупного индекса колонок

    # print(f"dfBaseFiltered = {dfBaseFiltered} / (SqlitePandasProcessor.get_baseDF_rows_not_existing_in_compairedDF_by_key_colmns_index_pandas)")

    # if getCols == '*': # То выводятся все колонки
    #     df =  dfBaseFiltered
    # else:
    #     df =  dfBaseFiltered[[getCols]] # Иначе вводятся запрашиваемые в списке getCols колонки


    # print (f"df = {df} / PandasManager.filter_df_by_multiple_cols_vals")
    # query_list = []
    # for key, value in kwargs.items():
    #     if value is not None:
    #         query_list.append(f"{key} {qrOper} @kwargs['{str(key)}']")
    # query = f' {logicOper} '.join(query_list)
    # print(f"query = {query}") # не удалять !!
    # print(f"kwargs = {kwargs}")
    # print(f"colsNames = {list(df)}")
    









    # # ПРИМЕР: Проработка получения dFrame с сортировкой

    # # Массив текущих облигаций из таблицы bonds_current BD = /home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/bonds.db
    # bondsMngr = BondsManagerHTML() # При этом в файле func_general.py в проекте bonds были заблокированы употребление библиотеки pyautogui (почему то не видит ее отсюда)
    # dsBondsCurr = bondsMngr.get_bonds_current () # Массив облигаций с полями в соответствии с таблицей bonds_current    

    # # Получить Pandas dataFrame
    # pandMangr = PandasManager()
    # tbBondsCurr = 'bonds_current'
    # tbFields = bondsMngr.get_tb_fields(tbBondsCurr) # Получение спсика полей таблицы bonds_current
    # dfBonds = pandMangr.get_pandas_data_frame(dsBondsCurr, tbFields)  # dataFrame      


    # ## Параметры сортировки 
    # # desc = request.args.get('desc') # Получение значения флага сортировки по заданному полю
    # # sort = request.args.get('sort') # Получение значения флага сортировки по заданному полю

    # desc = '0'
    # sort = '1'

    # # Словарь  выбора sortFlag в зависимости от поступающей переменной desc, Если не установлен sort = 1.
    # #  Служит для присваивания порядка сортировки, если не было смены порядка при нажатии на заголовок
    # sortFlagByDescDict = { 
    #     '1' : True,
    #     '0' : False,
    #     'None' : True,
    #     None : True
    # }

    # if sort == '1': # Если флаг сортировки  = 1, то запускаем бинарное переключение порядка сортировки. Если  = 0, то не запускаем и порядок сортировки остается такм же, как был
    #     # Бинарное переключение переменной в зависимости от собственного ее значения
    #     biRes = LGF.binary_switch_str_var(desc) # Бинарный переключатель задаваемой бинарной переменной
    #     desc = biRes[0] # бинарное значение переменной
    #     sortFlag = biRes [1]
    # else: # Если  = 0, то не запускаем и порядок сортировки остается такм же, как был
    #     sortFlag = sortFlagByDescDict[desc]

    # # Передаваемое из сайта значение индекса сортируемой колонки
    # # sortCol = request.args.get('sortcol') 
    # sortCol = 4

    # print(f" sortCol = {sortCol}")
    # if sortCol =='' or sortCol == None:
    #     sortCol = 1
    # ## END Параметры сортировки 


    # # Сортировка в зависимости от поступающего параметра  desc <1,0> и названия колонки в параметре col
    # # Pars:
    # sortColName = tbFields[int(sortCol)] # Название поля по которому происводится сортировка. Соотвтествует по номеру индексу в названии полей в таблице bonds_current
    # dfSorted = pandMangr.sort_df_by_col_name(dfBonds, sortColName, ASC = sortFlag, na_position = 'first')    






    # # # ПРИМЕР: Сортировка массива облигаций по колонкам через dataFrame Pandas
    # pandMangr = PandasManager()
    # bondsMngr = BondsManagerHTML() # При этом в файле func_general.py в проекте bonds были заблокированы употребление библиотеки pyautogui (почему то не видит ее отсюда)
    # dsBondsCurr = bondsMngr.get_bonds_current () # Массив облигаций с полями в соответствии с таблицей bonds_current

    # # # Получение спсика полей таблицы bonds_current
    # tbBondsCurr = 'bonds_current'
    # tbFields = bondsMngr.get_tb_fields(tbBondsCurr)

    # df = pandMangr.get_pandas_data_frame(dsBondsCurr, tbFields)

    # # Pars:
    # colName = 'inn_ref'

    # dfSorted = pandMangr.sort_df_by_col_name(df, colName, ASC = True, na_position = 'first')

    # dfSortedSize = dfSorted.size
    # print(dfSortedSize)
