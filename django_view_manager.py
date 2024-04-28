
from noocube.request_manager_jango import RequestManagerJango
from noocube.dsource_output_cube_v2 import DSourceOutputCube
from noocube.decorators_jango_cube_v3 import DecoratorsJangoCube
from noocube.funcs_general_class import FunctionsGeneralClass
from noocube.funcs_general import get_intersection_of_two_list
from noocube.re_manager import ReManager
import noocube.re_constants as rc
import re
from noocube.paginator_data_frame_cube_v2 import PaginatorWithDataFrame
from noocube.html_manager_django import HTMLSiteManagerJango
from noocube.pandas_manager import PandasManager
from noocube.bonds_main_manager_speedup import BondsMainManagerSpeedup
from collections import OrderedDict
import pandas  as pd

import sys
sys.path.append('/home/ak/projects/P19_Bonds_Django/bonds_django_proj')
import settings_bdp_main as ms # общие установки для всех модулей

from noocube.switch import Switch
# from bonds_dj_app.local_classes.project_bonds_funcs import ProjectBondsFunctions


class DjangoViewManager ():
    """ 
    Управление View в Django. 
    В первую очередь фреймами и созданием на их базе html-кода для выводимых на страницах сайта таблиц
    """


    def __init__(self, request, viewSettings = {}):
        self.request = request
        self.viewSettings = viewSettings
        
        # инициализация сквозного словаря dicThrough. ПРИМ: Существующая последовательность - важна!
        
        # I. Старт сквозного словаря данных !!!
        self.dicThrough = {} 
        
        # II. основные методы с облигациями на уровне noocube (TODO: Перенести все в проектный класс ProjectBondsFunctions)
        # TODO: Удалить эту инициализацию. инициировать обьект  bmms в самом View, так как иначе нет перехода по функциям курсором и неудобно поэтому
        self.dicThrough['bmms'] = BondsMainManagerSpeedup(ms.DB_CONNECTION) # Подключение к конекшену
        # self.dicThrough['pbf']  = ProjectBondsFunctions(self.dicThrough)

        # III. Словарь URL-параметров
        
        # OBSOLETED:
        self.dicThrough['requestDic']  = RequestManagerJango.read_urls_args_dic_from_request_django(self.request) # OBSOLETED: использовать self.dicThrough['requestDicGet']
        
        self.dicThrough['requestDicGet']  = RequestManagerJango.read_urls_args_dic_from_request_django(self.request)
        self.dicThrough['requestDicPost']  = RequestManagerJango.read_urls_args_dic_from_request_post_django(self.request)
        
        # III-A. Фрейм с request-параметрами
        self.dicThrough['requestFrame'] = RequestManagerJango.read_df_from_request_params_rmdj_static(self.request)
        
        
        # IV. Считывание и внесение в dicDecorRes названий приложения и текущего View . Обязательно использовать при использовании декораторов вначале каждого view с декораторами!!!
        self.dicThrough = RequestManagerJango.read_curr_application_and_view_names_to_dic_decor (self.request, self.dicThrough)
        
        
        # V. Инициализация настроек текущего функционального процессора для обработки процедкрного фрейма (если необходимо)
        # TODO: Сделать альтернативную возможность запуска настроек процессора, а так же его внутренних индивидуальных настроек. 
        # В данном методе используется классический вариант настройки процессора фрейма с дополнительной гибкостью настроек через viewSettings - параметр
        # 
        if len(self.viewSettings) > 0: # Если заданы настройки для процессинга над фреймом
            self.inicialize_functional_processing()


        # VI. Базовая настройка выходного контекста
        # TODO: 
        self.view_basic_context_inicialization_through()
        
        

        


    ### ОБЬЕКТНЫЕ МЕТОДЫ SELF


    def process_frame(self):
        """ 
        Обработка заданного фрейма для вывода конечной таблицы на странице сайта со всем стандартным функционалом (сортировка, наименования столбцов, форматирование колонок, и т.д.)
        """
        
        # ОСНОВНОЙ ДЕКОРАТОР ПРОЦЕДУРНОГО ФРЕЙМА
        @self.decor_proccessor_classic()
        def prepare_data_frame_():
            """Подготовить фрейм с данными. Прим: request необходимо передавать на выходе для оберточных функций"""
            
            # Считывание фрейма со всеми облигациями из сессии
            # self.dicDecorRes['df'] = RequestManagerJango.read_df_as_json_from_session(self.request, 'dfComplexBonds')
            return self.dicDecorRes
        
        # ЗАПУСК вспомогательной декорированной функции
        self.dicDecorRes = prepare_data_frame_()



    def process_frame_with_given_decors(self, dicGivenDecors):
        """ 
        Обработка заданного фрейма задаваемой обоймой декораторов для вывода конечной таблицы на странице сайта со всем стандартным функционалом (сортировка, наименования столбцов, форматирование колонок, и т.д.)
        """
        
        # Константный словарь с ассоциативными никами декораторов и соотвтетсвующими функциями-декораторами
        dicDecorsFunc = {
            'assoc_titles_decor' : '',
            
        }
        
        # ОСНОВНОЙ ДЕКОРАТОР ПРОЦЕДУРНОГО ФРЕЙМА
        @self.decor_given_proccessors_with_order()
        def prepare_data_frame_():
            """Подготовить фрейм с данными. Прим: request необходимо передавать на выходе для оберточных функций"""
            
            # Считывание фрейма со всеми облигациями из сессии
            # self.dicDecorRes['df'] = RequestManagerJango.read_df_as_json_from_session(self.request, 'dfComplexBonds')
            return self.dicDecorRes
        
        # ЗАПУСК вспомогательной декорированной функции
        self.dicDecorRes = prepare_data_frame_()




### ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ 



    @staticmethod
    def view_inicilization (request, viewFrameProcSettings):
        """ 
        Инициализировать необходимые обще-дефолтные данные для View, а именно:
        bmms - модуль необходимых методов работы с облигациями
        requestDic - словарь аргументов url-строки из request
        dicDecorRes - сквозной словарь для декораторов, в котором инициализируются названия приложения dicDecorRes['appName']  и название метода view dicDecorRes['appView']
        dicDecorRes['decor_kwargs']  - общие настройки для всех Views, которые связаны с построением табличного кода для вывода на сайт
        Category: Request JANGO
        """
        
        bmms = BondsMainManagerSpeedup(ms.DB_CONNECTION) # Подключение к конекшену

        # Словарь GET URL-параметров
        requestGetDic = RequestManagerJango.read_urls_args_dic_from_request_get_django(request)
        

        # # Словарь POST URL-параметров
        # requestPostDic = RequestManagerJango.read_urls_args_dic_from_request_post_django(request)
        
        # TODO: Изменить имя. Сквозной словарь не связан только с результатом по декораторам. Он более общий. имя типа: dicProjEndToEnd
        dicDecorRes = {} # Сквозной входной-выходной словарь декораторов, куда можно записывать любые данные и который проходит сквозь все декораторы как репозиторий параметров
        
        # Присвоить в сквозной словарь словарь текущих атрибутов URL строки
        dicDecorRes['requestDic'] = requestGetDic
        
        # # Присвоить в сквозной словарь словарь текущих атрибутов GET URL строки
        # dicDecorRes['requestGetDic'] = requestGetDic
        
        # # Присвоить в сквозной словарь словарь текущих атрибутов POST URL строки
        # dicDecorRes['requestPostDic'] = requestPostDic
        
        
        # Считывание и внесение в dicDecorRes названий приложения и текущего View . Обязательно использовать при использовании декораторов вначале каждого view с декораторами!!!
        dicDecorRes = RequestManagerJango.read_curr_application_and_view_names_to_dic_decor (request, dicDecorRes)
        
        # Дефолтные установки по именным параметрам декораторов, если они не заданы в settings.py
        
        if 'formatters' in viewFrameProcSettings : # Форматеры
            fromaters = viewFrameProcSettings['formatters']
        else:
            fromaters = {}
            
        
        if 'table_codes' in viewFrameProcSettings : # Форматеры
            tableCodes = viewFrameProcSettings['table_codes']
        else:
            tableCodes = {}
        
        if 'assoc_titles' in viewFrameProcSettings : # Форматеры
            assocTitles = viewFrameProcSettings['assoc_titles']
        else:
            assocTitles = {}
            
            
        # Настройки именных параметров для основного декоратора процедурного фрейма с учетом дефолтных настроек
        # TODO: Изменить ключ на что-то типа : 'gen_decor_settings' или 'view_gen_settings'
        dicDecorRes['decor_kwargs'] = {
            
            'table_codes' :tableCodes,
            'pagination' : ms.PAGINATOR_SET_FUNCS_,
            'filtering' : ms.FILTERS_EXPR_TEMPLATES_FOR_FUNCS_BY_TYPE_V2_, # Общая для всех Views ( все фильтры хранятся в одной и той же константе)
            'sorting' : ms.SORT_SETTINGS,
            'formatters': fromaters,
            'assoc_titles': assocTitles,
            
        }
        
        return bmms, requestDic, dicDecorRes
    
    
    
    
    def inicialize_functional_processing(self):
        """ 
        Инициализация настроек функционального процессинга для текущего View 
        """
    
            # Дефолтные установки по именным параметрам декораторов, если они не заданы в settings.py
        
        if 'formatters' in self.viewSettings : # Форматеры
            fromaters = self.viewSettings['formatters']
        else:
            fromaters = {}
            
        
        if 'table_codes' in self.viewSettings : # Форматеры
            tableCodes = self.viewSettings['table_codes']
        else:
            tableCodes = {}
        
        if 'assoc_titles' in self.viewSettings : # Форматеры
            assocTitles = self.viewSettings['assoc_titles']
        else:
            assocTitles = {}
            
            
        # Настройки именных параметров для основного декоратора процедурного фрейма с учетом дефолтных настроек
        # TODO: Изменить ключ на что-то типа : 'gen_decor_settings' или 'view_gen_settings'
        self.dicThrough['decor_kwargs'] = {
            
            'table_codes' :tableCodes,
            'pagination' : ms.PAGINATOR_SET_FUNCS_,
            'filtering' : ms.FILTERS_EXPR_TEMPLATES_FOR_FUNCS_BY_TYPE_V2_, # Общая для всех Views ( все фильтры хранятся в одной и той же константе)
            'sorting' : ms.SORT_SETTINGS,
            'formatters': fromaters,
            'assoc_titles': assocTitles,
            
        }




    def view_basic_context_inicialization_through (self):
        """ 
        DjangoViewManager
        Инициализировать необходимые обще-дефолтные данные для View,  без подключения функционалов. То есть для тех View, в которых нет фреймов
        bmms - модуль необходимых методов работы с облигациями. 
        Со сквозным словарем dicThrough !!!
        requestDic - словарь аргументов url-строки из request
        dicDecorRes - сквозной словарь для декораторов, в котором инициализируются названия приложения dicDecorRes['appName']  и название метода view dicDecorRes['appView']
        dicDecorRes['decor_kwargs']  - общие настройки для всех Views, которые связаны с построением табличного кода для вывода на сайт
        Category: Request JANGO
        """
        
        # 
        # Раскрытие раздела левой панели навигации в зависимости от названия текущего View
        # TODO: перенести из уровня noocube на проектный уровень
        if self.dicThrough['appView'] in ms.LEFT_NAVIGATOR_ACTIVE_: # Если есть ннастройки и необходимость раскрывать раздел левого меню, то:
            leftNavActive = ms.LEFT_NAVIGATOR_ACTIVE_[self.dicThrough['appView']] # dicDecor['appView'] - Название текущего View задает маркер раскрытия левого навигатора
        else: 
            leftNavActive = 'No need to expand left navigator division'
        # print(f" KKKKKKKKKKKK  PR_118 leftNavActive = {leftNavActive}")
            
            
        # Стандартные параметры для контекста вывода таблиц по фрейму на сайт
        baseContext = {
            'left_nav_view' : leftNavActive, # Открывающийся раздел в левом навигаторе
            'dfPackages' : self.dicThrough['bmms'].get_index_packages_df_BMMS(), # фрейм с индексными пакетами 
        }
        
        # Для выделения подразделов левого навигатора и прочих применений
        baseContext['view'] = self.dicThrough['appView']
        
        # Вставка элемента в зависимости от его присутствия в self.requestDic
        # Добавить месяц в baseContext
        if 'payment_month' in self.dicThrough['requestDic']:
            baseContext['payment_month'] = self.dicThrough['requestDic']['payment_month']
            
        # Добавить поисковый текстовый фрагмент
        if 'srch_str' in self.dicThrough['requestDic']:
            baseContext['srch_str'] = self.dicThrough['requestDic']['srch_str']
            
            
        self.dicThrough['context'] = baseContext
        





    
    
    @staticmethod
    def view_inicilization_simple_through_static (request):
        """ 
        DjangoViewManager
        Инициализировать необходимые обще-дефолтные данные для View,  без подключения функционалов. То есть для тех View, в которых нет фреймов
        bmms - модуль необходимых методов работы с облигациями. 
        Со сквозным словарем dicThrough !!!
        requestDic - словарь аргументов url-строки из request
        dicDecorRes - сквозной словарь для декораторов, в котором инициализируются названия приложения dicDecorRes['appName']  и название метода view dicDecorRes['appView']
        dicDecorRes['decor_kwargs']  - общие настройки для всех Views, которые связаны с построением табличного кода для вывода на сайт
        Category: Request JANGO
        """
        
        # TODO: Изменить имя. Сквозной словарь не связан только с результатом по декораторам. Он более общий. имя типа: dicProjEndToEnd
        dicThrough = {} # Сквозной входной-выходной словарь декораторов, куда можно записывать любые данные и который проходит сквозь все декораторы как репозиторий параметров

        
        dicThrough['bmms'] = BondsMainManagerSpeedup(ms.DB_CONNECTION) # Подключение к конекшену

        # Словарь URL-параметров
        dicThrough['requestDic']  = RequestManagerJango.read_urls_args_dic_from_request_django(request)
        
        
        # Считывание и внесение в dicDecorRes названий приложения и текущего View . Обязательно использовать при использовании декораторов вначале каждого view с декораторами!!!
        dicThrough = RequestManagerJango.read_curr_application_and_view_names_to_dic_decor (request, dicThrough)
        
        
        # Инициализация стандартного выходного КОНТЕКСТА
        # Раскрытие раздела левой панели навигации в зависимости от названия текущего View
        if dicThrough['appView'] in ms.LEFT_NAVIGATOR_ACTIVE_: # Если есть ннастройки и необходимость раскрывать раздел левого меню, то:
            leftNavActive = ms.LEFT_NAVIGATOR_ACTIVE_[dicThrough['appView']] # dicDecor['appView'] - Название текущего View задает маркер раскрытия левого навигатора
        else: 
            leftNavActive = 'No need to expand left navigator division'
        # print(f" KKKKKKKKKKKK  PR_118 leftNavActive = {leftNavActive}")
            
        # Стандартные параметры для контекста вывода таблиц по фрейму на сайт
        baseContext = {
            'left_nav_view' : leftNavActive, # Открывающийся раздел в левом навигаторе
            'dfPackages' : dicThrough['bmms'].get_index_packages_df_BMMS(), # фрейм с индексными пакетами 
        }
        
        # Для выделения подразделов левого навигатора и прочих применений
        baseContext['view'] = dicThrough['appView']
        
        # Вставка элемента в зависимости от его присутствия в self.requestDic
        # Добавить месяц в baseContext
        if 'payment_month' in dicThrough['requestDic']:
            baseContext['payment_month'] = dicThrough['requestDic']['payment_month']
            
        # Добавить поисковый текстовый фрагмент
        if 'srch_str' in dicThrough['requestDic']:
            baseContext['srch_str'] = dicThrough['requestDic']['srch_str']
            
            
        dicThrough['context'] = baseContext
        
        

        return dicThrough

    
    
    # @staticmethod
    # def view_inicilization_simple (request, viewFrameProcSettings):
    #     """ 
    #     Инициализировать необходимые обще-дефолтные данные для View !!! без фрейма!!!, а именно:
    #     bmms - модуль необходимых методов работы с облигациями
    #     requestDic - словарь аргументов url-строки из request
    #     dicDecorRes - сквозной словарь для декораторов, в котором инициализируются названия приложения dicDecorRes['appName']  и название метода view dicDecorRes['appView']
    #     dicDecorRes['decor_kwargs']  - общие настройки для всех Views, которые связаны с построением табличного кода для вывода на сайт
    #     Category: Request JANGO
    #     """
        
    #     bmms = BondsMainManagerSpeedup(ms.DB_CONNECTION) # Подключение к конекшену

    #     # Словарь URL-параметров
    #     requestDic = RequestManagerJango.read_urls_args_dic_from_request_django(request)
        
    #     # TODO: Изменить имя. Сквозной словарь не связан только с результатом по декораторам. Он более общий. имя типа: dicProjEndToEnd
    #     dicDecorRes = {} # Сквозной входной-выходной словарь декораторов, куда можно записывать любые данные и который проходит сквозь все декораторы как репозиторий параметров
        
    #     # Присвоить в сквозной словарь словарь текущих атрибутов URL строки
    #     dicDecorRes['requestDic'] = requestDic
        
    #     # Считывание и внесение в dicDecorRes названий приложения и текущего View . Обязательно использовать при использовании декораторов вначале каждого view с декораторами!!!
    #     dicDecorRes = RequestManagerJango.read_curr_application_and_view_names_to_dic_decor (request, dicDecorRes)

        
    #     return bmms, requestDic, dicDecorRes

    
    
    
    def view_context_inicialization (self):
        """ 
        OBSOLETED: Так как это индивидуальные настройки проекта, то метод переносится в проектный класс ProjectBondsFunctions
        Инициализация дефолтных парметров контекста View
        """
        
        # Раскрытие раздела левой панели навигации в зависимости от названия текущего View
        leftNavActive = ms.LEFT_NAVIGATOR_ACTIVE_[self.dicDecorRes['appView']] # dicDecor['appView'] - Название текущего View задает маркер раскрытия левого навигатора
            
        # Стандартные параметры для контекста вывода таблиц по фрейму на сайт
        
        baseContext = {
            'tbCode' : self.dicDecorRes['tableCode'],
            'left_nav_view' : leftNavActive, # Открывающийся раздел в левом навигаторе
            'df_qn' : self.dicDecorRes['dfQn'],
            'dfPackages' : self.bmms.get_index_packages_df_BMMS(), # фрейм с индексными пакетами 
            # 'srch_str' : srch_str,
        }
        
        
        # Для выделения подразделов левого навигатора и прочих применений
        baseContext['view'] = self.dicDecorRes['appView']
        # print(f"LLLLLLLLLLL   PR_119 baseContext['view'] = {baseContext['view']}")
        
        # Вставка элемента в зависимости от его присутствия в self.requestDic
        
        # Добавить месяц в baseContext
        if 'payment_month' in self.requestDic:
            baseContext['payment_month'] = self.requestDic['payment_month']
            
        # Добавить поисковый текстовый фрагмент
        if 'srch_str' in self.requestDic:
            baseContext['srch_str'] = self.requestDic['srch_str']
            
            
        # # добавить динамические разделы -подразделы левого меню
        # inxPckgs = 

        return baseContext


    @staticmethod
    def view_context_inicialization_static (request):
        """ 
        OBSOLETED: Так как это индивидуальные настройки проекта, то метод переносится в проектный класс ProjectBondsFunctions
        Инициализация дефолтных парметров контекста View
        """
            
        # Раскрытие раздела левой панели навигации в зависимости от названия текущего View
        leftNavActive = ms.LEFT_NAVIGATOR_ACTIVE_[self.dicDecorRes['appView']] # dicDecor['appView'] - Название текущего View задает маркер раскрытия левого навигатора
            
        # Стандартные параметры для контекста вывода таблиц по фрейму на сайт
        
        baseContext = {
            'tbCode' : self.dicDecorRes['tableCode'],
            'left_nav_view' : leftNavActive, # Открывающийся раздел в левом навигаторе
            'df_qn' : self.dicDecorRes['dfQn'],
            'dfPackages' : self.bmms.get_index_packages_df_BMMS(), # фрейм с индексными пакетами 
            # 'srch_str' : srch_str,
        }
        
        # Вставка элемента в зависимости от его присутствия в self.requestDic
        
        # Добавить месяц в baseContext
        if 'payment_month' in self.requestDic:
            baseContext['payment_month'] = self.requestDic['payment_month']
            
        # Добавить поисковый текстовый фрагмент
        if 'srch_str' in self.requestDic:
            baseContext['srch_str'] = self.requestDic['srch_str']

        return baseContext






    @staticmethod
    def get_dynamic_decor_func (decorNick):
        """ 
        Получить обьект динамической функции - декоратора по ее нику
        """
    
        classObj = globals()['DjangoViewManager'] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        funcObj = getattr(classObj, decorNick) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
    
        return funcObj



    def df_functional_processing(self, dicOfDecorFuncs, origTargetedDfQnStage = 'mask_delete'):
        """ 
        DjangoViewManager
        Применить обойму функционалов к процедурному фрейму
        origTargetedDfQnStage - название функционала, после наложения которого на процедурный фрейм надо зафиксировать изначальное кол-во рядов процедурного 
        выходного фрейма. По дефолту - кол-во рядов в исходном целевом фрейме фиксируется на этапе после функционала 'mask_delete' : 'delete_df_rows_by_column_mask'
        Но этот этап можно изменить, задав в origTargetedDfQnStage ник функционала, после которого будет фиксироваться кол-во рядов в таргетовом фрейме изначальное. 
        (потому что потом пагинатор производит расслоение общего фрейма на страницы и dicDecorRes['df'] выдает уже порции с максимальны кол-вом равным настройка
        пагинатора для вывода по странице)
        
        Стандартные ники функционалов в их иерархическо последовательности сверху вниз и их названия методов-функционалов в этом классе:

        1 : 'assoc_titles' : 'df_assoc_titles_and_calcs_dd', # трансформация названий колонок процедурного фрейма
        2 : 'formatters' : 'df_formatting_dd', # форматирование колонок процедурного фрейма
        3 : 'mask_delete' : 'delete_df_rows_by_column_mask', # удаление рядов в зависимости от колонки-маски 
        4 : 'sorting' : 'df_sorting_dd', # сортировка по колонкам таблицы на странице сайта
        5 : 'filtration' : 'df_filt_dd', # фильтрация  процедурного фрейма
        6 : 'paginator' : 'df_paginator_dd', # пагинация процедурного фрейма
        7 : 'table_codes' : 'df_table_code_dd', # трансформация названий колонок процедурного фрейма
        
        """
        
        
        print(f'-->  START PR_306 --> : df_functional_processing()')
        
        dicOfDecorFuncsOrd = OrderedDict(sorted(dicOfDecorFuncs.items()))
        
        listFuncsOrd = list(dicOfDecorFuncsOrd.values())
        
        # print(f"IIIIIIIIIIIIIIIIIIII   ^^^^^^^^^^^^^^^^   listFuncsOrd = {listFuncsOrd}")
        
        for funcDecor in listFuncsOrd:

            
            completeFuncname = ms.DF_FUNCTIONAL_NICKS_ASSOC[funcDecor]
            
            oFunc = DjangoViewManager.get_dynamic_decor_func(completeFuncname)
            
            # ПРОЦЕССИНГ ФРЕЙМА
            oFunc(self)
            
            # Этап , после которого  нужно зафиксировать кол-во рядов процедурного фрейма для фиксации изначального кол-ва рядов в исходном целевом фрейме
            if funcDecor == origTargetedDfQnStage:
                self.dicDecorRes['df_qn_orig'] = len(self.dicDecorRes['df'])
            
        
        print(f'-->  END PR_307 --> : df_functional_processing()')





    def df_functional_processing_through(self, dicOfDecorFuncs, origTargetedDfQnStage = 'mask_delete', **fkwargs):
        """ 
        DjangoViewManager
        Применить обойму функционалов к процедурному фрейму
        origTargetedDfQnStage - название функционала, после наложения которого на процедурный фрейм надо зафиксировать изначальное кол-во рядов процедурного 
        выходного фрейма. По дефолту - кол-во рядов в исходном целевом фрейме фиксируется на этапе после функционала 'mask_delete' : 'delete_df_rows_by_column_mask'
        Но этот этап можно изменить, задав в origTargetedDfQnStage ник функционала, после которого будет фиксироваться кол-во рядов в таргетовом фрейме изначальное. 
        (потому что потом пагинатор производит расслоение общего фрейма на страницы и dicDecorRes['df'] выдает уже порции с максимальны кол-вом равным настройка
        пагинатора для вывода по странице)
        
        Стандартные ники функционалов в их иерархическо последовательности сверху вниз и их названия методов-функционалов в этом классе:

        1 : 'assoc_titles' : 'df_assoc_titles_and_calcs_dd', # трансформация названий колонок процедурного фрейма
        2 : 'formatters' : 'df_formatting_dd', # форматирование колонок процедурного фрейма
        3 : 'mask_delete' : 'delete_df_rows_by_column_mask', # удаление рядов в зависимости от колонки-маски 
        4 : 'sorting' : 'df_sorting_dd', # сортировка по колонкам таблицы на странице сайта
        5 : 'filtration' : 'df_filt_dd', # фильтрация  процедурного фрейма
        6 : 'paginator' : 'df_paginator_dd', # пагинация процедурного фрейма
        7 : 'table_codes' : 'df_table_code_dd', # трансформация названий колонок процедурного фрейма
        
        """
        
        
        print(f'-->  START PR_306 --> : df_functional_processing()')
        
        dicOfDecorFuncsOrd = OrderedDict(sorted(dicOfDecorFuncs.items()))
        
        listFuncsOrd = list(dicOfDecorFuncsOrd.values())
        
        # print(f"IIIIIIIIIIIIIIIIIIII   ^^^^^^^^^^^^^^^^   listFuncsOrd = {listFuncsOrd}")
        
        for funcDecor in listFuncsOrd:

            
            completeFuncname = ms.DF_FUNCTIONAL_NICKS_ASSOC[funcDecor]
            
            oFunc = DjangoViewManager.get_dynamic_decor_func(completeFuncname)
            
            # ПРОЦЕССИНГ ФРЕЙМА
            oFunc(self)
            
            # Этап , после которого  нужно зафиксировать кол-во рядов процедурного фрейма для фиксации изначального кол-ва рядов в исходном целевом фрейме
            if funcDecor == origTargetedDfQnStage:
                self.dicThrough['df_qn_orig'] = len(self.dicThrough['df'])
            
        
        print(f'-->  END PR_307 --> : df_functional_processing()')






### END ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ 






### ДИНАМИЧЕСКИЕ ДЕКОРАТОРЫ (DD) (ИЛИ ФУНКЦИОНАЛЫ)



    # def df_assoc_titles_and_calcs_dd(self, **fkwargs):
    #     """
    #     OBSOLETED: Переход на использование сквозного словаря dicThrough. Использовать df_assoc_titles_and_calcs_dd_through()
    #     DjangoViewManager
    #     Динамический Декоратор-функционал для переименования колонок и добавления/изменения калькулируемых колонок
    #     RET: df
    #     Category: Декораторы
    #     """
        
    #     # НЕ УДАЛЯТЬ, для дебагинга
    #     # print(f"AAAAAAAAAAAAAAAAAAAAAA  assoc_titles = {self.dicDecorRes['decor_kwargs']['assoc_titles']} ")
        
    #     # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(self.dicDecorRes['df'], colsIndxed = True, ifPrintDF = True, 
    #     #                                                     marker = f"BBBBBBBBBBBBB $$$$$$$$$$$$###  {self.dicDecorRes['curr_df_nick']}"
    #     #                                                     )
    #     # END НЕ УДАЛЯТЬ, для дебагинга
        
    #     origColsAssocTitles_, calcColsAssocTitles_ = DSourceOutputCube.diffirenciate_orig_and_calc_columns_static_(self.dicDecorRes['decor_kwargs']['assoc_titles'])
    #     # E. Проработать массив данных на предмет названий колонок на базе assocTitles и вырезания из оригинального фрейма тех колонок, Которые заданы в assocTitles
    #     self.dicDecorRes['df'] = DSourceOutputCube.prepare_to_output_static(self.dicDecorRes['df'], origColsAssocTitles_)
    #     fkwargs = {}
    #     self.dicDecorRes['df'] = DSourceOutputCube.add_update_calculated_cols_static_v2_(self.dicDecorRes['df'], calcColsAssocTitles_, **fkwargs)
        
        
        
    def df_assoc_titles_and_calcs_dd_through(self, **fkwargs):
        """
        DjangoViewManager
        Динамический Декоратор-функционал для переименования колонок и добавления/изменения калькулируемых колонок
        RET: df
        Category: Декораторы
        """
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(self.dicThrough['df'], False, colsIndxed=True, marker="PR_900 --> df")
        
        origColsAssocTitles_, calcColsAssocTitles_ = DSourceOutputCube.diffirenciate_orig_and_calc_columns_static_(self.dicThrough['decor_kwargs']['assoc_titles'])
        # E. Проработать массив данных на предмет названий колонок на базе assocTitles и вырезания из оригинального фрейма тех колонок, Которые заданы в assocTitles
        self.dicThrough['df'] = DSourceOutputCube.prepare_to_output_static(self.dicThrough['df'], origColsAssocTitles_)
        fkwargs = {}
        self.dicThrough['df'] = DSourceOutputCube.add_update_calculated_cols_static_v2_(self.dicThrough['df'], calcColsAssocTitles_, **fkwargs)
        
        
        
        






    def df_formatting_dd_through (self):
        """
        DjangoViewManager
        proccessing_df_by_dynamic_funcs_with_row_as_argument () - альтернативное название метода
        Форматирование колонок фрейма  на базе результатов динамически задаваемой функции, где входящим аргументом для динамичекой функции служит ряд фрейма 
        В этом случае в динамической функции можно использовать значения разных ячеек передаваемого ряда для вычисления необходимого результата
        (в не колонка. как ранее)
        ПРИМ: Если мы хотим отформатировать последовательно одну и ту же колонку, то к ключу в форматтере необходимо добавить конечный маркер 
        типа <Название колонки фрейма>'_&&01' (обязательно 5 знаков, включающих '&&')(то есть может быть только 100 одинаковых изменений по одному полю в форматтере). 
        ПРИМ: Обязательно нужна привязка к полю (колонки) фрейма. Но можно задавать поле любое, в конце присваивать полю значение самого себя. Но
        нет смысла присваисвать другим полям какие-то расчетные значения. так как присваивается значение именно к ключевому полю. Так как лямбда - функция присваивает
        не ряд, а только заданное поле. А вот параметры могут передаваться как целый ряд. И из него могут добываться любые значчения из ряда
        Category: Функционалы
        
        """
        
        print(f"START PR_591 --> : df_formatting_dd_through()")
        
        # DEBUG:
        # print(f"FFFFFFFFFFF    ##############  self.dicDecorRes['decor_kwargs']['formatters'] = {self.dicDecorRes['decor_kwargs']['formatters']}")
        # END DEBUG
        if not isinstance(self.dicThrough['df'], int) and len(self.dicThrough['df'].index) > 0: # проверка наличия фрейма и так же наличия рядов в фрейме
            # Обертывание значений по стобцам в соотвтетсвии с заданынми в settings.py (корневой) обертками в константе COLS_WRAPS_FORMATTING_
            for key, wrapFaunc in self.dicThrough['decor_kwargs']['formatters'].items():
                # Получение обьекта функции заданного класса 
                # print(f"\nPR_985 --> key = {key}\n")
                oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (wrapFaunc, byClassFilePAth = True)
                # Применение обертки для соотвтетсвующих столбцов фрейма
                # row.name - представляет индекс ряда. Если задано имя или без имени ~ https://stackoverflow.com/questions/26658240/getting-the-index-of-a-row-in-a-pandas-apply-function
                
                
                # A. Если в ключе присутствует символ '&&', то весь анализ ключей обходится стороной, и просто выполняется функция с параметром = текущему ряду (как пустышка)
                if '&&' in key:
                    key = key[:-5] # Вычитаем последние 4 символа с конца ключа форматтера: '_&&01' (то есть может быть только 100 одинаковых изменений по одному полю в форматтере)
                    # Выполняются любые действия с рядом фрейма, без выделения какого-то особого поля
                    self.dicThrough['df'][key] =  self.dicThrough['df'].apply(lambda row: oFunc(row, row.name, **self.dicThrough), axis = 1)
                else: # Выполняется весь парсинг ключа с выполнением соотвтетсвующих процедур
                    # Анализ ключевого названия колонки. Если есть второе имя через | то это значит заводить новую колонку с резултатом в нее. А аргументом служит первое название колонки
                    keyParts = key.split('|')
                    
                    # TODO: Если было два имени и больше, то первые имена - это аргументы для функции, а последний - результирующая новая колонка . Пока лишь колонка аргумент | колонка результат, если есть
                    if len(keyParts) > 1: 
                        # Находим название новой колонки и ее необходимый порядок в фрейме. 
                        newColParts = keyParts[1].split(':')
                        # Если есть разделитель, то значит задан индекс порядка колонки в фрейме. и устанавливаем колонку по этому индексу. Иначе колонка просто остается в конце фрейма
                        if len(newColParts) > 1: 
                            newColName = newColParts[0]
                            
                            # !!!! ФОРМАТИРОВАНИЕ КОЛОНКИ !!!! . Подставляем в поле ключа - новое название колонки. И поэтмоу будет создана новая колонка. А аргументом выступает первое название колонки
                            self.dicThrough['df'][newColName] =  self.dicThrough['df'].apply(lambda row: oFunc(row, row.name, **self.dicThrough), axis = 1)
                            
                            # Передвигаем колонку на нужное место
                            self.dicThrough['df'] = PandasManager.shift_col_by_name_in_df (self.dicThrough['df'], newColParts[0], int(newColParts[1]))
                        else:
                            newColName = keyParts[1]
                            # ФОРМАТИРОВАНИЕ КОЛОНКИ. Подставляем в поле ключа - новое название колонки. И поэтмоу будет создана новая колонка. А аргументом выступает первое название колонки
                            self.dicThrough['df'][keyParts[1]] =  self.dicThrough['df'].apply(lambda row: oFunc(row, row.name, **self.dicThrough), axis = 1)
                    else: # Если одно ключевое название колонки, значит форматируется или декорируется сама эта колонка
                        
                        self.dicThrough['df'][key] =  self.dicThrough['df'].apply(lambda row: oFunc(row, row.name, **self.dicThrough), axis = 1)
                        
                
                
                # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(self.dicThrough['df'], ifPrintDF = False, colsIndxed = True, 
                #                                                 marker = f"\nPR_983 --> {key}  Formated df")
                
            
        print(f"END PR_591 --> : df_formatting_dd_through()")
        
        return self.dicThrough['df']







    def delete_df_rows_by_column_mask (self):
        """ 
        OBSOLETED: use delete_df_rows_by_column_mask_trhough()
        Удаляить ряды фрейма в зависимости от True/False колонки-маски
        """
        # DEBUG:
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static (self.dicDecorRes['df'], ifPrintDF = False,  colsIndxed = False, marker = 'AAAAAAAAAAAA  ########')
        # END DEBUG
        
        print(f'-->  START PR_301 --> : delete_df_rows_by_column_mask()') # Маркер старта метода для лога в консоли

        
        if 'mask_column' in self.requestDic:
            maskCol = self.requestDic['mask_column']
            self.dicDecorRes['df']  = PandasManager.clear_df_by_mask_column_name_bool_pandas(self.dicDecorRes['df'], maskCol)
            
        print(f'-->  END PR_302 --> : delete_df_rows_by_column_mask()')




    def delete_df_rows_by_column_mask_trhough (self):
        """ 
        Удаляить ряды фрейма в зависимости от True/False колонки-маски
        """
        # DEBUG:
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static (self.dicDecorRes['df'], ifPrintDF = False,  colsIndxed = False, marker = 'AAAAAAAAAAAA  ########')
        # END DEBUG
        
        print(f'-->  START PR_301 --> : delete_df_rows_by_column_mask()') # Маркер старта метода для лога в консоли

        
        if 'mask_column' in self.dicThrough['requestDic']:
            maskCol = self.dicThrough['requestDic']['mask_column']
            self.dicThrough['df']  = PandasManager.clear_df_by_mask_column_name_bool_pandas(self.dicThrough['df'], maskCol)
            
        print(f'-->  END PR_302 --> : delete_df_rows_by_column_mask()')






    def df_sorting_dd (self, **skwargs):
        """
        OBSOLETED: use df_sorting_dd_through()
        DjangoViewManager
        Динамический Декоратор-функционал для сортировки колонок процедурного фрейма
        RET: df
        Category: Декораторы
        """
        
        print(f'-->  START PR_304 --> : df_sorting_dd()')
        
        # Словарь для перевода стрингового True/False в булиновые значения
        toBool = {'True':True,'False':False}

        # Текущее состояние по сортировке из requestDic
        requestSortCurrState = {}
        # Если не задана колонка сортировки, то присваивается первая колонка из списка колонок, подлежащих сортировке в TABLE_SORT_COLS_FUNCS_
        if 'sort_col' in self.requestDic:
            requestSortCurrState['sort_col'] = self.requestDic['sort_col'] # Текущая колонка сортировки
        else:
            # Сортировка по умолчанию {SORT_COLUMN_BY_DEFAULT}
            if 'default_sort_col' in skwargs: # Если задана колонка для сортировки по умолчанию
                requestSortCurrState['sort_col'] =  skwargs['default_sort_col'] #dicDecorRes['df'].columns.tolist()[5] # 'Название' # df.columns.tolist()[0]
            else: # Если не задана дефолтная колонка для сортирвки, то сортировка идет по первой колонке с индексом 0
                requestSortCurrState['sort_col'] = self.dicDecorRes['df'].columns.tolist()[0]
            
        # Если не задана страница
        if 'pg' not in self.requestDic:
            self.requestDic['pg'] = '1' 

        # Если не задано направление сортировки, то присваивается направление = True (то есть ASC)
        if 'sort_asc' in self.requestDic:
            requestSortCurrState['sort_asc'] = toBool[self.requestDic['sort_asc']]   # Текщее направление сортировки
        else:
            if 'default_sort_dir' in skwargs: # Если задано направление сортировки по умолчанию, то используем ее
                # Направление сортировки по умолчанию {SORT_DIRECTION_BY_DEFAULT}
                requestSortCurrState['sort_asc'] = skwargs['default_sort_dir']
            else: # Если не задано направление сортировки по умолчанию, то равно True (то есть asc, по возрастающей)
                requestSortCurrState['sort_asc'] = True

        if 'sort_col' in requestSortCurrState and 'sort_asc' in requestSortCurrState:
            self.dicDecorRes['df'] = self.dicDecorRes['df'].sort_values(by=[requestSortCurrState['sort_col']], ascending = requestSortCurrState['sort_asc'])
            
        print(f'-->  END PR_305 --> : df_sorting_dd()')





    def df_sorting_dd_through (self, **skwargs):
        """
        DjangoViewManager
        Динамический Декоратор-функционал для сортировки колонок процедурного фрейма
        RET: df
        Category: Декораторы
        """
        
        print(f'-->  START PR_304 --> : df_sorting_dd_through()')
        
        # Словарь для перевода стрингового True/False в булиновые значения
        toBool = {'True':True,'False':False}

        # Текущее состояние по сортировке из requestDic
        requestSortCurrState = {}
        # Если не задана колонка сортировки, то присваивается первая колонка из списка колонок, подлежащих сортировке в TABLE_SORT_COLS_FUNCS_
        if 'sort_col' in self.dicThrough['requestDic']:
            requestSortCurrState['sort_col'] = self.dicThrough['requestDic']['sort_col'] # Текущая колонка сортировки
        else:
            # Сортировка по умолчанию {SORT_COLUMN_BY_DEFAULT}
            if 'default_sort_col' in skwargs: # Если задана колонка для сортировки по умолчанию
                requestSortCurrState['sort_col'] =  skwargs['default_sort_col'] #dicDecorRes['df'].columns.tolist()[5] # 'Название' # df.columns.tolist()[0]
            else: # Если не задана дефолтная колонка для сортирвки, то сортировка идет по первой колонке с индексом 0
                requestSortCurrState['sort_col'] = self.dicThrough['df'].columns.tolist()[0]
            
        # Если не задана страница
        if 'pg' not in self.dicThrough['requestDic']:
            self.dicThrough['requestDic']['pg'] = '1' 

        # Если не задано направление сортировки, то присваивается направление = True (то есть ASC)
        if 'sort_asc' in self.dicThrough['requestDic']:
            requestSortCurrState['sort_asc'] = toBool[self.dicThrough['requestDic']['sort_asc']]   # Текщее направление сортировки
        else:
            if 'default_sort_dir' in skwargs: # Если задано направление сортировки по умолчанию, то используем ее
                # Направление сортировки по умолчанию {SORT_DIRECTION_BY_DEFAULT}
                requestSortCurrState['sort_asc'] = skwargs['default_sort_dir']
            else: # Если не задано направление сортировки по умолчанию, то равно True (то есть asc, по возрастающей)
                requestSortCurrState['sort_asc'] = True

        if 'sort_col' in requestSortCurrState and 'sort_asc' in requestSortCurrState:
            self.dicThrough['df'] = self.dicThrough['df'].sort_values(by=[requestSortCurrState['sort_col']], ascending = requestSortCurrState['sort_asc'])
            
        print(f'-->  END PR_305 --> : df_sorting_dd()')







    def df_filt_dd (self):
        """
        DjangoViewManager
        Динамический Декоратор-функционал для фильтрации  процедурного фрейма
        RET: df
        Category: Декораторы
        """

        print(f'-->  START PR_308 --> : df_filt_dd()')
        
        
        # print(f"PR_313 --> df = \n{self.dicDecorRes['df']}")


        # Пересечение по ключам между request url-аргументов и ключами в словаре формул для фильтрации () (В фильтрации участвуют только те фильтры из settings.py, 
        # которые запускают url-аргументы в url-request своими названиями. если название ключа словаря набора фильтров совпадают с возможным  url-аргументом 
        # request, то фильтр активизируется)
        kysIntersect = get_intersection_of_two_list(list(self.requestDic.keys()), list(self.dicDecorRes['decor_kwargs']['filtering'].keys()))
        
        # print (f"%%%%%%%%%%%%%%%%   &&&&&&&&&&&  kysIntersect = {kysIntersect}")
        
        # Цикл по списку задаваемой обоймы фильтров в filtsIni
        for key in kysIntersect:
            
            print(f"PROJ PR PR_314 --> : Текущий ключ обоймы фильтров -> {key}")
            print(f"PR_891 --> requestDic : {key}")
            # Если url-аргумент в request не пустой (так как могут быть пустые аргументы, Которые просто игнорируются)
            if len(self.requestDic[key]) > 0:
                
                fExprByKey = self.dicDecorRes['decor_kwargs']['filtering'][key]
                print(f"PR_890 --> Текущее выражение фильтрации : {fExprByKey}")
                
                # Если в формуле присутствует локальная переменная, начинающаяся с @<url-arg == key in filter formula>,  то замещаем эту локальную переменную
                # с именем равным ключу ф словаре фильтров, а так же равной url-аргументу в request ( так как именно этот фактор связывает нахождение формулы в словаре фильтров: )
                if '@' in fExprByKey:
                    fExprByKey = fExprByKey.replace('@' + key, self.requestDic[key])
                    
                    
                    
                # ЗАЩИТА от применения комплексного или простого фильтра к тем полям, которых нет в процедурном фрейме !!!
                
                # Проверить, Есть ли поле в формуле фильтра в фрейме (это позволит универсализировать константу по фильтрам в settings.py)
                # Если нет, то не фильтровать по этому полю, иначе ошибка в jquery ajax
                # Сложная проверка и парсер для формулы, Если выражение комплексное, то есть из логических обьединений через & или |
                filterFlag = False # Флаг: Фильтрация разрешается или нет
                
                # A. Парсинг регулярными выражениями формулы фильтра
                rExpr = r"([&|])"
                mo  = ReManager.find_all_matches_from_text(fExprByKey, rExpr)
                
                # print (f'%%%%%%%%%%%%%  RESEARCH  &&&&&&&& mo = {mo}')
                
                dfColumns = list(self.dicDecorRes['df']) 
                
                if len(mo) > 1: # Если частей больше 1, то это значит комплексное выражение и особый парсинг
                    # filterFlag = False
                    # print(f'%%%%%%%%%%%%%  COMPLEX &&&&&&&&  fExprByKey = {fExprByKey}')
                    
                    # Найти все поля во всех соединенных частях комплексной формулы фидьтрации
                    rExp = rc.STRINGS_WITH_DOT_AT_END
                    mo  = ReManager.find_all_matches_from_text(fExprByKey, rExp)
                    
                    # B. Найти обращение к полям в формуле и выделить эти поля в список
                    # Выделить только первое слово, заканчивающееся на точку. И это будет - поле
                    mo = [x.split('.')[0] for x in mo]
                    
                    # print(f'%%%%%%%%%%%%%  COMPLEX &&&&&&&&  fExprByKey = {fExprByKey}')
                    # print(f'%%%%%%%%%%%%%  COMPLEX RESULT &&&&&&&&  mo = {mo}')
                    # print(f'%%%%%%%%%%%%%  COMPLEX REXP &&&&&&&&  rExp = {rExp}')
                    
                    
                    # C. Найти пересечение списка названий колонок фрейма и списка колонок из фильтра fExprByKey
                    lIntersect = get_intersection_of_two_list(dfColumns, mo)
                    # print(f'%%%%%%%%%%%%%  COMPLEX INTERSECT &&&&&&&&  lIntersect = {lIntersect}')
                    
                    # D. Сформировать формулу из тех частей комплексной формулы фильтрации, в которых есть только разрешенные поля из пересечения lIntersect
                    rExp = r"[&|]"
                    logicOperands  = ReManager.find_all_matches_from_text(fExprByKey, rExp) # последовательный список операндов
                    # print(f'%%%%%%%%%%%%%  COMPLEX RES &&&&&&&&  logicOperands = {logicOperands}')
                    
                    filterParts = re.split(rExp, fExprByKey) # Суб-части формулы комплексного фильтра
                    # print(f'%%%%%%%%%%%%%  COMPLEX PARTS &&&&&&&&  filterParts = {filterParts}')
                    
                    # E. Сформировать словарь суб-частей фильтра, где ключ - формула, значение - операнд слева. Первая суб-часть формулы будет иметь значение - ''
                    dicFilterSubParts = {}
                    for inx, x in enumerate(filterParts): # Цикл по 
                        # Очистить x от прбелов по концам
                        x = x.strip()
                        if inx == 0:
                            dicFilterSubParts[x] = ''
                        else:
                            dicFilterSubParts[x] = logicOperands[inx-1]
                    
                    
                    # print(f'%%%%%%%%%%%%%  COMPLEX DICT &&&&&&&&  dicFilterSubParts = {dicFilterSubParts}')
                    
                    # F. Исключить из словаря dicFilterSubParts те записи, где поля суб-частей (которые в ключах) не входят в резрешенные поля lIntersect
                    
                    # dicFilterSubParts = {key:value for (key,value) in dicFilterSubParts.items() if }
                    dicsubPartExcluded = [] # Список исключаемых из фильтрации суб-частей фильтра и поля этих суб-частей
                    finalComplexFilter = ''# Конечный фильтр, в котором исключены суб-части, где используются поля, Которых нет в фрейме
                    for subPart, operand in  dicFilterSubParts.items():
                        subField = subPart.split('.')[0] # Название поля, участвующего в суб-части составного фильтра
                        # print(f'%%%%%%%%%%%%%  COMPLEX SUB-FIELD &&&&&&&&  subField = {subField}')
                        if subField in lIntersect: # если поле в суб-части фильтра иммется в разрешительном списке lIntersect, то суб-часть допускается для фильтрации
                            # print(f'%%%%%%%%%%%%%  COMPLEX SUB-FIELD ALLOWED &&&&&&&&  subField = {subField}')
                            finalComplexFilter += operand + subPart
                            
                            # Включение флага разрешения фильтрации 
                            filterFlag = True
                        
                        else: # Инче суб-часть фильтра не допускается для фильтрации. Добавить исключенную суб-часть и поле в список исключенных суб-частей фильтра
                            dicsubPartExcluded.append(subPart)
                            # Програмный принтинг
                            print(f'PROJ LOG ----> PR_312 --> : В составном фильтре выявлена и исключена суб-часть с отсутствующим в фрейме полем: \'{subPart}\' | Декоратор: @filter_by_query_v2()')
                    
                    
                    # print(f'%%%%%%%%%%%%%  COMPLEX FINAL &&&&&&&&  finalComplexFilter = {finalComplexFilter}')
                    # print(f'%%%%%%%%%%%%%  COMPLEX EXCLUDED &&&&&&&&  dicsubPartExcluded = {dicsubPartExcluded}')
                    
                    
                else: # Если частей = 1, то это значит Простая формула, не составная. Но все равно проверяем наличие поля
                    
                    field = fExprByKey.split('.')[0] # Парсинг поля из формулы фильтра
                
                    # print(f'%%%%%%%%%%%%%  SIMPLE &&&&&&&&  field = {field} and dfColumns = {dfColumns} and fExprByKey = {fExprByKey}')
                    # Включение флага разрешения фильтрации
                    if field in dfColumns: # Если поле находится в списке полей фрейма
                        filterFlag = True
                        finalComplexFilter = fExprByKey
                    else: # В ином случае фильтр не допускается к фильтрации
                        print(f'PROJ LOG  ----> PR_311 --> : Фильтр по полю, которого нет в фрейме. Дезактивирован: \'{subPart}\' | Декоратор: @filter_by_query_v2()')

                # END ЗАЩИТА от применения комплексного  или простого фильтра к тем полям, которых нет в процедурном фрейме !!!

                import pandas
                pandas.set_option('display.max_columns', None)
                print(f"PR_461 --> df = \n{self.dicDecorRes['df']}")
                # Если разрешена фильтрация
                if filterFlag:
                    self.dicDecorRes['df'] =  self.dicDecorRes['df'].query(f"{finalComplexFilter}", engine='python')
                    
                    # Програмный принтинг
                    print(f'PROJ LOG ----> PR_310 --> : Проведена фильтрация фрейма по формуле: \'{finalComplexFilter}\' | Декоратор: @filter_by_query_v2()')
                
                # print (f"$$$$$$$$$$$$$$$$  SFTER FILT  ^^^^^^^^^ dicDecorRes['df']_N = {len(dicDecorRes['df'])}")

        print(f'-->  END PR_309 --> : df_filt_dd()')






    def df_filt_dd_through (self):
        """
        DjangoViewManager
        Динамический Декоратор-функционал для фильтрации  процедурного фрейма
        RET: df
        Category: Декораторы
        """

        print(f'-->  START PR_308 --> : df_filt_dd()')
        
        
        # print(f"PR_313 --> df = \n{self.dicDecorRes['df']}")


        # Пересечение по ключам между request url-аргументов и ключами в словаре формул для фильтрации () (В фильтрации участвуют только те фильтры из settings.py, 
        # которые запускают url-аргументы в url-request своими названиями. если название ключа словаря набора фильтров совпадают с возможным  url-аргументом 
        # request, то фильтр активизируется)
        kysIntersect = get_intersection_of_two_list(list(self.dicThrough['requestDic'].keys()), list(self.dicThrough['decor_kwargs']['filtering'].keys()))
        
        # print (f"%%%%%%%%%%%%%%%%   &&&&&&&&&&&  kysIntersect = {kysIntersect}")
        
        # Цикл по списку задаваемой обоймы фильтров в filtsIni
        for key in kysIntersect:
            
            print(f"PROJ PR PR_314 --> : Текущий ключ обоймы фильтров -> {key}")
            
            # Если url-аргумент в request не пустой (так как могут быть пустые аргументы, Которые просто игнорируются)
            if len(self.dicThrough['requestDic'][key]) > 0:
            
                fExprByKey = self.dicThrough['decor_kwargs']['filtering'][key]
                
                
                # Если в формуле присутствует локальная переменная, начинающаяся с @<url-arg == key in filter formula>,  то замещаем эту локальную переменную
                # с именем равным ключу ф словаре фильтров, а так же равной url-аргументу в request ( так как именно этот фактор связывает нахождение формулы в словаре фильтров: )
                if '@' in fExprByKey:
                    fExprByKey = fExprByKey.replace('@' + key, self.dicThrough['requestDic'][key])
                    
                print(f"PR_890 --> Текущее выражение фильтрации : {fExprByKey}")
                    
                # ЗАЩИТА от применения комплексного или простого фильтра к тем полям, которых нет в процедурном фрейме !!!
                
                # Проверить, Есть ли поле в формуле фильтра в фрейме (это позволит универсализировать константу по фильтрам в settings.py)
                # Если нет, то не фильтровать по этому полю, иначе ошибка в jquery ajax
                # Сложная проверка и парсер для формулы, Если выражение комплексное, то есть из логических обьединений через & или |
                filterFlag = False # Флаг: Фильтрация разрешается или нет
                
                # A. Парсинг регулярными выражениями формулы фильтра
                rExpr = r"([&|])"
                mo  = ReManager.find_all_matches_from_text(fExprByKey, rExpr)
                
                # print (f'%%%%%%%%%%%%%  RESEARCH  &&&&&&&& mo = {mo}')
                
                dfColumns = list(self.dicThrough['df']) 
                
                if len(mo) > 1: # Если частей больше 1, то это значит комплексное выражение и особый парсинг
                    # filterFlag = False
                    # print(f'%%%%%%%%%%%%%  COMPLEX &&&&&&&&  fExprByKey = {fExprByKey}')
                    
                    # Найти все поля во всех соединенных частях комплексной формулы фидьтрации
                    rExp = rc.STRINGS_WITH_DOT_AT_END
                    mo  = ReManager.find_all_matches_from_text(fExprByKey, rExp)
                    
                    # B. Найти обращение к полям в формуле и выделить эти поля в список
                    # Выделить только первое слово, заканчивающееся на точку. И это будет - поле
                    mo = [x.split('.')[0] for x in mo]
                    
                    # print(f'%%%%%%%%%%%%%  COMPLEX &&&&&&&&  fExprByKey = {fExprByKey}')
                    # print(f'%%%%%%%%%%%%%  COMPLEX RESULT &&&&&&&&  mo = {mo}')
                    # print(f'%%%%%%%%%%%%%  COMPLEX REXP &&&&&&&&  rExp = {rExp}')
                    
                    
                    # C. Найти пересечение списка названий колонок фрейма и списка колонок из фильтра fExprByKey
                    lIntersect = get_intersection_of_two_list(dfColumns, mo)
                    # print(f'%%%%%%%%%%%%%  COMPLEX INTERSECT &&&&&&&&  lIntersect = {lIntersect}')
                    
                    # D. Сформировать формулу из тех частей комплексной формулы фильтрации, в которых есть только разрешенные поля из пересечения lIntersect
                    rExp = r"[&|]"
                    logicOperands  = ReManager.find_all_matches_from_text(fExprByKey, rExp) # последовательный список операндов
                    # print(f'%%%%%%%%%%%%%  COMPLEX RES &&&&&&&&  logicOperands = {logicOperands}')
                    
                    filterParts = re.split(rExp, fExprByKey) # Суб-части формулы комплексного фильтра
                    # print(f'%%%%%%%%%%%%%  COMPLEX PARTS &&&&&&&&  filterParts = {filterParts}')
                    
                    # E. Сформировать словарь суб-частей фильтра, где ключ - формула, значение - операнд слева. Первая суб-часть формулы будет иметь значение - ''
                    dicFilterSubParts = {}
                    for inx, x in enumerate(filterParts): # Цикл по 
                        # Очистить x от прбелов по концам
                        x = x.strip()
                        if inx == 0:
                            dicFilterSubParts[x] = ''
                        else:
                            dicFilterSubParts[x] = logicOperands[inx-1]
                    
                    
                    # print(f'%%%%%%%%%%%%%  COMPLEX DICT &&&&&&&&  dicFilterSubParts = {dicFilterSubParts}')
                    
                    # F. Исключить из словаря dicFilterSubParts те записи, где поля суб-частей (которые в ключах) не входят в резрешенные поля lIntersect
                    
                    # dicFilterSubParts = {key:value for (key,value) in dicFilterSubParts.items() if }
                    dicsubPartExcluded = [] # Список исключаемых из фильтрации суб-частей фильтра и поля этих суб-частей
                    finalComplexFilter = ''# Конечный фильтр, в котором исключены суб-части, где используются поля, Которых нет в фрейме
                    for subPart, operand in  dicFilterSubParts.items():
                        subField = subPart.split('.')[0] # Название поля, участвующего в суб-части составного фильтра
                        # print(f'%%%%%%%%%%%%%  COMPLEX SUB-FIELD &&&&&&&&  subField = {subField}')
                        if subField in lIntersect: # если поле в суб-части фильтра иммется в разрешительном списке lIntersect, то суб-часть допускается для фильтрации
                            # print(f'%%%%%%%%%%%%%  COMPLEX SUB-FIELD ALLOWED &&&&&&&&  subField = {subField}')
                            finalComplexFilter += operand + subPart
                            
                            # Включение флага разрешения фильтрации 
                            filterFlag = True
                        
                        else: # Инче суб-часть фильтра не допускается для фильтрации. Добавить исключенную суб-часть и поле в список исключенных суб-частей фильтра
                            dicsubPartExcluded.append(subPart)
                            # Програмный принтинг
                            print(f'PROJ LOG ----> PR_312 --> : В составном фильтре выявлена и исключена суб-часть с отсутствующим в фрейме полем: \'{subPart}\' | Функционал-обработчик: df_filt_dd_through()')
                    
                    
                    # print(f'%%%%%%%%%%%%%  COMPLEX FINAL &&&&&&&&  finalComplexFilter = {finalComplexFilter}')
                    # print(f'%%%%%%%%%%%%%  COMPLEX EXCLUDED &&&&&&&&  dicsubPartExcluded = {dicsubPartExcluded}')
                    
                    
                else: # Если частей = 1, то это значит Простая формула, не составная. Но все равно проверяем наличие поля
                    
                    # ПРИМ: Если идет динамическая формула, то есть формула вставляемая в textzrea на странице сайта динамически, то
                    # она считается простой и в ней пока проверяется только первое поле. Потом надо сделать проверку всех полей
                    
                    # field = fExprByKey.split('.')[0] # Парсинг поля из формулы фильтра
                    print(f"PR_893 --> Точка прохождения ")
                    field = ReManager.get_first_word_special_019(fExprByKey)  # Парсинг первого слова (названия поля) из формулы фильтра
                    # Удалить точку в конце, если есть (это нужно, если фильтр стационарный в settings, который contain какой-то фрагмент текста)
                    field = field.rstrip('.')
                    
                    print(f"PR_891 --> Название поля при простом фильтре, парсинг через reg expr: field = {field}")
                
                    # print(f'%%%%%%%%%%%%%  SIMPLE &&&&&&&&  field = {field} and dfColumns = {dfColumns} and fExprByKey = {fExprByKey}')
                    # Включение флага разрешения фильтрации
                    if field in dfColumns: # Если поле находится в списке полей фрейма
                        print(f"PR_892 --> Точка прохождения ")
                        filterFlag = True
                        finalComplexFilter = fExprByKey
                    else: # В ином случае фильтр не допускается к фильтрации
                        print(f'PROJ LOG  ----> PR_311 --> : Фильтр по полю, которого нет в фрейме или неправильное выражение фильтра.  | Функционал-обработчик: df_filt_dd_through()')

                # END ЗАЩИТА от применения комплексного  или простого фильтра к тем полям, которых нет в процедурном фрейме !!!

                import pandas
                pandas.set_option('display.max_columns', None)
                print(f"PR_461 --> df = \n{self.dicThrough['df']}")
                # Если разрешена фильтрация
                if filterFlag:
                    self.dicThrough['df'] =  self.dicThrough['df'].query(f"{finalComplexFilter}", engine='python')
                    
                    # Програмный принтинг
                    print(f'PROJ LOG ----> PR_310 --> : Проведена фильтрация фрейма по формуле: \'{finalComplexFilter}\' | Функционал-обработчик: df_filt_dd_through()')
                
                # print (f"$$$$$$$$$$$$$$$$  SFTER FILT  ^^^^^^^^^ dicDecorRes['df']_N = {len(dicDecorRes['df'])}")

        print(f'-->  END PR_309 --> : df_filt_dd()')









    def df_paginator_dd (self):
        """
        OBSOLETED
        DjangoViewManager
        Динамический Декоратор-функционал для фильтрации  процедурного фрейма
        RET: df
        Category: Декораторы
        """



        # Кол-во записей после филльтрации или у исходного массива (после пагинации не менять это кол-во, так как пагинатор устанавливает dicDecorRes['df'] равной страничной выборке)
        self.dicDecorRes['dfQn'] = len(self.dicDecorRes['df'])
        # Если  есть ряды в фрейме
        if len(self.dicDecorRes['df']) > 0:
            
            # Если не задана активная страница в requestDic, но есть фрейм с рядами
            if not 'pg' in self.requestDic:
                pg = '1'
            # Если есть активная страница в reuest возврате со страницы сайта
            else : 
                pg = self.requestDic['pg']
                
            paginator = PaginatorWithDataFrame(self.dicDecorRes['df'], self.dicDecorRes['decor_kwargs']['pagination']['paginGenSet'] ) # инициализация обьекта пагинатора в общей форме
            paginator = PaginatorWithDataFrame.get_curr_paginator_from_gen(paginator,  pg) 
            
            self.dicDecorRes['cuuPaginator'] = paginator # Текущий пагинатор
            
            
            # Выходной постраничный активный массив обработанных данных, соотвтетсвующий активной страницы пагинатора self.pgCell
            dfPage = paginator.dfLimByPgNumb
            
            # Подготовить HTML-код нумератора для активнйо страницы
            
            # Базовая ссылка с суб-доменами названия приложения и названия метода View для ссылок страниц нумератора
            url = f"/{self.dicDecorRes['appName']}/{self.dicDecorRes['appView']}"

            # Константная суб-строка с аргументами в ссылке сортировки по заголовкам  с вычетом аргументов в спсиках исключениях genExcludeListFoSort и self.excludeUrlArgsForSort
            constUrlArgsPaginLine = HTMLSiteManagerJango.prpare_const_line_from_url_args_matrix_with_exclusions(self.requestDic, self.dicDecorRes['decor_kwargs']['pagination']['genExcludeListFoPagin'])
            pState = paginator.curr_paginator_state_dict
            paginatorHtml = f"""
            <div class="pagination">
            <a href="{url}?pg=1{constUrlArgsPaginLine}">В начало</a>
                <a href="{url}?pg={pState['prevBlockPageToActivate']}{constUrlArgsPaginLine}">&laquo;</a>"""
                
            for pg in pState['pagesList']:
                if pg == pState['pgToActivate']:
                    paginatorHtml += f'<a class="active">{pg}</a>'
                else:
                    paginatorHtml += f'<a href="{url}?pg={pg}{constUrlArgsPaginLine}">{pg}</a>'
                    
            paginatorHtml += f"""        
                <a href="{url}?pg={pState['nextBlockPageToActivate']}{constUrlArgsPaginLine}">&raquo;</a>
            </div>
            """
            # END Подготовить HTML-код нумератора для активнйо страницы
            
            self.dicDecorRes['df'] = dfPage
            self.dicDecorRes['paginatorHtml'] = paginatorHtml
                
        # Если нет рядовв фрейме (то есть фрейм - пустой)        
        else:
            self.dicDecorRes['df'] = -1
            self.dicDecorRes['paginatorHtml'] = ''





    def df_paginator_dd_through (self):
        """
        DjangoViewManager
        Динамический Декоратор-функционал для фильтрации  процедурного фрейма
        RET: df
        Category: Декораторы
        """



        # Кол-во записей после филльтрации или у исходного массива (после пагинации не менять это кол-во, так как пагинатор устанавливает dicDecorRes['df'] равной страничной выборке)
        self.dicThrough['dfQn'] = len(self.dicThrough['df'])
        # Если  есть ряды в фрейме
        if len(self.dicThrough['df']) > 0:
            
            # Если не задана активная страница в requestDic, но есть фрейм с рядами
            if not 'pg' in self.dicThrough['requestDic']:
                pg = '1'
            # Если есть активная страница в reuest возврате со страницы сайта
            else : 
                pg = self.dicThrough['requestDic']['pg']
                
            paginator = PaginatorWithDataFrame(self.dicThrough['df'], self.dicThrough['decor_kwargs']['pagination']['paginGenSet'] ) # инициализация обьекта пагинатора в общей форме
            paginator = PaginatorWithDataFrame.get_curr_paginator_from_gen(paginator,  pg) 
            
            self.dicThrough['cuuPaginator'] = paginator # Текущий пагинатор
            
            
            # Выходной постраничный активный массив обработанных данных, соотвтетсвующий активной страницы пагинатора self.pgCell
            dfPage = paginator.dfLimByPgNumb
            
            # Подготовить HTML-код нумератора для активнйо страницы
            
            # Базовая ссылка с суб-доменами названия приложения и названия метода View для ссылок страниц нумератора
            url = f"/{self.dicThrough['appName']}/{self.dicThrough['appView']}"

            # Константная суб-строка с аргументами в ссылке сортировки по заголовкам  с вычетом аргументов в спсиках исключениях genExcludeListFoSort и self.excludeUrlArgsForSort
            constUrlArgsPaginLine = HTMLSiteManagerJango.prpare_const_line_from_url_args_matrix_with_exclusions(self.dicThrough['requestDic'], self.dicThrough['decor_kwargs']['pagination']['genExcludeListFoPagin'])
            pState = paginator.curr_paginator_state_dict
            paginatorHtml = f"""
            <div class="pagination">
            <a href="{url}?pg=1{constUrlArgsPaginLine}">В начало</a>
                <a href="{url}?pg={pState['prevBlockPageToActivate']}{constUrlArgsPaginLine}">&laquo;</a>"""
                
            for pg in pState['pagesList']:
                if pg == pState['pgToActivate']:
                    paginatorHtml += f'<a class="active">{pg}</a>'
                else:
                    paginatorHtml += f'<a href="{url}?pg={pg}{constUrlArgsPaginLine}">{pg}</a>'
                    
            paginatorHtml += f"""        
                <a href="{url}?pg={pState['nextBlockPageToActivate']}{constUrlArgsPaginLine}">&raquo;</a>
            </div>
            """
            # END Подготовить HTML-код нумератора для активнйо страницы
            
            self.dicThrough['df'] = dfPage
            self.dicThrough['paginatorHtml'] = paginatorHtml
                
        # Если нет рядовв фрейме (то есть фрейм - пустой)        
        else:
            self.dicThrough['df'] = -1
            self.dicThrough['paginatorHtml'] = ''







    def df_table_code_dd (self):
        """
        OBSOLETED
        DjangoViewManager
        Динамический Декоратор-функционал для фильтрации  процедурного фрейма
        RET: df
        Category: Декораторы
        """



        # Получить динамический обьект метода, отвечающего за формирование html кода для выходной таблицы
        oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (self.dicDecorRes['decor_kwargs']['table_codes']['prepareTableHtmlFunc'], byClassFilePAth = True)
        # Подготовить выходной HTML-код для таблицы на бызе страницы процедурного (прошедшего все процедуры) фрейма
        tableCode = oFunc(**self.dicDecorRes)
        
        
        
        # dicDecorRes['tableCode'] = tableCode
        # dicDecorRes['dfQn'] = len(dicDecorRes['df'])
        
        
        # # D. Проверяем, нужно ли добавлять итоговоые или дополнительные ряды сверху или внизу таблицы
        if isinstance(self.dicDecorRes['df'], pd.DataFrame): # Проверяем есть ли после фильтрации фрейм и если есть добавляем добавочные ряды. Если нет рядов , то будет -1
            if 'addedSpecialRows' in self.dicDecorRes['decor_kwargs']['table_codes']:
                # Получить HTML-код дополнительных вспоогательных рядов в таблицу
                oFuncAddedRows = FunctionsGeneralClass.get_func_obj_by_its_full_name (self.dicDecorRes['decor_kwargs']['table_codes']['addedSpecialRows'], byClassFilePAth = True)
                additionalRowsHtml = oFuncAddedRows(self.dicDecorRes['cuuPaginator'].df)
                # print(f'$$$$$$$$$$$$$$$$$$$$$$$    &&&&&&&&&&&&&&&&&&&&&&&&&&    @@@@@@@@@@@@@@@@@@@@@@')
                tableCode +=  additionalRowsHtml
                
        # Обертываем в тэг начала и конца таблицы с заданными классами для таблицы, если они заданы
        if 'tableStyleClasses' in self.dicDecorRes['decor_kwargs']['table_codes']:
            tableCode = f"<table class='{self.dicDecorRes['decor_kwargs']['table_codes']['tableStyleClasses']}'>{tableCode}</table>"
        else:
            tableCode = f"<table class='table'>{tableCode}</table>"
        
        # print(f'$$$$$$$$$$$   ***********   tableCode = {tableCode}')
        
        # S. Обернуть табличный код в тэги формы , если задан паарметр tkwargs['form_for_table']
        # Если заданы парметры формы в установках , то обернуть табличный код в форму
        if 'form_for_table' in self.dicDecorRes['decor_kwargs']['table_codes']:
            self.dicDecorRes['tableCode'] = f"""
                                        <form id="{self.dicDecorRes['decor_kwargs']['table_codes']['form_for_table']['id']}" name = "{self.dicDecorRes['decor_kwargs']['table_codes']['form_for_table']['name']}" action="{self.dicDecorRes['decor_kwargs']['table_codes']['form_for_table']['action']}">
                                        %TABLE_CODE%
                                        </form>
                                        """
            self.dicDecorRes['tableCode'] = self.dicDecorRes['tableCode'].replace('%TABLE_CODE%',tableCode)
            
        # Если не заданы, то просто передать код таблицы выходной в сквозной словарь декораторов
        else:
            self.dicDecorRes['tableCode'] = tableCode
        
        
        
        
        # V. обернуть tableCode , поступающий из предыдущих декораторов , сверху и снизу дивами со вставкой htnl- пагинатора
        tableCode = self.dicDecorRes['tableCode']

        tbPaginDecorator = """ 
                                <div class = "table_top">
                                    %PAGINATOR_HTML%
                                </div>
                                    %TABLE%
                                <div class = "table_bottom">
                                    %PAGINATOR_HTML%
                                </div>
                            """
        
        tbPaginDecorator = tbPaginDecorator.replace('%PAGINATOR_HTML%', self.dicDecorRes['paginatorHtml'])
        
        self.dicDecorRes['tableCode'] = tbPaginDecorator.replace('%TABLE%', tableCode)
        






    def df_table_code_dd_through (self):
        """
        DjangoViewManager
        Динамический Декоратор-функционал для фильтрации  процедурного фрейма
        RET: df
        Category: Декораторы
        """



        # Получить динамический обьект метода, отвечающего за формирование html кода для выходной таблицы
        oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (self.dicThrough['decor_kwargs']['table_codes']['prepareTableHtmlFunc'], byClassFilePAth = True)
        # Подготовить выходной HTML-код для таблицы на бызе страницы процедурного (прошедшего все процедуры) фрейма
        tableCode = oFunc(**self.dicThrough)
        
        
        
        # dicDecorRes['tableCode'] = tableCode
        # dicDecorRes['dfQn'] = len(dicDecorRes['df'])
        
        
        # # D. Проверяем, нужно ли добавлять итоговоые или дополнительные ряды сверху или внизу таблицы
        if isinstance(self.dicThrough['df'], pd.DataFrame): # Проверяем есть ли после фильтрации фрейм и если есть добавляем добавочные ряды. Если нет рядов , то будет -1
            if 'addedSpecialRows' in self.dicThrough['decor_kwargs']['table_codes']:
                # Получить HTML-код дополнительных вспоогательных рядов в таблицу
                oFuncAddedRows = FunctionsGeneralClass.get_func_obj_by_its_full_name (self.dicThrough['decor_kwargs']['table_codes']['addedSpecialRows'], byClassFilePAth = True)
                additionalRowsHtml = oFuncAddedRows(self.dicThrough['cuuPaginator'].df)
                # print(f'$$$$$$$$$$$$$$$$$$$$$$$    &&&&&&&&&&&&&&&&&&&&&&&&&&    @@@@@@@@@@@@@@@@@@@@@@')
                tableCode +=  additionalRowsHtml
                
        # Обертываем в тэг начала и конца таблицы с заданными классами для таблицы, если они заданы
        if 'tableStyleClasses' in self.dicThrough['decor_kwargs']['table_codes']:
            tableCode = f"<table class='{self.dicThrough['decor_kwargs']['table_codes']['tableStyleClasses']}'>{tableCode}</table>"
        else:
            tableCode = f"<table class='table'>{tableCode}</table>"
        
        # print(f'$$$$$$$$$$$   ***********   tableCode = {tableCode}')
        
        # S. Обернуть табличный код в тэги формы , если задан паарметр tkwargs['form_for_table']
        # Если заданы парметры формы в установках , то обернуть табличный код в форму
        if 'form_for_table' in self.dicThrough['decor_kwargs']['table_codes']:
            self.dicThrough['tableCode'] = f"""
                                        <form id="{self.dicThrough['decor_kwargs']['table_codes']['form_for_table']['id']}" name = "{self.dicThrough['decor_kwargs']['table_codes']['form_for_table']['name']}" action="{self.dicThrough['decor_kwargs']['table_codes']['form_for_table']['action']}">
                                        %TABLE_CODE%
                                        </form>
                                        """
            self.dicThrough['tableCode'] = self.dicThrough['tableCode'].replace('%TABLE_CODE%',tableCode)
            
        # Если не заданы, то просто передать код таблицы выходной в сквозной словарь декораторов
        else:
            self.dicThrough['tableCode'] = tableCode
        
        
        
        
        # V. обернуть tableCode , поступающий из предыдущих декораторов , сверху и снизу дивами со вставкой htnl- пагинатора
        tableCode = self.dicThrough['tableCode']

        tbPaginDecorator = """ 
                                <div class = "table_top">
                                    %PAGINATOR_HTML%
                                </div>
                                    %TABLE%
                                <div class = "table_bottom">
                                    %PAGINATOR_HTML%
                                </div>
                            """
        
        tbPaginDecorator = tbPaginDecorator.replace('%PAGINATOR_HTML%', self.dicThrough['paginatorHtml'])
        
        self.dicThrough['tableCode'] = tbPaginDecorator.replace('%TABLE%', tableCode)
        









### END ДИНАМИЧЕСКИЕ ДЕКОРАТОРЫ (ИЛИ ФУНКЦИОНАЛЫ)







    ### СТАТИЧНЫЕ ДЕКОРАТОРЫ И МЕТОДЫ КЛАССА ИЗ ПРЕДЫДУЩЕЙ ВЕРСИИ ПОДХОДА
    # Накладываются на фрейм в ступенчатом порядке. Можно использовать в люых вариантах с фреймом. 
    # Они продублированы из noocube.Decorators... Пока оставить
    
    
    def process_frame_static_decors(self):
        """ 
        Обработка заданного фрейма для вывода конечной таблицы на странице сайта со всем стандартным функционалом (сортировка, наименования столбцов, форматирование колонок, и т.д.)
        """

        # ОСНОВНОЙ ДЕКОРАТОР ПРОЦЕДУРНОГО ФРЕЙМА
        @self.decor_proccessor_classic_static_decors(**self.dicDecorRes['decor_kwargs'])
        def prepare_data_frame_():
            """Подготовить фрейм с данными. Прим: request необходимо передавать на выходе для оберточных функций"""
            
            # Считывание фрейма со всеми облигациями из сессии
            # self.dicDecorRes['df'] = RequestManagerJango.read_df_as_json_from_session(self.request, 'dfComplexBonds')
            return self.dicDecorRes
        
        # ЗАПУСК вспомогательной декорированной функции
        self.dicDecorRes = prepare_data_frame_()
    
    
    
    @staticmethod
    def df_assoc_titles_and_calcs_static(requestDic, **atkwargs):
        """
        DjangoViewManager
        Декоратор для переименования колонок и добавления/изменения калькулируемых колонок
        RET: df
        Category: Декораторы
        """
        
        def view(func_to_decorate):
            """
            Обертка для функции из модуля Views в системе Jango
            """
            
            def wrapper(*args, **kwargs):
                # Считывание return первичной функции (которая должна возвращать df - DataFrame и request - возвратные параметры со страницы сайта в формате Jango)
                dicDecorRes = func_to_decorate(*args, **kwargs)
                
                if isinstance(dicDecorRes['df'], int):
                    dicDecorRes['df'] = -1
                else:
                    # D. Проработка названий колонок и расчетных добавочных колонок
                    # Разделение словаря на словарь обычных origColsAssocTitles_ названий и на словарь с расчетными полями calcColsAssocTitles_
                    origColsAssocTitles_, calcColsAssocTitles_ = DSourceOutputCube.diffirenciate_orig_and_calc_columns_static_(atkwargs['dicTabTitles'])
                    # E. Проработать массив данных на предмет названий колонок на базе assocTitles и вырезания из оригинального фрейма тех колонок, Которые заданы в assocTitles
                    dicDecorRes['df'] = DSourceOutputCube.prepare_to_output_static(dicDecorRes['df'], origColsAssocTitles_)
                    fkwargs = {}
                    dicDecorRes['df'] = DSourceOutputCube.add_update_calculated_cols_static_v2_(dicDecorRes['df'], calcColsAssocTitles_, **fkwargs)

                # print(f"~~~~~~~~~~~~  ДЕКОР: df_assoc_titles_and_calcs  ^^^^^^^^^^^^^^^^  dicRes = {dicRes}  ")    
                    
                return dicDecorRes

            return wrapper

        return view
    




    @staticmethod
    def df_columns_formatting_with_row_as_argument_static(requestDic, **dkwargs):
        """

        Декоратор для  окончательного оформления форматов колонок для вывода (цвета,  bold и т.д.)
        Отличается от подобного декоратора : df_columns_formatting() тем, что динамическая функия, Которая обрабатывает колонки, принимает в качестве аргумента не значение ячейки
        текущего ряда фрейма, а весь ряд. Что дает возможность использовать значения разных ячеек в ряду для вычисления необходимого результата и дальнейшего форматирования
        колонок (или добавления колонок)
        В принципе может делать все , что делает алгоритм создания калькулируемых колонок. И даже, возможно, лучше перейти полностью на оформление колонок таким образом,
        отказавшись от механизма калькулируемых колонок
        RET: df
        Category: Декораторы
        """
        
        dkwargs['requestDic'] = requestDic
        
        def view(func_to_decorate):
            """
            Обертка для функции из модуля Views в системе Jango
            """
            
            def wrapper(*args, **kwargs):
                # Считывание return первичной функции (которая должна возвращать df - DataFrame и requestDic - возвратные параметры со страницы сайта в формате Jango)
                dicDecorRes = func_to_decorate(*args, **kwargs)
                
                if isinstance(dicDecorRes['df'], int) :
                    pass
                else:

                    dicDecorRes['df'] = FunctionsGeneralClass.proccessing_df_by_dynamic_funcs_with_row_as_argument (dicDecorRes['df'], **dkwargs)
                        
                # print(f"~~~~~~~~~~~~  ДЕКОР: df_columns_decoration  ^^^^^^^^^^^^^^^^  dicRes = {dicOut}  ") 
                    
                return dicDecorRes

            return wrapper

        return view




    @staticmethod
    def df_sort_v2_static(requestDic, **skwargs):
        """
        Декоратор для сортировки фрейма
        v2 - версия 2 : Добавлены возможность задавать сортировку по умолчанию - 'default_sort_col'  и 'default_sort_dir'
        Предыдущая версия: df_sort()
        Category: Декораторы
        """
        
        def view(func_to_decorate):
            """
            Обертка для функции из модуля Views в системе Jango
            """
            
            def wrapper(*args, **kwargs):

                # Считывание return первичной функции (которая должна возвращать df - DataFrame и requestDic - возвратные параметры со страницы сайта в формате Jango)
                dicDecorRes = func_to_decorate(*args, **kwargs)
                
                # Если нет рядов в df
                if len(dicDecorRes['df']) < 1:
                    dicDecorRes['df'] = -1
                else:
                    
                    # Словарь для перевода стрингового True/False в булиновые значения
                    toBool = {'True':True,'False':False}

                    # Текущее состояние по сортировке из requestDic
                    requestSortCurrState = {}
                    # Если не задана колонка сортировки, то присваивается первая колонка из списка колонок, подлежащих сортировке в TABLE_SORT_COLS_FUNCS_
                    if 'sort_col' in requestDic:
                        requestSortCurrState['sort_col'] = requestDic['sort_col'] # Текущая колонка сортировки
                    else:
                        # Сортировка по умолчанию {SORT_COLUMN_BY_DEFAULT}
                        if 'default_sort_col' in skwargs: # Если задана колонка для сортировки по умолчанию
                            requestSortCurrState['sort_col'] =  skwargs['default_sort_col'] #dicDecorRes['df'].columns.tolist()[5] # 'Название' # df.columns.tolist()[0]
                        else: # Если не задана дефолтная колонка для сортирвки, то сортировка идет по первой колонке с индексом 0
                            requestSortCurrState['sort_col'] = dicDecorRes['df'].columns.tolist()[0]
                        
                    # Если не задана страница
                    if 'pg' not in requestDic:
                        requestDic['pg'] = '1' 

                    # Если не задано направление сортировки, то присваивается направление = True (то есть ASC)
                    if 'sort_asc' in requestDic:
                        requestSortCurrState['sort_asc'] = toBool[requestDic['sort_asc']]   # Текщее направление сортировки
                    else:
                        if 'default_sort_dir' in skwargs: # Если задано направление сортировки по умолчанию, то используем ее
                            # Направление сортировки по умолчанию {SORT_DIRECTION_BY_DEFAULT}
                            requestSortCurrState['sort_asc'] = skwargs['default_sort_dir']
                        else: # Если не задано направление сортировки по умолчанию, то равно True (то есть asc, по возрастающей)
                            requestSortCurrState['sort_asc'] = True

                    if 'sort_col' in requestSortCurrState and 'sort_asc' in requestSortCurrState:
                        dicDecorRes['df'] = dicDecorRes['df'].sort_values(by=[requestSortCurrState['sort_col']], ascending = requestSortCurrState['sort_asc'])
                        
                # print(f"~~~~~~~~~~~~  ДЕКОР: df_sort  ^^^^^^^^^^^^^^^^  dicOut = {dicOut}  ")
                
                return dicDecorRes

            return wrapper

        return view





    @staticmethod
    def filter_by_query_v2_static(requestDic, **fkwargs):
        """
        Декоратор для создания обьекта класса DsTableOutputCube на основе входящего фрейма
        RET: Обьект класса DsTableOutputCube
        
        Инициализация фильтров
            Словарь задает обойму фильтров, которые будут применены поочереди к фрейму . Формулы фильров задаются ключем словаря и свзяаны со словарем общих фильтрационных формул 
            в словаре типа FILTERS_EXPR_TEMPLATES_FOR_FUNCS_BY_CATEG_, задаваемых в settings.py
            Если в filtsIni ключ = -1 ... -N, то это означает, что фильтр работает по прямому выражению query, который содержится в значении filtsIni (при ключе равном -1 ... -N).
            Прямые выражения query так же могут быть обоймой, тогда в них ключ унифицируется любым целым числом (пока используем негативные числа, хотя можно любые)
            Если в словаре инициализации фильтров в значениях стоит 'SIMPLE FILTER QUERY', то это означает, что нет никаких переменных и фильтр является константой
            Тогда просто считываем его из словаря query-выражений фильтров по заданному ключу в словаре инициализации фильтров
            Если же есть какое-то другое значение, кроме как 'SIMPLE FILTER QUERY', то это означает, что это значение должно заместить переменную с именем ключа
            в выражении фильтра из словаря фильтров dsocObj.viewFilterFormulas на то, значение, которое находится по ключу в словаре инициализации фильтров
            
            kysIntersect в коде метода - Пересечение по ключам между request url-аргументов и ключами в словаре формул для фильтрации () 
            (В фильтрации участвуют только те фильтры из settings.py, 
            которые запускают url-аргументы в url-request своими названиями. если название ключа словаря набора фильтров совпадают с возможным  url-аргументом 
            request, то фильтр активизируется)
            
        Задание фильтра через словарь формул с ключем 'categ_name' через обойму-словарь инициализации filtsIni
        filtsIni = {'categ_name' : categName}
        
        Задание обоймы прямых фильтров через обойму-словарь инициализации filtsIni
        filtsIni = {-1 : 'Категория == "Конвертация типов"'}
        
        ПРИМЕР:
        categName = requestDic['categ']
        Инициализация фильтров
        filtsIni = {'categ_name' : categName}
        
        @DecoratorsJangoCube.dtoc(requestDic, **DTOC_OUT_KWARGS_FUNCS_BY_CATEG_) # Возвращает обьект класса DsTableOutputCube
        @DecoratorsJangoCube.filter_by_query(requestDic, filtsIni = filtsIni, viewFilterFormulas = FILTERS_EXPR_TEMPLATES_FOR_FUNCS_BY_CATEG_)
        @DecoratorsJangoCube.dsoc(requestDic, **DSOC_INP_KWARGS_FUNCS_BY_CATEG_) # Возвращает обьект класса DsTableOutputCube 
        def prepare_data_frame_():
            dfFuncs = pd.DataFrame(json.loads(requestDic.session['df_funcs']))
            return dfFuncs
        Category: Декораторы
        """
        def view(func_to_decorate):
            """
            Обертка для функции из модуля Views в системе Jango
            """
            def wrapper(*args, **kwargs):
                
                dicDecorRes = func_to_decorate(*args, **kwargs)
                
                # print (f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ filter_by_query_v2   &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                
                # Если обьект имеет тип число, то это значит -1 или уведомление об отсутствии фрейма (или еще каких-то непоняток)
                if isinstance(dicDecorRes['df'], int):
                    dicDecorRes['df'] = -1

                # Иначе работаем с обычным фреймом
                else:
                    
                    # Пересечение по ключам между request url-аргументов и ключами в словаре формул для фильтрации () (В фильтрации участвуют только те фильтры из settings.py, 
                    # которые запускают url-аргументы в url-request своими названиями. если название ключа словаря набора фильтров совпадают с возможным  url-аргументом 
                    # request, то фильтр активизируется)
                    kysIntersect = get_intersection_of_two_list(list(requestDic.keys()), list(fkwargs.keys()))
                    
                    # print (f"%%%%%%%%%%%%%%%%   &&&&&&&&&&&  kysIntersect = {kysIntersect}")
                    
                    # Цикл по списку задаваемой обоймы фильтров в filtsIni
                    for key in kysIntersect:
                        
                        # Если url-аргумент в request не пустой (так как могут быть пустые аргументы, Которые просто игнорируются)
                        if len(requestDic[key]) > 0:
                        
                            fExprByKey = fkwargs[key]
                            
                            # Если в формуле присутствует локальная переменная, начинающаяся с @<url-arg == key in filter formula>,  то замещаем эту локальную переменную
                            # с именем равным ключу ф словаре фильтров, а так же равной url-аргументу в request ( так как именно этот фактор связывает нахождение формулы в словаре фильтров: )
                            if '@' in fExprByKey:
                                fExprByKey = fExprByKey.replace('@' + key, requestDic[key])
                                
                                
                                
                            # ЗАЩИТА от применения комплексного или простого фильтра к тем полям, которых нет в процедурном фрейме !!!
                            
                            # Проверить, Есть ли поле в формуле фильтра в фрейме (это позволит универсализировать константу по фильтрам в settings.py)
                            # Если нет, то не фильтровать по этому полю, иначе ошибка в jquery ajax
                            # Сложная проверка и парсер для формулы, Если выражение комплексное, то есть из логических обьединений через & или |
                            filterFlag = False # Флаг: Фильтрация разрешается или нет
                            
                            # A. Парсинг регулярными выражениями формулы фильтра
                            rExpr = r"([&|])"
                            mo  = ReManager.find_all_matches_from_text(fExprByKey, rExpr)
                            
                            # print (f'%%%%%%%%%%%%%  RESEARCH  &&&&&&&& mo = {mo}')
                            
                            dfColumns = list(dicDecorRes['df']) 
                            
                            if len(mo) > 1: # Если частей больше 1, то это значит комплексное выражение и особый парсинг
                                # filterFlag = False
                                # print(f'%%%%%%%%%%%%%  COMPLEX &&&&&&&&  fExprByKey = {fExprByKey}')
                                
                                # Найти все поля во всех соединенных частях комплексной формулы фидьтрации
                                rExp = rc.STRINGS_WITH_DOT_AT_END
                                mo  = ReManager.find_all_matches_from_text(fExprByKey, rExp)
                                
                                # B. Найти обращение к полям в формуле и выделить эти поля в список
                                # Выделить только первое слово, заканчивающееся на точку. И это будет - поле
                                mo = [x.split('.')[0] for x in mo]
                                
                                # print(f'%%%%%%%%%%%%%  COMPLEX &&&&&&&&  fExprByKey = {fExprByKey}')
                                # print(f'%%%%%%%%%%%%%  COMPLEX RESULT &&&&&&&&  mo = {mo}')
                                # print(f'%%%%%%%%%%%%%  COMPLEX REXP &&&&&&&&  rExp = {rExp}')
                                
                                
                                # C. Найти пересечение списка названий колонок фрейма и списка колонок из фильтра fExprByKey
                                lIntersect = get_intersection_of_two_list(dfColumns, mo)
                                # print(f'%%%%%%%%%%%%%  COMPLEX INTERSECT &&&&&&&&  lIntersect = {lIntersect}')
                                
                                # D. Сформировать формулу из тех частей комплексной формулы фильтрации, в которых есть только разрешенные поля из пересечения lIntersect
                                rExp = r"[&|]"
                                logicOperands  = ReManager.find_all_matches_from_text(fExprByKey, rExp) # последовательный список операндов
                                # print(f'%%%%%%%%%%%%%  COMPLEX RES &&&&&&&&  logicOperands = {logicOperands}')
                                
                                filterParts = re.split(rExp, fExprByKey) # Суб-части формулы комплексного фильтра
                                # print(f'%%%%%%%%%%%%%  COMPLEX PARTS &&&&&&&&  filterParts = {filterParts}')
                                
                                # E. Сформировать словарь суб-частей фильтра, где ключ - формула, значение - операнд слева. Первая суб-часть формулы будет иметь значение - ''
                                dicFilterSubParts = {}
                                for inx, x in enumerate(filterParts): # Цикл по 
                                    # Очистить x от прбелов по концам
                                    x = x.strip()
                                    if inx == 0:
                                        dicFilterSubParts[x] = ''
                                    else:
                                        dicFilterSubParts[x] = logicOperands[inx-1]
                                
                                
                                # print(f'%%%%%%%%%%%%%  COMPLEX DICT &&&&&&&&  dicFilterSubParts = {dicFilterSubParts}')
                                
                                # F. Исключить из словаря dicFilterSubParts те записи, где поля суб-частей (которые в ключах) не входят в резрешенные поля lIntersect
                                
                                # dicFilterSubParts = {key:value for (key,value) in dicFilterSubParts.items() if }
                                dicsubPartExcluded = [] # Список исключаемых из фильтрации суб-частей фильтра и поля этих суб-частей
                                finalComplexFilter = ''# Конечный фильтр, в котором исключены суб-части, где используются поля, Которых нет в фрейме
                                for subPart, operand in  dicFilterSubParts.items():
                                    subField = subPart.split('.')[0] # Название поля, участвующего в суб-части составного фильтра
                                    # print(f'%%%%%%%%%%%%%  COMPLEX SUB-FIELD &&&&&&&&  subField = {subField}')
                                    if subField in lIntersect: # если поле в суб-части фильтра иммется в разрешительном списке lIntersect, то суб-часть допускается для фильтрации
                                        # print(f'%%%%%%%%%%%%%  COMPLEX SUB-FIELD ALLOWED &&&&&&&&  subField = {subField}')
                                        finalComplexFilter += operand + subPart
                                        
                                        # Включение флага разрешения фильтрации 
                                        filterFlag = True
                                    
                                    else: # Инче суб-часть фильтра не допускается для фильтрации. Добавить исключенную суб-часть и поле в список исключенных суб-частей фильтра
                                        dicsubPartExcluded.append(subPart)
                                        # Програмный принтинг
                                        print(f'PROJ LOG ----> PR_389 --> : В составном фильтре выявлена и исключена суб-часть с отсутствующим в фрейме полем: \'{subPart}\' | Декоратор: @filter_by_query_v2()')
                                
                                
                                # print(f'%%%%%%%%%%%%%  COMPLEX FINAL &&&&&&&&  finalComplexFilter = {finalComplexFilter}')
                                # print(f'%%%%%%%%%%%%%  COMPLEX EXCLUDED &&&&&&&&  dicsubPartExcluded = {dicsubPartExcluded}')
                                
                                
                            else: # Если частей = 1, то это значит Простая формула, не составная. Но все равно проверяем наличие поля
                                
                                field = fExprByKey.split('.')[0] # Парсинг поля из формулы фильтра
                            
                                # print(f'%%%%%%%%%%%%%  SIMPLE &&&&&&&&  field = {field} and dfColumns = {dfColumns} and fExprByKey = {fExprByKey}')
                                # Включение флага разрешения фильтрации
                                if field in dfColumns: # Если поле находится в списке полей фрейма
                                    filterFlag = True
                                    finalComplexFilter = fExprByKey
                                else: # В ином случае фильтр не допускается к фильтрации
                                    print(f'PROJ LOG ----> PR_390 --> : Фильтр по полю, которого нет в фрейме. Дезактивирован: \'{subPart}\' | Декоратор: @filter_by_query_v2()')

                            # END ЗАЩИТА от применения комплексного  или простого фильтра к тем полям, которых нет в процедурном фрейме !!!


                            # Если разрешена фильтрация
                            if filterFlag:
                                dicDecorRes['df'] =  dicDecorRes['df'].query(f"{finalComplexFilter}", engine='python')
                                
                                # Програмный принтинг
                                print(f'PROJ LOG ----> PR_391 --> : Проведена фильтрация фрейма по формуле: \'{finalComplexFilter}\' | Декоратор: @filter_by_query_v2()')
                            
                            # print (f"$$$$$$$$$$$$$$$$  SFTER FILT  ^^^^^^^^^ dicDecorRes['df']_N = {len(dicDecorRes['df'])}")
                            
                # print(f"~~~~~~~~~~~~  ДЕКОР: filter_by_query_v2  ^^^^^^^^^^^^^^^^  dicOut = {dicOut}  ")
                
                return dicDecorRes
            
            return wrapper
        
        return view





    @staticmethod
    def df_paginator_with_sorting_and_html_pagin_v2_static(requestDic, **pkwargs):
        """
        Декоратор для формирования кодов пагинатора на основе фрейма и с учетом текущей сортировки. 
        v2 - Версия 2 - базовая url и субдомен с названием View теперь формируется из сквозного декор-словаря 
        Предыдущая версия: df_paginator_with_sorting_and_html_pagin ()
        ( View   задается теперь в этот словарь в самой текущей View через dicDecorRes['appView'] в начале, перед декораторами)
        Плюс формирует HTML-код для нумератора страниц пагинатора
        class="pagination" : Задается в главном базовом html-фале темплейта
        Category: Декораторы
        """
        
        def view(func_to_decorate):
            """
            Обертка для функции из модуля Views в системе Jango
            """
            
            def wrapper(*args, **kwargs):
                # Считывание входящего фрейма из источника первичного фрейма или из предыдущего декоратора
                dicDecorRes = func_to_decorate(*args, **kwargs)
                # Если не существует df (в ином случае тип df = pd.DataFrame)
                if isinstance(dicDecorRes['df'], int):
                    dicDecorRes['df'] = -1
                    dicDecorRes['paginatorHtml'] = ''

                else:
                    # Кол-во записей после филльтрации или у исходного массива (после пагинации не менять это кол-во, так как пагинатор устанавливает dicDecorRes['df'] равной страничной выборке)
                    dicDecorRes['dfQn'] = len(dicDecorRes['df'])
                    # Если  есть ряды в фрейме
                    if len(dicDecorRes['df']) > 0:
                        
                        # Если не задана активная страница в requestDic, но есть фрейм с рядами
                        if not 'pg' in requestDic:
                            pg = '1'
                        # Если есть активная страница в reuest возврате со страницы сайта
                        else : 
                            pg = requestDic['pg']
                            
                        paginator = PaginatorWithDataFrame(dicDecorRes['df'], pkwargs['paginGenSet'] ) # инициализация обьекта пагинатора в общей форме
                        paginator = PaginatorWithDataFrame.get_curr_paginator_from_gen(paginator,  pg) 
                        
                        dicDecorRes['cuuPaginator'] = paginator # Текущий пагинатор
                        
                        
                        # Выходной постраничный активный массив обработанных данных, соотвтетсвующий активной страницы пагинатора self.pgCell
                        dfPage = paginator.dfLimByPgNumb
                        
                        # Подготовить HTML-код нумератора для активнйо страницы
                        
                        # Базовая ссылка с суб-доменами названия приложения и названия метода View для ссылок страниц нумератора
                        url = f"/{dicDecorRes['appName']}/{dicDecorRes['appView']}"

                        # Константная суб-строка с аргументами в ссылке сортировки по заголовкам  с вычетом аргументов в спсиках исключениях genExcludeListFoSort и self.excludeUrlArgsForSort
                        constUrlArgsPaginLine = HTMLSiteManagerJango.prpare_const_line_from_url_args_matrix_with_exclusions(requestDic, pkwargs['genExcludeListFoPagin'])
                        pState = paginator.curr_paginator_state_dict
                        paginatorHtml = f"""
                        <div class="pagination">
                        <a href="{url}?pg=1{constUrlArgsPaginLine}">В начало</a>
                            <a href="{url}?pg={pState['prevBlockPageToActivate']}{constUrlArgsPaginLine}">&laquo;</a>"""
                            
                        for pg in pState['pagesList']:
                            if pg == pState['pgToActivate']:
                                paginatorHtml += f'<a class="active">{pg}</a>'
                            else:
                                paginatorHtml += f'<a href="{url}?pg={pg}{constUrlArgsPaginLine}">{pg}</a>'
                                
                        paginatorHtml += f"""        
                            <a href="{url}?pg={pState['nextBlockPageToActivate']}{constUrlArgsPaginLine}">&raquo;</a>
                        </div>
                        """
                        # END Подготовить HTML-код нумератора для активнйо страницы
                        
                        dicDecorRes['df'] = dfPage
                        dicDecorRes['paginatorHtml'] = paginatorHtml
                            
                    # Если нет рядовв фрейме (то есть фрейм - пустой)        
                    else:
                        dicDecorRes['df'] = -1
                        dicDecorRes['paginatorHtml'] = ''
                        
                return dicDecorRes

            return wrapper

        return view





    @staticmethod
    def decor_df_to_html_table_v3_static(requestDic, **tkwargs):
        """
        Декоратор для формирования кода выходной таблицы HTML  на основе фрейма и с учетом сортировки и возможного оборачивания таблицы в форму, если необходимо
        Версия 3.  динмическая функция подготовки кода таблицы возвращает код без обертки тэгом <table></table>,
        что бы можно было довставлять какие-то дополнительные ряды, типа итогов и пр. То есть декоратор позволяет довставлять ряды в таблицу и только потом оборачивает в <table></table>
        Версия 2. В ней tableCode обертывается сверху и снизу дивами с вставкой html-пагинатора/ Все берется из сквозного словаря декораторов dicDecorRes
        Предыдущая версия: df_table_html_input_paginator_html_sorting()
        И , если перед ним испоьзуется декоратор пагинации, который возвращает фрейм страницы из общего входного фрейма и html-код умератора пагинатора
        RET: tableCode, paginatorHtml
        Category: Декораторы
        """
        
        def view(func_to_decorate):
            """
            Обертка для функции из модуля Views в системе Jango
            """
            
            def wrapper(*args, **kwargs):
                # Считывание return первичной функции (которая должна возвращать df - DataFrame и requestDic - возвратные параметры со страницы сайта в формате Jango)
                dicDecorRes = func_to_decorate(*args, **kwargs)

                # Если нет рядов в фрейме
                if isinstance(dicDecorRes['df'], int):
                    
                    dicDecorRes['tableCode'] = ''
                    dicDecorRes['paginatorHtml'] = ''
                    dicDecorRes['dfQn'] = 0
                    
                # Если есть ряды в фрейме
                else:
                    # Добавляем в параметры - requestDic
                    tkwargs['requestDic'] = requestDic
                    
                    # Добавляем сквозной декор-словарь в kwargs-парамметры для динамической функции. В нем уже хранятся настройки по названию приложения и текущей View
                    tkwargs['dicDecorRes'] = dicDecorRes
                    
                    # Получить динамический обьект метода, отвечающего за формирование html кода для выходной таблицы
                    oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['prepareTableHtmlFunc'], byClassFilePAth = True)
                    # Подготовить выходной HTML-код для таблицы на бызе страницы процедурного (прошедшего все процедуры) фрейма
                    tableCode = oFunc(dicDecorRes['df'], **tkwargs)
                    
                    
                    
                    # dicDecorRes['tableCode'] = tableCode
                    # dicDecorRes['dfQn'] = len(dicDecorRes['df'])
                    
                    
                    # # D. Проверяем, нужно ли добавлять итоговоые или дополнительные ряды сверху или внизу таблицы
                    if 'addedSpecialRows' in tkwargs:
                        # Получить HTML-код дополнительных вспоогательных рядов в таблицу
                        oFuncaddedRows = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['addedSpecialRows'], byClassFilePAth = True)
                        additionalRowsHtml = oFuncaddedRows(dicDecorRes['cuuPaginator'].df)
                        # print(f'$$$$$$$$$$$$$$$$$$$$$$$    &&&&&&&&&&&&&&&&&&&&&&&&&&    @@@@@@@@@@@@@@@@@@@@@@')
                        tableCode +=  additionalRowsHtml
                        
                    # Обертываем в тэг начала и конца таблицы с заданными классами для таблицы, если они заданы
                    if 'tableStyleClasses' in tkwargs:
                        tableCode = f"<table class='{tkwargs['tableStyleClasses']}'>{tableCode}</table>"
                    else:
                        tableCode = f"<table class='table'>{tableCode}</table>"
                    
                    # print(f'$$$$$$$$$$$   ***********   tableCode = {tableCode}')
                    
                    # S. Обернуть табличный код в тэги формы , если задан паарметр tkwargs['form_for_table']
                    # Если заданы парметры формы в установках , то обернуть табличный код в форму
                    if 'form_for_table' in tkwargs:
                        dicDecorRes['tableCode'] = f"""
                                                    <form id="{tkwargs['form_for_table']['id']}" name = "{tkwargs['form_for_table']['name']}" action="{tkwargs['form_for_table']['action']}">
                                                    %TABLE_CODE%
                                                    </form>
                                                    """
                        dicDecorRes['tableCode'] = dicDecorRes['tableCode'].replace('%TABLE_CODE%',tableCode)
                        
                    # Если не заданы, то просто передать код таблицы выходной в сквозной словарь декораторов
                    else:
                        dicDecorRes['tableCode'] = tableCode
                    
                    
                    
                    
                    # V. обернуть tableCode , поступающий из предыдущих декораторов , сверху и снизу дивами со вставкой htnl- пагинатора
                    tableCode = dicDecorRes['tableCode']

                    tbPaginDecorator = """ 
                                            <div class = "table_top">
                                                %PAGINATOR_HTML%
                                            </div>
                                                %TABLE%
                                            <div class = "table_bottom">
                                                %PAGINATOR_HTML%
                                            </div>
                                        """
                    
                    tbPaginDecorator = tbPaginDecorator.replace('%PAGINATOR_HTML%', dicDecorRes['paginatorHtml'])
                    
                    dicDecorRes['tableCode'] = tbPaginDecorator.replace('%TABLE%', tableCode)
                    
                    
                # print(f"~~~~~~~~~~~~  ДЕКОР: df_table_html_input_paginator_html_sorting  ^^^^^^^^^^^^^^^^  dicInp = {dicInp}  ")
                
                return dicDecorRes

            return wrapper

        return view




    def decor_proccessor_classic_static_decors(self, **dkwargs):
        """
        Комплексный декоратор, классический, то есть применяется последовательность атомарных декораторов для стандартного и наиболее часто употребляемого варианта вывода таблицы
        с данными на сайте, ее оформление и пагинация, сортировка, оформление данных в колонках, фильтрация - как через перезагрузку страницы, так и через AJAX
        Category: Декораторы
        """
        
        def view(func_to_decorate):
            """
            Обертка для макетода из View модуля
            """
            
            @DjangoViewManager.decor_df_to_html_table_v3_static(self.requestDic, **dkwargs['table_codes']) # Декоратор подготовки HTML-кода выходной таблицы с возможной сортировкой колонок
            @DjangoViewManager.df_paginator_with_sorting_and_html_pagin_v2_static(self.requestDic, **dkwargs['pagination']) # Декоратор для пагинации фрейма с учетом текщей сортировки
            @DjangoViewManager.filter_by_query_v2_static(self.requestDic, **dkwargs['filtering'])
            @DjangoViewManager.df_sort_v2_static(self.requestDic) # декоратор сортировки фрейма
            @DjangoViewManager.df_columns_formatting_with_row_as_argument_static(self.requestDic, column_decorator = dkwargs['formatting']) # Декоратор форматирования колонок фрейма
            
            
            @DjangoViewManager.df_assoc_titles_and_calcs_static(self.requestDic, dicTabTitles = dkwargs['assoc_titles']) # Декоратор переименования заголовков колонок фрейма
            def wrapper(*args, **kwargs):

                dicDecorRes = func_to_decorate(*args, **kwargs)
                
                return dicDecorRes
            return wrapper
        return view



    @staticmethod
    def view_inicilization_static (request, viewSettings):
        """ 
        Инициализировать необходимые обще-дефолтные данные для View, а именно:
        bmms - модуль необходимых методов работы с облигациями
        requestDic - словарь аргументов url-строки из request
        dicDecorRes - сквозной словарь для декораторов, в котором инициализируются названия приложения dicDecorRes['appName']  и название метода view dicDecorRes['appView']
        dicDecorRes['decor_kwargs']  - общие настройки для всех Views, которые связаны с построением табличного кода для вывода на сайт
        Category: Request JANGO
        """
        
        bmms = BondsMainManagerSpeedup(ms.DB_CONNECTION) # Подключение к конекшену

        # Словарь URL-параметров
        requestDic = RequestManagerJango.read_urls_args_dic_from_request_django(request)
        
        dicDecorRes = {} # Сквозной входной-выходной словарь декораторов, куда можно записывать любые данные и который проходит сквозь все декораторы как репозиторий параметров
        
        # Присвоить в сквозной словарь словарь текущих атрибутов URL строки
        dicDecorRes['requestDic'] = requestDic
        
        # Считывание и внесение в dicDecorRes названий приложения и текущего View . Обязательно использовать при использовании декораторов вначале каждого view с декораторами!!!
        dicDecorRes = RequestManagerJango.read_curr_application_and_view_names_to_dic_decor (request, dicDecorRes)
        
        
        
        
        # Дефолтные установки по именным параметрам декораторов, если они не заданы в settings.py
        
        if 'fromaters' in viewSettings : # Форматеры
            fromaters = viewSettings['fromaters']
        else:
            fromaters = {}
            

        
        if 'table_codes' in viewSettings : # Форматеры
            tableCodes = viewSettings['table_codes']
        else:
            tableCodes = {}
        
        
        if 'assoc_titles' in viewSettings : # Форматеры
            assocTitles = viewSettings['assoc_titles']
        else:
            assocTitles = {}
            

            
        # Настройки именных параметров для основного декоратора процедурного фрейма с учетом дефолтных настроек
        dicDecorRes['decor_kwargs'] = {
            
            'table_codes' :tableCodes,
            'pagination' : ms.PAGINATOR_SET_FUNCS_,
            'filtering' : ms.FILTERS_EXPR_TEMPLATES_FOR_FUNCS_BY_TYPE_V2_, # Общая для всех Views ( все фильтры хранятся в одной и той же константе)
            'sorting' : ms.SORT_SETTINGS,
            'formatting': fromaters,
            'assoc_titles': assocTitles,
            
        }
        

        return bmms, requestDic, dicDecorRes
    
    
    
    
    def view_context_inicialization_static (dim):
        """ 
        Инициализация дефолтных парметров контекста View
        """
        
        requestDic = dim.requestDic
        dicDecorRes = dim.dicDecorRes
        bmms = dim.bmms
        
        # Проверка и настройка контекстных параметров (TODO: Скрыть настройки в другом методе. Придумать)
        if 'srch_str' in requestDic:
            srch_str =  requestDic['srch_str']
        else:
            srch_str = ''
            
            
        # Раскрытие раздела левой панели навигации в зависимости от названия текущего View
        
        leftNavActive = ms.LEFT_NAVIGATOR_ACTIVE_[dicDecorRes['appView']] # dicDecor['appView'] - Название текущего View задает маркер раскрытия левого навигатора
        
            
        # Стандартные параметры для контекста вывода таблиц по фрейму на сайт
        baseContext = {
            'tbCode' : dicDecorRes['tableCode'],
            'left_nav_view' : leftNavActive, # Открывающийся раздел в левом навигаторе
            'df_qn' : dicDecorRes['dfQn'],
            'dfPackages' : bmms.get_index_packages_df_BMMS(), # фрейм с индексными пакетами 
            'srch_str' : srch_str,
        }
        
        return baseContext




    
    
    ### END СТАТИЧНЫЕ ДЕКОРАТОРЫ И МЕТОДЫ КЛАССА
    

### END ДЕКОРАТОРЫ 



if __name__ == '__main__':
    pass













































