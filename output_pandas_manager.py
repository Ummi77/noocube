
from noocube.sqlite_pandas_processor import SqlitePandasProcessor
# from project_bonds_html.projr.classes.pseudo_request import PseudoRequest
# from project_bonds_html.projr.classes.sys_algorithms_ import SysAlgorithms
import noocube.funcs_general as FG
from noocube.pandas_manager import PandasManager
from noocube.settings import *
from noocube.paginator_data_frame import PaginatorWithDataFrame
from noocube.bonds_main_manager import  BondsMainManager
from noocube.exceptions import *

class OutputPandasManager (PandasManager): 
    """ЗАГОТОВКА. Вывод визуальной информации в разных средах с применением PANDAS data frames
    !!! Пока не удалять родительсуий класс. Метод get_df_sorted_pandas () 
    """



    def __init__(self):
        pass





    def convert_assoc_dic_from_indices_to_name_based_pandas(self, df, outputColindicesAccordDic):
        """
        OutputPandasManager
        Конвертировать словарь соответствий , основанный на индексах колонок в фрейме и их новыми названиями в словарь , основанный на именах колонок и новых названий
        Category: Фреймы
        """
        BondsMainManager.print_IF_DEBUG_bmm("\n-------- START PR_NC_121 ->  ",  {
            'method' : 'convert_assoc_dic_from_indices_to_name_based_pandas()',
            'module' : 'OutputPandasManager',
            })
        
        dfColsNames = list(df) # список названий колонок из фрейма
        # print (f"PR_110 dfColsNames = {dfColsNames}")
        changeIndices = list(outputColindicesAccordDic.keys()) # список индексов колонок фрейма, которые надо переименовать
        # print (f"PR_111 changeIndices = {changeIndices}")
        newColsNames = list(outputColindicesAccordDic.values()) # список индексов колонок фрейма, которые надо переименовать
        #print (f"PR_112 newColsNames = {newColsNames}")
        
        # print(f"dfColsNames.__getitem__ = {list(map(dfColsNames.__getitem__, changeIndices))}")
        
        try: 
            prevColsNames = list(map(dfColsNames.__getitem__, changeIndices))
        except Exception as err:
            raise  exception_factory(AssocDicConversionIndicesToNamesAssocDic, "Ошибка в convert_assoc_dic_from_indices_to_name_based_pandas() / OutputPandasManager/ output_pandas_manager.py")
                
        # print (f"prevColsNames = {prevColsNames}")
        outputColNamesAccordDic = FG.convert_two_lists_to_dictionary(prevColsNames,newColsNames)
        
        BondsMainManager.print_IF_DEBUG_bmm("-------- END PR_NC_122 ->  ",  {
            'method' : 'convert_assoc_dic_from_indices_to_name_based_pandas()',
            'module' : 'OutputPandasManager\n',
            })
        return outputColNamesAccordDic



    def format_df_according_final_output_table_pandas (self, df, outputColAccordDic):
        """
        OutputPandasManager 
        Индексы колонок и их соответствий НЕ должны быть расположены по возрастанию <Еще раз проверить. Порядок индексов колонок меняет и структуру фрейма !!!>
        Переформатировать входной сырой общТрансформий фрейм с данными в структуру эквивалентную необходимой структуре выводимой в конечном итоге таблицы (например в конечной таблице на 
        странице HTML сайта. Но могут быть и другие варианты. Например, в экселе или ворде)
        А именно, переименовать названия столбцов и усеч кол-во столбцов ровно таких, какие необходимы для выводимой Output - таблице
        (в том случае, если кол-во выводимых столбцов Output-таблицы меньше, чем в исходном сыром массиве с данными)
        outputColAccordDic - словарь соотвтетствий между индексами колонок во входном фрейме и названиями всех колонок в выводимой конечной таблице Output
        Category: Фреймы
        """
        
        BondsMainManager.print_IF_DEBUG_bmm("\n-------- START PR_NC_119 ->  ",  {
            'method' : 'format_df_according_final_output_table_pandas()',
            'module' : 'OutputPandasManager',
            })
        
        # print(f"222@@@@@@@@@@@@@@@@@@@@22 outputColAccordDic = {outputColAccordDic}")
        
        # Конвертируем словарь соотвтетсвий , основанный на индексах колонок, в словарь соответствий, основанный на именах колонок фрейма
        outputColNamesAccordDic = self.convert_assoc_dic_from_indices_to_name_based_pandas(df, outputColAccordDic)
        colsIndicesToLeave = list(outputColAccordDic.keys()) # Индексы колонок фрейма, которые надо оставить в результате усечения
    
        # Вырезка из врейма по индексам колонок 
        dfSliced = self.slice_df_by_cols_indices_pandas (df, colsIndicesToLeave)

        # Переименование колонок в соответсвии со списком названий колонок для переименования (vals in outputColAccordDic)
        # <!!! индексы колонок и их соответствий должны быть расположены по возрастанию !!!>
        # outputColAccordDicSorted = sorted(outputColAccordDic.items()) # Пока не удалять !!!
        # dfSlicedRenamed =self.rename_columns_by_lebel_list(dfSliced, colsNewNames)
        dfSlicedRenamed =self.rename_cols_by_associate_dic_pandas(dfSliced, outputColNamesAccordDic)

        # if DEBUG_:
        #     print(f"dfSlicedRenamed = \n{dfSlicedRenamed} / OutputPandasManager.format_df_according_final_output_table_pandas")
        
        BondsMainManager.print_IF_DEBUG_bmm("-------- END PR_NC_120 ->  ",  {
            'method' : 'format_df_according_final_output_table_pandas()',
            'module' : 'OutputPandasManager\n',
            })
        
        return dfSlicedRenamed





    def prepare_df_output_with_paginator_panadas(self, df, outputColsAssocDic, paginSets, pgToActvate, sort = 0, sortCol = '', flagASC = True):
        """
        OutputPandasManager
        Подготовка фрейма к выводу вовнешнее поле
        outputColsAssocDic - словарь соотвтествий индексов колонок в фрейме и названий колонок в таблицы для вывода (выводятся только эти колонки из фрейма с титульными названиями)
                            #TODO: Переделать.Возможно избыточная информация, так как это все может хранится в самом фрейму уже!!!???
        sortCol - индекс колонки для сортировки, если задана. По умолчанию сортировки нет
        paginSets - Настройки пагинатора 
        pgToActvate - страница для создания постраничной выборки из отсотрированного фрейма для вывода наружу
        Category: Фреймы
        """

        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&") # для выделения в терминале для визуального обнаружения лога
        print (f"sortCol = {sortCol} / OutputPandasManager.prepare_df_output_with_paginator_panadas()")

        # НАстройка списка колонок к выводу на странице 
        outputColsAssocDic = {   
                4 : 'Название', # Поле 'bond_name'
                1 : 'ISIN', # 'isin'   
                2 : 'ИНН', # 'inn_ref'
                10 : 'ГКД' ,
                11 : 'Последний ГКД' ,        
                12 : 'Тек.цена',
                14 : 'Купон',
                15 : 'Частота' ,                           
                20 : 'Квалиф.' 
                } 

        # ## Входные Параметры сортировки , которые необходимо передать в HTML-шаблон для настройки ссылок пагинатора и заголовков таблицы облигаций
        # Сортировка в зависимости от поступающего параметров в request :   desc - Получение значения флага сортировки по заданному полю, 
        # desc = flagASC # Получение значения порадка сортировки в запрашиваемом с сайта значении
        # sort = True # Временно параметр фиксируется тут. Но должен передаваться в параметрах для метода
        sortParams = {}
        sortParams ['desc'] = flagASC # Получение значения флага сортировки по заданному полю
        sortParams ['sort'] = sort # Получение значения флага нужна сортировка вообще или нет
        sortParams ['sortCol'] = sortCol # Индекс колонки для сортировки (пока одна колонка для тестирования)

        if DEBUG_:
            print (f"sortCol = {sortCol} / OutputPandasManager.prepare_df_output_with_paginator_panadas  <output_pandas_manager.py>")

        sortColsList = outputColsAssocDic[sortCol] # Название колонки для сортирвки в виде спсика с одним элементом (пока один, для тестирвоаняи)
        dfSorted, desc, sortCol = self.get_df_sorted_with_switch_sort_dir_pandas(df, sortColsList, sortParams)

        # Текущий общий пагинатор на основе настроек в settings.py PAGIN_BONDS_CURR_SET_
        paginatorGen = PaginatorWithDataFrame(dfSorted, paginSets) # инициализация общего пагинатора на основе общих настроек PAGIN_BONDS_CURR_SET_ и входного массива dfSorted
        # Получение текущего пагинатора из общего, через получение параметров активации: страницы к активации и блока
        currPaginator = PaginatorWithDataFrame.get_curr_paginator_from_gen (paginatorGen,  pgToActvate)
        dfLimitByPg = currPaginator.dfLimByPgNumb # Вырезка из общего dFrame на основе заданной странице к активации

        # Возврат  результатов в словаре
        resDic = {}
        resDic['colsTitlesDic'] = outputColsAssocDic
        resDic['dfLimitByPg'] = dfLimitByPg # # Вырезка из общего dFrame на основе заданной странице к активации
        resDic['sortCol'] = sortCol# Колонка сортировки, в запрашиваем с сайта значении по заголовку колонки таблицы 
        resDic['desc'] = desc# Значение флага сортировки по заданному полю
        resDic['currPaginator'] = currPaginator # Пагинатор с текущим состоянием
        
        return resDic # Словарь с набором высех необходимых данных для формирования HTML таблицы









    #### HTML Output








    #### END HTML Output    


# if __name__ == '__main__':
#     pass


#     # ПРИМЕР: Прорпботка функции convert_index_assoc_dic_to_old__new_names_dic_pandas()

#     srchStr = "ювелир*"
#     ftsInterpretor = 'FTS' # тип поиска

    
#         # Создание и настройка pseudo-request object (PRO) для тестирования тех алгоритмов, где используются атрибуты возвратных параметров с сервера сайта
#     request = PseudoRequest() # Обьек псевдо-request для теста
#     request['desc'] = '1'  # Установка флага сортировки фрейма с данными
#     request['sortCol'] = 10 # Установка колонки сортировки
#     request['sort'] = '1' # Установка флага сортировки
#     request['pg'] = 1 # Установка страницы пагинатора

#     # Словарь соотвтествий между названиями в выводимой таблице и колонкми фрейма, содержащего результаты по полнотекстовому поиску облигаций, чьи эмитенты 
#     # удовлетворяют заданным критериям поиска
#     outputColsAssocDic = COLS_ASSOC_FOR_BONDS_TYPE01_
    
#     request ['outputColsAssocDic'] = outputColsAssocDic # словарь соотвтетсвий индексов колонок в фрейме и назаний колонок в выводимой в HTML таблице

#     resDic = SysAlgorithms.a__002_search_comps_data_from_virtual_comps_sescr_tb (request, srchStr, ftsInterpretor)











