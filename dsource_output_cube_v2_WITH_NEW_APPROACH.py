

# from bonds.lo_calc_pandas_db import LibreCalcPandasDB
# from noocube.bonds_main_manager import BondsMainManager
from pandas import DataFrame
from noocube.pandas_manager import PandasManager
from noocube.output_pandas_manager import OutputPandasManager
from noocube.paginator_data_frame import PaginatorWithDataFrame
from noocube.settings import *
from noocube.df_fields_calc_funcs import DataFrameFieldsCalcFuncs


# TODO: Продумать систему наследования этого класса и родителей. Так как в программирвоании с БД и пандой нужны не только конечные обьекты дял вывода таблиц на конечных ресурсах,
#  но и подобные обьекты вообще, до вывода на конечный ресурс
# 
class DSourceOutputCube ():
    """ПРИМ: TODO: Использовать функционал из view_table_cube.py  для формирования источника данных из разных типов источников. 
    Класс для организации вывода таблицы из подготовленного фрейма  на любой внешний  рессурс (HTML, Excel и т.д.) 
    В нем фрейм подвергается пагинации, подготовки необходимого набора колонок, соотвтетвующий конечной таблице для вывода на внешний ресурс и оформление необходимых заголовков для 
    колонок этой таблицы.
    
    
    assocTitles = {dfColIndx : tbOutputTitle} - словарь соотвтетсвий индексов колонок во входном фрейме и соотвтетсвующих им названий колонок для конечной таблицы на внешнем ресурсе, которая будет
    строится из подготовленного фрейма в self.dfOutput
    Если передаются параметры 'filtParams', то происходит фильтрация при подготовке выходного фрейма с данными по условиям в параметрах condsDic (словарь с параметрами)
    ФОРМИРУЕТ ДОБАВОЧНЫЕ РАСЧЕТНЫЕ КОЛОНКИ!!! add_calculated_cols_() на основе задаваемого слова    # paginatorParams['pgToActivate'] = request.args.get('pg')
    ря соотвтетсвий названий колонок с их индексом и название специализированной функции,
    которая добавляет в фрейм расетную колонку
    Формат словаря соотвтетсвий выходных колонок с вычисляемыми колонками такой:
    COLS_ASSOC_FOR_BONDS_TYPE01_ = {   
                4 : 'Название', # Поле 'bond_name'
                1 : 'ISIN', # 'isin'   
                ....
                -1 : 'CALC:Мес выплаты/BondsMainManager.add_col_to_df_for_cupone_date_for_bonds',
                15 : 'Частота' ,                           
        } 

    """        

    def __init__(self, dfInput : DataFrame, **kwargs):
        
        print(f"--START: DSourceOutputCube.__init__() | noocube/dsource_output_cube_v2.py")
        
        # A. ----------------- ##### НОВЫЙ ПОДХОД v2 - заранее готовы ячейки - атрибуты для присваивания и через них идет управление всем --------------
        # Можно присваивать напрямую, а можно через **kwargs
        
        # Флаг инициации обьекта. Только один раз True, когда проходит инициализацию в констроукторе обьект. Пока закоментен, так как используется ниже по старому образцу работы
        # self.iniConstr = True 
        
        # --- ОСНОВНЫЕ ВХОДНЫЕ ПАРАМЕТРЫ НАСРОЕК ВЫХОДНОГО МАССИВА (пагинация,сортировка, названия колонок)
        
        self.dfInput = dfInput
        
        # Названия колонок. Если заданы, то присвиваются из словаря. Если не заданы, то остаются равные названиям колонок из источника
        if kwargs['assocTitles']:
            self.assocTitlesCell = kwargs['assocTitles']
        else:
            self.assocTitlesCell = {}
        
        # Настройки пагинации. 
        # 'pagesRowMax' : максимальное число показа нумерации страниц в ряду
        # 'dsRowsQnOnPage' : число записей из входного массива, показываемых на одной странице  
        if kwargs['paginGenSet']:
            self.paginGenSetCell = kwargs['paginGenSet']
        else:
            self.paginGenSetCell = {}
            
        # Активная страница в пагинаторе
        if 'pg' in kwargs:
            self.pgToActivateCell = kwargs['pg']
        else:
            self.pgToActivateCell = 1
        
        # Флаг сортировки. Если True, то сортировка по заданным колонкам производится. Если False - то не производится, несмотря на то
        # что прочие параметры сортировки могут быть заданы
        if 'sortFlag' in kwargs:
            self.sortFlagCell = kwargs['sortFlag']
        else:
            self.sortFlagCell = False
        
        # Направление сортировки по заданной колонки в self.sortColInxCell или в self.sortColName
        if 'sortASC' in kwargs:
            self.sortASCCell = kwargs['sortASC']
        else:
            self.sortASCCell = True
        
        # Колонка для сортировки по ее индексу в выходно источнике (после всех процедур над массивом данных)
        if 'sortColInx' in kwargs:
            self.sortColInxCell = kwargs['sortColInx']
        else:
            self.sortColInxCell = 0

        # Колонка для сортировки по ее имени в выходном источнике (после всех процедур над массивом данных)
        if 'sortColName' in kwargs:
            self.sortColNameCell = kwargs['sortColName'].strip()
        else:
            self.sortColNameCell = ''

        # --- END ОСНОВНЫЕ ВХОДНЫЕ ПАРАМЕТРЫ НАСРОЕК ВЫХОДНОГО МАССИВА (пагинация,сортировка, названия колонок)
        
        # E. ВЫХОДНЫЕ ДАННЫЕ КЛАССА
        
        # Выходной общий конечный обработанный массив данных (в виде фрейма)
        self.dfOutputCell = None
        
        # Выходной постраничный активный массив обработанных данных, соотвтетсвующий активной страницы пагинатора self.pgCell
        self.dfActivePageFrameCell = None
        
        # Пагинатор
        self.paginator = None
        
        # E. END ВЫХОДНЫЕ ДАННЫЕ КЛАССА
        
  
        # Активация обьекта. Запуск методов процессинга над массивом данных в self.dfInput
        self.activate()
        
        # Флаг инициации обьекта. Только один раз True, когда проходит инициализацию в констроукторе обьект. Пока закоментен, так как используется ниже по старому образцу работы
        # self.iniConstr = False 
        
        print(f"--END: DSourceOutputCube.__init__() ")

    def activate (self):
        """
        активировать настройки обьекта, если они были заданы напрямую (не через **kwargs) в уже существующем обьекте. То есть
        без использования конструктора класса
        Category: Вспомогательные
        """
        
        print(f"---- START: activate() | noocube/dsource_output_cube_v2.py")
        
        # D. Проработка названий колонок и расчетных добавочных колонок
        
        # Разделение словаря на словарь обычных origColsAssocTitles_ названий и на словарь с расчетными полями calcColsAssocTitles_
        origColsAssocTitles_, calcColsAssocTitles_ = DSourceOutputCube.diffirenciate_orig_and_calc_columns_static_(self.assocTitlesCell)
        
        print(f"origColsAssocTitles_ = {origColsAssocTitles_} | noocube/dsource_output_cube_v2.py")
        
        # E. Проработать массив данных на предмет названий колонок на базе assocTitles и вырезания из оригинального фрейма тех колонок, Которые заданы в assocTitles
        self.dfInput = DSourceOutputCube.prepare_to_output_static(self.dfInput, origColsAssocTitles_)
        
        
        
        # F. Добавить или обновить расчетные коллонки в фрейме
        fkwargs = {}
        self.dfInput, self.assocTitlesCell = DSourceOutputCube.add_update_calculated_cols_static_v2_(self.dfInput, self.assocTitlesCell, calcColsAssocTitles_, **fkwargs)
        
        


        print(f"---- END: activate() | noocube/dsource_output_cube_v2.py")




    def sort_by_index(self):
        """ 
        Для сортировки фрейма @@@ self.outputDf  по индексу колонки в конечном , выходном фрейме
        Уже должны быть значения В собственных переменных:
        self.outputDf - сам фрейм с данынми
        self.sortColInx - индекс колонки, по которой необходимо провести сортировку
        self.sortFlag - флаг сортировки (включатель сортировки)
        sortDirection - Направление сортировки sortDict['desc'] или self.sortDirection:  False или True. По умолчанию ascending=True
        Category: Фреймы
        """
        print(f"START: sort_by_index()")
        self.print_sort_params_()
        pandProc = PandasManager()
        self.dfOutput = pandProc.get_df_sorted_by_col_index(self.dfOutput, self.sortColInx, self.ascTrue)
        
        
    @staticmethod
    def sort_by_index_static(df, sortColInx, ascTrue = True):
        """ 
        Для сортировки фрейма @@@ self.outputDf  по индексу колонки в конечном , выходном фрейме
        Уже должны быть значения В собственных переменных:
        sortColInx - индекс колонки, по которой необходимо провести сортировку
        ascTrue - Направление сортировки False или True. По умолчанию ascending=True
        Category: Фреймы
        """
        print(f"START: sort_by_index()")
        # self.print_sort_params_()
        pandProc = PandasManager()
        df = pandProc.get_df_sorted_by_col_index(df, sortColInx, ascTrue)
        return df



    @staticmethod
    def sort_by_name_static(df, sortColName, ascTrue = True):
        """ 
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
    def prepare_to_output_static(dfInput, assocTitles):
        """
        DSourceOutputCube
        Подготавливает источник данных dataSrc в виде фрейма (если он был задан другими типами данных, нежели входной фрейм) на основе создания обьекта
        класса DSourceCube или DSearchCube и оттуда уже берет конечный фрейм для вывода (присваивает этот фрейм в собственную переменную self.outputDf ) на внешний ресурс в том виде, 
        в котором это необходимо (в частности в виде таблицы на странице HTML)
        Аббревиатура 'dfds' - dataFrame на основе входного dataSet  
        Category: Вспомогательные
        """

        outPandaMngr = OutputPandasManager()
        # Подготовить конечный фрейм @@@ self.dfOutput
        if len(assocTitles) > 0: # Если заданы колонки для преобразования входного массива , то форматируем фрейм
            dfOutput = outPandaMngr.format_df_according_final_output_table_pandas(dfInput, assocTitles)
        else: # Иначе выходной фрейм не форматируется и приравнивается входному
            dfOutput = dfInput
            
        return dfOutput









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

            # TODO: Сделать, чтобы пагинатор активировался только один раз. Сейчас он при фильтрации снова инициализируется, так как dfOutput изменяется при фильтрации
            # <В последнюю очерередь> Проверка наличия установок и исходного фрейма с данными перед запуском пагинатора
            if  len(self.paginGenSet)  > 0 and len(self.dfOutput) > 0:   
                self.paginator = PaginatorWithDataFrame(self.dfOutput, self.paginGenSet) # инициализация обьекта пагинатора в общей форме
                # Активация пагинатора по заданной странице к активации
                self.paginator = PaginatorWithDataFrame.get_curr_paginator_from_gen (self.paginator,  self.pgToActivate) 


    def filter_frame_by_query_expr_(self, filtQuery):
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
        if len(filtQuery) > 0: 
            self.dfOutput = self.dfOutput.query(f"{filtQuery}", engine='python')
            # @@@ Qn
            self.qn = len(self.dfOutput)

            # # TODO: Сделать, чтобы пагинатор активировался только один раз. Сейчас он при фильтрации снова инициализируется, так как dfOutput изменяется при фильтрации
            # # <В последнюю очерередь> Проверка наличия установок и исходного фрейма с данными перед запуском пагинатора
            # if  len(self.paginGenSet)  > 0 and len(self.dfOutput) > 0:   
            #     self.paginator = PaginatorWithDataFrame(self.dfOutput, self.paginGenSet) # инициализация обьекта пагинатора в общей форме
            #     # Активация пагинатора по заданной странице к активации
            #     self.paginator = PaginatorWithDataFrame.get_curr_paginator_from_gen (self.paginator,  self.pgToActivate) 





    # ВЫЧИСЛЯЕМЫЕ ДОБАВОЧНЫЕ КОЛОНКИ


    def get_fcalss_fname_from_str_alg_infor_(self):
        """
        @@@ Парсинг строки вида fClassName.funcName с названием класса и метода алогоритма, который отвечает за формирование фрейма с необходимыми данными для вывода на 
        внешний рессурс в виде таблицы
        Category: Глобальные функции
        """
        parts = self.frAlgorithmInfor.split('.') # Вычисление названий класса в которой находится АИФП и  имени атомарной поисковой функции
        self.fClassName = parts[0] # названий класса в которой находится АИФП 
        self.funcName = parts[1] # имени атомарной поисковой функции


    # def find_func_in_globals_(self, fClassName, funcName):
    #     """@@@ Найти функцию по названию ее класса и имени , находящихся в проекте"""
    #     classObj = globals()[fClassName] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
    #     funcObj = getattr(classObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
    #     return funcObj
    
    
    def find_func_in_globals_static_(fClassName, funcName):
        """
        DSourceOutputCube
        Найти функцию по названию ее класса и имени , находящихся в проекте
        Category: Глобальные функции
        """
        classObj = globals()[fClassName] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        funcObj = getattr(classObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        return funcObj






    @staticmethod                
    def diffirenciate_orig_and_calc_columns_static_(assocTitles):
        """
        DSourceOutputCube
        Анализ словаря сотвтетсвий для выводимых в кончном варианте колонок на внешний рессурс. Среди элементов этого словаря могут быть задаваемые вычисляемые колонки
        Поэтому этот словарь должен быть разделен на словарь с оригинальными колонками и словарь с добавляемыми искуственными вычисляемыми колонками для дальнейшей обработки
        Вычислякмые колонки ключами имеют отрицательные негативные порядковые целые числа. Их нужно отфильтровать. На выходе должны быть два словаря: Один с оригинальными
        колонкми, другой - с вычисляемыми и дополняеыми в конце фрейма, псле формирования фрейма с оригинальными колонками. В результате должен быть построен прежный словарь, но 
        с уже вычесленными колонками , их индексами и названиями в комплексе с оргинальными для подачи на выход на внешний рессурс
        Category: Цветовые дифференциаторы
        """
        
        origColsAssocTitles_ = {} # @@@ Словарь для настроек по оригинальным выводимым столбцам (временно-служебный)
        calcColsAssocTitles_ = {} # @@@ Словарь для настроек вычисляемых искуственных добавляемых столбцов (временно-служебный)

        if len(assocTitles) > 0: # Если был передан словарь настроек выводимых колонок на внешний ресурс


            for key, val in assocTitles.items(): # Цикл по общему словарю настроек выходных колонок
                pass
                if key > 0 : # Если ключ больше 0, то это оригинальныая колонка и вносим в соотв. временный словарь элемент
                    origColsAssocTitles_[key] = val

                elif key<0: # Если ключ меньше 0, то это вычисляемая колонка и вносим ее в соотв. словарь
                    calcColsAssocTitles_[key] = val
                    
        return origColsAssocTitles_, calcColsAssocTitles_







    @staticmethod
    def add_calculated_cols_static_(df, assocTitles, calcColsAssocTitles_, **fkwargs):
        """
        DSourceOutputCube
        Добавить в конечный фрейм искуственные расчетные коллонки
        Формат настроек колонок такой и парсинг его соотвтетсвующий:
        -1 : 'CALC:Мес выплаты/BondsMainManager.add_col_to_df_for_cupone_date_for_bonds' (более полный пример в описании класса)
        Category: Калькуляторы полей
        """

        # Словарь соотвтетствий новых вычисляемых колонок фрейма и функций , на основе которой они расичтываются из существующих колонок
        # addAssocDic = self.calcColsAssocTitles_

        # Добавляем калькулируемые коллонки в соответствии со словарем соотвтетсвий для вычисляемых колонок, найденных в методе diffirenciate_orig_and_calc_columns_(),
        # в конец входного фрейма м запоминаем соотвтетсвия их новых индексов в общем фрейме с уже добавленными вычисляемыми колонками

        newInxColsNamesAssocDic_ = {} # Словарь соотвтетвий новых индексов вычисляемых колонок в общем фрейме и их задаваемых названий
        for key, val in calcColsAssocTitles_.items(): # Цикл по словарю соответствий вычисляемых колонок

            # 1. Из величин словаря получаем название добавляемой вычисляемой колонки и класс-функцию, которая вычисляет колонку по заданному алгоритму и добавляет ее в конец
            #  общего входного фрейма с заданным названием
            mainPart = val.split(':')[1] # Получаем основную информационную часть значения. Метка 'CALC' - носит визуальный характер для настройки элементов словаря, поэтому не нужна
            infoParts = mainPart.split('/') # Делим на название колонки и класс-функцию , которая создает саму новую колонку (она где-то уже проработана и мы знаем ее  координаты класса и названия функции)
            newColName = infoParts[0] # Название новой колонки
            classFuncPart = infoParts[1] # Часть  содержащая инфрмацию по классу-функции 
            parts = classFuncPart.split('.') # Делим на Класс и название функции , которая создает вычисляемую колонку
            className = parts[0] # Название класса
            funcName = parts[1] # Название функции
 
            # Нахождение и получение обьекта-функции , которая создает вычисляемую колонку
            oFunc = DSourceOutputCube.find_func_in_globals_static_(className, funcName)

            # <ЗАПУСК> спец функции добавления вычисляемой этой же функцией колонки в конец входного общего фрейма
            newColInx = oFunc(df, newColName, **fkwargs)

            # @@@ Запоминаем какая новая колонка с именем находится по какому адресу в общем фрейме, после добавления колонки в общий фрейм, для будущего замещения в словаре соотвтетсвий изначальном
            newInxColsNamesAssocDic_[newColInx] = newColName 

        # print(f"$$$$#####@@@@@ self.newInxColsNamesAssocDic_ = {self.newInxColsNamesAssocDic_}")    

        # 2. Замещаем элементы для калькулируемых колонок в установочном словаре соответствий настроек выходных столбцов таблицы , которые хранятся в self.assocTitles, 
        # теперь уже нормальными стандартными элементами с индексом и названиями новых вычисляемых колонок. И они будут в необходимой задаваемой последовательности при этом
        newDic = {} # Новый словарь, где будет создаваться копия порядка исходного словаря, но с замещенными элементами, в которых были калькулируемые поля
        for keySetting, valSetting in assocTitles.items(): # Цикл по изначальному словарю настроек выходных колонок таблицы

            flagFound = -1 # Флаг нахождения поля в словаре фиксации newInxColsNamesAssocDic_
            for keyCalc, valCalc in newInxColsNamesAssocDic_.items(): # Цикл по словарю соотвтетсвий новых колонок в общем фрейме

                if valCalc in valSetting: # Если название новой калькулируемой колонки находится в знаении исходного настроечного словаря колонок, то то вносим элемент из словаря новых колонок
                    newDic[keyCalc] = valCalc
                    flagFound = 1 # Если совпадение найдено

            if flagFound < 0: # Если не найдено поле в словаре фиксации newInxColsNamesAssocDic_,  то вносим старое значение из исходного словаря
                newDic[keySetting] = valSetting


        # @@@ Присваиваем вновь сформированный словарь соотвтетсвий в собственную переменную, отвечающую за формирвоание названий и последовательности выходных колонок
        assocTitles = newDic
        
        return df, assocTitles

        # print(f"$$$$#####@@@@@ self.assocTitles = {self.assocTitles}")   



    @staticmethod
    def add_update_calculated_cols_static_v2_(df, assocTitles, calcColsAssocTitles_, **fkwargs):
        """
        DSourceOutputCube
        Добавить в конечный фрейм искуственные расчетные коллонки
        Формат настроек колонок такой и парсинг его соотвтетсвующий:
        -1 : 'CALC:Мес выплаты/BondsMainManager.add_col_to_df_for_cupone_date_for_bonds' (более полный пример в описании класса)
        Category: Калькуляторы полей
        """

        print(f"----START: add_update_calculated_cols_static_v2_() | noocube/dsource_output_cube_v2.py")

        # Словарь соотвтетствий новых вычисляемых колонок фрейма и функций , на основе которой они расичтываются из существующих колонок
        # addAssocDic = self.calcColsAssocTitles_

        # Добавляем калькулируемые коллонки в соответствии со словарем соотвтетсвий для вычисляемых колонок, найденных в методе diffirenciate_orig_and_calc_columns_(),
        # в конец входного фрейма м запоминаем соотвтетсвия их новых индексов в общем фрейме с уже добавленными вычисляемыми колонками


        # A. Цикл по калькулируемым колонкам из словаря calcColsAssocTitles_
        newInxColsNamesAssocDic_ = {} # Словарь соотвтетвий новых индексов вычисляемых колонок в общем фрейме и их задаваемых названий
        for key, val in calcColsAssocTitles_.items(): # Цикл по словарю соответствий вычисляемых колонок

            # 1. Из величин словаря получаем название добавляемой вычисляемой колонки и класс-функцию, которая вычисляет колонку по заданному алгоритму и добавляет ее в конец
            #  общего входного фрейма с заданным названием
            mainPart = val.split(':')[1] # Получаем основную информационную часть значения. Метка 'CALC' - носит визуальный характер для настройки элементов словаря, поэтому не нужна
            infoParts = mainPart.split('/') # Делим на название колонки и класс-функцию , которая создает саму новую колонку (она где-то уже проработана и мы знаем ее  координаты класса и названия функции)
            newColName = infoParts[0] # Название новой колонки
            classFuncPart = infoParts[1] # Часть  содержащая инфрмацию по классу-функции 
            parts = classFuncPart.split('.') # Делим на Класс и название функции , которая создает вычисляемую колонку
            className = parts[0] # Название класса
            funcName = parts[1] # Название функции

            # B. Нахождение и получение обьекта-функции , которая создает вычисляемую колонку
            oFunc = DSourceOutputCube.find_func_in_globals_static_(className, funcName)
            
            # C. <ЗАПУСК> спец функции добавления вычисляемой этой же функцией колонки в конец входного общего фрейма
            newColInx = oFunc(df, **fkwargs)

            # D. Запоминаем какая новая колонка с именем находится по какому адресу в общем фрейме, после добавления колонки в общий фрейм, для будущего замещения в словаре соотвтетсвий изначальном
            newInxColsNamesAssocDic_[newColInx] = newColName 

        # E. Замещаем элементы для калькулируемых колонок в установочном словаре соответствий настроек выходных столбцов таблицы , которые хранятся в self.assocTitles, 
        # теперь уже нормальными стандартными элементами с индексом и названиями новых вычисляемых колонок. И они будут в необходимой задаваемой последовательности при этом
        newDic = {} # Новый словарь, где будет создаваться копия порядка исходного словаря, но с замещенными элементами, в которых были калькулируемые поля
        for keySetting, valSetting in assocTitles.items(): # Цикл по изначальному словарю настроек выходных колонок таблицы

            flagFound = -1 # Флаг нахождения поля в словаре фиксации newInxColsNamesAssocDic_
            for keyCalc, valCalc in newInxColsNamesAssocDic_.items(): # Цикл по словарю соотвтетсвий новых колонок в общем фрейме

                if valCalc in valSetting: # Если название новой калькулируемой колонки находится в знаении исходного настроечного словаря колонок, то то вносим элемент из словаря новых колонок
                    newDic[keyCalc] = valCalc
                    flagFound = 1 # Если совпадение найдено

            if flagFound < 0: # Если не найдено поле в словаре фиксации newInxColsNamesAssocDic_,  то вносим старое значение из исходного словаря
                newDic[keySetting] = valSetting


        # @@@ Присваиваем вновь сформированный словарь соотвтетсвий в собственную переменную, отвечающую за формирвоание названий и последовательности выходных колонок
        assocTitles = newDic
        
        print(f"----END: add_update_calculated_cols_static_v2_() | noocube/dsource_output_cube_v2.py")
        
        return df, assocTitles

        # print(f"$$$$#####@@@@@ self.assocTitles = {self.assocTitles}")   


        




    # END ВЫЧИСЛЯЕМЫЕ ДОБАВОЧНЫЕ КОЛОНКИ





if __name__ == '__main__':
    pass
































