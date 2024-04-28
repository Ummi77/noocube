import sys

sys.path.append('/home/ak/projects/3_Proj_Bonds_HTML_Center/project_bonds_html') # Прописываем path в системную переменную Python, что бы можно было запускать функции из данного модуля напрямую


import bonds.funcs_general as FG
from bonds.bonds_main_manager import BondsMainManager
from project_bonds_html.projr.settings import *
from math import ceil
from bonds.sqlite_bonds_macros import SqliteBondsMacros
from project_bonds_html.projr.classes.bonds_html_main_manager import BondsHTMLMainManager
from project_bonds_html.projr.classes.paginator_2dimlist import Paginator2DimList
from project_bonds_html.projr.classes.request_manager import RequestManager
import pandas as pd

class HTMLSiteManager (): # 
    """ 
    BASE CLASS:  HTMLSiteManager
    Класс для организации динамических компонентов сайта  и прочих вспомогательных функций на разных уровнях
    """

    # Конструктор
    def __init__(self):
        pass



    @staticmethod
    def print_pseudo_request(pseuRequest):
        """
        OBSOLETED: Преернесено в класс самого псевдо-request
        HTMLSiteManager
        Распечатка параметров псевдо-request
        Category: Распечатки
        """

        for key,val in pseuRequest.items():
            print(f"key = {key} : val = {val}")



    @staticmethod
    def print_request(request):
        """
        Распечатка параметров request
        Category: Распечатки
        """
        for key,val in request.items():
            print(f"key = {key} : val = {val}")
    




    # МЕТОДЫ КАЧЕСТВЕННОГО ВЫДЕЛЕНИЯ

    @staticmethod
    def table_row_color_diff (condCol, selTbRow, df, defaultColor = 'White'):
        """
        РАСШИРЯЕМАЯ ФУНКЦИЯ (то есть модифицируемая функция)
        Выделение рядов таблицы в зависимости от величины в колонке условий, в которой пока предусматриватеся нахождение значения цвета бэкграунда
        Но в дальнейшем метод усложняется и может анализировать различные условия вообще. Или даже формулы из нескольких колонок
        Вставочная функция при формировании рядов в таблце HTML
        df - фрейм, по которому идет цикл при формировании рядов HTML таблицы
        selTbRow - обьект Selenium <tr>
        condCol - Название колонки, в котором хранится цвет бэкграунда в задаваемом источнике df
        Бэкграунд ряда выставляется в тэге <tr bgcolor="{trBcgrColor}">
        Category: Цветовые дифференциаторы
        """

        if condCol in df : # Проверка наличия колонки цветовой дифференциации облигаций по категории
            trBcgrColor = selTbRow[condCol] 
        else:
            trBcgrColor = defaultColor

        return trBcgrColor



    @staticmethod
    def table_row_color_diff_by_condition(funcDescr, selTbRow, defaultColors = ['White','Red']):
        """
        РАСШИРЯЕМАЯ ФУНКЦИЯ (то есть модифицируемая функция)
        Выделение рядов таблицы в зависимости от условий, которые формируются в динамической функции dynamicFunc и возвращает True или False
        Вставочная функция при формировании рядов в таблце HTML
        funcDescr - описательная функция, то есть которая формируется на базе названия класса и метода
        defaultColors - список из двух цветов - дефолтного и выделяемого
        selTbRow - обьект Selenium <tr> как входной параметр для динамической функции
        Бэкграунд ряда выставляется в тэге <tr bgcolor="{trBcgrColor}">
        Category: Цветовые дифференциаторы
        """
        
        oFunc = HTMLSiteManager.find_func_in_globals_HM(funcDescr)

        if oFunc(selTbRow)  : # Если динамическая функция выдает True по условиям в этой функции, то выделяем 2м цветом в списке
            trBcgrColor = defaultColors[1] 
        else:
            trBcgrColor = defaultColors[0]  # Иначе - 1м цветом в списке

        return trBcgrColor



    # END МЕТОДЫ КАЧЕСТВЕННОГО ВЫДЕЛЕНИЯ




    # МЕТОДЫ ПОДГОТОВКИ HTML-КОДА ТАБЛИЦ

    @staticmethod
    def prepare_table_code_v5_HM(df, totalAgrigate = ''):
        """
        @@@ Подготовить код таблицы последней версии 6
        Возвращает код без безопасности, то есть именно HTML код
        Прим: Пока что очень специализированный, не обобщенный метод
        totalAgrigate - Добавочные ряды с какими-то суммирующими данными итоговыми
        Category: HTML код мейкеры
        """
        # # # Названия колонок для вывода таблицы
        # # self.titles = self.dsocInpObj.colsOutput
        # htmlMngr = HTMLSiteManager()
        # # КОНТРОЛЬ РИСКОВ:
        # #Получить список inn из таблицы raex_comps_withdrawn
        # bmm = BondsMainManager(DB_BONDS_) 
        # innsWithdrown = bmm.get_inn_list_from_raex_comps_withdrawn()

        tableCode = ''
        for index, row in df.iterrows():

            tbClass = 'table' 
            isin = row['ISIN']
            # print(f"@@@@@############%%%%%%%%%%%%% {isin}") 
            strISIN = isin




            tableCode += f'<tr class = ""   onclick="mouseclkevt(event,this);">'  + f'<td><input class="form-check-input" type="checkbox" name="inp_{isin}" ></td>'
            for col in df.columns.values.tolist():
                if col == 'ИНН': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    tableCode += f'<td><a href = "/comp_descr?inn={row.loc[col]}" target = "_balnk" >{ row.loc[col] }</a></td>'

                elif col == 'ISIN': # Если колонка ИНН, то присваиваем процедуру нажатия ссылки на ячейках этой колонки
                    tableCode += f'<td><a href = "https://smart-lab.ru/q/bonds/{row.loc[col]}/" target = "_balnk" >{ row.loc[col] }</a></td>'

                elif 'HIDDEN' in col:  # Если в имени колонки присутствует маркер 'HIDDEN', то поле не выводится, но наличиствует для какой-то аналитики значит
                    pass

                elif 'Дата покупки' in col:  # Если в имени колонки присутствует маркер 'HIDDEN', то поле не выводится, но наличиствует для какой-то аналитики значит
                     tableCode += f'<td><input type = "hidden" name = "buy_date" value = "{row.loc[col]}">{row.loc[col]}</td>'

                else: # Иначе обычная ячейка таблицы, пассивная
                    tableCode += f'<td>{ row.loc[col] }</td>'
            tableCode += '</tr>'  

            tableBody = tableCode

        return tableBody




    # END МЕТОДЫ ПОДГОТОВКИ HTML-КОДА ТАБЛИЦ





    # ВСПОМОГАТЕЛЬНЫЕ

    @staticmethod
    def popover_ststem_with_combo_set_HM(viewTbManger = None):
        """
        HTMLSiteManager
        Настройки для системы popover для внесения облигаций в индексный пакет
        Category: Облигации
        """

        bmm = BondsMainManager(DB_BONDS_)
        # Фрем с индексными пакетами
        dfPackages = bmm.get_index_packages_BMM(['id', 'nick'])

        if viewTbManger:
            print(f"viewTbManger > None")
            viewTbManger.viewKwargs['dfPackages'] = dfPackages

        return dfPackages
    




    @staticmethod
    def ix_packg_popover_code_prepare():
        """
        HTMLSiteManager
        Создание кода контента popover для внесения облигации в индексный пакет
        Category: Облигации
        """

        # D. Подготовка контента  popover box с индексными пакетами для внесения облигаций в индексы

        bmm = BondsMainManager(DB_BONDS_)
        # Фрем с индексными пакетами
        dfPackages = bmm.get_index_packages_BMM(['id', 'nick'])
        # HTML div с контентом popover box
        popoverContent = """
            <br>
            <div  hidden> <!--  Popover html content  Контент для popover при нажатии на иконку добавления в индексный пакет в таблицах с облигациями-->
            <div data-name="popover-content"  id="popover-content">
                <div class="popover-title">Индексы</div>
                <div class="label_popover_isin" id="label_popover_isin"></div>
                
                            <form id="save_bond_to_index_form">

                            <select class="popover_select" multiple aria-label="multiple select example" id="popover_inx_package" name="popover_inx_package" >"""

        options = ''
        for key,value in dfPackages.iterrows(): # Цикл по индексным пакетам из табл 

            nick = value['nick']
            id = value['id']
            pckNick = bmm.get_nickname_by_inx_package_id_bmm(id) # Ник индексного пакета

            options += f"""<option  onclick="save_row_bond_to_index_AJAX({id},{pckNick},document.getElementById('popover_isin').value)" >{nick} : {id}</option>"""


        popoverEnd = """ </select>
                            <input type = "hidden" name="popover_isin" id="popover_isin" value="" >
                            </form>
            </div>
            </div>
            <br>
        """

        # Присоединяем HTML div of popover content к коду таблицы, как независимого соседствующего тэга, что бы передать и обновить его на страницу через AJAX подключение
        popoverContent += options + popoverEnd 

        return popoverContent


    # END ВСПОМОГАТЕЛЬНЫЕ


    # ПОДОГОТОВКА ПАРАМЕТРОВ 


    @staticmethod
    def prepare_dsoc_kwargs_parameters(**viewSets):
        """
        ЗАГОТОВКА, пока отложена на том, что есть. Возможно ее использование в FViewTableManager для оптимизации кода - все в одном методе, в данном
        HTMLSiteManager
        Подготовка **dsoc_kwargs параметров для активации обьекта класса DSourceOutputCube
        Category: Вспомогательные
        """
        request = viewSets['request']
        reqDic = RequestManager.get_request_as_dict(request) # Словарь аргументов из request

        dsoc_kwargs = {}

        # Обработка возможных необходимых аргументов, которые могут понадобится в разных вьюерах, и занесение их в требуемой форме в **dsoc_kwargs


        # Получение, дефолтная настройка и присвоение поисковых параметров по описанию компаний в табл comps_descr, если они наличиствуют

        # Входные параметры request, переведенные в словарь, которым можно управлять при начальных настройках view
        reqDic = viewSets['reqDic']





        if 'ascStr' in reqDic:
            ascStr = reqDic['pg']  
        else:
            ascStr = '1'


        if 'pg' in reqDic:
            pg = reqDic['pg']  
        else:
            pg = '1'


        if 'chSort' in reqDic:
            chSort = reqDic['chSort']  
        else:
            chSort = '0'


        # Сортировка по колонке
        if 'sortCol' in reqDic:
            sortCol = reqDic['sortCol']  
        else:
            sortCol = viewSets['sortCol']




        # Параметр шаблонов - поисковая строка
        if 'srchStr' in reqDic:
            srchStr = reqDic['srchStr']  
        else:
            srchStr = ''

        # Параметр шаблонов - интерпретатор поисковой строки
        if  'interp' in reqDic :
            interp = reqDic['interp']   
        else:
            interp = ''


        #  Присвоение параметров фильтрации из request, если они были
        if  'filtQuery' in reqDic :
            filtQuery = reqDic['filtQuery']  
        else :
            filtQuery = ''

        #  Присвоение параметров фильтрации filtIsin, если они были (isin в input раздела фильтрации)
        if 'filtIsin' in reqDic   :
            filtIsin = reqDic['filtIsin']  
        else:
            filtIsin = ''

        # Присвоение параметров фильтрации filtBondName, если они были (filtBondName в input раздела фильтрации - фильтрация по названию облигации)
        if 'filtBondName' in reqDic :
            filtBondName = reqDic['filtBondName']   
        else:
            filtBondName = ''


        #  Присвоение параметра ключа для словаря фиксированных выражений фильтрации
        if 'filtExprDicKey' in reqDic :
            filtExprDicKey =  reqDic['filtExprDicKey']   
        else:
            filtExprDicKey = ''

        # Установка флага направления сортировки
        if 'ascBool' in reqDic :
            ascBool =  reqDic['ascBool']   
        else:
            ascBool = True

        # Присвоить искомый месяц в целочисленном варианте из request в fvtm_kwargs, передаваемый в алгоритм
        if 'payMonth' in reqDic  : 
            payMonth =  reqDic['payMonth']   
        else:
            payMonth = ''

        # Параметр для выбора вида ценных бумаг для фильтрации по месцам. В данном варианте для комплесной смеси всех видов бумаг
        # if 'monthNavFor' in reqDic  : 
        #     monthNavFor =  reqDic['monthNavFor']   
        # else:
        #     monthNavFor = ''

        if 'monthNavFor' in viewSets['reqDic']:
            monthNavFor = viewSets['reqDic']['monthNavFor']
        elif 'monthNavFor' in viewSets:
            viewSets['monthNavFor']
        else:
            monthNavFor = ''

        
        # ID индексного пакета 
        if 'ixPkgId' in reqDic:
            ixPkgId = reqDic['ixPkgId']
        else:
            ixPkgId = '1'


        # # Инициация параметров в собственных переменных с дефолтными значениями   
        
        # Pars сортировки: для сортировки данных по облигациям (используется в суб-блоке sb003_3)
        sortParams = {}

        sortParams['ascTrue'] = ascBool  # Установка флага направления сортировки  !!!!!!!!!!! NOT DELETE

        sortParams['sortCols'] = {} # Установка колонок сортировки
        sortParams['sortFlag'] = True # Установка флага сортировки
        sortParams['sortColInx'] =  int(sortCol) # Начальная колонка для сортировки   
        # sortParams['sortColName'] =  'Купон' # Начальная колонка для сортировки  


        # Настройки пагинатора 
        paginatorParams = {} # **kwargs
        paginatorParams['paginGenSet'] = viewSets['paginGenSet']
        paginatorParams['pgToActivate'] = int(pg)  # Общие параметры пагинатора

        # genParams = {}
        # genParams['sortParams'] = sortParams
        # genParams['paginatorParams'] = paginatorParams



        #  настройки **dsoc_kwargs

        # Request параметры HTML- запроса
        dsoc_kwargs['reqDic'] = viewSets['reqDic']

        # Параметры сортировки  !!!!! Вот этот параметр отвечает за сортировку по умолчанию  <DEFAULT SETTING>
        if 'sortCol' in reqDic: # если в словаре request аргументов есть запись с искомым ключем, то
            dsoc_kwargs['sortCol'] = reqDic['sortCol']
        else:
            dsoc_kwargs['sortCol'] = 0 # Если нет, то установка по умолчанию 

        print(f"$$$$$$$$$$$$$$$$$$****************  reqDic = {reqDic}")

        # id индексного пакета
        if 'ixPkgId' in reqDic: # если в словаре request аргументов есть запись с искомым ключем, то
            dsoc_kwargs['ixPkgId'] = reqDic['ixPkgId']

        dsoc_kwargs['paginatorParams'] = paginatorParams # Параметры пагинатора
        dsoc_kwargs['assocTitles'] = viewSets['assocTitles'] # Параметры соответтствия заголовков фрейма


        dsoc_kwargs['filtExprDicKey'] = filtExprDicKey # Передать через kwargs-параметры ключ для фиксирвоанного словаря выражений фильтрации , получаемый из request

        # !!! Формирование именнованных параметров для всех вариантов манипуляций с данными (сортировка, фильтрация и пр)
        # TODO: ВСЕ ПЕРЕДЕЛАТЬ ЧЕРЕЗ **KWARGS !!!!!
        # dsoc_kwargs['paginatorParams'] = paginatorParams # Присвоить именно для именнованных параметров собственных. Через них передается все.

        dsoc_kwargs['sortParams'] = sortParams #  для сортировки данных по облигациям  !!!!!!!!!!!!

        dsoc_kwargs['filtQuery'] = filtQuery  # запрос фильтрации из окошка редактора фильтра
        dsoc_kwargs['filtIsin'] = filtIsin  # Isin из input раздела фильтрации (фильтрация по одиночному полю input для фильтрации по ISIN)
        dsoc_kwargs['filtBondName'] = filtBondName  # filtBondName из input раздела фильтрации (фил'ascTrue'ьтрация по одиночному полю input для фильтрации по названию облигации)
        # self.kwargs['constFiltExprDic'] = self.filtBondName 

        # ПОИСКОВЫЕ параметры через genParams. Переделыть через **kwargs СДЕЛАТЬ ИХ НАСТРОЙКУ В МОДУЛЕ ВНУТРЕННЕМ !!! FViewTableManager  или глубже
        # print(f"$$%###@#$%%^% self.srchStr = {srchStr}")
        # print(f"$$%###@#$@#$%%^% self.interp = {interp}")
        srchParams = {}
        srchParams['srchStr'] = srchStr
        # srchParams['srchStr'] = "ювелир*"
        srchParams['srchInterpretor'] = interp
        # !!! Настройка передаваемых параметров перед активацией обьекта viewTbManger, которые передаются для формирования конечного фрейма в обьекте класса DSourceOutputCube при активации viewTbManger
        dsoc_kwargs['srchParams'] = srchParams # формирование именного параметра для поиска 


        # Словарь соотвтетсвий по индексам колонок в фрейме и названиям колонок выходной таблицы
        if 'monthSrch' in   reqDic:
            dsoc_kwargs['monthSrch'] = reqDic['monthSrch']
        else:
            dsoc_kwargs['monthSrch'] = None


        dsoc_kwargs['payMonth'] = payMonth

        # Параметр для выбора вида ценных бумаг для фильтрации по месцам. В данном варианте для комплесной смеси всех видов бумаг
        dsoc_kwargs['monthNavFor'] = monthNavFor

        dsoc_kwargs['ixPkgId'] = ixPkgId


        # Параметры настройки цифровой дифференциации рядов в выходной таблице, настраиваемые в каждом индивидуальном вьюере при необходимости
        if 'colorColPars' in viewSets:
            dsoc_kwargs['colorColPars'] = viewSets['colorColPars']
        else:
            dsoc_kwargs['colorColPars'] = {}
            
            
        # Парметры фильтрации по дате регистрации облигации в БД
        if 'limDate' in viewSets['reqDic']:
            dsoc_kwargs['limDate'] = viewSets['reqDic']['limDate']
        else:
            dsoc_kwargs['limDate'] = ''
            



        return dsoc_kwargs


    @staticmethod
    def prepare_template_params(dsOutput, viewSets, **dsoc_kwargs):
        """ЗАГОТОВКА
        Подготовка выходных параметров для JinJa темплейта
        fviewTbObj - обьект класса FViewTableManager, возвращающий результаты активированного выходного источника данных на базе задаваемого алгоритма или
        в будущем другие выходные источники
        Category: Вспомогательные
        """

        templateKwargs = {
                # 'titles' : dsOutput.titles,
                # 'tablePgBody' : tablePgBody,
                # # 'tbClass' : tbClass,
                # 'pState' : self.paginator.curr_paginator_state_dict,
                # 'view' : self.noduleViewName,
                # 'pg' : self.pg,
                # 'dfLimitByPg' : self.pgFrame,
                # # 'leftMenu' : oLeftNavigator,
                # 'ascStr' : self.ascStr,
                # 'sortCol' : self.sortCol,
                # 'view' : self.noduleViewName,
                # # 'dfQn' : dfQn,
                # 'filtQuery' : self.filtQuery,
                # 'filtIsin' : self.filtIsin,
                # 'filtBondName' : self.filtBondName,
                # 'filtExprDicKey' : self.filtExprDicKey,
                # 'dfQn' : self.dfQn,
                # 'frCols' :list(self.pgFrame),

                }

        return templateKwargs

    # END ПОДОГОТОВКА ПАРАМЕТРОВ 





    def prepare_ul_checkbox_list_hm (self, dataItter, keyValFieldsList, checkedKeyList = [], **kwargs):
        """ 
        Подготовить  html ul список с чек-боксами по заданному ключевому полю и полю значений в фрейме df
        Если задан спиок checkedKeyList, то если значение key подпадает под множество checkedKeyList, то чек-бокс этого элемента 
        выделяется галочкой
        ПРИМ: Код для использования с JQuery ( не с элементами формы)
        
        dataItter - массив данных  itterable
        keyValFieldsList - Ключевое поле и поле значений последовательноо в списке
        checkedKeyList - значения ключа в списке, по которым чекбоксы должны быть выделены
        
        В именных параетрах могут устанавливаться:
        kwargs['ulClass'] - класс для <ul>
        kwargs['liMarker'] - маркер для унификации класса для элементов списка и чекбоксов
        """
        
        print(f"PR_NC_219 --> START: prepare_ul_checkbox_list_hm()")
        
        #INI
        if 'ulClass' in kwargs:
            ulClass = kwargs['ulClass']
        else:
            ulClass = 'list'
        
        if 'liMarker' in kwargs:
            liMarker = kwargs['liMarker']
        else:
            liMarker = ''
            
        dataKeyField = keyValFieldsList[0]
        dataValueField = keyValFieldsList[1]
            
        # Если массив данных -DataFrame
        if isinstance(dataItter, pd.DataFrame):

            # Если фрейм пустой. то он будет передан в виде -1
            if isinstance(dataItter, int) : 
                outDataBlock = f'Ничего не найдено'
            # иначе - создаем html код со списком чек-боксов по всем статусам. Если задана книга, то статусы этой книги в этом списке необходимо выделить checked
            else:
                
                print(f"PR_NC_220 --> Фрейм - не пустой. Формируем html-код для списка с чекбоксами")
                
                outDataBlock = f'''
                                    <ul class="{ulClass}">
                                '''
                
                for inx, row in dataItter.iterrows():
                    
                    # INI
                    keyFieldVal = row[dataKeyField]
                    valueFieldVal = row[dataValueField]
                    checked =''
                    
                    # Для них чек-боксы нужно выделить как checked
                    if not isinstance(checkedKeyList, int) and keyFieldVal in checkedKeyList:
                        checked = 'checked'
                            
                    
                    # JS148^^
                    outDataBlock += f'''
                                        <li>
                                        <p>
                                        <input type="checkbox" field_value = "{valueFieldVal}"  class="checkboxb_{liMarker}" name="inp_name_{keyFieldVal}" value="{keyFieldVal}" {checked}>
                                        <span class="spn_class_{liMarker}" key_val_{liMarker}="{keyFieldVal}" style="cursor:pointer">{valueFieldVal}</span>
                                        </p>
                                        </li>
                                    '''

                outDataBlock += "</ul>"
            
        print(f"PR_NC_221 --> END: prepare_ul_checkbox_list_hm()")
        
        return outDataBlock








if __name__ == '__main__':
    pass



    # # ПРОРАБОТКА: Получение словаря дифференциатора
    # # htmlMngr = HTMLSiteManager()
    # sysMarker = 'ROW_COLOR_IXPKGS'
    # diffDic = HTMLSiteManager.get_diff_dic_by_marker_name (sysMarker)

    # print(f"diffDic = {diffDic}")


    # # ПРИМЕР: Проверка формирования HTML пагинатора
    # bondsMngr = BondsManagerHTML() # При этом в файле func_general.py в проекте bonds были заблокированы употребление библиотеки pyautogui (почему то не видит ее отсюда)
    # dsBondsCurr = bondsMngr.get_bonds_current () # Массив облигаций с полями в соответствии с таблицей bonds_current    

    # # Paginator settings
    # pagesRowMax  = 5 # максимальное число показа нумерации страниц в ряду
    # dsRowsQnOnPage = 20 # число записей из входного массива, показываемых на одной странице   

    # paginator = Paginator(dsBondsCurr, pagesRowMax, dsRowsQnOnPage)
    # paginator.set_paged_limited_ds(3) # Получение вырезки из обще БД на основе передаваемого номера страницы 
    # dsPgLim = paginator.dsLimByPgNumb

    # htmlMngr = HTMLSiteManager()

    
    # paginatorHTML = htmlMngr.get_paginator_bonds_curr(paginator, 3)

    # print (paginatorHTML)




    # # ПРИМЕР: Получение и использование обьекта класса Paginator
    # bondsMngr = BondsManagerHTML() # менеджер обллигаций
    # dsBondsCurr = bondsMngr.get_bonds_current() # Получение массива текущих облигаций

    # # Paginator settings
    # pagesRowMax  = 5 # максимальное число показа нумерации страниц в ряду
    # dsRowsQnOnPage = 20 # число записей из входного массива, показываемых на одной странице    

    # paginator = Paginator(dsBondsCurr, pagesRowMax, dsRowsQnOnPage)

    # # 1. Показать текущее состояние Пагинатора
    # # paginator.show_curr_paginator_state()
    # # currpaginState = paginator.curr_paginator_state_dict


    # # 2. Получение нового сосотояния пагинатора при смене страницы
    # # paginator.set_paged_limited_ds(2)
    # # currPaginState = paginator.curr_paginator_state_dict
    # # print(currPaginState)

    # # 3. Получение нового состояния пагинатора при смене блока нумерации (блок нумерации - это блок показываемых страниц в нумераторе . Переход по блоку осуществляется при нажатии на ссылки >> или <<)
    # paginator.compose_paginator_state_by_current_pgs_block_number(2)
    # currPaginState = paginator.curr_paginator_state_dict
    # print(currPaginState)
    # print('\n\n')


    # # 4. Получение нового состояния пагинатора при смене блока нумерации (блок нумерации - это блок показываемых страниц в нумераторе . Переход по блоку осуществляется при нажатии на ссылки >> или <<)
    # paginator.compose_paginator_state_by_current_pgs_block_number(1)
    # currPaginState = paginator.curr_paginator_state_dict
    # print(currPaginState)
    # print('\n\n')





    # # ПРИМЕР: Организация пагинации 
    # bondsMngr = BondsManagerHTML() # менеджер обллигаций
    # dsBondsCurr = bondsMngr.get_bonds_current() # Получение массива текущих облигаций

    # # Paginator settings
    # pagesRowMax  = 5 # максимальное число показа нумерации страниц в ряду
    # dsRowsQnOnPage = 20 # число записей из входного массива, показываемых на одной странице

    # # Анализ массива для слияния с пагинатором
    # dsN = len(dsBondsCurr) # Общее кол-во рядов во входном массиве
    # pagesNeededForDs = ceil(dsN/dsRowsQnOnPage) # всего необходимо будет страниц, чтобы вывести все записи массива с заданным кол-вом показа рядов на странице
    # dsPages = [p+1 for p in range(pagesNeededForDs)] # массив нумерации для общего количества страниц, необходимы, что бы вывести все записи входного массива

    # pagesBlocksMaxQn = ceil(pagesNeededForDs/pagesRowMax) # Максимальное число блоков (эпох) для вывода всех расчитанных страниц , необходимых для вывода нумерации всех страниц с размером кол-ва номеров страниц, выводимых в ряду перечисления номеров страниц видимых в пагинаторе

    # pgsBlockNumberCurr = 1 # Текущий номер блока выводимых страниц в пагинаторе

    # pgsBlockNumberPrev = pgsBlockNumberCurr - 1 # Предыдущий номер блока выводимых страниц (для метки <<)
    # if pgsBlockNumberPrev < 0 : # Если предыдущий номер блока меньше 0, то устанавливаем его в 0 (так как это предел по Previous Block Number)
    #     pgsBlockNumberPrev = 0

    # pgsBlockNumberNext = pgsBlockNumberCurr + 1 # Следующий номер блока выводимых страниц в показе
    # if pgsBlockNumberNext > pagesNeededForDs: # Если следующий номер блока выводимых страниц > необходимого числа блоков страниц pagesNeededForDs, то устанавливаем его = pagesNeededForDs (так как это макимально возможный номер блока выводимых страниц)
    #     pgsBlockNumberNext = pagesNeededForDs

    # dsPagesInRowShown = dsPages[pgsBlockNumberCurr * pagesRowMax : pgsBlockNumberCurr * pagesRowMax + pagesRowMax ] # Массив для текущего вывода в рядо показываемых нумераторов страниц

    # print (dsPagesInRowShown)

















