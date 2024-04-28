""" Декораторы для системы CUBE в JANGO"""
from django.http import HttpResponse
from noocube.request_manager_jango import RequestManagerJango
from noocube.dsource_output_cube_v2 import DSourceOutputCube
from noocube.ds_table_output_cube_v2 import  DsTableOutputCube
from django.shortcuts import render
import pandas as pd
from noocube.funcs_general_class import FunctionsGeneralClass
from noocube.paginator_data_frame_cube_v2 import PaginatorWithDataFrame
from noocube.html_manager_django import HTMLSiteManagerJango
from noocube.settings import *  # Импорт из самого верхнего уровня проекта, где находится файл manage.py
from noocube.funcs_general import get_intersection_of_two_list
from noocube.bonds_main_manager import BondsMainManager
from noocube.pandas_manager import PandasManager

from noocube.re_manager import ReManager
import noocube.re_constants as rc
import re

from noocube.funcs_general import  get_intersection_of_two_list

class DecoratorsJangoCube():
    """Хранилище для декораторов"""
    

    def filter_by_query_v2(requestDic, **fkwargs):
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
                                        print(f'PROJ LOG ----> : В составном фильтре выявлена и исключена суб-часть с отсутствующим в фрейме полем: \'{subPart}\' | Декоратор: @filter_by_query_v2()')
                                
                                
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
                                    print(f'PROJ LOG ----> : Фильтр по полю, которого нет в фрейме. Дезактивирован: \'{subPart}\' | Декоратор: @filter_by_query_v2()')

                            # END ЗАЩИТА от применения комплексного  или простого фильтра к тем полям, которых нет в процедурном фрейме !!!


                            # Если разрешена фильтрация
                            if filterFlag:
                                dicDecorRes['df'] =  dicDecorRes['df'].query(f"{finalComplexFilter}", engine='python')
                                
                                # Програмный принтинг
                                print(f'PROJ LOG ----> : Проведена фильтрация фрейма по формуле: \'{finalComplexFilter}\' | Декоратор: @filter_by_query_v2()')
                            
                            # print (f"$$$$$$$$$$$$$$$$  SFTER FILT  ^^^^^^^^^ dicDecorRes['df']_N = {len(dicDecorRes['df'])}")
                            
                # print(f"~~~~~~~~~~~~  ДЕКОР: filter_by_query_v2  ^^^^^^^^^^^^^^^^  dicOut = {dicOut}  ")
                
                return dicDecorRes
            
            return wrapper
        
        return view





    def filter_by_query_v3(**fkwargs):
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
                                        print(f'PROJ LOG ----> : В составном фильтре выявлена и исключена суб-часть с отсутствующим в фрейме полем: \'{subPart}\' | Декоратор: @filter_by_query_v2()')
                                
                                
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
                                    print(f'PROJ LOG ----> : Фильтр по полю, которого нет в фрейме. Дезактивирован: \'{subPart}\' | Декоратор: @filter_by_query_v2()')

                            # END ЗАЩИТА от применения комплексного  или простого фильтра к тем полям, которых нет в процедурном фрейме !!!


                            # Если разрешена фильтрация
                            if filterFlag:
                                dicDecorRes['df'] =  dicDecorRes['df'].query(f"{finalComplexFilter}", engine='python')
                                
                                # Програмный принтинг
                                print(f'PROJ LOG ----> : Проведена фильтрация фрейма по формуле: \'{finalComplexFilter}\' | Декоратор: @filter_by_query_v2()')
                            
                            # print (f"$$$$$$$$$$$$$$$$  SFTER FILT  ^^^^^^^^^ dicDecorRes['df']_N = {len(dicDecorRes['df'])}")
                            
                # print(f"~~~~~~~~~~~~  ДЕКОР: filter_by_query_v2  ^^^^^^^^^^^^^^^^  dicOut = {dicOut}  ")
                
                return dicDecorRes
            
            return wrapper
        
        return view








    def df_sort(requestDic, **skwargs):
        """
        Декоратор для сортировки фрейма
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
                        requestSortCurrState['sort_col'] =  dicDecorRes['df'] .columns.tolist()[0] # 'Название' # df.columns.tolist()[0]
                        
                    # Если не задана страница
                    if 'pg' not in requestDic:
                        requestDic['pg'] = '1' 

                    # Если не задано направление сортировки, то присваивается направление = True (то есть ASC)
                    if 'sort_asc' in requestDic:
                        requestSortCurrState['sort_asc'] = toBool[requestDic['sort_asc']]   # Текщее направление сортировки
                    else:
                        # Направление сортировки по умолчанию {SORT_DIRECTION_BY_DEFAULT}
                        requestSortCurrState['sort_asc'] = False

                    if 'sort_col' in requestSortCurrState and 'sort_asc' in requestSortCurrState:
                        dicDecorRes['df'] = dicDecorRes['df'].sort_values(by=[requestSortCurrState['sort_col']], ascending = requestSortCurrState['sort_asc'])
                        
                # print(f"~~~~~~~~~~~~  ДЕКОР: df_sort  ^^^^^^^^^^^^^^^^  dicOut = {dicOut}  ")
                
                return dicDecorRes

            return wrapper

        return view


    def df_sort_v2(requestDic, **skwargs):
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






    def df_table_html_input_paginator_html_sorting(requestDic, **tkwargs):
        """
        Декоратор для формирования кода выходной таблицы HTML  на основе фрейма и с учетом сортировки
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

                if isinstance(dicDecorRes['df'], int):
                    
                    dicDecorRes['tableCode'] = ''
                    dicDecorRes['paginatorHtml'] = ''
                    dicDecorRes['dfQn'] = 0
                    
                else:
                    # Добавляем в параметры - requestDic
                    tkwargs['requestDic'] = requestDic
                    # Получить динамический обьект метода, отвечающего за формирование html кода для выходной таблицы
                    oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['prepareTableHtmlFunc'], byClassFilePAth = True)
                    # Подготовить выходной HTML-код для таблицы на бызе страницы процедурного (прошедшего все процедуры) фрейма
                    tableCode = oFunc(dicDecorRes['df'], **tkwargs)
                    
                    dicDecorRes['tableCode'] = tableCode
                    # dicDecorRes['dfQn'] = len(dicDecorRes['df'])
                    
                # print(f"~~~~~~~~~~~~  ДЕКОР: df_table_html_input_paginator_html_sorting  ^^^^^^^^^^^^^^^^  dicInp = {dicInp}  ")
                
                return dicDecorRes

            return wrapper

        return view




    def decor_df_to_html_table_v2(requestDic, **tkwargs):
        """
        Декоратор для формирования кода выходной таблицы HTML  на основе фрейма и с учетом сортировки и возможного оборачивания таблицы в форму, если необходимо
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
    
    
    
    
    
    def decor_df_to_html_table_v3(requestDic, **tkwargs):
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



    def decor_df_to_html_table_v3_prev(requestDic, **tkwargs):
        """
        Предыдущий
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






    def decor_df_to_html_table_v4(requestDic, **tkwargs):
        """
        Декоратор для формирования кода выходной таблицы HTML  на основе фрейма и с учетом сортировки и возможного оборачивания таблицы в форму, если необходимо
        Версия 4: Добавлена возможность добавлять фиксированные url-атрибуты и их значения в в формируемую автоматом константную url-строку. Для этого теперь в
        динасическую функцию передается не фрейм, а сквозной словарь, который содержит как фрейм, так и прочие параметры, которые могут понадобится для формирования html-кода таблицы
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
                    # tkwargs['dicDecorRes'] = dicDecorRes
                    
                    # Получить динамический обьект метода, отвечающего за формирование html кода для выходной таблицы
                    oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['prepareTableHtmlFunc'], byClassFilePAth = True)
                    # Подготовить выходной HTML-код для таблицы на бызе страницы процедурного (прошедшего все процедуры) фрейма
                    tableCode = oFunc(dicDecorRes, **tkwargs)
                    
                    
                    
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




    
    
    # def decorate_table_with_from(requestDic, **fkwargs):
    #     """
    #     ПРОРАБАТЫВАЕТСЯ...
    #     Декоратор для обертывания html-кода выходной таблицы в форму. Форма нужна тогда, когда в таблице есть поля типа checkbox или radio-button и т.п., что бы отправлять выбранные
    #     данные в рядах таблице через POSt на какую-то обработку. 
    #     В декоратор через **fkwargs передаются возможные параметры для построения формы:
    #         - id формы
    #         - name формы
    #         - action-link, ссылка , по которой будут обрабатываться запросы с POST-параметрами из формы
    #         - Прочие параметры могут быть так же добавлены, при этом надо производить изменения декоратора
    #     RET: tableCodeDecoratedWithForm (но переменная остается 'tableCode'), paginatorHtml
    #     Category: Декораторы
    #     """
        
    #     def view(func_to_decorate):
    #         """
    #         Обертка для функции из модуля Views в системе Jango
    #         """
            
    #         def wrapper(*args, **kwargs):
    #             # Считывание return первичной функции (которая должна возвращать df - DataFrame и requestDic - возвратные параметры со страницы сайта в формате Jango)
    #             dicDecorRes = func_to_decorate(*args, **kwargs)

    #             # Если нет рядов в фрейме
    #             if isinstance(dicDecorRes['df'], int):
                    
    #                 dicDecorRes['tableCode'] = ''
    #                 dicDecorRes['paginatorHtml'] = ''
    #                 dicDecorRes['dfQn'] = 0
                    
    #             # Если есть ряды в фрейме
    #             else:

    #                 # Обернуть tableCode , поступающий из предыдущих декораторов в форму с заданынми параметрами
    #                 tableCode = dicDecorRes['tableCode'] # Код таблицы, обернцтый в пагинатор или пагинаторы, которые могут быть снизу и/или сверху
                    
    #                 # A. Выделить из кода с пагинаторами отдельно коды табдицы и пагинаторов.

    #                 tbDecoratingWithForm = """ 
    #                                         <form id="save_bonds_wp" name = "save_bonds_wp" action="/save_chosen_bonds_to_inx_pckg">
    #                                             %TABLE_WITH_PAGIN%
    #                                         </form>
    #                                     """
                    
    #                 tbPaginDecorator = tbPaginDecorator.replace('%PAGINATOR_HTML%', dicDecorRes['paginatorHtml'])
                    
    #                 dicDecorRes['tableCode'] = tbPaginDecorator.replace('%TABLE%', tableCode)
                    
                    
    #             # print(f"~~~~~~~~~~~~  ДЕКОР: df_table_html_input_paginator_html_sorting  ^^^^^^^^^^^^^^^^  dicInp = {dicInp}  ")
                
    #             return dicDecorRes

    #         return wrapper

    #     return view

    




    def df_paginator_with_sorting_and_html_pagin(requestDic, **pkwargs):
        """
        Декоратор для формирования кодов пагинатора на основе фрейма и с учетом текущей сортировки. 
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
                        url = pkwargs['url'] # Ссылка на модуль полная
                        # Словарь с текущими аргументами requestDic
                        # urlsArgsMatrix = requestDic
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
                        
                        # paginatorHtml = paginator
                        
                        # print(f"%%%%%%%%%%%%%%%%   &&&&&&&&&&&&   df_paginator_with_sorting_and_html_pagin ****************   paginatorHtml = {paginatorHtml}")
                        
                        dicDecorRes['df'] = dfPage
                        dicDecorRes['paginatorHtml'] = paginatorHtml
                        
                        # else: # Если нет активной страницы в requestDic,  то возвращаем весь df без пагинации
                            
                        #     dicDecorRes['paginatorHtml'] = ''
                            
                    # Если нет рядовв фрейме (то есть фрейм - пустой)        
                    else:
                        dicDecorRes['df'] = -1
                        dicDecorRes['paginatorHtml'] = ''
                        
                # print(f"~~~~~~~~~~~~  ДЕКОР: df_paginator_with_sorting_and_html_pagin  ^^^^^^^^^^^^^^^^  dicOut = \n{dicDecorRes}  ")
                        
                return dicDecorRes

            return wrapper

        return view
    
    
    
    def df_paginator_with_sorting_and_html_pagin_v2(requestDic, **pkwargs):
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
    
    



    def df_paginator_with_sorting_and_html_pagin_v3(requestDic, **pkwargs):
        """
        Декоратор для формирования кодов пагинатора на основе фрейма и с учетом текущей сортировки и с учетом заданных дополнительных url-параметров с их значениями
        Версия 2 - базовая url и субдомен с названием View теперь формируется из сквозного декор-словаря 
        Версия 3 - с учетом заданных дополнительных url-параметров с их значениями 
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
                        # сначала проверяем были ли переданы из View дополнителльные парметры с заданынми значениями для добавления в к url-строке 
                        if 'dicUrlArgsAdd' in dicDecorRes:
                            dicUrlArgsAdd = dicDecorRes['dicUrlArgsAdd'] # Дополнительные заданные url-аргументы
                        else:
                            dicUrlArgsAdd = {}
                            
                        # print(f'44$$$$4$$$$$$   &&&&&&&&&&&&&  dicUrlArgsAdd = {dicUrlArgsAdd}')
                            
                        constUrlArgsPaginLine = RequestManagerJango.prepare_url_const_line_from_request_dic_with_exclusions_and_addings(requestDic, pkwargs['genExcludeListFoPagin'], dicUrlArgsAdd)
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

    
    
    
    
    


    def df_assoc_titles_and_calcs(request, **atkwargs):
        """
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








    def df_columns_decoration(requestDic, **dkwargs):
        """
        Декоратор для  окончательного оформления форматов колонок для вывода (цвета,  bold и т.д.)
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
                    dicDecorRes['df'] = FunctionsGeneralClass.wrap_df_with_cols_formatting_dict_indexed_v2 (dicDecorRes['df'], **dkwargs)
                        
                # print(f"~~~~~~~~~~~~  ДЕКОР: df_columns_decoration  ^^^^^^^^^^^^^^^^  dicRes = {dicOut}  ") 
                    
                return dicDecorRes

            return wrapper

        return view




    def df_columns_formatting(requestDic, **dkwargs):
        """
        На данный момент - копия декоратора df_columns_decoration(). Но в будущем форматирование колонки и декорирование могут быть различными в нюансах
        Как минимум абстрактное отличие есть уже. Форматер может создавать новые колонки. А декоратор может только оформлять существующие !!
        Декоратор для  окончательного оформления форматов колонок для вывода (цвета,  bold и т.д.)
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

                    dicDecorRes['df'] = FunctionsGeneralClass.wrap_df_with_cols_formatting_dict_indexed_v2 (dicDecorRes['df'], **dkwargs)
                        
                # print(f"~~~~~~~~~~~~  ДЕКОР: df_columns_decoration  ^^^^^^^^^^^^^^^^  dicRes = {dicOut}  ") 
                    
                return dicDecorRes

            return wrapper

        return view




    def df_columns_formatting_with_row_as_argument(requestDic, **dkwargs):
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






    def delete_df_rows_by_column_mask(requestDic, **dkwargs):
        """

        Обработка фрейма по колонке-маски : удаление рядов
        RET: df
        Category: Декораторы
        """
        
        # dkwargs['requestDic'] = requestDic
        
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
                    
                    if 'mask_column' in requestDic:
                        maskCol = requestDic['mask_column']
                        dicDecorRes['df']  = BondsMainManager.clear_df_by_mask_column_name_bool_pandas(dicDecorRes['df'], maskCol)
                        
                # print(f"~~~~~~~~~~~~  ДЕКОР: df_columns_decoration  ^^^^^^^^^^^^^^^^  dicRes = {dicOut}  ") 
                    
                return dicDecorRes

            return wrapper

        return view




    def convert_df_columns_decor_v1(requestDic, **dkwargs):
        """

        Конвертирование колонок в фрейме
        RET: df
        Category: Декораторы
        """
        
        # dkwargs['requestDic'] = requestDic
        
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
                    
                    
                    dicDecorRes['df']  = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dicDecorRes['df'], 'annual_yield')
                    dicDecorRes['df']  = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dicDecorRes['df'], 'last_annual_yield')  # !!
                    dicDecorRes['df']   = PandasManager.convert_str_empty_with_persent_and_empty_str_to_float(dicDecorRes['df'], 'curr_price')
                            
                        
                # print(f"~~~~~~~~~~~~  ДЕКОР: df_columns_decoration  ^^^^^^^^^^^^^^^^  dicRes = {dicOut}  ") 
                    
                return dicDecorRes

            return wrapper

        return view





### ГЕНЕРАЛЬНЫЕ КОМПЛЕКСНЫЕ ДЕКОРАТОРЫ 



    def decor_proccessor_classic(requestDic, **dkwargs):
        """
        Комплексный декоратор, классический, то есть применяется последовательность атомарных декораторов для стандартного и наиболее часто употребляемого варианта вывода таблицы
        с данными на сайте, ее оформление и пагинация, сортировка, оформление данных в колонках, фильтрация - как через перезагрузку страницы, так и через AJAX
        Category: Декораторы
        """
        
        def view(func_to_decorate):
            """
            Обертка для макетода из View модуля
            """
            
            @DecoratorsJangoCube.decor_df_to_html_table_v3_prev(requestDic, **dkwargs['table_codes']) # Декоратор подготовки HTML-кода выходной таблицы с возможной сортировкой колонок
            # @DecoratorsJangoCube.df_columns_decoration(requestDic, **dkwargs) # Декоратор форматирования колонок фрейма
            @DecoratorsJangoCube.df_paginator_with_sorting_and_html_pagin_v2(requestDic, **dkwargs['pagination']) # Декоратор для пагинации фрейма с учетом текщей сортировки
            @DecoratorsJangoCube.filter_by_query_v2(requestDic, **dkwargs['filtering'])
            @DecoratorsJangoCube.df_sort_v2(requestDic) # декоратор сортировки фрейма
            @DecoratorsJangoCube.df_columns_formatting(requestDic, column_decorator = dkwargs['formatting']) # Декоратор форматирования колонок фрейма
            @DecoratorsJangoCube.df_assoc_titles_and_calcs(requestDic, dicTabTitles = dkwargs['assoc_titles']) # Декоратор переименования заголовков колонок фрейма
            def wrapper(*args, **kwargs):

                dicDecorRes = func_to_decorate(*args, **kwargs)
                
                return dicDecorRes
            return wrapper
        return view




    def decor_proccessor_classic_with_decor_settings(requestDic, **dkwargs):
        """
        ЗАГОТОВКА - комплексный декоратор, где включение декораторов настривается (некоторые могут быть отключены) НЕ ПРОРАБОТАНО НИЧЕГО
        Комплексный декоратор, классический, то есть применяется последовательность атомарных декораторов для стандартного и наиболее часто употребляемого варианта вывода таблицы
        с данными на сайте, ее оформление и пагинация, сортировка, оформление данных в колонках, фильтрация - как через перезагрузку страницы, так и через AJAX
        Category: Декораторы
        """
        
        def view(func_to_decorate):
            """
            Обертка для макетода из View модуля
            """
            
            @DecoratorsJangoCube.df_table_html_input_paginator_html_sorting(requestDic, **dkwargs['table_out']) # Декоратор подготовки HTML-кода выходной таблицы с возможной сортировкой колонок
            @DecoratorsJangoCube.df_columns_decoration(requestDic, **dkwargs) # Декоратор форматирования колонок фрейма
            @DecoratorsJangoCube.df_paginator_with_sorting_and_html_pagin(requestDic, **dkwargs['paginator']) # Декоратор для пагинации фрейма с учетом текщей сортировки
            @DecoratorsJangoCube.filter_by_query_v2(requestDic, **dkwargs['filters'])
            @DecoratorsJangoCube.df_sort(requestDic) # декоратор сортировки фрейма
            def wrapper(*args, **kwargs):

                dicDecorRes = func_to_decorate(*args, **kwargs)
                
                return dicDecorRes
            return wrapper
        return view


### END ГЕНЕРАЛЬНЫЕ КОМПЛЕКСНЫЕ ДЕКОРАТОРЫ 












    # def sort_dtoc_set(request, **skwargs):
    #     """
    #     Декоратор для настройки
    #     RET: Обьект класса DsTableOutputCube
    #     """
        
    #     def view(func_to_decorate):
    #         """
    #         Обертка для функции из модуля Views в системе Jango
    #         """
            
    #         def wrapper(*args, **kwargs):
                

    #             dsocObj = func_to_decorate(*args, **kwargs)
                
    #             # Если обьект имеет тип число, то это значит -1 или уведомление об отсутствии фрейма (или еще каких-то непоняток)
    #             if isinstance(dsocObj, int):
    #                 return -1
                
    #             else:
                
    #                 dsocObj.viewFilterFormulas = skwargs['viewFilterFormulas']
    #                 dsocObj.reproccessByRequest()



    #                 # # Считывание return первичной функции (которая должна возвращать df - DataFrame и request - возвратные параметры со страницы сайта в формате Jango)
    #                 # dsocObj = func_to_decorate(*args, **kwargs)
    #                 # # Изменяет матрицу url-аргументов на базе входящего request со страницы сайта
    #                 # urlsArgsMatrix = RequestManagerJango.read_urls_args_dic_from_request_django(request)
    #                 # # Обьект с выходной таблицей для сайта
    #                 # dtoc = DsTableOutputCube(dsocObj, urlsArgsMatrix = urlsArgsMatrix, **tkwargs)
                    
    #                 return dsocObj

    #         return wrapper

    #     return view



# -- Декораторы сортировки, фильтрации, переименования колонок и расчетные колонки



















