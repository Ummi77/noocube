

# from bonds.lo_calc_pandas_db import LibreCalcPandasDB
# from noocube.bonds_main_manager import BondsMainManager
from pandas import DataFrame
from noocube.pandas_manager import PandasManager
from noocube.output_pandas_manager import OutputPandasManager
# from noocube.paginator_data_frame import PaginatorWithDataFrame
from noocube.settings import *
from noocube.df_fields_calc_funcs import DataFrameFieldsCalcFuncs
from noocube.paginator_data_frame_cube_v2 import PaginatorWithDataFrame
import time
from noocube.funcs_general_class import FunctionsGeneralClass
from noocube.settings import *
import inspect
from noocube.dataframe_filter_manager import DataFrameFilterManager
from noocube.switch import Switch
from noocube.bonds_main_manager import BondsMainManager


# TODO: Продумать систему наследования этого класса и родителей. Так как в программирвоании с БД и пандой нужны не только конечные обьекты дял вывода таблиц на конечных ресурсах,
#  но и подобные обьекты вообще, до вывода на конечный ресурс ??
# TODO: Использовать функционал из view_table_cube.py  для формирования источника данных из разных типов источников??
class DSourceOutputCube ():
    """
    Класс для организации вывода таблицы из подготовленного фрейма  на любой внешний  рессурс (HTML, Excel и т.д.) 
    В нем фрейм подвергается пагинации, подготовки необходимого набора колонок, соотвтетвующий конечной таблице для вывода на внешний ресурс и оформление необходимых заголовков для 
    колонок этой таблицы. А так же осуществляется вставка или апдейт расчетных колонок. Так же осуществляется филььрация по заданным формулам фильтрации
    
    assocTitles = {dfColIndx : tbOutputTitle} - словарь соотвтетсвий индексов колонок во входном фрейме и соотвтетсвующих им названий колонок для конечной таблицы на внешнем ресурсе, которая будет
    строится из подготовленного фрейма в self.dfOutput
    ФОРМИРУЕТ ДОБАВОЧНЫЕ РАСЧЕТНЫЕ КОЛОНКИ!!! add_calculated_cols_() на основе задаваемого слова    # paginatorParams['pgToActivate'] = request.args.get('pg')
    ря соотвтетсвий названий колонок с их индексом и название специализированной функции,
    которая добавляет в фрейм расчетную колонку
    """        

    def __init__(self, dfInput : DataFrame, activate = True, **kwargs):

        
        print(f"--START PR_392 --> : DSourceOutputCube.__init__() | noocube/dsource_output_cube_v2.py")
        
        # A. ----------------- ##### НОВЫЙ ПОДХОД v2 - 
        
        self.dfInput = dfInput # Всегда оригинальный массив
        
        # Процессинговый фрейм (над которым выполняются все опреации и который выходит в результате обработки) Вначале оригинальный массив, а затем массив претерпевающий 
        # все необходимые процедуры. В результате он же является конечным
        self.df = dfInput 
        
        # self.kwargs = kwargs
        
        # Названия колонок. Если заданы, то присвиваются из словаря. Если не заданы, то остаются равные названиям колонок из источника
        if 'assocTitles' in kwargs:
            self.assocTitlesCell = kwargs['assocTitles']
        else:
            self.assocTitlesCell = {}
        
        # Настройки пагинации. 
        # 'pagesRowMax' : максимальное число показа нумерации страниц в ряду
        # 'dsRowsQnOnPage' : число записей из входного массива, показываемых на одной странице  
        if 'paginGenSet' in kwargs:
            self.paginGenSetCell = kwargs['paginGenSet']
        else:
            self.paginGenSetCell = {}
            
            
        # Матрица аргументов для ссылок на странице HTML при сортировке по заголовкам колонок таблицы
        if 'urlsArgsMatrix' in kwargs:
            self.urlsArgsMatrix = kwargs['urlsArgsMatrix']
            
            if 'pg' not in self.urlsArgsMatrix:
                self.urlsArgsMatrix['pg'] = 1
            if 'sort_col_name' not in self.urlsArgsMatrix:
                self.urlsArgsMatrix['sort_col_name'] = ''
            if 'sort_col' not in self.urlsArgsMatrix:
                self.urlsArgsMatrix['sort_col'] = 0
            if 'sort_asc' not in self.urlsArgsMatrix:
                self.urlsArgsMatrix['sort_asc'] = 1
            if 'sort_flag' not in self.urlsArgsMatrix:
                self.urlsArgsMatrix['sort_flag'] = True
                
        else:
            self.urlsArgsMatrix = {
                'pg' : 1,
                'sort_col' : 0,
                'sort_asc' : 1,
                'filts_inps' : '',
                'sort_flag' : True,
                'sort_col_name' : '',
            }
            
            
        # Словарь с формулами фильтров для разных фильтров на заданнйо странице сайта (или другими словами - для заданного View)
        if 'viewFilterFormulas' in kwargs:
            self.viewFilterFormulas = kwargs['viewFilterFormulas']
        else:
            self.viewFilterFormulas = {}
            

        # Шаблон пагинатора по системе CUBE
        # TODO: Переделать пагинатор. Сделть не по шаблону, а что бы формировался только в одном месте и что бы его можно было отправлять через AJAX (как сейчас в 
        # классе DsTableOutputCube | ~ noocube/ds_table_output_cube_v2.py)
        if 'paginHTMLTemplate' in kwargs:
            self.paginHTMLTemplate = kwargs['paginHTMLTemplate'].strip()
        else:
            self.paginHTMLTemplate = ''
        
        
        
        # Флаг включения обновления колонок в методе reproccessByRequest, при необходимости использования этого метода. В self.activate() тайтлы и 
        # калькулируемые обрабатываюются автоматом
        if 'updateTitles' in kwargs:
            self.updateTitles = kwargs['updateTitles']
        else:
            self.updateTitles = False
        
        
        
        
        # Выходной постраничный активный массив обработанных данных, соотвтетсвующий активной страницы пагинатора self.pgCell
        self.dfActivePageFrameCell = None
        
        # Пагинатор
        self.paginator = None
        
        
        # Активация обьекта. Запуск методов процессинга над массивом данных в self.dfInput
        if activate:
            self.activate()
        # else:
        #     self.reproccessByRequest()
            
        # ДЛЯ РАСПЕЧАТОК В ЛОГАХ



    @staticmethod
    def get_dsoc_obj_from_df_static (dfInput : DataFrame, activate = True, **kwargs):
        """
        Получение обьекта dsoc из фрейма из статичного метода (пока этот метод нужен для тестов декораторов сортировки, фильтрации и т.д.)
        Category: Фреймы
        """
        
        dsocObj = DSourceOutputCube(dfInput, activate, **kwargs)
        return dsocObj
        
        
        


    ## СЛУЖЕБНЫЕ


    @staticmethod
    def _print_mark(id, func, mark, markVal, prefix):
        """
        DSourceOutputCube
        Вспомогательыня функция для распечатки принт-маркеров
        ПРИМ: Что бы использовать эту вспомогательныую функцию необходимо добвать ее в кажый класс и заменить константные значения className и file на соотвтетсвующие этому классу
        Category: Распечатки
        """
        
        FunctionsGeneralClass.print_any_mark_by_id(
            PRINT_TERMINAL_START_END_FUNCTIONS_,
            id,
            func = func,
            mark = mark,
            markVal = markVal,
            className = 'DSourceOutputCube',
            calssFile = 'noocube/dsource_output_cube_v2.py',
            prefix = prefix
        )
        
        
        
        
        
        
    ## END СЛУЖЕБНЫЕ





    def activate (self):
        """
        активировать настройки обьекта, если они были заданы напрямую (не через **kwargs) в уже существующем обьекте. То есть
        без использования конструктора класса
        Category: Вспомогательные
        """
        
        print(f"---- START PR_393 --> : activate() | noocube/dsource_output_cube_v2.py")
        
        # F. Добавить или обновить расчетные коллонки в фрейме после их переименования в соотвтетсвии со словарем self.assocTitlesCell
        self.add_update_calc_columns()
        # G. Сортировка массива по заданнйо колонке и направлению
        self.sort_df()
        # L. Фильтрация по возможным фильтрационным выражениям, пришедшим со страниы сайта в виде возвратного request
        self.filter_df()
        # F. Пагинация готового массива
        self.pagin_df()
        
        print(f"---- END PR_394 --> : activate() | noocube/dsource_output_cube_v2.py")


    def add_update_calc_columns (self):
        """
        Добавить или обновить расчетные колонки
        Category: Калькуляторы полей
        """
        
        # D. Проработка названий колонок и расчетных добавочных колонок
        # Разделение словаря на словарь обычных origColsAssocTitles_ названий и на словарь с расчетными полями calcColsAssocTitles_
        origColsAssocTitles_, calcColsAssocTitles_ = DSourceOutputCube.diffirenciate_orig_and_calc_columns_static_(self.assocTitlesCell)
        # E. Проработать массив данных на предмет названий колонок на базе assocTitles и вырезания из оригинального фрейма тех колонок, Которые заданы в assocTitles
        self.df = DSourceOutputCube.prepare_to_output_static(self.df, origColsAssocTitles_)
        fkwargs = {}
        self.df = DSourceOutputCube.add_update_calculated_cols_static_v2_(self.df, calcColsAssocTitles_, **fkwargs)


    def sort_df(self):
        """
        Сортировать фрейм
        Category: Фреймы
        """
        # print(f"^^^^^^^^^^^^^ &&&&&&&&&& urlsArgsMatrix = {self.urlsArgsMatrix}")
        
        # TODO: Сделать сортировку по двум полям , как минимум !!!
        if len(self.urlsArgsMatrix)>0 and 'sort_flag' in self.urlsArgsMatrix:  
            # print(f"$$$$$$$$$$$ ^^^^^^^^^^^^^ &&&&&&&&&& urlsArgsMatrix = {self.urlsArgsMatrix}")
            # Если задано название колонки сортировки, то сортирует по названию колонки. Иначе - по индексу (если флаг сортировки self.sortFlag = True)
            if len(self.urlsArgsMatrix['sort_col_name']) > 0:
                self.df = DSourceOutputCube.sort_by_name_static(self.df, self.urlsArgsMatrix['sort_col_name'], bool(self.urlsArgsMatrix['sort_asc']))
            else :
                self.df = DSourceOutputCube.sort_by_index_static(self.df, int(self.urlsArgsMatrix['sort_col']), bool(int(self.urlsArgsMatrix['sort_asc'])))
                


    def filter_df(self):
        """
        Фильтровать фрейм
        Category: Фильтрация
        """
        
        print(f"---- START PR_395 --> : filter_df() | DSourceOutputCube")
        
        if len(self.viewFilterFormulas) > 0 and len(self.urlsArgsMatrix)>0 and  'filts_inps' in self.urlsArgsMatrix and len(self.urlsArgsMatrix['filts_inps']) > 0: 
            # Распарсить входную строку с заданынми мульти-фильтрами , приходящими из request с сайта в url-аргументе 'filts_inps'
            # Составить словарь параметров со значениями аргументов фильтров со страницы сайта (фрагменты текстовые, по содержанию которых в колонках фильтруется фрейм)
            # pars:
            genDelim = ','
            dicDelim = ':'
            dicFiltersFormulasVals = FunctionsGeneralClass.read_split_parts_with_dic_delimetr_to_dic(self.urlsArgsMatrix['filts_inps'], genDelim, dicDelim)
            # Подготовить фрейм с фильтрами dfFilters , которые будут примененыв к операционному фрейму
            dfFilters = DataFrameFilterManager.prepare_multi_filter_df_by_filter_formulas_dic_and_filter_vals_dic_fm (self.viewFilterFormulas, dicFiltersFormulasVals)
            # ФИЛЬТРАЦИЯ процедурного фрейма self.df по мульти-фильтрам из dfFilters
            self.df = DataFrameFilterManager.filter_df_by_multi_formulas_df_static_fm (self.df, dfFilters)
            
            

        
        
        
        
            
            
    def pagin_df(self):
        """
        Пагинация фрейма
        Category: Пагинация
        """
        
        if  len(self.df) > 0:
            self.paginator = PaginatorWithDataFrame(self.df, self.paginGenSetCell) # инициализация обьекта пагинатора в общей форме
            self.paginator = PaginatorWithDataFrame.get_curr_paginator_from_gen(self.paginator,  self.urlsArgsMatrix['pg']) 
            # Выходной постраничный активный массив обработанных данных, соотвтетсвующий активной страницы пагинатора self.pgCell
            self.dfActivePageFrameCell = self.paginator.dfLimByPgNumb
        else:
            self.paginator = -1
            self.dfActivePageFrameCell = -1



    
    def reproccessByRequest(self):
        """Обработать массив данных на основе нового возврата request с сервера
        Метод включается, когда фрейм готиовый достается из сессии и в нем уже не нужно делать переименование колонок и расчет колонок, то есть 
        не нужен метод self.add_update_calc_columns(), котоырй есть в activate()
        Если self.titlesCalcks = True, который передается через **kwargs, то в фреймей будут переименованы заголовки и добавлены или обновлены расчетные колонки по словарю self.assocTitlesCell
        Category: Вспомогательные
        """
        
        
        
        print(f"-- START PR_396 --> : reproccessByRequest() | DSourceOutputCube")
        
        if self.updateTitles :
            # F. Добавить или обновить расчетные коллонки в фрейме после их переименования в соотвтетсвии со словарем self.assocTitlesCell
            self.add_update_calc_columns()

        # G. Сортировка массива по заданнйо колонке и направлению
        self.sort_df()
        # L. Фильтрация по возможным фильтрационным выражениям, пришедшим со страниы сайта в виде возвратного request
        self.filter_df()
        # F. Пагинация готового массива
        self.pagin_df()
        
        print(f"-- END PR_397 --> : reproccessByRequest() | DSourceOutputCube")

        



        
    @staticmethod
    def sort_by_index_static(df, sortColInx, ascTrue = 1):
        """ 
        DSourceOutputCube +
        Для сортировки фрейма @@@ self.outputDf  по индексу колонки в конечном , выходном фрейме
        Уже должны быть значения В собственных переменных:
        sortColInx - индекс колонки, по которой необходимо провести сортировку
        ascTrue - Направление сортировки False или True. По умолчанию ascending=True
        Category: Фреймы
        """
        print(f"START PR_398 --> : sort_by_index()")
        # self.print_sort_params_()
        pandProc = PandasManager()
        df = pandProc.get_df_sorted_by_col_index(df, sortColInx, bool(ascTrue))
        print(f"START PR_399 --> : sort_by_index()")
        return df



    @staticmethod
    def sort_by_name_static(df, sortColName, ascTrue = True):
        """ 
        DSourceOutputCube +
        Для сортировки фрейма @@@ self.outputDf по названию колонки в конечном , выходном фрейме
        Уже должны быть значения В собственных переменных:src
        sortColName - название колонки, по которой необходимо провести сортировку
        ascTrue - Направление сортировки False или True. По умолчанию ascending=True
        Category: Фреймы
        """
        # print(f"START: sort_by_name()")
        # self.print_sort_params_()
        pandProc = PandasManager()
        df = pandProc.get_df_sorted_by_col_name_v02(df, sortColName, ascTrue)
        return df
        
        



    @staticmethod
    def prepare_to_output_static(df, assocTitles):
        """
        DSourceOutputCube +
        Подготавливает источник данных dataSrc в виде фрейма (если он был задан другими типами данных, нежели входной фрейм) на основе создания обьекта
        класса DSourceCube или DSearchCube и оттуда уже берет конечный фрейм для вывода (присваивает этот фрейм в собственную переменную self.outputDf ) на внешний ресурс в том виде, 
        в котором это необходимо (в частности в виде таблицы на странице HTML)
        Аббревиатура 'dfds' - dataFrame на основе входного dataSet  
        Category: Вспомогательные
        """

        outPandaMngr = OutputPandasManager()
        # Подготовить конечный фрейм @@@ self.dfOutput
        if len(assocTitles) > 0: # Если заданы колонки для преобразования входного массива , то форматируем фрейм
            df = outPandaMngr.format_df_according_final_output_table_pandas(df, assocTitles)
        else: # Иначе выходной фрейм не форматируется и приравнивается входному
            df = df
            
        return df





    def filter_frame_by_conds_dic(self, filterCondsDic):
        """
        Метод писка - фильтрации фреймов
        Результирующий отфильтрованный фрейм записывается в конечный self.dfOutput , который был сформирован в результате метода в конструкторе prepare_to_output ()
        filterCondsDic - словарь услвоий как для SQL
        !!! Перед фильтрацией по числовым колонкам с использованием в условиях чисовых значений для сравнения или поиска - провести их чистку , если в таблице или входном массиве
        они были выражены стрингами или смеью стрингов и числовых. Поэтому метод фильтрации вынесен из конструктора и делается вручную, после проверки на очистку колонок в условиях
        И присваиваем параметры, значит, тоже врус=чную перед фиьтрованием
        Перед фильтрацией форматируем колонку colName из стринга в флоат с очисткой от ненужных символов строковых функцией :
        PandasManager.convert_str_empty_with_persent_and_empty_str_to_float ()
        Category: Фильтрация
        """
        pandProc = PandasManager()
        # Фильтрует в том случае, если параметры фильтрации заданы конкретно, а не просто задана сама переменная типа {}. В ином случае выходной массив self.dfOutput остается нетронутым
        if len(filterCondsDic) > 0: 
            self.dfOutput = pandProc.filter_frame_by_multiple_conds_sintaxer (self.dfOutput, filterCondsDic)
            # @@@ Qn
            self.qn = len(self.dfOutput)




    def filter_frame_by_query_expr_(self, filtQuery):
        """
        Фильтрация текущего фрейма через query-выражение
        Category: Фильтрация
        """
        # Фильтрует в том случае, если параметры фильтрации заданы конкретно, а не просто задана сама переменная типа {}. В ином случае выходной массив self.dfOutput остается нетронутым
        if len(filtQuery) > 0: 
            self.dfOutput = self.dfOutput.query(f"{filtQuery}", engine='python')

    @staticmethod
    def filter_frame_by_query_expr_static(df, filtQuery):
        """
        DSourceOutputCube
        Фильтрация текущего фрейма через query-выражение
        """
        # Фильтрует в том случае, если параметры фильтрации заданы конкретно, а не просто задана сама переменная типа {}. В ином случае выходной массив self.dfOutput остается нетронутым
        df = df.query(f"{filtQuery}", engine='python')
        return df






    @staticmethod
    def find_func_in_globals_static_(fClassName, funcName):
        """
        DSourceOutputCube +
        Найти функцию по названию ее класса и имени , находящихся в проекте
        Category: Глобальные функции
        """
        classObj = globals()[fClassName] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        funcObj = getattr(classObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        return funcObj






    @staticmethod                
    def diffirenciate_orig_and_calc_columns_static_(assocTitles):
        """
        DSourceOutputCube +
        Анализ словаря сотвтетсвий для выводимых в кончном варианте колонок на внешний рессурс. Среди элементов этого словаря могут быть задаваемые вычисляемые колонки
        Поэтому этот словарь должен быть разделен на словарь с оригинальными колонками и словарь с добавляемыми искуственными вычисляемыми колонками для дальнейшей обработки
        Вычислякмые колонки ключами имеют отрицательные негативные порядковые целые числа. Их нужно отфильтровать. На выходе должны быть два словаря: Один с оригинальными
        колонкми, другой - с вычисляемыми и дополняеыми в конце фрейма, псле формирования фрейма с оригинальными колонками. В результате должен быть построен прежный словарь, но 
        с уже вычесленными колонками , их индексами и названиями в комплексе с оргинальными для подачи на выход на внешний рессурс
        Category: Цветовые дифференциаторы
        """
        
        # print(f"222@@@@@@@@@@@@@@@@@@@@22 assocTitles = {assocTitles}")
        
        origColsAssocTitles_ = {} # @@@ Словарь для настроек по оригинальным выводимым столбцам (временно-служебный)
        calcColsAssocTitles_ = {} # @@@ Словарь для настроек вычисляемых искуственных добавляемых столбцов (временно-служебный)

        if len(assocTitles) > 0: # Если был передан словарь настроек выводимых колонок на внешний ресурс


            for key, val in assocTitles.items(): # Цикл по общему словарю настроек выходных колонок
                pass
                if key >= 0 : # Если ключ больше 0, то это оригинальныая колонка и вносим в соотв. временный словарь элемент
                    origColsAssocTitles_[key] = val

                elif key < 0: # Если ключ меньше 0, то это вычисляемая колонка и вносим ее в соотв. словарь
                    calcColsAssocTitles_[key] = val
                    
        return origColsAssocTitles_, calcColsAssocTitles_




    @staticmethod                
    def diffirenciate_orig_and_calc_columns_static_v2(assocTitles):
        """
        DSourceOutputCube +
        
        ИЗМ v2: Теперь разделяем  origColsAssocTitles_ не по положительному ключу, а по типу str, так как теперь ригинальные колонки - соответтсвуют названиям 
        колонок в таблицах БД. Остальное пока все так же остается. Начиная с проекта PROJ_021 (но пока не реализовано) [28-01-2024]
        
        Анализ словаря сотвтетсвий для выводимых в кончном варианте колонок на внешний рессурс. Среди элементов этого словаря могут быть задаваемые вычисляемые колонки
        Поэтому этот словарь должен быть разделен на словарь с оригинальными колонками и словарь с добавляемыми искуственными вычисляемыми колонками для дальнейшей обработки
        Вычислякмые колонки ключами имеют отрицательные негативные порядковые целые числа. Их нужно отфильтровать. На выходе должны быть два словаря: Один с оригинальными
        колонкми, другой - с вычисляемыми и дополняеыми в конце фрейма, псле формирования фрейма с оригинальными колонками. В результате должен быть построен прежный словарь, но 
        с уже вычесленными колонками , их индексами и названиями в комплексе с оргинальными для подачи на выход на внешний рессурс
        Category: Цветовые дифференциаторы
        """
        
        # print(f"222@@@@@@@@@@@@@@@@@@@@22 assocTitles = {assocTitles}")
        
        origColsAssocTitles_ = {} # @@@ Словарь для настроек по оригинальным выводимым столбцам (временно-служебный)
        calcColsAssocTitles_ = {} # @@@ Словарь для настроек вычисляемых искуственных добавляемых столбцов (временно-служебный)

        if len(assocTitles) > 0: # Если был передан словарь настроек выводимых колонок на внешний ресурс


            for key, val in assocTitles.items(): # Цикл по общему словарю настроек выходных колонок
                pass
                if isinstance(key, str) : # Если ключ является стрингом, то это оригинальныая колонка и вносим в соотв. временный словарь элемент
                    origColsAssocTitles_[key] = val

                elif key < 0: # Если ключ меньше 0, то это вычисляемая колонка и вносим ее в соотв. словарь
                    calcColsAssocTitles_[key] = val
                    
        return origColsAssocTitles_, calcColsAssocTitles_








    @staticmethod
    def add_update_calculated_cols_static_v2_(df, calcColsAssocTitles_, **fkwargs):
        """
        DSourceOutputCube +
        Добавить в конечный фрейм искуственные расчетные коллонки
        Формат настроек колонок такой и парсинг его соотвтетсвующий:
        -1 : 'CALC:Мес выплаты/BondsMainManager.add_col_to_df_for_cupone_date_for_bonds' (более полный пример в описании класса)
        TODO: !!!! Добавить или обновить расчетные коллонки в фрейме add_update_calculated_cols_static_v2_() : 4.223592281341553 seconds    !!!!!
        Каждое конвертирование колонок занимает примерно 1.2 сек !!! Значит надо сохранять фреймы для расчетных колонок в сессию  и брать оттуда потом!!!
        ИДЕИ: !!! что бы уменьшить время , затрачиваемое на калькуляцию новых значений колонок
        1. Все массивы данных, которые нужны для расчетных полей, сохраняем изначально в сесссии
        2. Возможно конвертация колонки затратнее, чем, если создать новую расчетную колонку, а затем удалить изначальную, колонку источник, в которую переконвертируется расчетные данные
        3. Осуществлять процессинг расчетных колонок не над всем массивом, а только над массивом страницы по пагинации
        Category: Калькуляторы полей
        """

        print(f"----START PR_NC_123 --> : add_update_calculated_cols_static_v2_() | noocube/dsource_output_cube_v2.py")
        
        # A. Цикл по калькулируемым колонкам из словаря calcColsAssocTitles_
        # newInxColsNamesAssocDic_ = {} # Словарь соотвтетвий новых индексов вычисляемых колонок в общем фрейме и их задаваемых названий
        for key, val in calcColsAssocTitles_.items(): # Цикл по словарю соответствий вычисляемых колонок

            # 1. Из величин словаря получаем название добавляемой вычисляемой колонки и класс-функцию, которая вычисляет колонку по заданному алгоритму и добавляет ее в конец
            #  общего входного фрейма с заданным названием
            mainPart = val.split(':')[1] # Получаем основную информационную часть значения. Метка 'CALC' - носит визуальный характер для настройки элементов словаря, поэтому не нужна
            infoParts = mainPart.split('/') # Делим на название колонки и класс-функцию , которая создает саму новую колонку (она где-то уже проработана и мы знаем ее  координаты класса и названия функции)
            # newColName = infoParts[0] # Название новой колонки
            classFuncPart = infoParts[1] # Часть  содержащая инфрмацию по классу-функции 
            parts = classFuncPart.split('.') # Делим на Класс и название функции , которая создает вычисляемую колонку
            className = parts[0] # Название класса
            funcName = parts[1] # Название функции

            # B. Нахождение и получение обьекта-функции , которая создает вычисляемую колонку
            oFunc = DSourceOutputCube.find_func_in_globals_static_(className, funcName)
            
            # C. <!!ЗАПУСК!!> спец функции добавления вычисляемой этой же функцией колонки в конец входного общего фрейма
            df = oFunc(df, **fkwargs)



        print(f"----END PR_NC_124 --> : add_update_calculated_cols_static_v2_() | noocube/dsource_output_cube_v2.py")
        
        return df






    # END ВЫЧИСЛЯЕМЫЕ ДОБАВОЧНЫЕ КОЛОНКИ





if __name__ == '__main__':
    pass
































