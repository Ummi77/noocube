
from pandas import DataFrame
from noocube.bonds_main_manager import BondsMainManager
from markupsafe import Markup
from noocube.re_manager import ReManager
from project_bonds_html.projr.classes.local_manager_BH import LocalManager
# from project_bonds_html.projr.classes.pandas_manager import PandasManager
# from bonds.sql_syntaxer import SQLSyntaxer
import noocube.funcs_general as FG
from bonds.switch import Switch 
# from project_bonds_html.projr.classes.pseudo_request import PseudoRequest
# from project_bonds_html.projr.classes.sys_subblocks import SysSubblocks
# from project_bonds_html.projr.classes.output_pandas_manager import OutputPandasManager
# from project_bonds_html.projr.classes.sys_algorithms import SysAlgorithms
from noocube.dsource_output_cube import DSourceOutputCube
from noocube.html_manager import HTMLSiteManager
from project_bonds_html.projr.settings import COLS_ASSOC_FOR_BONDS_TYPE01_, DB_BONDS_, DEBUG_, PAGIN_BONDS_CURR_SET_
# from project_bonds_html.projr.classes.request_manager import RequestManager


class FViewTableManager():
    """OBSOLETED: Использовать весто него класс ViewTableCube in /home/ak/projects/3_Proj_Bonds_HTML_Center/project_bonds_html/projr/classes/view_table_cube.py
     НЕ ДОВЕДЕН ДО УМА. Поэтому еще статус ЗАГОТОВКА у view_table_cube.py. Поэтому пока использовать этот класс
    
    Класс обслуживающий view Фласка - Flask View Table Manager, который реайлизует какой-нибудь !!!!алгоритм!!! <это - не собственный обьект, а РЕАЛИЗАТОР АЛГОРИТМА>,
    в котором на выходе обязательно должен быть обьект класса  !!! DSourceOutputCube !!! -
    содержащий в себе уже полность. подготовленный фрейм для вывода на внешний ресурс. В котором уже произведены все неободимые поиски, фильтрации, сортировки и т.д. 
    Настройка поиска , фильтрации, сортировки и пр. производится до активации обьекта данного класса, путем настройки генеральных параметров обьекта класса FViewTableManager.genParams
    Алгоритм может принимать параметры сортировки, поимка, фильтрации и пр. в виде передаваемого на его вход FViewTableManager.genParams !!!
    То есть, для реализации данного класса необходим готовый алгоритм, на вход которого пода.тся параметры и он выдает в результате конечный обьект класса DSourceOutputCube,
    в котором все уже готово для вывода. Сам этот класс не производит никаких операций с сортировкой, поиском,фильтрацией

    dsInputData - либо класс и название етода, который расчитывает и возвращает обьект типа DSourceOutputCube. Либо уже готовый обьект DSourceOutputCube
    **kwargs - именованные аргументы для сортировки, пагинации и т.д. фрейма в обьекте  DSourceOutputCube

    !!! Настройка передаваемых параметров перед активацией обьекта viewTbManger, которые передаются для формирования конечного фрейма в обьекте класса DSourceOutputCube при активации viewTbManger
    viewTbManger.genParams['srchParams'] = srchParams
    ПР: 
    srchParams = {}
    srchParams['srchStr'] = srchStr
    srchParams['srchStr'] = "ювелир*"
    srchParams['srchInterpretor'] = interp

    fviewName - название view Фласка
    request - возвращаемый запрос с сайта с параметрами ответа от сервера HTML
    frAlgorithmInfor - стринг формата : fClassName.funcName  -  название класса и название метода этого класса, который отвечает за получение конечного фрейма с данными, 
    для вывода в таблицу на внешнем рессурсе
    После настройки обьекта производится запуск алгоритма методом activate_ . На выходе активации всегда должен приниматься обьект класса DSourceOutputCube, форма фрейма 
    в подготовленном для вывода на внешний рессурс формате, имеющий пагинатор, выборку по странице активной, основной исходный массив -фрейм, из которого формировался обьект этого
    класса
    """

    def __init__(self, fviewName, request, dsInputData, **kwargs):
        
        print(f"START: ViewFlaskManager.Constructor  / ViewName = {fviewName}")

        self.noduleViewName = fviewName # название view Фласка
        self.request = request # возвращаемый запрос с сайта с параметрами ответа от сервера HTML
        self.dsInputData = dsInputData # название класса и название метода этого класса, который отвечает за получение конечного фрейма с данными
        self.kwargs = kwargs # Параметры kwargs, которые передеются в результате на создаваемый обьект DSourceOutputCube, являющийся реализацией заданного алгоритма frAlgorithmInfor
        self.filtQuery = ''
        self.filtIsin = '' # одиночное поле input для isin-фильтрации (по ISIN облигации)
        self.filtBondName = '' # одиночное поле input для filtBondName-фильтрации (по названию облигации)



        # Расшифровываем и присваеваем аргументы-параметры ответа request с HTML-сервера
        if len(self.request) > 0:
            self.get_request_params_()

        # # Инициация собственных переменных, хранящих текущие парметры request, с дефолтными значениями
        self.local_vars_ini_()

        # Обратный бинарный переключатель для пагинатора
        self.binary_pagin_switch_()

        # Формирование параметров для обработки в классе DSourceOutputCube  для формирования необходимой выборки из общего источника данных - фрейма 
        self.set_self_params_()

        # Сформировать собственные kwargs - параметры, то есть те, которые потенциально могут возникнуть в любом из обращении к этому модулю и классу
        self.set_kwargs_params()





    ## СЛУЖЕБНЫЕ


    def activate_(self):
        """
        @@@ Активировать метод - алгоритм, получающий конечный фрейм с данными для вывода в таблицу
        Получает Входной обьект self.dsocInpObj с конечным фреймом, подготовленным для вывода на внешний ресурс с проработанными парметрами , которые были необходимы для 
        фильтрации, сортировки, пагинации или полнотекстового поиска self.genParams, которые передаются вручную перед активацией обьекта данного класса этим методом activate_()
        Category: Вспомогательные
        """

        print(f"&&&&&&&%%%%%%%% dsInputData_TYPE = {self.dsInputData}")
        # Альтернативная активация обьекта FViewTableManager в зависимости от входного источника данных self.dsInputData
        if type(self.dsInputData) == str: # Если входной источник данных (ИВД) задан в виде строки с названием алгоритма, возвращающего обьект DSourceOutputCube

            # Подготовка обьекта - алгоритма, который получает обьект класса DSourceOutputCube со всеми необходимыми данными в конечном фрейме для вывода во внешнюю таблицу
            self.get_fcalss_fname_from_str_alg_infor_() # Парсинг строки вида fClassName.funcName с названием класса и метода алогоритма
            # <АЛГОРИТМ - ФУНКЦИЯ @@@ self.algFuncObj>
            self.find_func_in_globals_(self.fClassName, self.funcName) # Найти функцию по названию ее класса и имени , находящихся в проекте
            
            # <ALGORITHM> ЗАПУСК АЛГОРИТМА @@@
            # Входной обьект с конечным фреймом, подготовленным для вывода на внешний ресурс задаваемым в параметрах алгоритмом self.algFuncObj()
            self.dsocInpObj : DSourceOutputCube = self.algFuncObj(**self.kwargs)  

        elif type(self.dsInputData) == DSourceOutputCube: # Если ИВД задан обьектом DSourceOutputCube

            self.dsocInpObj : DSourceOutputCube = self.dsInputData
        
        
        # @@@ Пагинатор из полученного обьекта класса DSourceOutputCube
        if self.dsocInpObj.paginator:
            self.paginator = self.dsocInpObj.paginator

        # @@@ Выборка из конечного общего фрейма, соотвтествующего активной страницы  пагинатора - 
        if len(self.dsocInpObj.dfOutput) > 0: # Проверка пустоты источника данных
            self.pgFrame = self.paginator.dfLimByPgNumb
        else:
            self.pgFrame = DataFrame()

        self.dfQn = self.dsocInpObj.qn # Кол-во рядов в общем фрейме

        self.genDf = self.dsocInpObj.genDf # Общий начальный массив данных

        # Бинарный переключатель направления сортировки для подачи на шаблоны <!!! Должен стоять после присваивания в параметры его значения для переключения бинарного>
        self.binary_templates_switch_()

        # Формирование параметров для шаблонов
        self.set_templates_params_()

        # Названия колонок для вывода таблицы
        self.titles = self.dsocInpObj.colsOutput

        

    # def activate_from_dsoc_object_ (self, dsocObj):
    #     """@@@ Активировать метод - алгоритм, получающий конечный фрейм с данными для вывода в таблицу
    #     Получает Входной обьект self.dsocInpObj с конечным фреймом, подготовленным для вывода на внешний ресурс с проработанными парметрами , которые были необходимы для 
    #     фильтрации, сортировки, пагинации или полнотекстового поиска self.genParams, которые передаются вручную перед активацией обьекта данного класса этим методом activate_()
    #     """

    #     # <ALGORITHM> ЗАПУСК АЛГОРИТМА @@@
    #     # Входной обьект с конечным фреймом, подготовленным для вывода на внешний ресурс задаваемым в параметрах алгоритмом self.algFuncObj()
    #     self.dsocInpObj : DSourceOutputCube = dsocObj
        
    #     # @@@ Пагинатор из полученного обьекта класса DSourceOutputCube
    #     if self.dsocInpObj.paginator:
    #         self.paginator = self.dsocInpObj.paginator

    #     # @@@ Выборка из конечного общего фрейма, соотвтествующего активной страницы  пагинатора - 
    #     self.pgFrame = self.paginator.dfLimByPgNumb

    #     self.dfQn = self.dsocInpObj.qn # Кол-во рядов в общем фрейме

    #     self.genDf = self.dsocInpObj.genDf # Общий начальный массив данных

    #     # Бинарный переключатель направления сортировки для подачи на шаблоны <!!! Должен стоять после присваивания в параметры его значения для переключения бинарного>
    #     self.binary_templates_switch_()

    #     # Формирование параметров для шаблонов
    #     self.set_templates_params_()

    #     # Названия колонок для вывода таблицы
    #     self.titles = self.dsocInpObj.colsOutput





    def local_vars_ini_(self):
        """
        Инициализация переменных класса, если они не имеют значения по каким-либо причинам
        Category: Вспомогательные
        """

        # # Инициация параметров в собственных переменных с дефолтными значениями
        if hasattr(self, 'pg') :
        
            if self.pg =='' or self.pg == None: # дефолтная страница к активации
                self.pg = 1
            else:
                self.pg = int(self.pg)

        if hasattr(self, 'ascStr') :
            if self.ascStr =='' or self.ascStr == None:  # Дефолтное направление сортировки asc
                self.ascStr = '1'

        if hasattr(self, 'chSort') :
            if self.chSort =='' or self.chSort == None:  # Дефолтное значение флага включения направление сортировки asc
                self.chSort = '0'

        if hasattr(self, 'sortCol') :
            if self.sortCol =='' or  self.sortCol == None:
                self.sortCol ='0'

            if 'sortCol' in self.kwargs:
                self.sortCol =  self.kwargs['sortCol']

        # КОНСТАНТА. Словарь соотвтетсвий стрингового флага направления ('1', '0') и их соотвтетствия для параметров (True, False)
        self.sortFlagByDescDict_ = { 
            '1' : True,
            '0' : False,
        }

        
        



    def get_fcalss_fname_from_str_alg_infor_(self):
        """
        @@@ Парсинг строки вида fClassName.funcName с названием класса и метода алогоритма, который отвечает за формирование фрейма с необходимыми данными для вывода на 
        внешний рессурс в виде таблицы
        Category: Глобальные функции
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


    def set_kwargs_params(self):
        """
        Сформировать собчтвенные kwargs - параметры, то есть те, которые зависят от каких-то действий и велеичин в этом модуле и будут переданы создаваемому при
        активации обьекту класса DSourceOutputCube в методе activate_()
        Category: Вспомогательные
        """
        if hasattr (self, 'filtExprDicKey'):
            self.kwargs['filtExprDicKey'] = self.filtExprDicKey # Передать через kwargs-параметры ключ для фиксирвоанного словаря выражений фильтрации , получаемый из request

        # !!! Формирование именнованных параметров для всех вариантов манипуляций с данными (сортировка, фильтрация и пр)
        # TODO: ВСЕ ПЕРЕДЕЛАТЬ ЧЕРЕЗ **KWARGS !!!!!
        if hasattr (self, 'paginatorParams'):
            self.kwargs['paginatorParams'] = self.paginatorParams # Присвоить именно для именнованных параметров собственных. Через них передается все.
            
        if hasattr (self, 'sortParams'):
            self.kwargs['sortParams'] = self.sortParams #  для сортировки данных по облигациям
            
        if hasattr (self, 'filtQuery'):
            self.kwargs['filtQuery'] = self.filtQuery  # запрос фильтрации из окошка редактора фильтра
            
        if hasattr (self, 'filtIsin'):
            self.kwargs['filtIsin'] = self.filtIsin  # Isin из input раздела фильтрации (фильтрация по одиночному полю input для фильтрации по ISIN)
            
        if hasattr (self, 'filtBondName'):
            self.kwargs['filtBondName'] = self.filtBondName  # filtBondName из input раздела фильтрации (фил'ascTrue'ьтрация по одиночному полю input для фильтрации по названию облигации)
        # self.kwargs['constFiltExprDic'] = self.filtBondName 

        # ПОИСКОВЫЕ параметры через genParams. Переделыть через **kwargs СДЕЛАТЬ ИХ НАСТРОЙКУ В МОДУЛЕ ВНУТРЕННЕМ !!! FViewTableManager  или глубже
        # print(f"$$%###@#$%%^% self.srchStr = {self.srchStr}")
        # print(f"$$%###@#$@#$%%^% self.interp = {self.interp}")
        srchParams = {}
        if hasattr (self, 'srchStr'):
            srchParams['srchStr'] = self.srchStr
        # srchParams['srchStr'] = "ювелир*"
        if hasattr (self, 'interp'):
            srchParams['srchInterpretor'] = self.interp
        # !!! Настройка передаваемых параметров перед активацией обьекта viewTbManger, которые передаются для формирования конечного фрейма в обьекте класса DSourceOutputCube при активации viewTbManger
        
        self.kwargs['srchParams'] = srchParams # формирование именного параметра для поиска 


        # Словарь соотвтетсвий по индексам колонок в фрейме и названиям колонок выходной таблицы
        if 'monthSrch' in self.kwargs:
            self.kwargs['monthSrch'] = self.kwargs['monthSrch']
        else:
            self.kwargs['monthSrch'] = None




    def set_self_params_(self):
        """
        Установка собственных парметров обьекта класса FViewTableManager
        Category: Вспомогательные
        """
        # PAPS:
        # Pars сортировки: для сортировки данных по облигациям (используется в суб-блоке sb003_3)
        self.sortParams = {}
        if hasattr (self, 'ascBool'):
            self.sortParams['ascTrue'] = self.ascBool  # Установка флага направления сортировки
        self.sortParams['sortCols'] = {} # Установка колонок сортировки
        self.sortParams['sortFlag'] = True # Установка флага сортировки
        if hasattr (self, 'sortCol'):
            self.sortParams['sortColInx'] =  int(self.sortCol) # Начальная колонка для сортировки   
        # sortParams['sortColName'] =  'Купон' # Начальная колонка для сортировки  

        # Pars пагинации: для пагинации конечного фрейма  (используется в суб-блоке sb003_3)
        self.paginatorParams = {}
        self.paginatorParams['paginGenSet'] = PAGIN_BONDS_CURR_SET_  # Общие параметры пагинатора
        if hasattr (self, 'pg'):
            self.paginatorParams['pgToActivate'] = int(self.pg)  # Общие параметры пагинатора



        self.genParams = {}
        if hasattr (self, 'sortParams'):
            self.genParams['sortParams'] = self.sortParams
            
        if hasattr (self, 'paginatorParams'):
            self.genParams['paginatorParams'] = self.paginatorParams



        # Словарь соотвтетсвий по индексам колонок в фрейме и названиям колонок выходной таблицы
        if 'assocTitles' in self.kwargs:
            self.genParams['assocTitles'] = self.kwargs['assocTitles']
        else:
            self.genParams['assocTitles'] = {}



    def set_templates_params_ (self):
        """
        @@@ Установка параметров для подачи на HTML-шаблоны для заголовков таблицы и пагинатора
        Category: Вспомогательные
        """

        # Формирование параметров для передачи на шаблон для вывода данных в таблице
        if len(self.dsocInpObj.dfOutput) > 0: # Проверка пустоты источника данных
            self.dfLimitByPg = self.dsocInpObj.paginator.dfLimByPgNumb  # # Вырезка из общего dFrame на основе заданной странице к активации
        else:
            self.dfLimitByPg = DataFrame()

        self.sortCol = self.dsocInpObj.sortColInx # Колонка сортировки, в запрашиваем с сайта значении по заголовку колонки таблицы 
        self.currPaginator = self.dsocInpObj.paginator # Пагинатор с текущим состоянием




    def binary_pagin_switch_(self):
        """ 
        @@@ Обратный бинарный переключатель направления сортировки для пагинатора
        Category: Аналитические методы
        """
        # В будущем придумать более продвинутую систему, а то тут голову сломаешь
        if hasattr (self, 'ascStr') and hasattr (self, 'sortFlagByDescDict_') and  hasattr (self, 'chSort'): 
            self.ascBool = self.sortFlagByDescDict_[self.ascStr] 
            if self.chSort == '0': # Если приходит с пагинатора, то надо взять обратное значение тому, что приходит, так как пагинатор не может поменять направление сортировки
                # ascBool = sortFlagByDescDictfvtm_kwargs[ascStr] 
                self.ascBool = FG.binary_switch_bool_var(self.ascBool)  


    def binary_templates_switch_(self):
        """
        @@@ Бинарныйй переключатель для параметра сортировки для подачи на HTML-шаблоны
        Category: Аналитические методы
        """
        # # Бинарный переключатель направления сортировки для подачи на шаблоны <!!! Должен стоять после присваивания в параметры его значения доя переключения бинарного>
        if self.chSort == '1':
            self.ascStr, self.ascBool = FG.binary_switch_str_var(self.ascStr)





    def get_request_params_ (self):
        """
        Расшифровать и присвоить необходимые паарметры из request
        @@@ Присвоение собственных переменных
        Category: Вспомогательные
        """
        # Расшифровка request
        self.ascStr = self.request.args.get('ascStr') # Направление сортировки колонки
        self.sortCol = self.request.args.get('sortCol') # Индекс колонки для сортировки
        self.chSort = self.request.args.get('chSort') # Флаг сортировки
        self.pg = self.request.args.get('pg') # Страница к активации нумератора и ,соотвтетственно, выборки из общего массива данных


        # Получение и присвоение поисковых параметров по описанию компаний в табл comps_descr, если они наличиствуют
        if self.request.args.get('srchStr'):
            self.srchStr = self.request.args.get('srchStr') # Параметр шаблонов - поисковая строка
        else:
            self.srchStr = ''

        if self.request.args.get('interp'):
            self.interp = self.request.args.get('interp') # Параметр шаблонов - интерпретатор поисковой строки
        else:
            self.interp = ''

        # @@@ Присвоение параметров фильтрации из request, если они были
        if self.request.args.get('filtQuery'):
            self.filtQuery = self.request.args.get('filtQuery')

        # @@@ Присвоение параметров фильтрации filtIsin, если они были (isin в input раздела фильтрации)
        if self.request.args.get('filtIsin'):
            self.filtIsin = self.request.args.get('filtIsin')
            # print(f"@@@#$@#$   filtIsin = {self.filtIsin} / FViewTableManager in line ~ 307")

        # @@@ Присвоение параметров фильтрации filtBondName, если они были (filtBondName в input раздела фильтрации - фильтрация по названию облигации)
        if self.request.args.get('filtBondName'):
            self.filtBondName = self.request.args.get('filtBondName')


        # @@@ Присвоение параметра ключа для словаря фиксированных выражений фильтрации
        if self.request.args.get('filtExprDicKey'):
            self.filtExprDicKey = self.request.args.get('filtExprDicKey')
        else:
            self.filtExprDicKey = ''




    def set_procedures_for_HTML_tb_col_cells_(self, colProceduresForTbCellHTML):
        """
        @@@ Присваивает необходимые ссылки или прочие процедуры для полей, выводимых на внешний рессурс таблицы, которые формируются в методе html_table_code_for_active_page_(),
        где формируется конечное тело таблицы, выводимой на внешний рессурс
        colProceduresForTbCellHTML - словарь HTML или JavaScript процедур в соотвтетсвии с названиями конечных полей в выходном таблице
        Category: Вспомогательные
        """
        self.colProceduresForTbCellHTML = colProceduresForTbCellHTML







    def html_table_code_for_active_page_standart_(self):
        """
        Сформировать пассивный стандартный (без присваивания HTML или JavaScript процедур ячейкам выходной таблицы) код HTML с данными для страницы пагмнатора
        Если нужны активные ячейки HTML-таблицы, то этот код формируется вручную во вьюхах Flask на основе тела кода данного метода
        Category: HTML код мейкеры
        """
        tableCode = ''
        for index, row in self.pgFrame.iterrows():
            tableCode += '<tr>'  
            for col in self.pgFrame.columns.values.tolist():
                tableCode += f'<td>{ row.loc[col] }</td>'
            tableCode += '</tr>'  
        return tableCode



    def html_table_code_with_color_diff_for_bonds_categ_(self, isinColName):
        """
        Сформировать код HTML с данными для страницы пагмнатора с цветовой дифференциацией
        Category: HTML код мейкеры
        """
        tableCode = ''
        for index, row in self.pgFrame.iterrows():

            # Получение isin ряда
            isin = row.loc[isinColName]
            bondCateg = self.get_bond_category_from_gen_fr_(isin)

            # Анализатор со SWITCH...CASE в зависимости от категории бумаги раскрашиваем бэкгрунд ряда таблицы
            for case in Switch(bondCateg):

                if case('ОФЗ'): 
                    trCls = "table-warning"
                    break

                if case('МУНИЦ'): 
                    trCls = "table-success"
                    break

                if case('КОРП'): 
                    trCls = ""
                    break

                if case(): # default
                    print('Не найдено')
                    break



            tableCode += f'<tr class = "{trCls}">'  
            for col in self.pgFrame.columns.values.tolist():
                
                tableCode += f'<td>{ row.loc[col] }</td>'
            tableCode += '</tr>'  
        return tableCode



    def prepare_table_code_v0(self, totalAgrigate = ''):
        """
        @@@ Подготовить код таблицы последней версии 3
        Возвращает код без безопасности, то есть именно HTML код
        Прим: Пока что очень специализированный, не обобщенный метод
        totalAgrigate - Добавочные ряды с какими-то суммирующими данными итоговыми
        Category: HTML код мейкеры
        """
        # # Названия колонок для вывода таблицы
        # self.titles = self.dsocInpObj.colsOutput
        htmlMngr = HTMLSiteManager()
        # КОНТРОЛЬ РИСКОВ:
        
        bmm = BondsMainManager(DB_BONDS_) 
        #Получить список inn из таблицы raex_comps_withdrawn
        innsWithdrown = bmm.get_inn_list_from_raex_comps_withdrawn()

        #Получить список inn из таблицы raex_comps_withdrawn
        innsBukrupt = bmm.get_inn_list_from_bunkrupt_bonds()
        # print(f"innsBukrupt = {innsBukrupt}")

        tableCode = ''
        for index, row in self.pgFrame.iterrows():

            tbClass = 'table' 
            isin = row['ISIN']
            # print(f"@@@@@############%%%%%%%%%%%%% {isin}")
            strISIN = isin

            # # Выделение рядов таблицы в зависимости от величины в колонке условий, в которой пока предусматриватеся нахождение значения цвета бэкграунда
            trBcgrColor = LocalManager.if_comp_in_raex_comps_withdrawn_tb(row, innsWithdrown) #  Контроль по отозванным по RAEX по inn в списке innsWithdrown
            if trBcgrColor =='White':
                trBcgrColor = LocalManager.if_comp_in_bunkrupt_bonds_tb(row, innsBukrupt, 'ИНН') #  Контроль по банкротам по inn в списке innsBukrupt


            tableCode += f'<tr class = "" bgcolor="{trBcgrColor}"  onclick="mouseclkevt(event,this);">'  + f'<td><input class="form-check-input" type="checkbox" name="inp_{isin}" ></td>'
            for col in self.pgFrame.columns.values.tolist():
                if col == 'ИНН': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    tableCode += f'<td><a href = "/comp_descr?inn={row.loc[col]}" target = "_balnk" >{ row.loc[col] }</a></td>'

                elif col == 'ISIN': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    tableCode += f'<td><a href = "https://smart-lab.ru/q/bonds/{row.loc[col]}/" target = "_balnk" >{ row.loc[col] }</a></td>'

                elif 'HIDDEN' in col:  # Если в имени колонки присутствует маркер 'HIDDEN', то поле не выводится, но наличиствует для какой-то аналитики значит
                    pass

                else: # Иначе обычная ячейка таблицы, пассивная
                    tableCode += f'<td>{ row.loc[col] }</td>'
            tableCode += '</tr>'  


        # Прибавление суммирующих итоговых агрегирующих рядов в таблицу, если они наличествуют в собственной переменной self.summaryRows
        # Их может быть несколько в списке, поэтому - цикл по self.summaryRows
        trAgrigate = '' # Добавочные ряды с какими-то суммирующими данными итоговыми
        for summRow in self.dsocInpObj.summaryRows:
            trAgrigate += summRow

        tableCode += trAgrigate

        self.tablePgBody = Markup(tableCode) # Превращение кода в HTML-вставку (иначе - защищено от вставки непосредственного кода,  а вставляется текст кода)

        return self.tablePgBody




    def prepare_table_code_v1(self, totalAgrigate = ''):
        """
        @@@ Подготовить код таблицы последней версии 3
        Возвращает код без безопасности, то есть именно HTML код
        Прим: Пока что очень специализированный, не обобщенный метод
        totalAgrigate - Добавочные ряды с какими-то суммирующими данными итоговыми
        Category: HTML код мейкеры
        """
        # # Названия колонок для вывода таблицы
        # self.titles = self.dsocInpObj.colsOutput
        htmlMngr = HTMLSiteManager()

        tableCode = ''
        for index, row in self.pgFrame.iterrows():

            tbClass = 'table' 
            isin = row['ISIN']
            # print(f"@@@@@############%%%%%%%%%%%%% {isin}")
            strISIN = isin

            rowBackground = ''
            trCode = f'<tr class = ""  style="@@@background" onclick="mouseclkevt(event,this);">'  + f'<td><input class="form-check-input" type="checkbox" name="inp_{isin}" ></td>'
            # tableCode += f'<tr class = ""  style="background-color:@@COLOR_;" onclick="mouseclkevt(event,this);">'  + f'<td><input class="form-check-input" type="checkbox" name="inp_{isin}" ></td>'
            for col in self.pgFrame.columns.values.tolist():
                if col == 'ИНН': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    trCode += f'<td><a href = "/comp_descr?inn={row.loc[col]}" target = "_balnk" >{ row.loc[col] }</a></td>'

                elif col == 'ISIN': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    trCode += f'<td><a href = "https://smart-lab.ru/q/bonds/{row.loc[col]}/" target = "_balnk" >{ row.loc[col] }</a></td>'

                elif 'HIDDEN' in col:  # Если в имени колонки присутствует маркер 'HIDDEN', то поле не выводится, но наличиствует для какой-то аналитики значит
                    pass

                elif 'COLOR_' in col: # Если есть цветовая расчетная колонка # Цветовая дифференциация 
                    rowBackground = f'background-color:{row.loc[col]};'   

                else: # Иначе обычная ячейка таблицы, пассивная
                    trCode += f'<td>{ row.loc[col] }</td>'

            trCode += '</tr>'  

            trCode = trCode.replace('@@@background', rowBackground)

            tableCode += trCode


        # Прибавление суммирующих итоговых агрегирующих рядов в таблицу, если они наличествуют в собственной переменной self.summaryRows
        # Их может быть несколько в списке, поэтому - цикл по self.summaryRows
        trAgrigate = '' # Добавочные ряды с какими-то суммирующими данными итоговыми
        for summRow in self.dsocInpObj.summaryRows:
            trAgrigate += summRow

        tableCode += trAgrigate

        self.tablePgBody = Markup(tableCode) # Превращение кода в HTML-вставку (иначе - защищено от вставки непосредственного кода,  а вставляется текст кода)

        return self.tablePgBody










    def prepare_table_code_v2(self, totalAgrigate = ''):
        """
        @@@ Подготовить код таблицы последней версии 3
        Возвращает код без безопасности, то есть именно HTML код
        Прим: Пока что очень специализированный, не обобщенный метод
        Category: HTML код мейкеры
        """
        # # Названия колонок для вывода таблицы
        # self.titles = self.dsocInpObj.colsOutput
        htmlMngr = HTMLSiteManager()


        tableCode = ''
        for index, row in self.pgFrame.iterrows():

            tbClass = 'table table-striped' # Оттенение через один
            # isin = row['isin']
            isin = row['ISIN'] # PREV
            # if 'HIDDEN:f7' in self.pgFrame : # Проверка наличия колонки цветовой дифференциации облигаций по категории
            #     trBcgrColor = row['HIDDEN:f7'] 
            # else:
            #     trBcgrColor = 'White'

            # Выделение рядов таблицы в зависимости от величины в колонке условий, в которой пока предусматриватеся нахождение значения цвета бэкграунда
            trBcgrColor = htmlMngr.table_row_color_diff('HIDDEN:f7', row, self.pgFrame)

          

            
            # print(f"@@@@@############%%%%%%%%%%%%% {isin}")
            strISIN = isin
            # isin = 6
            tableCode += f'<tr bgcolor="{trBcgrColor}"  onclick="mouseclkevt(event,this);">'  + f'<td><input class="form-check-input" type="checkbox" id="inp_{isin}" ></td>'
            for col in self.pgFrame.columns.values.tolist():

                # Значение поля по циклу 
                # print(f"###$$$%%% row.loc[col] = {row.loc[col]}")
                
                if row.loc[col] is None or row.loc[col]=='' or str(row.loc[col])=='nan' or row.loc[col]=='NULL': 
                    val = '-'
                else:
                    val = row.loc[col]

                if col == 'ИНН': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    tableCode += f'<td><a href = "/comp_descr?inn={val}" target = "_balnk" >{ val }</a></td>'

                elif col == 'ISIN': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    tableCode += f'<td><a href = "https://smart-lab.ru/q/bonds/{val}/" target = "_balnk" >{ val }</a></td>'

                elif 'HIDDEN' in col:  # Если в имени колонки присутствует маркер 'HIDDEN', то поле не выводится, но наличиствует для какой-то аналитики значит
                    pass

                else: # Иначе обычная ячейка таблицы, пассивная
                    tableCode += f'<td>{ val }</td>'
            tableCode += '</tr>'  


        # Прибавление суммирующих итоговых агрегирующих рядов в таблицу, если они наличествуют в собственной переменной self.summaryRows
        # Их может быть несколько в списке, поэтому - цикл по self.summaryRows
        trAgrigate = '' # Добавочные ряды с какими-то суммирующими данными итоговыми
        for summRow in self.dsocInpObj.summaryRows:
            trAgrigate += summRow

        tableCode += trAgrigate

        self.tablePgBody = Markup(tableCode) # Превращение кода в HTML-вставку (иначе - защищено от вставки непосредственного кода,  а вставляется текст кода)

        return self.tablePgBody





    def prepare_table_code_v3(self, totalAgrigate = ''):
        """
        @@@ Подготовить код таблицы последней версии 3
        Возвращает код без безопасности, то есть именно HTML код
        Прим: Пока что очень специализированный, не обобщенный метод
        Category: HTML код мейкеры
        """
        # # Названия колонок для вывода таблицы
        # self.titles = self.dsocInpObj.colsOutput
        htmlMngr = HTMLSiteManager()

        # КОНТРОЛЬ РИСКОВ:
        #Получить список inn из таблицы raex_comps_withdrawn
        bmm = BondsMainManager(DB_BONDS_) 
        innsWithdrown = bmm.get_inn_list_from_raex_comps_withdrawn()

        #Получить список inn из таблицы raex_comps_withdrawn
        innsBukrupt = bmm.get_inn_list_from_bunkrupt_bonds()

        tableCode = ''
        for index, row in self.pgFrame.iterrows():

            tbClass = 'table table-striped' # Оттенение через один
            # isin = row['isin']
            isin = row['ISIN'] # PREV
            # if 'HIDDEN:f7' in self.pgFrame : # Проверка наличия колонки цветовой дифференциации облигаций по категории
            #     trBcgrColor = row['HIDDEN:f7'] 
            # else:
            #     trBcgrColor = 'White'

            # Выделение рядов таблицы в зависимости от величины в колонке условий, в которой пока предусматриватеся нахождение значения цвета бэкграунда
            trBcgrColor = htmlMngr.table_row_color_diff('HIDDEN:f7', row, self.pgFrame)

            # # Выделение рядов таблицы в зависимости от величины в колонке условий, в которой пока предусматриватеся нахождение значения цвета бэкграунда
            trBcgrColor = LocalManager.if_comp_in_raex_comps_withdrawn_tb(row, innsWithdrown) #  Контроль по отозванным по RAEX по inn в списке innsWithdrown
            if trBcgrColor =='White':
                trBcgrColor = LocalManager.if_comp_in_bunkrupt_bonds_tb(row, innsBukrupt, 'ИНН') #  Контроль по банкротам по inn в списке innsBukrupt

            

            
            # print(f"@@@@@############%%%%%%%%%%%%% {isin}")
            strISIN = isin
            # isin = 6
            rowBackground = ''
            trCode = f'<tr  style="@@@background" onclick="mouseclkevt(event,this);"><td>'   
            trCode += f'<input class="form-check-input" type="checkbox" name="inp_wp_{isin}" value="{isin}">' # Для вноса в пакет индексов
            trCode += f'</td>'
            for col in self.pgFrame.columns.values.tolist():

                # Значение поля по циклу 
                # print(f"###$$$%%% row.loc[col] = {row.loc[col]}")
                
                if row.loc[col] is None or row.loc[col]=='' or str(row.loc[col])=='nan' or row.loc[col]=='NULL': 
                    val = '-'
                else:
                    val = row.loc[col]

                if col == 'ИНН': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    trCode += f'<td><a href = "/comp_descr?inn={val}" target = "_balnk" >{ val }</a></td>'

                elif col == 'ISIN': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    trCode += f'<td><a href = "https://smart-lab.ru/q/bonds/{val}/" target = "_balnk" >{ val }</a></td>'

                elif 'HIDDEN' in col:  # Если в имени колонки присутствует маркер 'HIDDEN', то поле не выводится, но наличиствует для какой-то аналитики значит
                    pass

                elif 'COLOR_' in col: # Если есть цветовая расчетная колонка # Цветовая дифференциация 
                    rowBackground = f'background-color:{row.loc[col]};'  

                else: # Иначе обычная ячейка таблицы, пассивная
                    trCode += f'<td>{ val }</td>'
            trCode += '</tr>'  

            trCode = trCode.replace('@@@background', rowBackground)

            tableCode += trCode

        # Прибавление суммирующих итоговых агрегирующих рядов в таблицу, если они наличествуют в собственной переменной self.summaryRows
        # Их может быть несколько в списке, поэтому - цикл по self.summaryRows
        trAgrigate = '' # Добавочные ряды с какими-то суммирующими данными итоговыми
        for summRow in self.dsocInpObj.summaryRows:
            trAgrigate += summRow

        tableCode += trAgrigate

        self.tablePgBody = Markup(tableCode) # Превращение кода в HTML-вставку (иначе - защищено от вставки непосредственного кода,  а вставляется текст кода)

        return self.tablePgBody




    def prepare_table_code_v4(self, totalAgrigate = ''):
        """
        @@@ Подготовить код таблицы  версии 4 с raidio-buttons
        Возвращает код без безопасности, то есть именно HTML код
        Category: HTML код мейкеры
        """
        # # Названия колонок для вывода таблицы
        # self.titles = self.dsocInpObj.colsOutput
        htmlMngr = HTMLSiteManager()

        # КОНТРОЛЬ НЕГАТИВНЫХ РИСКОВ:
        #Получить список inn из таблицы raex_comps_withdrawn
        bmm = BondsMainManager(DB_BONDS_) 
        innsWithdrown = bmm.get_inn_list_from_raex_comps_withdrawn()
        # print(f"innsWithdrown = {innsWithdrown}")

        #Получить список inn из таблицы raex_comps_withdrawn
        innsBukrupt = bmm.get_inn_list_from_bunkrupt_bonds()

        tableCode = ''
        for index, row in self.pgFrame.iterrows():

            # tbClass = 'table table-striped' 
            tbClass = 'table' 

            isin = row['ISIN']
            # print(f"@@@@@############%%%%%%%%%%%%% {isin}")
            strISIN = isin
            # isin = 6

            # # Выделение рядов таблицы в зависимости от величины в колонке условий, в которой пока предусматриватеся нахождение значения цвета бэкграунда
            trBcgrColor = LocalManager.if_comp_in_raex_comps_withdrawn_tb(row, innsWithdrown) #  Контроль по отозванным по RAEX по inn в списке innsWithdrown
            if trBcgrColor =='White':
                trBcgrColor = LocalManager.if_comp_in_bunkrupt_bonds_tb(row, innsBukrupt, 'ИНН') #  Контроль по банкротам по inn в списке innsBukrupt

            tableCode += f'<tr bgcolor="{trBcgrColor}" class = ""  onclick="mouseclkevt(event,this);">'  + f'<td><input class="form-check-input" type="radio" name = "raidio_bb" value="{isin}" ></td>'
            for col in self.pgFrame.columns.values.tolist():
                if col == 'ИНН': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    tableCode += f'<td><a href = "/comp_descr?inn={row.loc[col]}" target = "_balnk" >{ row.loc[col] }</a></td>'

                elif col == 'ISIN': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    tableCode += f'<td><a href = "https://smart-lab.ru/q/bonds/{row.loc[col]}/" target = "_balnk" >{ row.loc[col] }</a></td>'

                elif 'HIDDEN' in col:  # Если в имени колонки присутствует маркер 'HIDDEN', то поле не выводится, но наличиствует для какой-то аналитики значит
                    pass

                else: # Иначе обычная ячейка таблицы, пассивная
                    tableCode += f'<td>{ row.loc[col] }</td>'
            tableCode += '</tr>'  


        # Прибавление суммирующих итоговых агрегирующих рядов в таблицу, если они наличествуют в собственной переменной self.summaryRows
        # Их может быть несколько в списке, поэтому - цикл по self.summaryRows
        trAgrigate = '' # Добавочные ряды с какими-то суммирующими данными итоговыми
        for summRow in self.dsocInpObj.summaryRows:
            trAgrigate += summRow

        tableCode += trAgrigate

        self.tablePgBody = Markup(tableCode) # Превращение кода в HTML-вставку (иначе - защищено от вставки непосредственного кода,  а вставляется текст кода)

        return self.tablePgBody




    def prepare_view_kwargs(self, **viewSets):
        """
        Подготовить именованные аргументы view
        tbBody - либо код таблицы уже готовый , либо название метода, подготавливающего этот код таблицы 
        Category: Вспомогательные
        """

        bmm = BondsMainManager(DB_BONDS_)
        # request = viewSets['request']
        # reqDic = RequestManager.get_request_as_dict(request)
        
        tbBody = viewSets['tbBody']
        # tbBodyLines = tbBody.split('\n')
        tbBodyN = len(tbBody)


        if len(self.dsocInpObj.dfOutput)>0: # Проверка пустоты
            if tbBodyN <= 100: # Если задано название для метода получения тела таблицы, то получить этот метод по названию
                print(f"tbBodyN = {tbBodyN}")
                fPrepTbBody = self.find_func_in_this_class(tbBody) # Функция для подготовки тела таблицы
                tableCode = fPrepTbBody(self)
                # print(tableCode)

            else: # Иначе только может передеваться само тело таблицы
                print(f"tbBodyN = {tbBodyN}")
                tableCode = tbBody

            tablePgBody = Markup(tableCode)

        else:
            tablePgBody = ''



        # Настройки инициализации параметров viewSets
        
        # Левый навигатор
        if 'leftNavigator' in viewSets:
            leftNavigator = viewSets['leftNavigator']
        else:
            leftNavigator = None

        # Кдасс таблицы
        if 'tbClass' in viewSets:
            tbClass = viewSets['tbClass']
        else:
            tbClass = 'table table-striped'

        # Словарь фиксированных выражений фильтрации 
        if 'constFiltExprDic' in viewSets:
            constFiltExprDic = viewSets['constFiltExprDic']
        else:
            constFiltExprDic = {}

        # Заголовок страницы
        if 'pgTitle' in viewSets:
            pgTitle = viewSets['pgTitle']
        else:
            pgTitle = ''


        if 'monthNavFor' in viewSets:
            monthNavFor = viewSets['monthNavFor']
        else:
            monthNavFor = 1


        # ПОКАЗАТЕЛЬНЫЙ !!!!  Атрибут месяца для фильтрации
        if 'payMonth' in viewSets['reqDic']:
            payMonth = viewSets['reqDic']['payMonth']
        elif 'payMonth' in viewSets:
            viewSets['payMonth']
        else:
            payMonth = ''


        # Иначе дает ошибку в self.viewKwargs ниже , если источник данных пустой
        if len(self.dsocInpObj.dfOutput)>0: # Проверка на пустоту
            pState = self.paginator.curr_paginator_state_dict
        else:
            pState = ''


        if 'ixPkgId' in viewSets['reqDic']:
            ixPkgId = viewSets['reqDic']['ixPkgId']
        else:
            ixPkgId = ''


        if 'browserTitle' in viewSets:
            browserTitle = viewSets['browserTitle']
        else:
            browserTitle = 'ЗАГОЛОВОК БРАУЗЕРА'
            
        # Парметры фильтрации по дате регистрации облигации в БД    
        if 'limDate' in viewSets['reqDic']:
            limDate = viewSets['reqDic']['limDate']
        else:
            limDate = ''
                        



        # END Настройки инициализации параметров viewSets

        # viewTbManger.viewKwargs['dfQn'] = dfQn # Берется из viewTbManger, соотвтетвиенно может быть перенесено внутрь модуля

        self.viewKwargs = {
                'titles' : self.titles,
                'tablePgBody' : tablePgBody,
                # 'tbClass' : tbClass,
                'pState' : pState,
                'view' : self.noduleViewName,
                'pg' : self.pg,
                'dfLimitByPg' : self.pgFrame,
                # 'leftMenu' : oLeftNavigator,
                'ascStr' : self.ascStr,
                'sortCol' : self.sortCol,
                'view' : self.noduleViewName,
                # 'dfQn' : dfQn,
                'filtQuery' : self.filtQuery,
                'filtIsin' : self.filtIsin,
                'filtBondName' : self.filtBondName,
                'filtExprDicKey' : self.filtExprDicKey,
                'dfQn' : self.dfQn,
                'frCols' :list(self.pgFrame),
                'leftMenu' : leftNavigator,
                'tbClass' : tbClass, # Кдасс таблицы
                'constFiltExprDic' : constFiltExprDic, # Словарь фиксированных выражений фильтрации 
                'pgTitle' : pgTitle, # Заголовок страницы
                # Дополнительный верхний горизонтальный навигатор для распределения ссылок фильтрации облигаций по месяцам в рамках расклада по месячным выплатам
                'subTopNav' : bmm.get_top_navigator_by_monthly_payment_bmm(**viewSets),
                'payMonth' : payMonth, # 
                'monthNavFor' : monthNavFor, # 
                'ixPkgId' : ixPkgId, # 
                'browserTitle' : browserTitle,
                'limDate' : limDate

                } 
        
        print(f"**************************$$$$$$$$$$$$$$$$$$$$$$$$$$$$############################## self.viewKwargs = {self.viewKwargs['limDate']}")

        return self.viewKwargs


    def get_bond_category_from_gen_fr_(self, isin):
        """
        Узнать категорию бумаги из общего фрейма (ОФЗ, копоративная, муниципальная)
        Category: Облигации
        """
        dfFound = self.genDf.query(f"isin == '{isin}'")
        bondCateg = dfFound.iloc[0]['f8']
        return bondCateg





    def prepare_filt_conds_from_editor_text_(self):
        """
        OBSOLETED. НЕ УДАЛЯТЬ ПОКА. Выясниось, что превращать в словарь условий не нужно. Ведь в редакторе формируется чистый quey для фрейма УЖЕ!!!!
        ПЕРЕНЕСТИ В SQLSintaxer на всякий
        Обработка входящих фильтрационных параметров с сайта для составления стандартного словаря фильтрации для дальнейшей фильтрации выходного фрейма
        Category: Облигации
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



    

    # ПРОРАБОТКА: составление словаря условий для фильтрации из выражения условий в редакторе

    # filtEditorStr = " ГКД > 7  AND ГКД < '9'"

    # filtEditorStr = filtEditorStr.replace(' ','')

    # # парсинг и анализ фильтр-выражения 
    # if 'AND' in filtEditorStr: # Если есть 'AND' значит соединительный операнд - 'AND'
    #     logicOperand = 'AND'
    #     ifMultuCond = True # Флаг является ли условие множественным или унитарным
    # elif 'OR' in filtEditorStr: # Если есть 'OR' значит соединительный операнд - 'OR'
    #     logicOperand = 'OR'
    #     ifMultuCond = True
    # else:
    #     ifMultuCond = False

    # filtExprParts =  filtEditorStr.split(logicOperand)


    # condsList = [] # значение словаря в списке

    # for fPart in filtExprParts:

    #     # Определяем арифм оператор
    #     if '>' in fPart:
    #         arithmOperator = '>'
    #     elif '<' in fPart:
    #         arithmOperator = '<'
    #     elif '==' in fPart:
    #         arithmOperator = '=='
    #     elif '!=' in fPart:
    #         arithmOperator = '!='
    #     elif '>=' in fPart:
    #         arithmOperator = '>='
    #     elif '<=' in fPart:
    #         arithmOperator = '<='
    #     elif 'in' in fPart:
    #         arithmOperator = 'in'

    #     colAndVal = fPart.split(arithmOperator)

    #     # ФОРМИРОВАНИЕ ЭЛЕМЕНТА УСЛОВИЯ !!!
    #     # Проверяем было ли число обернуто в скобки, если это число. И если находим число обернутое в кавычки !!! одинарнае !!!, то это - стринг, а не число. 
    #     if bool(ReManager.find_pos_of_element_in_single_quotes(colAndVal[1])): 
    #         condElement = [colAndVal[0], arithmOperator, colAndVal[1].strip('\'')] # Значение одного элемента условия в списке. Убираем одни кавычки, иначе получаеются кавычки в кавычках
    #     #TODO: Нужен elif для определения, а число ли эо вообще обернуто в скобки или стринг
    #     else: # В ином случае число не было обернуто в кавычки !!! одинарнае !!! и значит его надо вводить в условие как число float
    #         condElement = [colAndVal[0], arithmOperator, float(colAndVal[1])]

    #     if ifMultuCond: # Если условие множественное, то вносим в двумерный список условий. Если нет, то элемент уже сам является одномерным списков
    #         condsList.append(condElement)

    # if ifMultuCond: # Если условие множественное, то вносим в двумерный список условий.
    #     filtConds = {logicOperand : condsList}
    # else:
    #     filtConds = {'ONE' : condElement}



    # print (f"filtConds = {filtConds}")





    # # ПРИМЕР: Проработка поиска -фильтрации при активации обьекта класса FViewTableManager путем настройки соотвтктсвующих параметров <РАБОТАЕТ>

    # # Pars:
    # genParams = {}
    # genParams['sortParams'] = {}
    # genParams['paginatorParams']  = {} 
    # genParams['assocTitles'] = {}

    # request = PseudoRequest ()
    # frAlgorithmInfor = 'SysAlgorithms.a__004_view_complex_table_with_OFZ_munic_and_corporat_bonds'

    # outTbManager = FViewTableManager('bonds_complex_current', request, frAlgorithmInfor)

    # # ТУТ НАСТРАИВАЮТСЯ ПАРАМЕТРЫ ЛОКАЛЬНЙО ФИЛЬТРАЦИИ-ПОИСКА ПО КОНЕЧНОУ ФРЕЙМУ
    # # Pars фильтрации:
    # colName = 'ГКД'
    # filterCondsDic = {'_ampers_' : [[colName, '>', 8], [colName, '<', 10]]}

    # # Перед активацией присваиваем обьекту outTbManager параметры  фильтрации, если необъходима фильтрация
    # # <ФИЛЬТРАЦИЯ>
    # outTbManager.genParams['filterCondsDic'] = filterCondsDic


    # # <АКТИВАЦИЯ> обьекта (то есть применение параметров поиска, фильтрации, сортировки и пр.) перед активацией
    # outTbManager.activate_() # Активацмя обьеекта

    # dfComplexFiltered = outTbManager.dsocInpObj.dfOutput
    # print(f"dsocBondsCurrent.genDf = {len(dfComplexFiltered)}")











    # # ПРОРАБОТКА: Проблемы с сортировкой стринговых float

    # from bonds.sqlite_pandas_processor import SqlitePandasProcessor
    
    # dfComplexBonds = SysSubblocks.sb004_1 ()

    # dbPandaProc = SqlitePandasProcessor(DB_BONDS_) 

    # #Pars:
    # sortColInx = 5 # Цена

    # dfComplexBondsSort = dbPandaProc.get_df_sorted_by_col_index(dfComplexBonds, sortColInx, True)




    # # ПРИМЕР: Проработка метода поска через query для фрейма get_bond_category_from_gen_fr_ ()

    # # Pars:
    # genParams = {}
    # genParams['sortParams'] = {}
    # genParams['paginatorParams']  = {} 
    # genParams['assocTitles'] = {}

    # request = PseudoRequest ()
    # frAlgorithmInfor = 'SysAlgorithms.a__004_view_complex_table_with_OFZ_munic_and_corporat_bonds'

    # outTbManager = FViewTableManager('bonds_complex_current', request, frAlgorithmInfor)
    # outTbManager.activate_() # Активацмя обьеекта

    # dfComplex = outTbManager.genDf
    # print(f"dsocBondsCurrent.genDf = {len(dfComplex)}")

    # isin = 'SU52002RMFS1'
    # bondsCateg = outTbManager.get_bond_category_from_gen_fr_(isin)
    
    # print(f"bondsCateg = {bondsCateg}")

    # # dfComplexBonds = SysSubblocks.sb004_1 ()





    




