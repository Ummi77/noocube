
from noocube.bonds_main_manager import BondsMainManager
from markupsafe import Markup
from noocube.re_manager import ReManager
from noocube.local_manager_BH import LocalManager
import noocube.funcs_general as FG
from noocube.switch import Switch 
from noocube.html_manager_django import HTMLSiteManagerJango
from noocube.settings import DB_BONDS_, DEBUG_
from noocube.dsource_output_cube_v2 import DSourceOutputCube
from noocube.files_manager import FilesManager
from noocube.re_manager import ReManager
from noocube.re_constants import *
from noocube.text_parser import TextParser
from noocube.settings import * 
import pandas as pd

# from noocube.funcs_general_class import FunctionsGeneralClass


class DsTableOutputCube():
    """ЗАГОТОВКА: Использовать весто него класс ViewTableCube in /home/ak/projects/3_Proj_Bonds_HTML_Center/project_bonds_html/projr/classes/view_table_cube.py
     НЕ ДОВЕДЕН ДО УМА. Поэтому еще статус ЗАГОТОВКА у view_table_cube.py. Поэтому пока использовать этот класс
    
    Класс обслуживающий view Фласка - Flask View Table Manager, который реайлизует какой-нибудь !!!!алгоритм!!! <это - не собственный обьект, а РЕАЛИЗАТОР АЛГОРИТМА>,
    в котором на выходе обязательно должен быть обьект класса  !!! DSourceOutputCube !!! -
    содержащий в себе уже полность. подготовленный фрейм для вывода на внешний ресурс. В котором уже произведены все неободимые поиски, фильтрации, сортировки и т.д. 
    Настройка поиска , фильтрации, сортировки и пр. производится до активации обьекта данного класса, путем настройки генеральных параметров обьекта класса FViewTableManager.genParams
    Алгоритм может принимать параметры сортировки, поимка, фильтрации и пр. в виде передаваемого на его вход FViewTableManager.genParams !!!
    То есть, для реализации данного класса необходим готовый алгоритм, на вход которого пода.тся параметры и он выдает в результате конечный обьект класса DSourceOutputCube,
    в котором все уже готово для вывода. Сам этот класс не производит никаких операций с сортировкой, поиском,фильтрацией

    self.prepareTableHtmlFunc - отвечает за путь к методу, который формирует html-код для выходной таблицы. Задаются в **DTOC_OUT_KWARGS_FUNCS_ в settings.py
    self.columnsToSort - отвечает за список колонок, подлежащих сортировке. Задаются в **DTOC_OUT_KWARGS_FUNCS_ в settings.py. Если не заданы, то не будет сортировки

    """

    def __init__(self, dsInput : DSourceOutputCube, **tkwargs):
    
        # Входной источник данных (пока в формате DSourceOutputCube)
        self.dsInput = dsInput
        self.dfPage = self.dsInput.dfActivePageFrameCell
        
        #  Кол-во записей в выходном фрейме
        self.qnDf = len(self.dsInput.df)
        
        # HTML -темплейт, на основе которого строится код выходной таблицы для сайта. В нем задаются классы, стили и пр в тэгах. Анализируются первые тэги в таблице - 
        # первая строка, и столбцы в первой строке (ПОДХОД для дальнейшего развития и детализации составления выходнйо таблицы на основе html-шаблона)
        if 'cubeTableTemplFile' in tkwargs:
            self.cubeTableTemplFile = tkwargs['cubeTableTemplFile']
        else:
            self.cubeTableTemplFile = ''

        # url для текущего view и текущей страницы сайта (нужен при формировании ссылок в заголовках таблицы, нужно оптимизировать, то есть оходится без этого аргумента)
        if 'url' in tkwargs:
            self.url = tkwargs['url']
        else:
            self.url = ''
        
        # Название модуля (приложения, application)
        if 'appName' in tkwargs:
            self.appName = tkwargs['appName']
        else:
            self.appName = ''
        
        # View в котором создается обьект класса DsTableOutputCube
        if 'appView' in tkwargs:
            self.appView = tkwargs['appView']
        else:
            self.appView = ''
            
        # Соварь текущего request с сайта
        if 'urlsArgsMatrix' in tkwargs:
            self.urlsArgsMatrix = tkwargs['urlsArgsMatrix']
            
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
            
        # Аргументы для исключения из строки-ссылки в названии колонки при сортировке
        if 'excludeUrlArgsForSort' in tkwargs:
            self.excludeUrlArgsForSort = tkwargs['excludeUrlArgsForSort']
        else:
            self.excludeUrlArgsForSort = []
            
        # Аргументы для исключения из строки-ссылки  при пагинации, если нужны
        if 'excludeUrlArgsForPagin' in tkwargs:
            self.excludeUrlArgsForPagin = tkwargs['excludeUrlArgsForPagin']
        else:
            self.excludeUrlArgsForPagin = []
            
            
        # Колонки в таблице, которые подлежат сортировке
        if 'columnsToSort' in tkwargs:
            self.columnsToSort = tkwargs['columnsToSort']
        else:
            self.columnsToSort = []
            
            
        # Задать функцию подготовки таблицы, которая будет отвечать за формирование HTML-кода таблицы на выход
        # Должна задавать полный путь к функции (в видимой или невидимой области - двумя разными методами)
        if 'prepareTableHtmlFunc' in tkwargs:
            self.prepareTableHtmlFunc = tkwargs['prepareTableHtmlFunc']
        else:
            self.prepareTableHtmlFunc = 'DsTableOutputCube.prepare_html_table_code_by_cube_template'
            
            
        # Ширина колонок таблицы в заданных полях таблицы 
        if 'tableColsWidth' in tkwargs:
            self.tableColsWidth = tkwargs['tableColsWidth']
        else:
            self.tableColsWidth = {}      
            
            
            
        # print(f"$$$$$$$$$$$$   %%%%%%%%%%%%%%%%%%%%%%   ************   self.prepareTableHtmlFunc = {self.prepareTableHtmlFunc}")
        # Получить обьект метода, отвечающего за формирование html кода для выходной таблицы
        oFunc = DsTableOutputCube.find_func_in_globals_static_(self.prepareTableHtmlFunc) 
        # Подготовить выходной HTML-код для таблицы на бызе страницы процедурного (прошедшего все процедуры) фрейма
        self.tableCode = oFunc(self)
        
        # Подготовить пагинатор для активной страницы на основе страницы процедурного (прошедшего все процедуры) фрейма
        self.prepare_paginator_html()


    ##  ВСПОМОГАТЕЛЬНЫЕ 
    
    @staticmethod
    def _print_mark(id, func, mark, markVal, prefix):
        """
        DsTableOutputCube
        Вспомогательыня функция для распечатки принт-маркеров
        ПРИМ: Что бы использовать эту вспомогательныую функцию необходимо добвать ее в кажый класс и заменить константные значения className и file на соотвтетсвующие этому классу
        Category: Распечатки
        """
        from noocube.funcs_general_class import FunctionsGeneralClass
        FunctionsGeneralClass.print_any_mark_by_id(
            PRINT_TERMINAL_START_END_FUNCTIONS_,
            id,
            func = func,
            mark = mark,
            markVal = markVal,
            className = 'DsTableOutputCube',
            classFile = '/home/ak/.virtualenvs/my_django_environment/lib/python3.10/site-packages/noocube/ds_table_output_cube_v2.py',
            prefix = prefix
        )
        

    
    @staticmethod
    def find_func_in_globals_static_(methodPath):
        """
        DsTableOutputCube +
        Найти функцию по названию ее класса и имени , находящихся в проекте
        Category: Глобальные функции
        """
        
        parts = methodPath.split('.') # Делим на Класс и название функции , которая создает вычисляемую колонку
        className = parts[0] # Название класса
        funcName = parts[1] # Название функции
        # res = (className, funcName)
        
        classObj = globals()[className] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        funcObj = getattr(classObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        return funcObj

        # END ВСПОМОГАТЕЛЬНЫЕ 
    
    
    def prepare_html_table_code_type1 (self):
        """
        Формирование кода таблице, основанного на фиксированных дивах в одной td на один ряд tr
        По образцу : ~ https://qna.habr.com/q/607788 !!! РЕШЕНИЕ ПРОБЛЕМЫ С ФИКСАЦИЕЙ ШИРИНЫ КОЛОНОК В BOOTSTRAP
        Category: HTML код мейкеры
        """
        
        # Если есть строки в фрейме,то есть , если есть фрейм
        if isinstance(self.dfPage, pd.DataFrame):
            
            
            # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
            genExcludeListForSort = [
                'sort_col_name',
                'sort_flag',
                'sort_asc',
                'sort_col',
            ]
            
            # Константная суб-строка с аргументами в ссылке сортировки по заголовкам  с вычетом аргументов в спсиках исключениях genExcludeListFoSort и self.excludeUrlArgsForSort
            constUrlArgsPaginLine = HTMLSiteManagerJango.prpare_const_line_from_url_args_matrix_with_exclusions(self.urlsArgsMatrix, genExcludeListForSort)
            
        
        
            tableCode = '<table class="table table-bordered table-striped">'
            # ЗАГОЛОВКИ ТАБЛИЦЫ
            tableCode += '<thead><tr><th class="col-lg-12"><div class="row">'
            for inx, col in enumerate(self.dfPage.columns.tolist()):
                
                # Формирование сортирвки и ее направления для заголовков
                # !!! Если индекс текущей колонки равен колонке, по которой производится сортировка, то только в этом случае меняется направление сортировки. В других колонках он всегда ASC
                if inx == int(self.urlsArgsMatrix['sort_col']): 
                    # Сменить направление сортировки на противоположный
                    if bool(int(self.urlsArgsMatrix['sort_asc'])):
                        sort_asc = 0
                    else:
                        sort_asc = 1
                else:
                    sort_asc = 1
                # Проверка списка заданных колонок, подлежащих сортировке
                if col in self.columnsToSort:    
                    tableCode += f'<div class="col-md-{self.tableColsWidth[inx]}"><a href = "/{self.appName}/{self.appView}?sort_col={str(inx)}&sort_asc={str(sort_asc)}{constUrlArgsPaginLine}">{col}</a></div>'
                else:
                    tableCode += f'<div class="col-md-{self.tableColsWidth[inx]}">{col}</div>'
            tableCode += '</div></th></tr></thead>'
            # END ЗАГОЛОВКИ ТАБЛИЦЫ
            
            # ТЕЛО ТАБЛИЦЫ
            tableCode += '<tbody>'
            # Формирование рядов
            for index, row in self.dfPage.iterrows():
                tableCode += '<tr><td><div class="row">'  
                # Формирование колонок
                for i, col in enumerate(self.dfPage.columns.values.tolist()):
                    tableCode += f'<div class="col-md-{self.tableColsWidth[i]}">{ row.loc[col] }</div>'
                tableCode += '<div class="row"></td></tr>'  
            tableCode += '</tbody></table>'  
            # END ТЕЛО ТАБЛИЦЫ
            
    
        # Если нет фрейма, тогда фрейм , обычно, равен -1
        else:
            tableCode = 'Не найдено ни одной записи'
            
        return  tableCode   
    

    # @staticmethod
    def prepare_html_table_code_by_cube_template (self):
        """Подготовить код выходной конечной таблицы на основе подготовленного ds и на базе cube-теплейтов. Таблица специфических маркеров позволит
        расшифровать cube-темплейт и перевести все в HTML-формат с нужными стилями и оперативным дизайном
        df - DataFrame, источник готовых данных (моэет быть страница данных, если есть пагинация)
        cubeTemplFile - файл с cube-темплейтом
        marksMatrix - словарь со специфическими маркерами, которыми помечен код темлейта и которые помогут системе перевести все в HTML-формат
        ПРИМ: !!! не держит постояннйо ширину колонок в таблице, что очень плохо выглядит
        Category: HTML код мейкеры
        """
        
        tagInnersDic = {}
        
        # A. Парсим тэги таблицы и ее стилей из шаблона
        fm = FilesManager(self.cubeTableTemplFile)
        
        # Парсинг <table>
        fTxt = fm.read_file_data_txt()
        
        tag = 'table'
        innerTagsList = TextParser.get_inside_of_mono_tags_result_dim_in_text_parser(fTxt, tag, 1)
        tagInnersDic[tag] = innerTagsList

        tag = 'div'
        innerTagsList = TextParser.get_inside_of_mono_tags_result_dim_in_text_parser(fTxt, tag, 1)
        tagInnersDic[tag] = innerTagsList

        # H.Определить кол-во <td> в ряду таблицы (или определить кол-во коонок в таблице шаблона по адресу: cubeTemplFile) для простановки размерности анализа колонок в шаблоне 
        tdList, tdQn = TextParser.get_tds_in_first_row_of_tbody_from_table_html(fTxt)
        tag = 'td'
        innerTagsList = TextParser.get_inside_of_mono_tags_result_dim_in_text_parser(fTxt, tag, tdQn)
        tagInnersDic[tag] = innerTagsList
        
        tableCode = f"<div  {tagInnersDic['div'][0]}><table {tagInnersDic['table'][0]}><tr>"
        
        # Если есть строки в фрейме,то есть , если есть фрейм
        if isinstance(self.dfPage, pd.DataFrame):

            # ФОРМИРОВАНИЕ ЗАГОЛОВКОВ
            # Список url-аргументов, которые должны быть исключены по умолчанию при формировании ссылки для сортировке 
            genExcludeListFoSort = [
                'sort_col',  # Колонка, по которой осуществляется сортировка при нажатии на заголовок таблицы
                'sort_asc',
                'sort_flag',
                'sort_col_name'
            ]
            
            # Константная суб-строка с аргументами в ссылке сортировки по заголовкам  с вычетом аргументов в спсиках исключениях genExcludeListFoSort и self.excludeUrlArgsForSort
            constUrlArgsSortLine = HTMLSiteManagerJango.prpare_const_line_from_url_args_matrix_with_exclusions(self.urlsArgsMatrix, genExcludeListFoSort + self.excludeUrlArgsForSort)
            
            for inx, col in enumerate(self.dfPage.columns.tolist()):
                
                # Формирование сортирвки и ее направления для заголовков
                # !!! Если индекс текущей колонки равен колонке, по которой производится сортировка, то только в этом случае меняется направление сортировки. В других колонках он всегда ASC
                if inx == int(self.urlsArgsMatrix['sort_col']): 
                    
                    # Сменить направление сортировки на противоположный
                    if bool(int(self.urlsArgsMatrix['sort_asc'])):
                        sort_asc = 0
                    else:
                        sort_asc = 1

                else:
                    sort_asc = 1
                    
                # Проверка списка заданных колонок, подлежащих сортировке
                if col in self.columnsToSort:    
                    tableCode += f'<th><a href = "/{self.appName}/{self.appView}?sort_col={str(inx)}&sort_asc={str(sort_asc)}{constUrlArgsSortLine}">{col}</a></th>'
                else:
                    tableCode += f'<th>{col}</th>'
                    
            # END ФОРМИРОВАНИЕ ЗАГОЛОВКОВ
                
            # ТЕЛО ТАБЛИЦЫ
            
            tableCode += '</tr>'
    
            for index, row in self.dfPage.iterrows():
                tableCode += '<tr>'  
                for i, col in enumerate(self.dfPage.columns.values.tolist()):
                    
                    if i < len(tagInnersDic['td']): # Если текущий индекс меньше размерности списка содержимого порядковых тэгов в tagInnersDic['td'], то проставляем стили и классы и пр. в текущем тэге
                        tableCode += f"<td {tagInnersDic['td'][i]}>{ row.loc[col] }</td>"
                    else: # Иначе просто тэг без наполнения внутренности
                        tableCode += f"<td>{ row.loc[col] }</td>"
                        
                tableCode += '</tr>'  
                
            tableCode += '</table></div>'  
            
            # END ТЕЛО ТАБЛИЦЫ
            
        # Если нет фрейма, тогда фрейм , обычно, равен -1
        else:
            tableCode = 'Не найдено ни одной записи'
            
        return tableCode
    
        
        
    
    
    def prepare_paginator_html(self): 
        """
        Подготовить текущий пагинатор на основе текущей активной страницы
        Category: HTML код мейкеры
        """
        
        
        
        # Если есть строки в фрейме,то есть , если есть фрейм
        if isinstance(self.dfPage, pd.DataFrame):
            
            # Список url-аргументов, которые должны быть исключены по умолчанию при формировании ссылки для пагинации 
            genExcludeListFoPagin = [
                'pg',   
                'sort_flag',
                'sort_col_name'
            ]
            
            # Константная суб-строка с аргументами в ссылке сортировки по заголовкам  с вычетом аргументов в спсиках исключениях genExcludeListFoSort и self.excludeUrlArgsForSort
            constUrlArgsPaginLine = HTMLSiteManagerJango.prpare_const_line_from_url_args_matrix_with_exclusions(self.urlsArgsMatrix, genExcludeListFoPagin + self.excludeUrlArgsForPagin)
            
            pState = self.dsInput.paginator.curr_paginator_state_dict
            paginator = f"""
            <div class="pagination">
            <a href="{self.url}?pg=1{constUrlArgsPaginLine}">В начало</a>
                <a href="{self.url}?pg={pState['prevBlockPageToActivate']}{constUrlArgsPaginLine}">&laquo;</a>"""
                
            
            for pg in pState['pagesList']:
                if pg == pState['pgToActivate']:
                    paginator += f'<a class="active">{pg}</a>'
                else:
                    paginator += f'<a href="{self.url}?pg={pg}{constUrlArgsPaginLine}">{pg}</a>'

                    
            paginator += f"""        
                <a href="{self.url}?pg={pState['nextBlockPageToActivate']}{constUrlArgsPaginLine}">&raquo;</a>
            </div>
            """
            
            self.paginatorHtml = paginator
            # print(f"$$$$$$$$ **********   @@@@@@@@@@   self.paginatorHtml = {self.paginatorHtml}")
        # Если нет фрейма, тогда фрейм , обычно, равен -1
        else: 
            self.paginatorHtml = ''
    
        
        
    
    


    def get_fcalss_fname_from_str_alg_infor_(self):
        """
        @@@ Парсинг строки вида fClassName.funcName с названием класса и метода алогоритма, который отвечает за формирование фрейма с необходимыми данными для вывода на 
        внешний рессурс в виде таблицы
        Category: Парсинг
        """
        parts = self.dsInputData.split('.') # Вычисление названий класса в которой находится АИФП и  имени атомарной поисковой функции
        self.fClassName = parts[0] # названий класса в которой находится АИФП 
        self.funcName = parts[1] # имени атомарной поисковой функции


    def find_func_in_globals_(self, fClassName, funcName):
        """
        @@@ Найти функцию по названию ее класса и имени , находящихся в проекте
        Category: Глобальные функции
        """
        self.algClassObj = globals()[fClassName] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        self.algFuncObj = getattr(self.algClassObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call



    def find_func_in_this_class(self, funcName):
        """
        Получить обьект- функцию по названию из данного self класса
        Category: Глобальные функции
        """
        selfClassObj = globals()['FViewTableManager'] 
        selfFuncObj = getattr(selfClassObj, funcName)
        return selfFuncObj




    def binary_pagin_switch_(self):
        """ 
        @@@ Обратный бинарный переключатель направления сортировки для пагинатора
        Category: Пагинация
        """
        # В будущем придумать более продвинутую систему, а то тут голову сломаешь
        if hasattr (self, 'ascStr') and hasattr (self, 'sortFlagByDescDict_') and  hasattr (self, 'chSort'): 
            self.ascBool = self.sortFlagByDescDict_[self.ascStr] 
            if self.chSort == '0': # Если приходит с пагинатора, то надо взять обратное значение тому, что приходит, так как пагинатор не может поменять направление сортировки
                # ascBool = sortFlagByDescDictfvtm_kwargs[ascStr] 
                self.ascBool = FG.binary_switch_bool_var(self.ascBool)  





    def prepare_filt_conds_from_editor_text_(self):
        """
        OBSOLETED. НЕ УДАЛЯТЬ ПОКА. Выясниось, что превращать в словарь условий не нужно. Ведь в редакторе формируется чистый quey для фрейма УЖЕ!!!!
        ПЕРЕНЕСТИ В SQLSintaxer на всякий
        Обработка входящих фильтрационных параметров с сайта для составления стандартного словаря фильтрации для дальнейшей фильтрации выходного фрейма
        Category: Фильтрация
        """


        self.filtEditor = self.filtEditor.replace(' ','')

        logicOperand = None

        # парсинг и анализ фильтр-выражения 
        if 'AND' in self.filtEditor: # Если есть 'AND' значит соединительный операнд - 'AND'
            logicOperand = 'AND'
            ifMultuCond = True # Флаг является ли условие множественным или унитарным
        elif 'OR' in self.filtEditor: # Если есть 'OR' значит соединительный операнд - 'OR'
            logicOperand = 'OR'
            ifMultuCond = True
        else:
            ifMultuCond = False


        if logicOperand: # Если есть логический операнд AND или OR, это значит что условие - множественное и разбиваем его на части по операнду как делиметру
            filtExprParts =  self.filtEditor.split(logicOperand)
        else: # Иначе выражение в редакторе - унитарное, разбивать на части ничего не надо и просваиваем выражение в список filtExprParts полностью как один из элементов условия
            filtExprParts = [self.filtEditor]


        condsList = [] # значение словаря в списке

        for fPart in filtExprParts:

            # Определяем арифм оператор
            if '>' in fPart:
                arithmOperator = '>'
            elif '<' in fPart:
                arithmOperator = '<'
            elif '==' in fPart:
                arithmOperator = '=='
            elif '!=' in fPart:
                arithmOperator = '!='
            elif '>=' in fPart:
                arithmOperator = '>='
            elif '<=' in fPart:
                arithmOperator = '<='
            elif 'in' in fPart:
                arithmOperator = 'in'
            else: # инае оператор не найден и значит выражение составлено неправилльно
                arithmOperator = None


            if arithmOperator: # Если в строке условий найден арифм.оператор, то формируем стандартное условие для словаря условий:
                colAndVal = fPart.split(arithmOperator)

                # ФОРМИРОВАНИЕ ЭЛЕМЕНТА УСЛОВИЯ !!!
                # Проверяем было ли число обернуто в скобки, если это число. И если находим число обернутое в кавычки !!! одинарнае !!!, то это - стринг, а не число. 
                if bool(ReManager.find_pos_of_element_in_single_quotes(colAndVal[1])): 
                    condElement = [colAndVal[0], arithmOperator, colAndVal[1].strip('\'')] # Значение одного элемента условия в списке. Убираем одни кавычки, иначе получаеются кавычки в кавычках
                #TODO: Нужен elif для определения, а число ли эо вообще обернуто в скобки или стринг
                else: # В ином случае число не было обернуто в кавычки !!! одинарнае !!! и значит его надо вводить в условие как число float
                    condElement = [colAndVal[0], arithmOperator, float(colAndVal[1])]

                if ifMultuCond: # Если условие множественное, то вносим в двумерный список условий. Если нет, то элемент уже сам является одномерным списков
                    condsList.append(condElement)

        if arithmOperator: # Если в строке условий найден арифм.оператор, то анализируем на множественность и формируем для каждого случая свой тип словаря условий
            if ifMultuCond: # Если условие множественное, то вносим в двумерный список условий.
                filtConds = {logicOperand : condsList}
            else:
                filtConds = {'ONE' : condElement}

            # @@@ Сформированы стандартные условия для фильтрации
            self.filtConds = filtConds

        else: # Если в строке условий найден арифм.оператор
            self.filtConds = {}
            print (f"Условия филььтрации не сформированы, так как скорее всего было введено неправильное выражение в редакторе")




    ## END СЛУЖЕБНЫЕ







if __name__ == '__main__':
    pass



