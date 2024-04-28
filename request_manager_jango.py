
# SELF: from noocube.request_manager_jango import RequestManagerJango

from noocube.bonds_main_manager import BondsMainManager
from noocube.settings import *
from noocube.funcs_general_class import FunctionsGeneralClass
from noocube.settings import *
import json
import pandas as pd
from noocube.pandas_manager import PandasManager
from noocube.bonds_main_manager_speedup import BondsMainManagerSpeedup
# from noocube.django_view_manager import DjangoViewManager

# # НЕ УДАЛЯТЬ ПОКА
# import sys
# sys.path.append('/home/ak/projects/P19_Bonds_Django/bonds_django_proj')
# import noocube.settings_bdp_main as ms # общие установки для всех модулей

class RequestManagerJango (): # 
    """ Менеджер request с сайта HTML
    """


    
    def _print_mark(id, func, mark, markVal, prefix):
        """
        RequestManagerJango
        Вспомогательыня функция для распечатки принт-маркеров
        ПРИМ: Что бы использовать эту вспомогательныую функцию необходимо добвать ее в кажый класс и заменить константные значения className и file на соотвтетсвующие этому классу
        """

        FunctionsGeneralClass.print_any_mark_by_id(
            PRINT_TERMINAL_START_END_FUNCTIONS_,
            id,
            func = func,
            mark = mark,
            markVal = markVal,
            className = 'RequestManagerJango',
            calssFile = 'noocube/request_manager_jango.py',
            prefix = prefix
        )
    
    
    @staticmethod
    def read_urls_args_dic_from_request_django(request):
        """
        OBSOLETED: использовать read_urls_args_dic_from_request_get_django и возвращать requestGetDic
        RequestManagerJango
        Считать  URL - аргументы из request в словарь
        Category: Request JANGO
        """

        requestDic = {}
        for key,val in request.GET.items():
            requestDic[key] = val

        return requestDic
    
    
    @staticmethod
    def read_urls_args_dic_from_request_get_django(request):
        """
        RequestManagerJango
        Считать  URL - аргументы из request в словарь
        Category: Request JANGO
        """

        requestGetDic = {}
        for key,val in request.GET.items():
            requestGetDic[key] = val

        return requestGetDic
    
    
    @staticmethod
    def read_urls_args_dic_from_request_post_django(request):
        """
        RequestManagerJango
        Считать  URL - аргументы из request , переданных методом POST, в словарь
        Category: Request JANGO
        """

        requestPostDic = {}
        for key,val in request.POST.items():
            requestPostDic[key] = val

        return requestPostDic
    
    
    @staticmethod
    def prepare_url_const_line_from_request_dic_with_exclusions (currRequestDic, listUrlArgsToExclude):
        """
        ОБНОВЛЕНИЕ. Сначала находился в модуле HTMLSiteManagerJango 
        RequestManagerJango
        Сформировать константную часть url-строки с аргументами на основе словаря - матрицы входных аргументов (обычно взятых из request) с вычетом тех аргументов,
        которые указаны в списке исключений
        currRequestDic - словарь типа {<url_arg> : <значение аргумента>}
        listUrlArgsToExclude - список аргументов которые надо исключить, даже если они находятся в входной матрице аргументов, при построении строки для части ссылки на странице
        RET: String
        Category: Request JANGO
        """

        constUrlArgsLine = ''
        for key, val in currRequestDic.items():
            if key in listUrlArgsToExclude: # Исключаем аргументы, которые не нужны в строке URL
                pass
            else:
                constUrlArgsLine += f'&{key}={val}'
                
        return constUrlArgsLine
    
    
    
    @staticmethod
    def prepare_url_const_line_from_request_dic_with_exclusions_and_addings (currRequestDic, listUrlArgsToExclude, dicArgsToAdd):
        """
        RequestManagerJango
        Сформировать константную часть url-строки с аргументами на основе словаря - матрицы входных аргументов (обычно взятых из request) с вычетом тех аргументов,
        которые указаны в списке исключений. И с добавками тех аргументов и их значений, которые передаются в словаре  dicArgsToAdd (Добавка аргументов дополнительных с заданынми значениями)
        currRequestDic - словарь типа {<url_arg> : <значение аргумента>}
        listUrlArgsToExclude - список аргументов которые надо исключить, даже если они находятся в входной матрице аргументов, при построении строки для части ссылки на странице
        RET: String
        Category: Request JANGO
        """
        
        # Список исключений индивидуально заданных url-аргументов  для исключения их из стандартной автоматической url-строки. Индивидуальные настраиваимые аргументы имеют приемущество 
        # перед общей строки ссылки с сайта
        addingArgsKeys  = list(dicArgsToAdd.keys())

        constUrlArgsLine = ''
        for key, val in currRequestDic.items():
            if key in listUrlArgsToExclude or key in addingArgsKeys: # Исключаем аргументы, которые не нужны в строке URL (включая индивидуально настроенные url-аргументы из dicArgsToAdd)
                pass
            else:
                constUrlArgsLine += f'&{key}={val}'
                
        # Добавка аргументов дополнительных с заданынми значениями (идет из индивидуальных потребнойстей в обработке фреймов декораторами. Поэтому перекрывает общие нстрйоки по
        # исключениям, если необходимо доавить исключенный аргумент из listUrlArgsToExclude но уже индивидуальной настройки)
        for key, val in dicArgsToAdd.items():
            constUrlArgsLine += f'&{key}={val}'
                
                
        # print(f'44$$$$4$$$$$$   &&&&&&&&&&&&&  constUrlArgsLine = {constUrlArgsLine}')
                
        return constUrlArgsLine
    
    
    
    
    # SESSIONS
    
    @staticmethod
    def read_df_from_session(request, varName):
        """ 
        RequestManagerJango
        OBSOLETED: Изменено название . Теперь использовать read_df_as_json_from_session()
        Считывание фрейма из сессии
        varName - название переменной с фреймом, в которой хранится необходимый фрейм
        Category: Request JANGO
        """
        
        if varName in request.session: 
            df = pd.DataFrame(json.loads(request.session[varName]))
            
            # # -----> PRINT
            # print(f'#############   %%%%%%%%%%%%%    ***************   ')
            # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(df, True, colsIndxed = True)
    
            
        else:
            df = -1
        return df
    
    
    @staticmethod
    def read_df_as_json_from_session(request, varName):
        """ 
        RequestManagerJango
        Считывание фрейма из сессии
        varName - название переменной с фреймом, в которой хранится необходимый фрейм
        Category: Request JANGO
        """
        
        if varName in request.session: 
            df = pd.DataFrame(json.loads(request.session[varName]))
            
            # # -----> PRINT
            # print(f'#############   %%%%%%%%%%%%%    ***************   ')
            # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(df, True, colsIndxed = True)
    
            
        else:
            df = -1
        return df
    
    
    @staticmethod
    def save_df_to_session(request, df, varName):
        """ 
        RequestManagerJango
        OBSOLETED: Изменено название. Теперь использовать save_df_to_session_as_json()
        Сохранить фрейм в сессию под именем переменной сессии varName
        Category: Request JANGO
        """
        
        request.session[varName]  = df.to_json() 
    
    
    @staticmethod
    def save_df_to_session_as_json(request, df, varName):
        """ 
        RequestManagerJango
        Сохранить фрейм в сессию под именем переменной сессии varName
        Category: Request JANGO
        """
        
        request.session[varName]  = df.to_json() 
    
    
    @staticmethod
    def print_all_session_variables_keys(request):
        """ 
        RequestManagerJango
        НЕ ПРОВЕРЕНО
        Распечатать все ключи сохраненных переменных в сессии
        Category: Request JANGO
        """
        print('\nSession keys:')
        for key in request.session.keys():
                print (f"key:=>'{key}'\n")
            
            


    # # НЕ УДАЛЯТЬ
    # def save_tb_from_db_to_session_as_data_frame (request, db, tb, sessionDfName):
    #     """ ЗАГОТОВКА. Не закончена 
    #     Сохранить таблицу tb из БД  db  в сессию в виде фрейма dataFrame под именем переменной сессии sessionDfName
    #     Category: Request JANGO
    #     """ 
            
    #     dfBondsArchive = bmm.read_table_by_sql_to_df_pandas(ms.TB_BONDS_ARCHIVE)
    #     RequestManagerJango.save_df_to_session(request, dfBondsArchive, 'dfBondsArchive')
    #     print(f'dfBondsArchive сохранен в сессию из таблицы bonds_archive из БД bonds.db ')
        
            
            
            
    # END SESSIONS
    

    @staticmethod
    def read_curr_application_and_view_names_to_dic_decor (request, dicDecorRes):
        """ 
        Считывание названий текущих приложения и метода view Django и запись их в сквозной декор-словарь для настроек текущего приложения и view, откуда идет процессинг фрейма
        по декораторам 
        Category: Request JANGO
        """

        # Считывание и внесение в dicDecorRes названий приложения и текущего View (для автоматического внесения текущих данных по приложению и методу View в сквозной декор-словарь)
        appAndVieMethodnames = request.resolver_match.view_name
        
        # print(f'@@@@@@@@@@@   $$$$$$$$$$$$$$$$$$  {appAndVieMethodnames}')
        
        namesParts = appAndVieMethodnames.split(':')
        appName = namesParts[0]
        # print(f'@@@@@@@@@@@   $$$$$$$$$$$$$$$$$$ appName =  {appName}')
        vieMethodname = namesParts[1]
        
        # Настройка названия приложения (в будущем TODO: что бы это название бралось автоматом из приложения, в котором View как-то)
        dicDecorRes['appName'] = appName
        # Настройка названия текущего модуля в сквозсном декор-словаре (в будущем TODO: что бы это название бралось автоматом из View как-то)
        dicDecorRes['appView'] = vieMethodname
        dicDecorRes['appViewUpper'] = vieMethodname.upper()
        
        return dicDecorRes
    
    



    # # НЕ УДАЛЯТЬ ПОКА
    # @staticmethod
    # def view_inicilization_static (request, viewSettings={}):
    #     """ 
    #     Инициализировать необходимые обще-дефолтные данные для View, а именно:
    #     bmms - модуль необходимых методов работы с облигациями
    #     requestDic - словарь аргументов url-строки из request
    #     dicDecorRes - сквозной словарь для декораторов, в котором инициализируются названия приложения dicDecorRes['appName']  и название метода view dicDecorRes['appView']
    #     dicDecorRes['decor_kwargs']  - общие настройки для всех Views, которые связаны с построением табличного кода для вывода на сайт
    #     Category: Request JANGO
    #     """
        
    #     bmms = BondsMainManagerSpeedup(ms.DB_CONNECTION) # Подключение к конекшену

    #     # Словарь URL-параметров
    #     requestDic = RequestManagerJango.read_urls_args_dic_from_request_django(request)
        
    #     dicDecorRes = {} # Сквозной входной-выходной словарь декораторов, куда можно записывать любые данные и который проходит сквозь все декораторы как репозиторий параметров
        
    #     # Присвоить в сквозной словарь словарь текущих атрибутов URL строки
    #     dicDecorRes['requestDic'] = requestDic
        
    #     # Считывание и внесение в dicDecorRes названий приложения и текущего View . Обязательно использовать при использовании декораторов вначале каждого view с декораторами!!!
    #     dicDecorRes = RequestManagerJango.read_curr_application_and_view_names_to_dic_decor (request, dicDecorRes)
        
        
        
        
    #     # Дефолтные установки по именным параметрам декораторов, если они не заданы в settings.py
        
    #     if 'fromaters' in viewSettings : # Форматеры
    #         fromaters = viewSettings['fromaters']
    #     else:
    #         fromaters = {}
            

        
    #     if 'table_codes' in viewSettings : # Форматеры
    #         tableCodes = viewSettings['table_codes']
    #     else:
    #         tableCodes = {}
        
        
    #     if 'assoc_titles' in viewSettings : # Форматеры
    #         assocTitles = viewSettings['assoc_titles']
    #     else:
    #         assocTitles = {}
            

            
    #     # Настройки именных параметров для основного декоратора процедурного фрейма с учетом дефолтных настроек
    #     dicDecorRes['decor_kwargs'] = {
            
    #         'table_codes' :tableCodes,
    #         'pagination' : ms.PAGINATOR_SET_FUNCS_,
    #         'filtering' : ms.FILTERS_EXPR_TEMPLATES_FOR_FUNCS_BY_TYPE_V2_, # Общая для всех Views ( все фильтры хранятся в одной и той же константе)
    #         'sorting' : ms.SORT_SETTINGS,
    #         'formatting': fromaters,
    #         'assoc_titles': assocTitles,
            
    #     }
        

    #     return bmms, requestDic, dicDecorRes
    
    
    
    # # НЕ УДАЛЯТЬ 
    # def view_context_inicialization_static (dim):
    #     """ 
    #     Инициализация дефолтных парметров контекста View
    #     """
        
    #     requestDic = dim.requestDic
    #     dicDecorRes = dim.dicDecorRes
    #     bmms = dim.bmms
        
    #     # Проверка и настройка контекстных параметров (TODO: Скрыть настройки в другом методе. Придумать)
    #     if 'srch_str' in requestDic:
    #         srch_str =  requestDic['srch_str']
    #     else:
    #         srch_str = ''
            
            
    #     # Раскрытие раздела левой панели навигации в зависимости от названия текущего View
        
    #     leftNavActive = ms.LEFT_NAVIGATOR_ACTIVE_[dicDecorRes['appView']] # dicDecor['appView'] - Название текущего View задает маркер раскрытия левого навигатора
        
            
    #     # Стандартные параметры для контекста вывода таблиц по фрейму на сайт
    #     baseContext = {
    #         'tbCode' : dicDecorRes['tableCode'],
    #         'left_nav_view' : leftNavActive, # Открывающийся раздел в левом навигаторе
    #         'df_qn' : dicDecorRes['dfQn'],
    #         'dfPackages' : bmms.get_index_packages_df_BMMS(), # фрейм с индексными пакетами 
    #         'srch_str' : srch_str,
    #     }
        
    #     return baseContext
        
        
    @staticmethod
    def standart_dframe_dic_decor_inicialization (dicDecorRes):
        """ 
        Инициализировать стандартные данные по формируемому декораторами фрейму во view в сквозном словаре dicDecorRes
        """
        
        dicDecorRes['dfQn']  = len(dicDecorRes['df']) # Кол-во рядов в фрейме
        dicDecorRes['df_col_inx_ini'] =  BondsMainManager.get_indexed_df_cols_dict(dicDecorRes['df']) # Словарь индексированных названий первоначальных колонок в фрейме
        
        
        return dicDecorRes







    @staticmethod
    def read_df_from_request_params_rmdj_static(request):
        """
        RequestManagerJango
        Считать парамметры GET request в data frame
        Category: Request FLASK
        """
        
        reqDict = RequestManagerJango.read_urls_args_dic_from_request_django(request) # Словарь request-параметров
        dfRequest = PandasManager.read_df_from_dictionary_static(reqDict) # Фрейм из словаря request-параметров
        return dfRequest



    @staticmethod
    def read_df_from_request_params_post_rmdj_static(request):
        """
        RequestManagerJango
        Считать парамметры POST request в data frame 
        Category: Request FLASK
        """
        
        reqDict = RequestManagerJango.read_urls_args_dic_from_request_post_django(request) # Словарь request-параметров
        dfRequest = PandasManager.read_df_from_dictionary_static(reqDict) # Фрейм из словаря request-параметров

        return dfRequest




    @staticmethod
    def read_df_from_given_request_params_post_rmdj_static(request, listParams):
        """
        RequestManagerJango
        Считать  заданные в listParams парамметры POST request в data frame 
        Category: Request FLASK
        """
        
        reqDict = RequestManagerJango.read_urls_args_dic_from_request_post_django(request) # Словарь request-параметров
        dfRequest = PandasManager.read_df_from_dictionary_static(reqDict) # Фрейм из словаря request-параметров
        
        dfRequestGiven = PandasManager.slice_df_by_cols_names_pandas_static (dfRequest, listParams)

        return dfRequestGiven




    # Получить чистое название View без модуля аппликэйшн
    def get_clean_view_name_static (request):
        """ 
        Получить чистое называние текущего View
        """
        viewWithModule = request.resolver_match.view_name
        
        parts = viewWithModule.split(':')
        # print(f"PR_987 --> parts = {parts}")
        view = parts[1]
        # print(f"PR_986 --> viewWithModule = {viewWithModule}")
        return view
        





if __name__ == '__main__':
    pass















