

from pandas import DataFrame
from project_bonds_html.projr.classes.sys_subblocks import SysSubblocks
from project_bonds_html.projr.classes.sys_algorithms import SysAlgorithms
from project_bonds_html.projr.classes.request_manager import RequestManager
from project_bonds_html.projr.classes.dsource_output_cube import DSourceOutputCube
# import bonds.switch as Switch
import bonds.funcs_general as FG
from markupsafe import Markup
from bonds.bonds_main_manager import BondsMainManager
from project_bonds_html.projr.settings import DB_BONDS_


class ViewTableCube():
    """ НЕ ДОВЕДЕН ДО УМА. Поэтому еще статус ЗАГОТОВКА
    Класс для подготовки к конечному выводу на внешнем рессурсе табличных данных на базе входного фрейма с данными с использованием  класса DSourceOutputCube
    dsInput - может быть всевозможных видов: фрейм, sql-запрос, название таблицы, выходной источник данных DSourceOutputCube и отдельный вариант - путь к алгоритму, 
    который на выходе дает необходимый источник данных для таблицы. (На данный момент реализована только одна процедурная ветка - 'Algorithm')
    Сами алгоритмы могут возвращать разные источники данных. На данный момент анализируются два возможных возвращаемых типа источника данных - фрейм и выходной источник DSourceOutputCube
    Все источники возможные в результате обработки должны сводится к единому типу источника данных , а именно, DSourceOutputCube, из которого уже подаются данные на HTML темплейты
    Сортировка и прочие стандартные манипуляции с данными таблицы настраиваются в методе prepare_kwargs_params (), где формируются **kwargs именные параметры, которые передаются затем 
    в обьект класса для внешнего источника данных. Некоторые из этих параметров настраиваются во внешнем модуле текущего вьюера (Например, настройка пагинатора, настроука 
    фиксированных выражений филттрации и т.д. - то есть те, которые надо настраивать вручную для каждого вьюера индивидуально)
    ПР: 
    путь к алгоритму - 'SysAlgorithms.a_006_get_ofz_bonds_data'  
    DBTAB = 'TB:wp_chosen_bonds_' - Префикс 'TB:' обязателен. Эта метка для определения, что задано название таблицы из БД
    Заместил предыдущий подобный класс FViewTableManager in /home/ak/projects/3_Proj_Bonds_HTML_Center/project_bonds_html/projr/classes/fview_table_manager.py , который OBSOLETED
    """

    def __init__(self, dsInput, viewName, request, **kwargs):
        # DSourceOutputCube.__init__(self, dsInput, **kwargs)
        self.dsInput = dsInput

        # D. Инициализация нужных параметров и собственных переменных

        self.request = request
        self.viewName = viewName
        self.kwargs = kwargs 
        self.rm = RequestManager()
        self.bmm = BondsMainManager(DB_BONDS_)
        self.templKwargs = {} # параметры для HTML-темплейта после активации обьекта

        # F. Инициализация и настройка параметров request по умолчанию
        self.rqIniDic = self.rm.get_request_as_dict_ini(request)




        # E. Подготовка **kwargs параметров для инициализации выходного источника данных(для сортировки, фильтрации, постоянных выражений фильтрации, поиска)
        self.prepare_kwargs_params()



        # A. Анализ входного источника данных, от которого зависит дальнейшая ветка обработки данных до приведения к нужному конечному варианту
        procBrench_ = self.analyze_input_data_source()
        print(f"@@@###$$$ procBrench_ = {procBrench_}")
        # procBrench_ = 'Algorithm'

        # B. Навигатор веток процессов обработки данных в зависимотси от того, какой тип источника был выявлен в dsInput
        # for case in Switch(procBrench_):
        if 'Algorithm' in procBrench_: 
            # Найти функцию по названию ее класса и имени , находящихся в dsInput и ее реализацию лобьекта сохранить в @@ self.algFuncObj
            self.algFuncObj = self.prepare_algorithm_function() 
            # self.algorithm_activate_()

        elif 'DSourceOutputCube' in procBrench_: 
            pass

        elif 'DataFrame' in procBrench_: 
            pass

        elif 'SQL' in procBrench_: 
            pass

        elif 'DBTAB' in procBrench_: 
            pass
            # self.activate_from_db_table (self.dsInput)
    
        else: # default
            print('Другое нечто)')









    def  prepare_data_sourse_from_db_table(self, tbName):
        """ВОЗМОЖНО НЕ НУЖНЫЙ МЕТОД
        Подготовить выходной источник данных из данных в таблице БД, заданной ее именем и настроенный через именные параметры **kwargs"""

        tb = (tbName.split(':'))[1]

        dfChoosenWP = self.bmm.read_table_to_df_pandas(tb)

        # self.bmm.print_df_gen_info_pandas_IF_DEBUG(dfChoosenWP, True)

        self.dsocCompBonds = DSourceOutputCube(dfChoosenWP, **self.kwargs) 








    def prepare_kwargs_params(self):
        """Подготовка **kwargs параметров для инициализации выходного источника данных(для сортировки, фильтрации, постоянных выражений фильтрации, поиска),
        Тех из них, которые могут быть сформированы из получаемого request и базовых субьективных параметров текущего View. 
        Сами базовые параметры View передаются через входные параметры **kwargs при создании обьекта данного класса"""

        # НАСТРОЙКА **fvtm_kwargs ПАРАМЕТРОВ !!! 
        # Настройка выводимых колонок и их названий в конечной таблице на внеш ресусрсе
        # assocTitles = self.kwargs['assocTitles'] 

        # Настройки пагинатора 
        # paginatorParams = {} # **kwargs
        # paginatorParams['paginGenSet'] = self.kwargs['paginGenSet']


        # kwargs = {} # именнованные параметры для менеджера FViewTableManager и для конечного алгоритма в итоге
        self.kwargs['paginatorParams'] = self.kwargs['paginGenSet']
        # self.kwargs['assocTitles'] = assocTitles
        

        # Настройки фильтрации 
        self.kwargs['filtQuery'] = self.rqIniDic['filtQuery']  # запрос фильтрации из окошка редактора фильтра

        # Выбранное на странице сайта выражение фильрации, если выбрано. Это - ключ для словаря фикс.выражений филльтрации self.kwargs['constFiltExprDic']. 
        # Сам словарь фиксированных выражений фильтрации задается в **kwargs в текущем View (индивидуально для каждого View)
        self.kwargs['filtExprDicKey'] = self.rqIniDic['filtExprDicKey'] 

        self.kwargs['filtIsin'] = self.rqIniDic['filtIsin'] # Isin из input раздела фильтрации (фильтрация по одиночному полю input для фильтрации по ISIN)
        self.kwargs['filtBondName'] = self.rqIniDic['filtBondName']  # filtBondName из input раздела фильтрации (фил'ascTrue'ьтрация по одиночному полю input для фильтрации по названию облигации)


        # Натройка сортировки с альтернативными значениями их иницизации (за счет последнего  не надо инициализировать вначале)
        # Тут же сожно настроить параметры сортировки первичной загрузки через параметры альтернативной инициализации
        sortParams = {}
        sortParams['sortColInx'] = int(self.rm.get_request_attr_val(self.request, 'sortColInx'))  if self.rm.if_attr_in_request_keys(self.request, 'sortColInx') else 0
        sortParams['sortFlag'] = self.rm.get_request_attr_val(self.request, 'sortFlag')  if self.rm.if_attr_in_request_keys(self.request, 'sortFlag') else 1
        sortParams['ascTrue'] = int(self.rm.get_request_attr_val(self.request, 'ascTrue'))  if self.rm.if_attr_in_request_keys(self.request, 'ascTrue') else 0
        self.kwargs['sortParams'] = sortParams


        # ID взвешенного пакета облигаций и его параметров
        self.kwargs['wpIndex'] = 1




    def analyze_input_data_source(self):
        """Анализировать входной источник данных, от которого зависит дальнейшая ветка обработки данных до приведения к нужному конечному варианту
        RET: procBrench_ - Название Ветки процесса обработки даныых в зависимости от типа данных входного источника"""

        procBrench_ = '' # Ветка процесса обработки даныых
        if type(self.dsInput)==str: # Если стринг, то анализируем sql это или путь к алгоритму

            if 'SQL:' in self.dsInput:
                procBrench_ = 'SQL'
            elif 'ALG:' in self.dsInput:
                procBrench_ = 'Algorithm'
            elif 'TB:' in self.dsInput:
                procBrench_ = 'DBTAB'
            else: 
                procBrench_ = 'НЕ НАЙДЕН'

        elif type(self.dsInput) == DSourceOutputCube:
            procBrench_ = 'DSourceOutputCube'
        elif type(self.dsInput) == DataFrame:
            procBrench_ = 'DataFrame'

        return procBrench_





    def prepare_algorithm_function(self):
        """@@@ Найти функцию по названию ее класса и имени , находящихся в dsInput
        Не забыть, что д.б. import искомого класса тут
        """
        algPath_ = (self.dsInput.split('ALG:'))[1]
        parts_ = algPath_.split('.') # Вычисление названий класса в которой находится АИФП и  имени атомарной поисковой функции
        fClassName_ = parts_[0] # названий класса в которой находится АИФП 
        funcName_ = parts_[1] # имени атомарной поисковой функции
        #@@@ Найти функцию по названию ее класса и имени , находящихся в проекте
        algClassObj_ = globals()[fClassName_] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        algFuncObj_ = getattr(algClassObj_, funcName_) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        return algFuncObj_





    def algorithm_activate_(self):
        """Активировать алгоритм, который уже содержится в собственной переменной self.algFuncObj с передачей полностью подготовленных **self.kwargs, где хранятся все необходимые
        критерии для сотрировки, фильтрации, поиска и т.д., если они предусмотрены задачами активируемого алгоритма
        """

        # <ALGORITHM> ЗАПУСК АЛГОРИТМА @@@
        # Входной обьект с конечным фреймом, подготовленным для вывода на внешний ресурс задаваемым в параметрах алгоритмом self.algFuncObj()
        # self.dsocObject = self.algFuncObj(**self.kwargs)  
        resDs_ = self.algFuncObj(**self.kwargs)  

        # Анализ типа источника данных, возвращаемых из алгоритма
        if type(resDs_) == DataFrame: # Если резулотат - фрейм, то доводим его до выходного источника DSourceOutputCube
             self.dsocObject = DSourceOutputCube(resDs_, **self.kwargs) 
        else:
            self.dsocObject = resDs_


        # TODO: Тут должна быть возможность вставить свою таблицу (не стандартную)


        # Бинарный переключатель направления сортировки для вывода на темплейт (после активации, потому что если была сортировка по колонке, то необходимо поменять ее направление)
        if self.rqIniDic['chSort'] == '1': # Если задано переключение направление сортировки. Если chSort == '0', то изменение направления сортировки не происходит (например, если с пагинатора)
            self.rqIniDic['ascTrue'] = (FG.binary_switch_str_var(self.rqIniDic['ascTrue']))[0]

        # Присвоить стандартный код заголовков талицы в виде html для вывода на странице сайта в собственную переменную (Эти собственные переменные могут переписываться в коде алгоритма)
        self.set_standart_html_table_head_code()

        # Присвоить стандартный код тела талицы в виде html для вывода на странице сайта в собственную переменную  (Эти собственные переменные могут переписываться в коде алгоритма)
        self.set_standart_html_table_body_code()

        # Присвоить стандартный код конечной талицы в виде html для вывода на странице сайта в собственную переменную  (Эти собственные переменные могут переписываться в коде алгоритма)
        self.set_final_table_code()


        # Присвоить  именные параметры для HTML-темплейта после активации обьекта
        self.prepare_template_kwargs()





    def activate_from_db_table (self):
        """Активировать или переактивировать уже имеющийся self.dsocObject - выходной источник табличных данных"""

        # tb = (self.dsInput.split('TB:'))[1]

        # dfChoosenWP = self.bmm.read_table_to_df_pandas(tb)

        # # self.bmm.print_df_gen_info_pandas_IF_DEBUG(dfChoosenWP, True)

        # self.dsocObject = DSourceOutputCube(dfChoosenWP, **self.kwargs) 

        # # Бинарный переключатель направления сортировки для вывода на темплейт (после активации, потому что если была сортировка по колонке, то необходимо поменять ее направление)
        # if self.rqIniDic['chSort'] == '1': # Если задано переключение направление сортировки. Если chSort == '0', то изменение направления сортировки не происходит (например, если с пагинатора)
        #     self.rqIniDic['ascTrue'] = (FG.binary_switch_str_var(self.rqIniDic['ascTrue']))[0]

        # # Присвоить стандартный код заголовков талицы в виде html для вывода на странице сайта в собственную переменную (Эти собственные переменные могут переписываться в коде алгоритма)
        # self.set_standart_html_table_head_code()

        # # Присвоить стандартный код тела талицы в виде html для вывода на странице сайта в собственную переменную  (Эти собственные переменные могут переписываться в коде алгоритма)
        # self.set_standart_html_table_body_code()

        # # Присвоить стандартный код конечной талицы в виде html для вывода на странице сайта в собственную переменную  (Эти собственные переменные могут переписываться в коде алгоритма)
        # self.set_final_table_code()


        # # Присвоить  именные параметры для HTML-темплейта после активации обьекта
        # self.prepare_template_kwargs()



    def activate_from_sql (self):
        """Активировать или переактивировать уже имеющийся self.dsocObject - выходной источник табличных данных"""

        sql_ = (self.dsInput.split('SQL:'))[1]

        df = self.bmm.read_sql_to_df_pandas(sql_)

        # self.bmm.print_df_gen_info_pandas_IF_DEBUG(df, colsIndxed = True)

        self.dsocObject = DSourceOutputCube(df, **self.kwargs) 

        # Бинарный переключатель направления сортировки для вывода на темплейт (после активации, потому что если была сортировка по колонке, то необходимо поменять ее направление)
        if self.rqIniDic['chSort'] == '1': # Если задано переключение направление сортировки. Если chSort == '0', то изменение направления сортировки не происходит (например, если с пагинатора)
            self.rqIniDic['ascTrue'] = (FG.binary_switch_str_var(self.rqIniDic['ascTrue']))[0]

        # Присвоить стандартный код заголовков талицы в виде html для вывода на странице сайта в собственную переменную (Эти собственные переменные могут переписываться в коде алгоритма)
        self.set_standart_html_table_head_code()

        # Присвоить стандартный код тела талицы в виде html для вывода на странице сайта в собственную переменную  (Эти собственные переменные могут переписываться в коде алгоритма)
        self.set_standart_html_table_body_code()

        # Присвоить стандартный код конечной талицы в виде html для вывода на странице сайта в собственную переменную  (Эти собственные переменные могут переписываться в коде алгоритма)
        self.set_final_table_code()


        # Присвоить  именные параметры для HTML-темплейта после активации обьекта
        self.prepare_template_kwargs()




    def prepare_template_kwargs(self):
        """Подготовить именные параметры для HTML-темплейта после активации обьекта, которые зависят от внутренних переменных, параметров и т.д. Параметры, которые зависят от
        внешней среды настраиваются во View"""

        self.templKwargs['tableFinalCode'] = self.dsocObject.tableFinal
        self.templKwargs['viewName'] = self.viewName
        self.templKwargs['filtQuery'] = self.rqIniDic['filtQuery'] # Формула фильтрации для проявления в редакторе фильтрации в левом навигаторе
        self.templKwargs['filtExprDicKey'] = self.rqIniDic['filtExprDicKey'] 

        self.templKwargs['filtIsin'] = self.rqIniDic['filtIsin'] # Фильтрация по окошку  input isin
        self.templKwargs['filtBondName'] = self.rqIniDic['filtBondName'] # Фильтрация по окошку  input НАзвания облигации
        self.templKwargs['outpQn'] = len(self.dsocObject.dfOutput)





    def set_standart_html_table_body_code(self, standart = 'TB_BODY_ST01'):
        """ЗАГОТОВКА
        @@ Присвоить стандартный код талицы в виде html для вывода на странице сайта в собственную переменную
        Если нужен нестандартный код, то его создавать либо во Viewer либо в дополнительном методе алгоритма, либо в шаблонах HTML
         (Эти собственные переменные могут переписываться в коде алгоритма)
        Параметр standart - ЗАГОТОВКА для реализации разных стандартных шаблонов таблиц в будущем
        """
        if len(self.dsocObject.tableBody) > 0: # Проверить, не присвоен ли код в предварительных методах заданного алгоритма или коде программы. Если нет, то присвоить стандартный код
            # print(f"@@@@@#####$$$$%%%% self.dsocObject.tableBody = {self.dsocObject.tableBody}")
            pass
        else:

            # Тело таблицы
            tableBody = ''
            for index, row in self.dsocObject.dfOutput.iterrows():
                tableBody += f'<tr class="%row_class%"  onclick="mouseclkevt(event,this);">'  
                tds = ''
                for col in self.dsocObject.dfOutput.columns.values.tolist():

                    if 'ISIN' in col: # Фиксация текущего isin по ряду
                        currIsin = row.loc[col]
                    else:
                        currIsin = ''

                    tds += f'<td><div>{ row.loc[col] }</div></td>'
                    
                tableBody +=  f'<td><input class="form-check-input" type="checkbox" name="inp_wp_{currIsin}" value = "{currIsin}" checked> '

                tableBody += '''</td>''' + tds
                tableBody += '</tr>'  


            self.dsocObject.tableBody = tableBody

        self.dsocObject.tableBody = Markup(self.dsocObject.tableBody)



    def set_standart_html_table_head_code(self, standart = 'TB_HEAD_ST01'):
        """
        @@ Присвоить стандартный код заголовков талицы в виде html для вывода на странице сайта в собственную переменную
        Если нужен нестандартный код, то его создавать либо во Viewer либо в дополнительном методе алгоритма, либо в шаблонах HTML
         (Эти собственные переменные могут переписываться в коде алгоритма)
        Параметр standart - ЗАГОТОВКА для реализации разных стандартных шаблонов таблиц в будущем"""

        if len(self.dsocObject.tableHead) > 0: # Проверить, не присвоен ли код в предварительных методах заданного алгоритма или коде программы. Если нет, то присвоить стандартный код
            pass
        else:
            tableHead = '<tr><th></th>'
            for index,colTitle in enumerate(self.dsocObject.dfOutput.columns.values.tolist()):
                tableHead += f'''
                <th>
                <a  href="/{self.viewName}?filtExprDicKey={self.rqIniDic['filtExprDicKey']}&ascTrue={self.rqIniDic['ascTrue']}&sortColInx={index}&chSort=1&pg={self.rqIniDic['pg']}&srchStr={self.rqIniDic['srchStr']}&interp={self.rqIniDic['interp']}&filtQuery={self.rqIniDic['filtQuery']}&monthSrch={self.rqIniDic['monthSrch']}&payMonth={self.rqIniDic['payMonth']}">
                {colTitle}
                </a>
                </th>'''
            tableHead +=' </tr>'
            self.dsocObject.tableHead = tableHead

        self.dsocObject.tableHead = Markup(self.dsocObject.tableHead)




    def set_final_table_code(self, standart = 'TB_FINAL_ST01'):
        """@@ Присвоить конечный код финальной таблицы в собственную переменную
        Если нужен нестандартный код, то его создавать либо во Viewer либо в дополнительном методе алгоритма, либо в шаблонах HTML
        (Эти собственные переменные могут переписываться в коде алгоритма)
        Параметр standart - ЗАГОТОВКА для реализации разных стандартных шаблонов таблиц в будущем"""

        if len(self.dsocObject.tableFinal) > 0: # Проверить, не присвоен ли код в предварительных методах заданного алгоритма или коде программы. Если нет, то присвоить стандартный код
            pass
        else:
            tableFinal = f"""
                        <table class="table table-sm ">
                        <thead>
                            {self.dsocObject.tableHead}
                        </thead>
                        <tbody>
                            {self.dsocObject.tableBody} 
                        </tbody>
                        </table>
            """
            self.dsocObject.tableFinal = tableFinal

        
        self.dsocObject.tableFinal = Markup(self.dsocObject.tableFinal)










