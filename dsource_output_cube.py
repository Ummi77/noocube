

# from bonds.lo_calc_pandas_db import LibreCalcPandasDB
from noocube.bonds_main_manager import BondsMainManager
from pandas import DataFrame
# import noocube.funcs_general as FG
# from noocube.switch import Switch
# from noocube.sqlite_pandas_processor import SqlitePandasProcessor
from noocube.pandas_manager import PandasManager
from noocube.output_pandas_manager import OutputPandasManager
from noocube.paginator_data_frame import PaginatorWithDataFrame
# from noocube.dsource_cube import DSourceCube
from noocube.settings import *


# TODO: Продумать систему наследования этого класса и родителей. Так как в программирвоании с БД и пандой нужны не только конечные обьекты дял вывода таблиц на конечных ресурсах,
#  но и подобные обьекты вообще, до вывода на конечный ресурс
# 
class DSourceOutputCube ():
    """Класс для организации вывода таблицы из подготовленного фрейма  на любой внешний  рессурс (HTML, Excel и т.д.) 
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
        
        
        
        # A. ----------------- ##### НОВЫЙ ПОДХОД v2 - заранее готовы ячейки - атрибуты для присваивания и через них идет управление всем --------------
        # Можно присваивать напрямую, а можно через **kwargs
        
        # Флаг инициации обьекта. Только один раз True, когда проходит инициализацию в констроукторе обьект. Пока закоментен, так как используется ниже по старому образцу работы
        # self.iniConstr = True 
        
        # --- ОСНОВНЫЕ ВХОДНЫЕ ПАРАМЕТРЫ НАСРОЕК ВЫХОДНОГО МАССИВА (пагинация,сортировка, названия колонок)
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
        
        
        # B. ----- Методы нового подхода v2:
        
        
        # D. Проработка названий колонок и расчетных добавочных колонок
        
        # Разделение словаря на словарь обычных origColsAssocTitles_ названий и на словарь с расчетными полями calcColsAssocTitles_
        origColsAssocTitles_, calcColsAssocTitles_ = DSourceOutputCube.diffirenciate_orig_and_calc_columns_static_(self.assocTitlesCell)
        
        # Добавить в конечный фрейм искуственные расчетные коллонки
        fkwargs = {}
        self.dfInput, self.assocTitlesCell = DSourceOutputCube.add_calculated_cols_static_(dfInput, self.assocTitlesCell, calcColsAssocTitles_, **fkwargs)
        
        # Проработать массив данных на предмет названий колонок и расчетных колонок
        self.dfOutputCell = DSourceOutputCube.prepare_to_output_static(dfInput, self.assocTitlesCell)
        
        # G. Сортировка массива по заданнйо колонке и направлению
        # TODO: Сделать сортировку по двум полям , как минимум !!!
        if self.sortFlagCell:
            # Если задано название колонки сортировки, то сортирует по названию колонки. Иначе - по индексу (если флаг сортировки self.sortFlag = True)
            if len(self.sortColNameCell) > 0:
                self.dfOutputCell = DSourceOutputCube.sort_by_name_static(self.dfOutputCell, self.sortColNameCell, self.sortASCCell)
            else :
                self.dfOutputCell = DSourceOutputCube.sort_by_index_static(self.dfOutputCell, self.sortColInxCell, self.sortASCCell)
        
        # C. ПОДГОТОВКА НЕОСНОВНЫХ НАСТРОЕК (фильтрация, поиск и т.д.)
        
        
        # F. Пагинация готового массива
        # <В последнюю очерередь> Проверка наличия установок и исходного фрейма с данными перед запуском пагинатора
        # Сделать флаг фильтрации для пагинатора (если предусматривается фильтрация, то пагинатор инициализируется после филтрации в  filter_frame() )
        if  len(self.paginGenSetCell)  > 0 and len(self.dfOutputCell) > 0:   
            self.paginator = PaginatorWithDataFrame(self.dfOutputCell, self.paginGenSetCell) # инициализация обьекта пагинатора в общей форме
            # Активация пагинатора по заданной странице к активации
            self.paginator = PaginatorWithDataFrame.get_curr_paginator_from_gen (self.paginator,  self.pgToActivateCell) 
            
            # Выходной постраничный активный массив обработанных данных, соотвтетсвующий активной страницы пагинатора self.pgCell
            self.dfActivePageFrameCell = self.paginator.dfLimByPgNumb

        else:
            self.paginator = -1
            self.dfActivePageFrameCell = -1
        
        
        
        # B. ----- END Методы нового подхода v2:
        
        # Флаг инициации обьекта. Только один раз True, когда проходит инициализацию в констроукторе обьект. В конце __init__ выключаем флаг инициализации
        # self.iniConstr = False 

        
        
        # A. ----------------- ##### END НОВЫЙ ПОДХОД v2 - заранее готовы ячейки - атрибуты для присваивания и через них идет управление всем --------------





        self.iniConstr = True # Флаг инициации обьекта. Только один раз True, когда проходит инициализацию в констроукторе обьект


        # Собственный список сцммирующих итоговых рядов <tr> для конечной внешней таблицы вывода данных по обьекту
        self.summaryRows = []


        # Входные именнованные параметры **kwargs
        self.kwargs = kwargs

        # Переменные для Входных параметров
        self.dfInput = dfInput # Входной источник данных в виде фрейма для обрабоки к выводу в конечном варианте на внешний ресурс

        # Исходный фрейм (Если входной источник dataSrc - фрейм, то он тождественно приравнивается к нему. В ином случае фрейм создается в зависимости от типа dataSrc)
        # Создается обьект класса DSourceCube, который сам анализирует источник данных и создает внутри себя необходимый нам фрейм для дальнейшей обработки и записывается в self.genDf
        self.genDf = dfInput

        # ДЕФОЛТНАЯ УСТАНОВКА СОБСТВЕННЫХ ПЕРЕМЕННЫХ, тех, которых необходимо устанавливать по умолчанию:


        self.paginatorParams = {}
        self.sortParams = {}
        self.assocTitles = {}

        self.tableBody = '' # Для хранения возможного или стандартного HTML - кода тела таблицы
        self.tableHead = ''  # Для хранения возможного или стандартного HTML - кода заголовков таблицы
        self.tableFinal = '' # Для хранения возможного или стандартного HTML - кода полной конечной таблицы

        # Собственные переменные пагинации
        # Общие настройки пагинатора по дефолту
        # self.paginGenSet = {
        #                         'pagesRowMax' : 5, # максимальное число показа нумерации страниц в ряду
        #                         'dsRowsQnOnPage' : 20 # число записей из входного массива, показываемых на одной странице  
        #                     } 

        self.paginGenSet = kwargs['paginGenSet']
        self.pgToActivate = 1 # Страница к активации в пагинаторе
        # self.paginFlag = True # Флаг (включатель) пагинации # Пока не нужна
        self.sortFlag = False # Флаг сортировки
        self.sortColInx = 0 #  Индекс колонки сортировки по умолчанию   = 0


        # конечный вариант фрейма для вывода на внешний ресурс (с готовым пагинатором, заанными колонкми и их названиями на внешнем ресурсе)
        self.dfOutput = DataFrame()

        # Настройка собственных переменных, которые соотвтетсвуют входным именнованным параметрам <!!! ВАЖНАЯ ФУНКЦИЯ>
        self.set_cls_vars_from_kwargs_dsourceoutputcube_ ()   # Настройка собственных переменных, которые соотвтетсвуют входным именнованным параметрам (именно этого родительского класса)


        # Анализ словаря сотвтетсвий для выводимых в кончном варианте колонок на внешний рессурс. Среди элементов этого словаря могут быть задаваемые вычисляемые колонки
        # Поэтому этот словарь должен быть разделен на словарь с оригинальными колонками и словарь с добавляемыми искуственными вычисляемыми колонками для дальнейшей обработки
        self.diffirenciate_orig_and_calc_columns_()

        # Добавлене расчетных искуственных колонок в полученный фрейм после self.prepare_to_output()
        if len(self.calcColsAssocTitles_)>0 and len(self.dfInput)>0:
            self.add_calculated_cols_()


        # Подготовить входной фрейм к выводу  и присвоить подготовленный фрейм self.dfOutput (подготовка необходимого набора колонок, соотвтетвующий конечной таблице 
        # для вывода на внешний ресурс и оформление необходимых заголовков для колонок этой таблицы)src
        self.prepare_to_output()



        # Запуск сортировки по задаваемым в self.sortCols  колонкам , если флаг сортировки self.sortFlag = True
        if self.sortFlag:
            # В зависимости от того, сортируем по индексу колонки или по имени запусткаются соотвтетсвенные методы сортировки
            if 'byIndex' in self.sortType:
                self.sort_by_index()
            elif 'byName' in self.sortType:
                self.sort_by_name()



        # Фильтрация по заданному выражению
        if "filtQuery" in kwargs  and len(kwargs['filtQuery']) > 0: # Если в genParams присутствуют параметры фильтрации, то проводим фильтрацию конечного массива данных
            filtQuery = kwargs['filtQuery']
            self.filter_frame_by_query_expr_(filtQuery)


        # Фильтрация по ISIN в одиночном input-поле filtIsin раздела фильтрации (для фильтрации по ISIN)
        if "filtIsin" in kwargs and len(kwargs['filtIsin']) > 0  : # Если в kwargs присутствуют непустой filtIsin , то проводим фильтрацию конечного массива данных
            isin = kwargs['filtIsin']
            filtQuery = f'ISIN == "{isin}"'
            self.filter_frame_by_query_expr_(filtQuery)


        # Фильтрация по filtBondName в одиночном input-поле filtBondName раздела фильтрации (для фильтрации по назвнию облигации)
        if "filtBondName" in kwargs and len(kwargs['filtBondName']) > 0  : # Если в kwargs присутствуют непустой filtIsin , то проводим фильтрацию конечного массива данных
            filtBondName = kwargs['filtBondName']
            filtQuery = f'Название == "{filtBondName}"'
            self.filter_frame_by_query_expr_(filtQuery)


        # Фильтрация по заданному выражению в словаре фиксированных выражений , находимому через получаемый ключ к этому словарю
        if "filtExprDicKey" in kwargs and len(kwargs['filtExprDicKey']) > 0  : # Если в kwargs присутствуют непустой filtIsin , то проводим фильтрацию конечного массива данных
            filtExprDicKey = kwargs['filtExprDicKey'] # Ключ к словарю
            filtExprQr = self.constFiltExprDic[filtExprDicKey][1] # Выражение query из фиксированного словаря для фильтрации фрейма, 2й член списка знаения словаря 
            self.filter_frame_by_query_expr_(filtExprQr) # Фильтровать фрейм выражением filtExprQr



        # <В последнюю очерередь> Проверка наличия установок и исходного фрейма с данными перед запуском пагинатора
        # Сделать флаг фильтрации для пагинатора (если предусматривается фильтрация, то пагинатор инициализируется после филтрации в  filter_frame() )
        if  len(self.paginGenSet)  > 0 and len(self.dfOutput) > 0:   
            self.paginator = PaginatorWithDataFrame(self.dfOutput, self.paginGenSet) # инициализация обьекта пагинатора в общей форме
            # Активация пагинатора по заданной странице к активации
            self.paginator = PaginatorWithDataFrame.get_curr_paginator_from_gen (self.paginator,  self.pgToActivate) 

        else:
            self.paginator = -1



        self.iniConstr = False # Флаг инициации обьекта. Только один раз True, когда проходит инициализацию в констроукторе обьект. В конце __init__ выключаем флаг инициализации



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


    def sort_by_name(self):
        """ 
        Для сортировки фрейма @@@ self.outputDf по названию колонки в конечном , выходном фрейме
        Уже должны быть значения В собственных переменных:src
        self.outputDf - сам фрейм с данынми
        self.sortColInx - индекс колонки, по которой необходимо провести сортировку
        self.sortFlag - флаг сортировки (включатель сортировки)
        sortDirection - Направление сортировки sortDict['desc'] или self.sortDirection:  False или True. По умолчанию ascending=True
        Category: Фреймы
        """
        print(f"START: sort_by_name()")
        self.print_sort_params_()
        pandProc = PandasManager()
        self.dfOutput = pandProc.get_df_sorted_by_col_name_v02(self.dfOutput, self.sortColName, self.ascTrue)
        
        
        
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
        
        

    def prepare_to_output(self):
        """DSourceOutputCube
        Подготавливает источник данных dataSrc в виде фрейма (если он был задан другими типами данных, нежели входной фрейм) на основе создания обьекта
        класса DSourceCube или DSearchCube и оттуда уже берет конечный фрейм для вывода (присваивает этот фрейм в собственную переменную self.outputDf ) на внешний ресурс в том виде, 
        в котором это необходимо (в частности в виде таблицы на странице HTML)
        Аббревиатура 'dfds' - dataFrame на основе входного dataSet  
        Category: Вспомогательные
        """

        BondsMainManager.print_IF_DEBUG_bmm("\n-------- START ->  ",  {
            'method' : 'prepare_to_output()',
            'module' : 'DSourceOutputCube',
            })

        # Словарь соотвтествий между названиями в выводимой таблице и колонкми фрейма, содержащего результаты по полнотекстовому поиску облигаций, чьи эмитенты 
        # удовлетворяют заданным критериям поиска
        
        # self.assocTitles =  COLS_ASSOC_FOR_BONDS_TYPE01_ # <ВРЕМЕННО ТУТ>
        # paginSets = PAGIN_BONDS_CURR_SET_ # Настройки пагинатора общие
        outPandaMngr = OutputPandasManager()
         # Подготовить конечный фрейм @@@ self.dfOutput
        if len(self.assocTitles) > 0: # Если заданы колонки для преобразования входного массива , то форматируем фрейм
            self.dfOutput = outPandaMngr.format_df_according_final_output_table_pandas(self.dfInput, self.assocTitles)
        else: # Иначе выходной фрейм не форматируется и приравнивается входному
            self.dfOutput = self.dfInput


        # # @@@ Если задаются параметры внутренней фильтрации по фрейму (не полнотекстовый поиск, а именно по фрейму)
        # if len(self.condsDic) > 0 :
        #     self.dfOutput = self.filter_frame() # Получаем условияфильтрации из параметров фильтрации

        # @@@ Индексированный список колонок в виде словаря на бызе конечного dfOutput
        self.colsOutpIndexed = PandasManager.get_indexed_df_cols_pandas(self.dfOutput) 

        # @@@ Список колонок простой
        self.colsOutput = list(self.colsOutpIndexed.values())

        # @@@ Qn
        self.qn = len(self.dfOutput)
        # <PRINT> Распечатка данных по фрейму 
        # outPandaMngr.print_df_gen_info_pandas_IF_DEBUG(self.dfOutput , ifPrintDF = False, dfId = 'dfOutput', srcId = ' / DSourceOutputCube.prepare_to_output()')

        BondsMainManager.print_IF_DEBUG_bmm("-------- END ->  ",  {
            'method' : 'prepare_to_output()',
            'module' : 'DSourceOutputCube\n',
            })


    @staticmethod
    def prepare_to_output_static(dfInput, assocTitles):
        """DSourceOutputCube
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


    ## Внутренние служебные методы класса



    def set_cls_vars_from_kwargs_dsourceoutputcube_ (self):
        """
        установка собственных переменных в зависимости от переданных переметров **kwargs с соответствующими ключами , предназаначенных, кроме всего, для настройки собственных
        соотвтетсвующих прееменных
        Тут идет установка собственных переменных из внешних входных параметров. Если параметры обьеденины в группу, то эта группа сама является 
        пременной-словарем типа self.sortParams = self.kwargs['sortParams'] . либо негрупповые, индивидуальные параметры, тогда считывается напрямую из именных параметров kwargs
        Category: Вспомогательные
        """


        # ИНДИВИДУАЛЬНЫЕ ПАРАМЕТРЫ:

        # @@@  self.assocTitles -  словарь соотвтетсвий индексов колонок выходного фрейма и соответствующие им титульные названия в таблице на внешнем ресурсе
        if "assocTitles" in self.kwargs :
            self.assocTitles = self.kwargs['assocTitles'] 
            print(f"self.assocTitles = {self.assocTitles}")



        ## ГРУППОВЫЕ ПЕРЕМЕННЫЕ ПАГИНАТОРА
        # @@@  self.paginatorParams - Параметры пагинации пагинации
        if "paginatorParams" in self.kwargs :
            self.paginatorParams = self.kwargs['paginatorParams'] 
            print(f"self.paginatorParams = {self.paginatorParams}")

            # Расшифровка и присвоение параметров сортировки, которые сами хранятся в параметре-словаре self.sortParams 
            # @@@ Общие настройки пагинатора
            if "paginGenSet" in self.paginatorParams :
                self.paginGenSet = self.paginatorParams['paginGenSet'] 
                print(f"self.paginGenSet = {self.paginGenSet}")

            # @@@ Страница к активации в пагинаторе
            if "pgToActivate" in self.paginatorParams :
                self.pgToActivate = self.paginatorParams['pgToActivate'] 
                print(f"self.pgToActivate = {self.pgToActivate}")



        ## ГРУППОВЫЕ ПЕРЕМЕННЫЕ СОРТИРОВКИ:
        # @@@  self.sortParams - Параметры сортировки, расшифровывающиеся и присваемые ниже
        if "sortParams" in self.kwargs :
            self.sortParams = self.kwargs['sortParams'] 
            # print(f"self.sortParams = {self.sortParams}")

            # Расшифровка и присвоение параметров сортировки, которые сами хранятся в параметре-словаре self.sortParams 
            # @@@ Настройка сортировки по колонкам и их порядку, задаваемые в словаре 
            if "sortCols" in self.sortParams :
                self.sortCols = self.sortParams['sortCols'] 
            else:
                self.sortCols = {}

            # @@@  Флаг запуска сорировки. По умолчанию - False, т.е. без сортировки вообще
            if "sortFlag" in self.sortParams :
                self.sortFlag = self.sortParams['sortFlag'] 
            else:
                self.sortFlag = False

            # @@@  Направление сортировки sortDict['desc'] или self.sortDirection:  False или True. По умолчанию ascending=True
            if "ascTrue" in self.sortParams :
                self.ascTrue = self.sortParams['ascTrue'] 
            else:
                self.ascTrue = True

            # @@@  self.sortColInx индекс колонки для сортировки, если задана. По умолчанию сортировки нет. По умолчанию стоит индекс колонки  = 0
            if "sortColInx" in self.sortParams :
                self.sortColInx = self.sortParams['sortColInx'] 
                self.sortType = 'byIndex'


            # @@@  self.sortColInx индекс колонки для сортировки, если задана. По умолчанию сортировки нет. По умолчанию стоит индекс колонки  = 0
            if "sortColName" in self.sortParams :
                self.sortColName = self.sortParams['sortColName'] 
                self.sortType = 'byName'
            else:
                self.sortColName = ''

        # @@@ Подключить словарь с заданным набором фильтрационных выражений
        if "constFiltExprDic" in self.kwargs :
            self.constFiltExprDic = self.kwargs['constFiltExprDic'] 
            print(f"@@@###$$$*&^ self.constFiltExprDic = {self.constFiltExprDic} / set_cls_vars_from_kwargs_dsourceoutputcube_() of DSourceOutputCube")
        else:
            self.constFiltExprDic = {}


        # # @@@ Получить заданное фильтрационное выражение из словаря с заданным набором фильтрационных выражений self.constFiltExprDic по ключу выражения в словаре
        # if "filtExprDicKey" in self.kwargs :
        #     self.constFiltDic = self.kwargs['constFiltDic'] 
        # else:
        #     self.constFiltDic = {}








    def print_sort_params_(self):
        """
        распечатка параметров сортировки
        Category: Вспомогательные
        """
        print (f"self.sortCols = {self.sortCols}")
        print (f"self.sortFlag = {self.sortFlag}")
        print (f"self.ascTrue = {self.ascTrue}")
        print (f"self.sortColInx = {self.sortColInx}")
        print (f"self.sortColName = {self.sortColName}")



    ## END Внутренние служебные методы класса





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


    def find_func_in_globals_(self, fClassName, funcName):
        """
        @@@ Найти функцию по названию ее класса и имени , находящихся в проекте
        Category: Глобальные функции
        """
        classObj = globals()[fClassName] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        funcObj = getattr(classObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        return funcObj
    
    
    def find_func_in_globals_static_(fClassName, funcName):
        """DSourceOutputCube
        Найти функцию по названию ее класса и имени , находящихся в проекте
        Category: Глобальные функции
        """
        classObj = globals()[fClassName] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        funcObj = getattr(classObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        return funcObj



    def diffirenciate_orig_and_calc_columns_(self):
        """
        @@@ Анализ словаря сотвтетсвий для выводимых в кончном варианте колонок на внешний рессурс. Среди элементов этого словаря могут быть задаваемые вычисляемые колонки
        Поэтому этот словарь должен быть разделен на словарь с оригинальными колонками и словарь с добавляемыми искуственными вычисляемыми колонками для дальнейшей обработки
        Вычислякмые колонки ключами имеют отрицательные негативные порядковые целые числа. Их нужно отфильтровать. На выходе должны быть два словаря: Один с оригинальными
        колонкми, другой - с вычисляемыми и дополняеыми в конце фрейма, псле формирования фрейма с оригинальными колонками. В результате должен быть построен прежный словарь, но 
        с уже вычесленными колонками , их индексами и названиями в комплексе с оргинальными для подачи на выход на внешний рессурс
        Category: Цветовые дифференциаторы
        """
        
        self.origColsAssocTitles_ = {} # @@@ Словарь для настроек по оригинальным выводимым столбцам (временно-служебный)
        self.calcColsAssocTitles_ = {} # @@@ Словарь для настроек вычисляемых искуственных добавляемых столбцов (временно-служебный)

        if len(self.assocTitles) > 0: # Если был передан словарь настроек выводимых колонок на внешний ресурс


            for key, val in self.assocTitles.items(): # Цикл по общему словарю настроек выходных колонок
                pass
                if key > 0 : # Если ключ больше 0, то это оригинальныая колонка и вносим в соотв. временный словарь элемент
                    self.origColsAssocTitles_[key] = val

                elif key<0: # Если ключ меньше 0, то это вычисляемая колонка и вносим ее в соотв. словарь
                    self.calcColsAssocTitles_[key] = val



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




    def add_calculated_cols_(self):
        """
        Добавить в конечный фрейм искуственные расчетные коллонки
        Формат настроек колонок такой и парсинг его соотвтетсвующий:
        -1 : 'CALC:Мес выплаты/BondsMainManager.add_col_to_df_for_cupone_date_for_bonds' (более полный пример в описании класса)
        Category: Калькуляторы полей
        """
        
        # Словарь соотвтетствий новых вычисляемых колонок фрейма и функций , на основе которой они расичтываются из существующих колонок
        # addAssocDic = self.calcColsAssocTitles_

        # Добавляем калькулируемые коллонки в соответствии со словарем соотвтетсвий для вычисляемых колонок, найденных в методе diffirenciate_orig_and_calc_columns_(),
        # в конец входного фрейма м запоминаем соотвтетсвия их новых индексов в общем фрейме с уже добавленными вычисляемыми колонками

        self.newInxColsNamesAssocDic_ = {} # Словарь соотвтетвий новых индексов вычисляемых колонок в общем фрейме и их задаваемых названий
        for key, val in self.calcColsAssocTitles_.items(): # Цикл по словарю соответствий вычисляемых колонок

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
            oFunc = self.find_func_in_globals_(className, funcName)

            # <ЗАПУСК> спец функции добавления вычисляемой этой же функцией колонки в конец входного общего фрейма
            newColInx = oFunc(self.dfInput, newColName, **self.kwargs)

            # @@@ Запоминаем какая новая колонка с именем находится по какому адресу в общем фрейме, после добавления колонки в общий фрейм, для будущего замещения в словаре соотвтетсвий изначальном
            self.newInxColsNamesAssocDic_[newColInx] = newColName 

        # print(f"$$$$#####@@@@@ self.newInxColsNamesAssocDic_ = {self.newInxColsNamesAssocDic_}")    

        # 2. Замещаем элементы для калькулируемых колонок в установочном словаре соответствий настроек выходных столбцов таблицы , которые хранятся в self.assocTitles, 
        # теперь уже нормальными стандартными элементами с индексом и названиями новых вычисляемых колонок. И они будут в необходимой задаваемой последовательности при этом
        newDic = {} # Новый словарь, где будет создаваться копия порядка исходного словаря, но с замещенными элементами, в которых были калькулируемые поля
        for keySetting, valSetting in self.assocTitles.items(): # Цикл по изначальному словарю настроек выходных колонок таблицы

            flagFound = -1 # Флаг нахождения поля в словаре фиксации newInxColsNamesAssocDic_
            for keyCalc, valCalc in self.newInxColsNamesAssocDic_.items(): # Цикл по словарю соотвтетсвий новых колонок в общем фрейме

                if valCalc in valSetting: # Если название новой калькулируемой колонки находится в знаении исходного настроечного словаря колонок, то то вносим элемент из словаря новых колонок
                    newDic[keyCalc] = valCalc
                    flagFound = 1 # Если совпадение найдено

            if flagFound < 0: # Если не найдено поле в словаре фиксации newInxColsNamesAssocDic_,  то вносим старое значение из исходного словаря
                newDic[keySetting] = valSetting


        # @@@ Присваиваем вновь сформированный словарь соотвтетсвий в собственную переменную, отвечающую за формирвоание названий и последовательности выходных колонок
        self.assocTitles = newDic

        # print(f"$$$$#####@@@@@ self.assocTitles = {self.assocTitles}")   


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







    def print_df_output_to_excel_(self, filePath):
        """
        Распечатать dfOutput в эксел filePath
        Не будет работать  Выключен модуль из импорта
        РАссмтаривать как заготовку. Надо проверять работу импорта uno класса lo_office.py. Этот UNO не импортируется нормально. Возможно, есть новые способы
        ~ https://pypi.org/project/uno/
        ~ http://www.openoffice.org/udk/python/python-bridge.html
        ~ http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html {LIBRE_OFFICE_LIBS_}
        Category: Распечатки
        """
        indxFlag = False
        startCell = [3,2]
        # LibreCalcPandasDB.write_from_df_to_exel_pandas(self.dfOutput, filePath, indxFlag, startCell)


    @staticmethod
    def print_df_output_to_excel_static(df, filePath):
        """
        DSourceOutputCube
        Распечатать dfOutput в эксел filePath через статичный метод
        Не будет работать  Выключен модуль из импорта
        РАссмтаривать как заготовку. Надо проверять работу импорта uno класса lo_office.py. Этот UNO не импортируется нормально. Возможно, есть новые способы
        ~ https://pypi.org/project/uno/
        ~ http://www.openoffice.org/udk/python/python-bridge.html
        ~ http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html {LIBRE_OFFICE_LIBS_}
        Category: Распечатки
        """
        indxFlag = False
        startCell = [3,2]
        # LibreCalcPandasDB.write_from_df_to_exel_pandas(df, filePath, indxFlag, startCell)




    # END ВЫЧИСЛЯЕМЫЕ ДОБАВОЧНЫЕ КОЛОНКИ





if __name__ == '__main__':
    pass



    # # ПРОРАБОТКА: более гибкой фильтрации

    # from project_bonds_html.projr.classes.sys_algorithms import SysAlgorithms # НЕ ПЕРЕНОСИТЬ отсюда!!!(этот import д.б. внутри функции)

    # # 1. Получение фрейма облигаций в разрезе рейтингов fapvdo

    # dsocFapvdoBonds = SysAlgorithms.a_015_get_bonds_under_raiting_fapvdo()
    # dfFapvdoBonds = dsocFapvdoBonds.genDf

    # query = ''

    # dfFapvdoBonds = dfFapvdoBonds.query('raiting_fapvdo.str.contains("A")', engine='python')

    # print(f"dfFapvdoBonds = \n{dfFapvdoBonds}")














    # # ПРОРАБОТКА: добавление расчетных колонок


    # db_proc = SqlitePandasProcessor(DB_BONDS_)
    # dataSrcFrame = db_proc.read_table_by_sql_to_df_pandas(TB_BONDS_CURRENT_) # Фрейм

    # # Pars pagination
    # paginatorParams = {}
    # paginatorParams['paginGenSet'] = PAGIN_BONDS_CURR_SET_  # Общие параметры пагинатора
    # paginatorParams['pgToActivate'] = 1  # Общие параметры пагинатора
    # # paginatorParams['paginFlag'] = False  # Общие параметры пагинатора

    # # Pars выборки по колонкам и их названия:
    # # При подставлении assocTitles дальнейшие опреации по фильтрации и сортировки проводятся уже по новым названиям колонок
    # assocTitles = COLS_ASSOC_FOR_BONDS_TYPE01_

    # dsocBondsCurrent = DSourceOutputCube(dataSrcFrame, paginatorParams = paginatorParams, assocTitles = assocTitles) # Создание обьекта класса 


    # print(dsocBondsCurrent.dfInput)
    # print(dsocBondsCurrent.newInxColsNamesAssocDic_)







    # # ПРОРАБОТКА: Фильтрация фрейма через query с комплексными названиями колонок  <РАБОТАЕТ>


    # db_proc = SqlitePandasProcessor(DB_BONDS_)
    # dataSrcFrame = db_proc.read_table_by_sql_to_df_pandas(TB_BONDS_CURRENT_) # Фрейм

    # # Pars pagination
    # paginatorParams = {}
    # paginatorParams['paginGenSet'] = PAGIN_BONDS_CURR_SET_  # Общие параметры пагинатора
    # paginatorParams['pgToActivate'] = 1  # Общие параметры пагинатора
    # # paginatorParams['paginFlag'] = False  # Общие параметры пагинатора

    # # Pars выборки по колонкам и их названия:
    # # При подставлении assocTitles дальнейшие опреации по фильтрации и сортировки проводятся уже по новым названиям колонок
    # assocTitles = COLS_ASSOC_FOR_BONDS_TYPE01_

    # dsocBondsCurrent = DSourceOutputCube(dataSrcFrame, paginatorParams = paginatorParams, assocTitles = assocTitles) # Создание обьекта класса 

    # # Перед фильтрацией форматируем колонку colName из стринга в флоат с очисткой от ненужных символов строковых
    # dsocBondsCurrent.dfOutput  = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dsocBondsCurrent.dfOutput, 'Тек.цена')

    # # print(f"dsocBondsCurrent.paginator.dfLimByPgNumb = \n{dsocBondsCurrent.paginator.dfLimByPgNumb}" )


    # df = dsocBondsCurrent.dfOutput

    # dfFiltered = df.query("`Тек.цена` < 100")

    # print(f"dfFiltered= \n{dfFiltered}" )




    # # ПРОРАБОТКА : фильтрации фрейма по передаваемым параметрам фильрации filtParams <РАБОТАЕТ>

    # db_proc = SqlitePandasProcessor(DB_BONDS_)
    # dataSrcFrame = db_proc.read_table_by_sql_to_df_pandas(TB_BONDS_CURRENT_) # Фрейм

    # # Pars pagination
    # paginatorParams = {}
    # paginatorParams['paginGenSet'] = PAGIN_BONDS_CURR_SET_  # Общие параметры пагинатора
    # paginatorParams['pgToActivate'] = 1  # Общие параметры пагинатора
    # # paginatorParams['paginFlag'] = False  # Общие параметры пагинатора

    # # Pars выборки по колонкам и их названия:
    # # При подставлении assocTitles дальнейшие опреации по фильтрации и сортировки проводятся уже по новым названиям колонок
    # assocTitles = COLS_ASSOC_FOR_BONDS_TYPE01_

    # # Pars фильтрации:
    # colName = 'ГКД'
    # filtParams = {}
    # filterCondsDic = {'_ampers_' : [[colName, '>', 8], [colName, '<', 10]]}

    # dsocBondsCurrent = DSourceOutputCube(dataSrcFrame, paginatorParams = paginatorParams, assocTitles = assocTitles) # Создание обьекта класса 

    # # Перед фильтрацией форматируем колонку colName из стринга в флоат с очисткой от ненужных символов строковых
    # dsocBondsCurrent.dfOutput  = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dsocBondsCurrent.dfOutput, 'ГКД')

    # dsocBondsCurrent.filter_frame(filterCondsDic)


    # print(f"dsocBondsCurrent.paginator.dfLimByPgNumb = \n{dsocBondsCurrent.paginator.dfLimByPgNumb}" )














    # # ПРИМЕР: Проработка класса


    # # # Разные типы источников данных для тестирования и подачи на вход коструктора класса
    # # dataSrclist = [['dfsdf', 'sd']] # Список
    # # srcListTitles = ['Title1', 'Title2'] # Названия колонок для списка

    # # dataSrcTbname = TB_BONDS_CURRENT_ # Название таблицы
    # # dataSrcSQL = 'SELECT * FROM comps_descr' # SQL

    # db_proc = SqlitePandasProcessor(DB_BONDS_)
    # dataSrcFrame = db_proc.read_table_by_sql_to_df_pandas(TB_BONDS_CURRENT_) # Фрейм


    # # Pars pagination
    # paginatorParams = {}
    # paginatorParams['paginGenSet'] = PAGIN_BONDS_CURR_SET_  # Общие параметры пагинатора
    # paginatorParams['pgToActivate'] = 1  # Общие параметры пагинатора
    # # paginatorParams['paginFlag'] = False  # Общие параметры пагинатора

    # dsocBondsCurrent = DSourceOutputCube(dataSrcFrame, paginatorParams = paginatorParams) # Создание обьекта класса 

    # print(dsocBondsCurrent.paginator.dfLimByPgNumb)










    # # ПРИМЕР: Работа с обьектом TableDbdfOutput ()

    # # Разные типы источников данных для тестирования и подачи на вход коструктора класса
    # dataSrclist = [['dfsdf', 'sd']]
    # srcListTitles = ['Title1', 'Title2']
    # dataSrcTbname = 'comps_descr'
    # dataSrcSQL = 'SELECT * FROM comps_descr'
    # db_proc = SqlitePandasProcessor(DB_BONDS_)
    # dataSrcFrame = db_proc.read_table_by_sql_to_df_pandas('comps_descr')

    # # Обьект класса TableDbdfOutput !!!
    # dbTabOutput = TableDfOutputCube(DB_BONDS_, dataSrcSQL, paginGenSet = PAGIN_BONDS_CURR_SET_)


    # # Работа с пагинатором
    # paginator = dbTabOutput.paginator
    # firstPgDf = dbTabOutput.paginator.dfLimByPgNumb
    # db_proc.print_df_gen_info_pandas_IF_DEBUG(dbTabOutput.paginator.dfLimByPgNumb, True, dfId = 'genDf', srcId = '')
    # pg = 5
    # paginator.set_curr_active_obj_paginator(pg)
    # db_proc.print_df_gen_info_pandas_IF_DEBUG(dbTabOutput.paginator.dfLimByPgNumb, True, dfId = 'genDf', srcId = '')



    # # Работа с сортировкой























