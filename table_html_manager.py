
# SELF: from  noocube.table_html_manager import TableHtmlManager

from noocube.request_manager_jango import RequestManagerJango
# from noocube.pandas_manager import PandasManager
from beeprint import pp


class TableHtmlManager ():
    """ 
    Формирует HTML коды для таблиц с данными для вывода на странице сайта. 
    Таблицы не обязателльно - именно таблицы. это могут быть разные массивы данных для сайта.
    """
    
    
    def __init__(self, **thmkwargs):
        """ 
        Конструктор. 
        thmkwargs['requestDic'] - requestDic, словарь, сформированный на базе request с сайта. 
        В пространстве noocube формируется методом RequestManagerJango.read_urls_args_dic_from_request_django(request)
        методов во Views
        """
        
        if 'requestDic' in thmkwargs:
            self.request = thmkwargs['requestDic']


    @staticmethod
    def prepare_tb_head_advanced (df, **tbkwargs):
        """ 
        В tbkwargs должны быть: 
            - tbkwargs['requestDic']
            - tbkwargs['standartExludingSortFields'] - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой
            - tbkwargs["tableColsWidth"] - для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth
        
        Подготовить часть <thead> таблицы. С сортировкой, шириной колонок. 
        Для формирования сортировки в заголовках, обычной, простой, необходимо 4 параметра:
            - sort_col - название сортируемой колонки
            - sort_asc - направление сортировки в виде 'True'/ 'False' - параметр из строки url, если задана сортировка
            - standartExludingSortFields - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой
            
            Прим: sort_col и sort_asc находятся в request с сайта или в словаре requestDic
            standartExludingSortFields - задается в settings.py в константе STANDART_FIELDS_EXCLUDING_WHEN_SORTING_
            
            Прим: названия сортировочных url-переменных должно быть именно таким: sort_col и sort_asc
            
        Для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth
        
        Прим: tableColsWidth задается в settings.py в константе COLS_NAMES_FUNCS_WIDTH_ (по задумкам может быть либо в px, либо в долях от 12 , понятных для bootstrap форматов)
        """

        # Словарь для перевода стрингового True/False в булиновые значения
        toBool = {'True':True,'False':False}
        # Текущее состояние по сортировке из request
        requestSortCurrState = {}
        # Если не задана колонка сортировки, то присваивается первая колонка из списка колонок, подлежащих сортировке в TABLE_SORT_COLS_FUNCS_
        if 'sort_col' in tbkwargs['requestDic']:
            requestSortCurrState['sort_col'] = tbkwargs['requestDic']['sort_col'] # Текущая колонка сортировки
        else:
            requestSortCurrState['sort_col'] = df.columns.tolist()[0] # Первая колонка фрейма
        # Если не задано направление сортировки, то присваивается направление = True (то есть ASC)
        if 'sort_asc' in tbkwargs['requestDic']:
            requestSortCurrState['sort_asc'] = toBool[tbkwargs['requestDic']['sort_asc']]   # Текщее направление сортировки
        else:
            requestSortCurrState['sort_asc'] = True
        
        # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
        standartExludingSortFields = tbkwargs['standartExludingSortFields']
        
        # Константная суб-строка с аргументами в ссылке сортировки по заголовкам  с вычетом аргументов в спсиках исключениях genExcludeListFoSort и self.excludeUrlArgsForSort
        constUrlArgsPaginLine = RequestManagerJango.prepare_url_const_line_from_request_dic_with_exclusions(tbkwargs['requestDic'] , standartExludingSortFields)
    
        # Сменить направление сортировки на противоположный
        if bool(requestSortCurrState['sort_asc']):
            sort_asc = False
        else:
            sort_asc = True
        
        
        tableHead = f'<thead><tr>'
                        
        for inx, col in enumerate(df.columns.tolist()):
            # Если название колонки в списке колонок  подлежащих сортировке, то:
            if col in tbkwargs["tableSortCols"]:
                # !!! Если  текущая колонка равна колонке, по которой производится сортировка, то только в этом случае меняется направление сортировки. В других колонках он всегда ASC
                if col == requestSortCurrState['sort_col']: 
                # Сменить направление сортировки на противоположный
                    if requestSortCurrState['sort_asc']:
                        sort_asc = False
                    else:
                        sort_asc = True
                if col in tbkwargs["tableColsWidth"]:
                    tableHead += f'<th style="width:{tbkwargs["tableColsWidth"][col]}">'
                else:
                    tableHead += f'<th >'
                
                tableHead += f'<a href = "/{tbkwargs["dicDecorRes"]["appName"]}/{tbkwargs["dicDecorRes"]["appView"]}?sort_col={col}&sort_asc={str(sort_asc)}{constUrlArgsPaginLine}">{col}</a></th>'
                
            else:
                if col in tbkwargs["tableColsWidth"]:
                    tableHead += f'<th     style="width:{tbkwargs["tableColsWidth"][col]}">{col}</th>'
                else:
                    tableHead += f'<th>{col}</th>'
                
        tableHead += '</tr></thead>'
        
        return tableHead
    
    
    @staticmethod
    def prepare_tb_head_advanced_with_color_diff_and_hidden_cols (df, **tbkwargs):
        """ 
        С цветовой дифференциацией рядов , в зависмисоти от скрытой колонки 'HIDDEN:bg_color', в названии которой присутствует часть 'HIDDEN' (задается в словаре тайтлов типа COLS_ASSOC_FOR_COMPLEX_BONDS_
        в формате 'HIDDEN:bg_color')
        В tbkwargs должны быть: 
            - tbkwargs['requestDic']
            - tbkwargs['standartExludingSortFields'] - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой
            - tbkwargs["tableColsWidth"] - для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth
        
        Подготовить часть <thead> таблицы. С сортировкой, шириной колонок. 
        Для формирования сортировки в заголовках, обычной, простой, необходимо 4 параметра:
            - sort_col - название сортируемой колонки
            - sort_asc - направление сортировки в виде 'True'/ 'False' - параметр из строки url, если задана сортировка
            - standartExludingSortFields - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой
            
            Прим: sort_col и sort_asc находятся в request с сайта или в словаре requestDic
            standartExludingSortFields - задается в settings.py в константе STANDART_FIELDS_EXCLUDING_WHEN_SORTING_
            
            Прим: названия сортировочных url-переменных должно быть именно таким: sort_col и sort_asc
            
        Для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth
        
        Прим: tableColsWidth задается в settings.py в константе COLS_NAMES_FUNCS_WIDTH_ (по задумкам может быть либо в px, либо в долях от 12 , понятных для bootstrap форматов)
        """

        # Словарь для перевода стрингового True/False в булиновые значения
        toBool = {'True':True,'False':False}
        # Текущее состояние по сортировке из request
        requestSortCurrState = {}
        # Если не задана колонка сортировки, то присваивается первая колонка из списка колонок, подлежащих сортировке в TABLE_SORT_COLS_FUNCS_
        if 'sort_col' in tbkwargs['requestDic']:
            requestSortCurrState['sort_col'] = tbkwargs['requestDic']['sort_col'] # Текущая колонка сортировки
        else:
            requestSortCurrState['sort_col'] = df.columns.tolist()[0] # Первая колонка фрейма
        # Если не задано направление сортировки, то присваивается направление = True (то есть ASC)
        if 'sort_asc' in tbkwargs['requestDic']:
            requestSortCurrState['sort_asc'] = toBool[tbkwargs['requestDic']['sort_asc']]   # Текщее направление сортировки
        else:
            requestSortCurrState['sort_asc'] = True
        
        # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
        standartExludingSortFields = tbkwargs['standartExludingSortFields']
        
        # Константная суб-строка с аргументами в ссылке сортировки по заголовкам  с вычетом аргументов в спсиках исключениях genExcludeListFoSort и self.excludeUrlArgsForSort
        constUrlArgsPaginLine = RequestManagerJango.prepare_url_const_line_from_request_dic_with_exclusions(tbkwargs['requestDic'] , standartExludingSortFields)
    
        # Сменить направление сортировки на противоположный
        if bool(requestSortCurrState['sort_asc']):
            sort_asc = False
        else:
            sort_asc = True
        
        
        tableHead = f'<thead><tr>'
                        
        for inx, col in enumerate(df.columns.tolist()):
            
            # Сокрытие колонок, которы емеют в своем названии 'HIDDEN__' - часть
            if 'HIDDEN__' in col:
                pass
            else:
                # Если название колонки в списке колонок  подлежащих сортировке, то:
                if col in tbkwargs["tableSortCols"]:
                    # !!! Если  текущая колонка равна колонке, по которой производится сортировка, то только в этом случае меняется направление сортировки. В других колонках он всегда ASC
                    if col == requestSortCurrState['sort_col']: 
                    # Сменить направление сортировки на противоположный
                        if requestSortCurrState['sort_asc']:
                            sort_asc = False
                        else:
                            sort_asc = True
                    if 'tableColsWidth' in tbkwargs and  col in tbkwargs["tableColsWidth"]:
                        tableHead += f'<th style="width:{tbkwargs["tableColsWidth"][col]}">'
                    else:
                        tableHead += f'<th >'
                    
                    tableHead += f'<a href = "/{tbkwargs["dicDecorRes"]["appName"]}/{tbkwargs["dicDecorRes"]["appView"]}?sort_col={col}&sort_asc={str(sort_asc)}{constUrlArgsPaginLine}">{col}</a></th>'
                    
                else:
                    if 'tableColsWidth' in tbkwargs and  col in tbkwargs["tableColsWidth"]:
                        tableHead += f'<th     style="width:{tbkwargs["tableColsWidth"][col]}">{col}</th>'
                    else:
                        
                        # Проверка на невидимость тайтла (Что задается, если в названии колонки присутствует __NOOTITLE)
                        if '__NOTITLE' in col:
                            tableHead += f'<th></th>'
                        else:
                            tableHead += f'<th>{col}</th>'
                
        tableHead += '</tr></thead>'
        
        return tableHead

    


    @staticmethod
    def prepare_tb_head_advanced_with_color_diff_and_hidden_cols_v2 (dicDecorRes, **tbkwargs):
        """ 
        Версия 2: Добавлена возможность добавлять фиксированные url-атрибуты и их значения в в формируемую автоматом константную url-строку и на вход подается не фрейм . а сквозной 
        словарь декораторов dicDecorRes
        
        С цветовой дифференциацией рядов , в зависмисоти от скрытой колонки 'HIDDEN:bg_color', в названии которой присутствует часть 'HIDDEN' (задается в словаре тайтлов типа COLS_ASSOC_FOR_COMPLEX_BONDS_
        в формате 'HIDDEN:bg_color')
        В tbkwargs должны быть: 
            - tbkwargs['requestDic']
            - tbkwargs['standartExludingSortFields'] - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой
            - tbkwargs["tableColsWidth"] - для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth
        
        Подготовить часть <thead> таблицы. С сортировкой, шириной колонок. 
        Для формирования сортировки в заголовках, обычной, простой, необходимо 4 параметра:
            - sort_col - название сортируемой колонки
            - sort_asc - направление сортировки в виде 'True'/ 'False' - параметр из строки url, если задана сортировка
            - standartExludingSortFields - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой
            
            Прим: sort_col и sort_asc находятся в request с сайта или в словаре requestDic
            standartExludingSortFields - задается в settings.py в константе STANDART_FIELDS_EXCLUDING_WHEN_SORTING_
            
            Прим: названия сортировочных url-переменных должно быть именно таким: sort_col и sort_asc
            
        Для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth
        
        Прим: tableColsWidth задается в settings.py в константе COLS_NAMES_FUNCS_WIDTH_ (по задумкам может быть либо в px, либо в долях от 12 , понятных для bootstrap форматов)
        """
        
        # print(f'33#########   %%%%%%%%%%%%%%%%%%%   ^^^^^^^^^^^^ dicDecorRes = {dicDecorRes} ')

        # Словарь для перевода стрингового True/False в булиновые значения
        toBool = {'True':True,'False':False}
        # Текущее состояние по сортировке из request
        requestSortCurrState = {}
        # Если не задана колонка сортировки, то присваивается первая колонка из списка колонок, подлежащих сортировке в TABLE_SORT_COLS_FUNCS_
        if 'sort_col' in tbkwargs['requestDic']:
            requestSortCurrState['sort_col'] = tbkwargs['requestDic']['sort_col'] # Текущая колонка сортировки
        else:
            requestSortCurrState['sort_col'] = dicDecorRes['df'].columns.tolist()[0] # Первая колонка фрейма
        # Если не задано направление сортировки, то присваивается направление = True (то есть ASC)
        if 'sort_asc' in tbkwargs['requestDic']:
            requestSortCurrState['sort_asc'] = toBool[tbkwargs['requestDic']['sort_asc']]   # Текщее направление сортировки
        else:
            requestSortCurrState['sort_asc'] = True
        
        # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
        standartExludingSortFields = tbkwargs['standartExludingSortFields']
        
        # Константная суб-строка с аргументами в ссылке сортировки по заголовкам  с вычетом аргументов в спсиках исключениях genExcludeListFoSort и self.excludeUrlArgsForSort
        
        
        # сначала проверяем были ли переданы из View дополнителльные парметры с заданынми значениями для добавления в к url-строке 
        if 'dicUrlArgsAdd' in dicDecorRes:
            dicUrlArgsAdd = dicDecorRes['dicUrlArgsAdd'] # Дополнительные заданные url-аргументы
        else:
            dicUrlArgsAdd = {}
        
        constUrlArgsPaginLine = RequestManagerJango.prepare_url_const_line_from_request_dic_with_exclusions_and_addings(tbkwargs['requestDic'] , standartExludingSortFields, dicUrlArgsAdd)
    
        # Сменить направление сортировки на противоположный
        if bool(requestSortCurrState['sort_asc']):
            sort_asc = False
        else:
            sort_asc = True
        
        
        tableHead = f'<thead><tr>'
                        
        for inx, col in enumerate(dicDecorRes['df'].columns.tolist()):
            
            # Сокрытие колонок, которы емеют в своем названии 'HIDDEN__' - часть
            if 'HIDDEN__' in col:
                pass
            else:
                # Если название колонки в списке колонок  подлежащих сортировке, то:
                if col in tbkwargs["tableSortCols"]:
                    # !!! Если  текущая колонка равна колонке, по которой производится сортировка, то только в этом случае меняется направление сортировки. В других колонках он всегда ASC
                    if col == requestSortCurrState['sort_col']: 
                    # Сменить направление сортировки на противоположный
                        if requestSortCurrState['sort_asc']:
                            sort_asc = False
                        else:
                            sort_asc = True
                    if 'tableColsWidth' in tbkwargs and  col in tbkwargs["tableColsWidth"]:
                        tableHead += f'<th style="width:{tbkwargs["tableColsWidth"][col]}">'
                    else:
                        tableHead += f'<th >'
                    
                    tableHead += f'<a href = "/{dicDecorRes["appName"]}/{dicDecorRes["appView"]}?sort_col={col}&sort_asc={str(sort_asc)}{constUrlArgsPaginLine}">{col}</a></th>'
                    
                else:
                    if 'tableColsWidth' in tbkwargs and  col in tbkwargs["tableColsWidth"]:
                        tableHead += f'<th     style="width:{tbkwargs["tableColsWidth"][col]}">{col}</th>'
                    else:
                        
                        # Проверка на невидимость тайтла (Что задается, если в названии колонки присутствует __NOOTITLE)
                        if '__NOTITLE' in col:
                            tableHead += f'<th></th>'
                        else:
                            tableHead += f'<th>{col}</th>'
                
        tableHead += '</tr></thead>'
        
        return tableHead

    
    

    
    
    @staticmethod
    def prepare_tb_head_advanced_with_color_diff_and_hidden_cols_v3 (**dicDecorRes):
        """ 
        Версия 3: Отменяются все прочие пареметры, кроме именных типа **tbkwargs. Все передается теперь только через них, включая фрейм. В применении с декораторами 
        эти параметры приравниваются к dicDecorRes: **tbkwargs =**dicDecorRes
        Версия 2: Добавлена возможность добавлять фиксированные url-атрибуты и их значения в в формируемую автоматом константную url-строку и на вход подается не фрейм . а сквозной 
        словарь декораторов dicDecorRes
        
        С цветовой дифференциацией рядов , в зависмисоти от скрытой колонки 'HIDDEN:bg_color', в названии которой присутствует часть 'HIDDEN' (задается в словаре тайтлов типа COLS_ASSOC_FOR_COMPLEX_BONDS_
        в формате 'HIDDEN:bg_color')
        В tbkwargs должны быть: 
            - tbkwargs['requestDic']
            - tbkwargs['standartExludingSortFields'] - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой
            - tbkwargs["tableColsWidth"] - для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth
        
        Подготовить часть <thead> таблицы. С сортировкой, шириной колонок. 
        Для формирования сортировки в заголовках, обычной, простой, необходимо 4 параметра:
            - sort_col - название сортируемой колонки
            - sort_asc - направление сортировки в виде 'True'/ 'False' - параметр из строки url, если задана сортировка
            - standartExludingSortFields - список полей, которые должны быть исключены из ссылки в саголовке с сортировкой
            
            Прим: sort_col и sort_asc находятся в request с сайта или в словаре requestDic
            standartExludingSortFields - задается в settings.py в константе STANDART_FIELDS_EXCLUDING_WHEN_SORTING_
            
            Прим: названия сортировочных url-переменных должно быть именно таким: sort_col и sort_asc
            
        Для формирования ширины колонок при формировании заголовков в <th></th> используется словарь tableColsWidth
        
        Прим: tableColsWidth задается в settings.py в константе COLS_NAMES_FUNCS_WIDTH_ (по задумкам может быть либо в px, либо в долях от 12 , понятных для bootstrap форматов)
        """
        
        # print(f'33#########   %%%%%%%%%%%%%%%%%%%   ^^^^^^^^^^^^ dicDecorRes = {dicDecorRes} ')

        # Словарь для перевода стрингового True/False в булиновые значения
        toBool = {'True':True,'False':False}
        # Текущее состояние по сортировке из request
        requestSortCurrState = {}
        # Если не задана колонка сортировки, то присваивается первая колонка из списка колонок, подлежащих сортировке в TABLE_SORT_COLS_FUNCS_
        if 'sort_col' in dicDecorRes['requestDic']:
            requestSortCurrState['sort_col'] = dicDecorRes['requestDic']['sort_col'] # Текущая колонка сортировки
        else:
            requestSortCurrState['sort_col'] = dicDecorRes['df'].columns.tolist()[0] # Первая колонка фрейма
        # Если не задано направление сортировки, то присваивается направление = True (то есть ASC)
        if 'sort_asc' in dicDecorRes['requestDic']:
            requestSortCurrState['sort_asc'] = toBool[dicDecorRes['requestDic']['sort_asc']]   # Текщее направление сортировки
        else:
            requestSortCurrState['sort_asc'] = True
        
        # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
        standartExludingSortFields = dicDecorRes['decor_kwargs']['table_codes']['standartExludingSortFields']
        
        # Константная суб-строка с аргументами в ссылке сортировки по заголовкам  с вычетом аргументов в спсиках исключениях genExcludeListFoSort и self.excludeUrlArgsForSort
        
        
        # сначала проверяем были ли переданы из View дополнителльные парметры с заданынми значениями для добавления в к url-строке 
        if 'dicUrlArgsAdd' in dicDecorRes:
            dicUrlArgsAdd = dicDecorRes['dicUrlArgsAdd'] # Дополнительные заданные url-аргументы
        else:
            dicUrlArgsAdd = {}
        
        constUrlArgsPaginLine = RequestManagerJango.prepare_url_const_line_from_request_dic_with_exclusions_and_addings(dicDecorRes['requestDic'] , standartExludingSortFields, dicUrlArgsAdd)
    
        # Сменить направление сортировки на противоположный
        if bool(requestSortCurrState['sort_asc']):
            sort_asc = False
        else:
            sort_asc = True
        
        
        tableHead = f'<thead><tr>'
                        
        for inx, col in enumerate(dicDecorRes['df'].columns.tolist()):
            
            # Сокрытие колонок, которы емеют в своем названии 'HIDDEN__' - часть
            if 'HIDDEN__' in col:
                pass
            else:
                # Если название колонки в списке колонок  подлежащих сортировке, то:
                if col in dicDecorRes['decor_kwargs']['table_codes']["tableSortCols"]:
                    # !!! Если  текущая колонка равна колонке, по которой производится сортировка, то только в этом случае меняется направление сортировки. В других колонках он всегда ASC
                    if col == requestSortCurrState['sort_col']: 
                    # Сменить направление сортировки на противоположный
                        if requestSortCurrState['sort_asc']:
                            sort_asc = False
                        else:
                            sort_asc = True
                    if 'tableColsWidth' in dicDecorRes['decor_kwargs']['table_codes'] and  col in dicDecorRes['decor_kwargs']['table_codes']["tableColsWidth"]:
                        tableHead += f'<th style="width:{dicDecorRes["decor_kwargs"]["table_codes"]["tableColsWidth"][col]}">'
                    else:
                        tableHead += f'<th >'
                    
                    tableHead += f'<a href = "/{dicDecorRes["appName"]}/{dicDecorRes["appView"]}?sort_col={col}&sort_asc={str(sort_asc)}{constUrlArgsPaginLine}">{col}</a></th>'
                    
                else:
                    if 'tableColsWidth' in dicDecorRes["decor_kwargs"]['table_codes'] and  col in dicDecorRes['decor_kwargs']['table_codes']["tableColsWidth"]:
                        tableHead += f'<th     style="width:{dicDecorRes["decor_kwargs"]["table_codes"]["tableColsWidth"][col]}">{col}</th>'
                    else:
                        
                        # Проверка на невидимость тайтла (Что задается, если в названии колонки присутствует __NOOTITLE)
                        if '__NOTITLE' in col:
                            tableHead += f'<th></th>'
                        else:
                            tableHead += f'<th>{col}</th>'
                
        tableHead += '</tr></thead>'
        
        return tableHead

    
    
    
    


    @staticmethod
    def prepare_table_body (df,**tbkwargs):
        """ 
        Подготоавливает обычный сектор <tbody> таблицы
        """
        
        tableBody = '<tbody>'
        # Формирование рядов
        for index, row in df.iterrows():
            tableBody += '<tr>'  
            
            # Формирование колонок
            for col in df.columns.values.tolist():
                tableBody += f'<td>{ row.loc[col] }</td>'
                
            tableBody += '</tr>'  
            
        tableBody += '</tbody>'  
        
        return tableBody





    @staticmethod
    def prepare_table_body_with_color_diff_and_hidden_cols (df,**tbkwargs):
        """ 
        Подготоавливает обычный сектор <tbody> таблицы c цветовой дифференциацией по рядам в зависимости от существущей колонки (которая может быть невидима) 
        с фиксированным названием 'bg_color' в фрейме df
        Невидимость колонки задается в настройках а константе типа COLS_ASSOC_FOR_COMPLEX_BONDS_
        """
        
        tableBody = '<tbody>'
        # Формирование рядов
        
        for index, row in df.iterrows():
            
            # Определение цвета ряда в зависимости от заданного значения в колонке ряда 'bg_color', если таковая колокна есть. Иначе - обычный цвет
            if 'HIDDEN__bg_color' in row:
                rowBgColor = row['HIDDEN__bg_color']
            else:
                rowBgColor = 'White'
            
            tableBody += f'<tr>'  
            
            # Формирование колонок
            for col in df.columns.values.tolist():
                
                # Если в названии колонки есть 'HIDDEN', то не показываем эту колонку
                if 'HIDDEN' in col:
                    
                    pass
                else:
                    
                    tableBody += f'<td style="background-color:{rowBgColor};">{ row.loc[col] }</td>'
                
            tableBody += '</tr>'  
            
        tableBody += '</tbody>'  
        
        return tableBody




    @staticmethod
    def prepare_table_body_with_color_diff_and_hidden_cols_v3 (**dicDecorRes):
        """ 
        Подготоавливает обычный сектор <tbody> таблицы c цветовой дифференциацией по рядам в зависимости от существущей колонки (которая может быть невидима) 
        с фиксированным названием 'bg_color' в фрейме df
        Требует, что бы таблица была класса от bootstrap, например : <table class='table table-condensed table-bordered table-sm color_table'>
        ПРИМ: При этом нет реакции на jQuery подсветки строк таблицы при нажатии 
        Версия 3: Только с именными параметрами в виде **dicDecorRes
        Невидимость колонки задается в настройках а константе типа COLS_ASSOC_FOR_COMPLEX_BONDS_
        """
        
        tableBody = '<tbody>'
        # Формирование рядов
        
        for index, row in dicDecorRes['df'].iterrows():
            
            # Определение цвета ряда в зависимости от заданного значения в колонке ряда 'bg_color', если таковая колокна есть. Иначе - обычный цвет
            if 'HIDDEN__bg_color' in row:
                rowBgColor = row['HIDDEN__bg_color']
            else:
                rowBgColor = 'White'
            
            tableBody += f'<tr>'  
            
            # Формирование колонок
            for col in dicDecorRes['df'].columns.values.tolist():
                
                # Если в названии колонки есть 'HIDDEN', то не показываем эту колонку
                if 'HIDDEN' in col:
                    
                    pass
                else:
                    
                    tableBody += f'<td style="background-color:{rowBgColor};">{ row.loc[col] }</td>'
                
            tableBody += '</tr>'  
            
        tableBody += '</tbody>'  
        
        return tableBody



    @staticmethod
    def prepare_custom_table_body_v4 (**dicThrough):
        """ 
        Подготоавливает обычный сектор <tbody> таблицы c цветовой дифференциацией по рядам в зависимости от существущей колонки (которая может быть невидима) 
        с фиксированным названием 'bg_color' в фрейме df
        ПРИМ: кастомный формат таблицы, то есть не зависит от бутсраповских классов. Никаких классов от бутсрап присваивать не надо таблице
        ПРИМ: Работают подсветки строк от jQuery
        ПРИМ: Необходимы свои стили для таблицы
        ПРИМ: Бэкграунд для строк на фиксированнйо основе (то есть не зависит от операций с курсором мыши, а от каких-то аналитических данных)
        идет не через цвет строки, а через названия стиля класса, который должен присваиваться скрытому столбцу HIDDEN__bg_color 
        ПРИМ: Что бы заработала дифференциация по цветам рядов, необходимо перебить бутстраповский класс таблицы путем задания своего класса для таблицы в 
        settings.py в TABLE_CODE константе в ключе 'tableStyleClasses'.В кастомны проектных стилях есть класс 'color_table', который в общем проработан для кастомной таблицы
        при наполнении фрейма данными и в зависимости от какой-то аналитики данных. 
        Версия 3: Только с именными параметрами в виде **dicDecorRes
        Невидимость колонки задается в настройках а константе типа COLS_ASSOC_FOR_COMPLEX_BONDS_
        """
        
        tableBody = '<tbody>'
        # Формирование рядов
        
        for index, row in dicThrough['df'].iterrows():
            
            # Определение цвета ряда в зависимости от заданного значения в колонке ряда 'bg_color', если таковая колокна есть. Иначе - обычный цвет
            if 'HIDDEN__bg_color' in row:
                rowClass = row['HIDDEN__bg_color']
            else:
                rowClass = 'White'
            
            tableBody += f'<tr class="{rowClass}">'  
            
            # Формирование колонок
            for col in dicThrough['df'].columns.values.tolist():
                
                # Если в названии колонки есть 'HIDDEN', то не показываем эту колонку
                if 'HIDDEN' in col:
                    
                    pass
                else:
                    
                    # Альтернативно по заданным параметрам в dicThrough['table_codes']['showSpecialCharictersCols'] выводить текст с показом специальных символов типа '/n' и т.д.
                    # списки колонок . где нужно показывать спец-символы задается в settings.py в разделе TABLE_CODE = {..., 'showSpecialCharictersCols' ; [],
                    if (
                        'showSpecialCharictersCols' in dicThrough['decor_kwargs']['table_codes'] and  
                        len(dicThrough['decor_kwargs']['table_codes']['showSpecialCharictersCols']) > 0 and 
                        # если колонка содержится в списке колонок для показа спец-символов
                        col in dicThrough['decor_kwargs']['table_codes']['showSpecialCharictersCols'] 
                    ):
                        
                        tableBody += f'<td >{ repr(row.loc[col]) }</td>' # repr() показывает спец-символы
                        
                    else: 
                        
                        tableBody += f'<td >{ row.loc[col] }</td>'
                
            tableBody += '</tr>'  
            
        tableBody += '</tbody>'  
        
        return tableBody





    @staticmethod
    def prepare_table_body_for_month_payment_matrix (**dicDecorRes):
        """ 
        Подготоавливает обычный сектор <tbody> таблицы c цветовой дифференциацией по рядам в зависимости от существущей колонки (которая может быть невидима) 
        ПРИМ: В данном коде пустые значения None заменяются на прочерк  '-'
        с фиксированным названием 'bg_color' в фрейме df
        Невидимость колонки задается в настройках а константе типа COLS_ASSOC_FOR_COMPLEX_BONDS_
        """
        
        tableBody = '<tbody>'
        # Формирование рядов
        
        for index, row in dicDecorRes['df'].iterrows():
            
            # Определение цвета ряда в зависимости от заданного значения в колонке ряда 'bg_color', если таковая колокна есть. Иначе - обычный цвет
            if 'HIDDEN__bg_color' in row:
                rowBgColor = row['HIDDEN__bg_color']
            else:
                rowBgColor = 'White'
            
            tableBody += f'<tr>'  
            
            # Формирование колонок
            for col in dicDecorRes['df'].columns.values.tolist():
                
                # Значение в текущей ячейке
                # cellVal = str(row.loc[col])
                
                #  Замена пустоты или None на прочерк '-' в текущем значении ячейки
                if row.loc[col] is None or row.loc[col]=='' or str(row.loc[col])=='nan' or row.loc[col]=='NULL':
                    cellVal = '-'
                else:
                    cellVal = str(row.loc[col])

                
                # Если в названии колонки есть 'HIDDEN', то не показываем эту колонку
                if 'HIDDEN' in cellVal:
                    
                    pass
                else:
                    
                    tableBody += f'<td style="background-color:{rowBgColor};">{ cellVal }</td>'
                
            tableBody += '</tr>'  
            
        tableBody += '</tbody>'  
        
        return tableBody

















if __name__ == "__main__":
    pass

