    
import inspect


# import imp 
import importlib.util
#https://stackoverflow.com/questions/49434118/python-how-to-create-a-class-object-using-importlib


import os
from noocube.switch import Switch
from noocube.pandas_manager import PandasManager
import datetime
import functools

# import re

from noocube.re_manager import ReManager

    
class FunctionsGeneralClass (): 
    """ 
    Класс для работы с Pandas
    """
    
    def __init__(self):
        pass
    
    
    
# ### DECORATORS 

#     def print_with_mark_analyze(func_to_decorate):
#         """Анализируует """
#         def wrapper(self,*args, **kwargs):
#             file = inspect.stack()[0][1] # Файл , откуда вызывается принт
#             func = inspect.stack()[0][3] # Функция, откуда вызывается принт
            
#         return wrapper




# ### END DECORATORS 

### 1. МЕТОДЫ КОНВЕРТИРОВАНИЯ  ------------------------

    @staticmethod
    def convert_str_with_persent_and_empty_str_to_float (strVal, nullReplaceDigit = '-1'):
        """FunctionsGeneralClass
        Если strVal равна '' (пустоте) или NULL/None , то превращает strVal в nullReplaceDigit, удаляет знак процента '%' и потом конвертирует strVal в float
        nullReplaceDigit - число в виде стринга. которое подставляется в случае, когда strVal равна '' (пустоте) или NULL/None
        Category: Конвертация типов
        """
        if isinstance(strVal, list): # Если передается параметром из лямбда-функции, то значить будит тип: list и надо взять первый элемент из списка, Что бы получить аргумент strVal
            strVal = strVal[0]
        if (isinstance(strVal, str) and len(strVal)<1) :
            strVal = strVal.replace('', nullReplaceDigit) # Перевести стринговые пустоты в '-1' 
        if (isinstance(strVal, str)):
            strVal = strVal.replace('%', '')
            strVal = strVal.replace(' ', '')
        # print(f"$$$$$$$$$$$%%%%%%%%%%  strVal = {strVal}")
        if strVal is None: # емли значение = NULL или None
            resVal = -1 
        else:
            resVal = float(strVal)
            
        return resVal
    
    
    
    
    @staticmethod
    def code_digits_sequence_to_alphabet_one_coder_01_blf (digitsSequence): 
        """
        Перевести цифровую последовательность, типа '43578' в буквенный типа 'dcegh' , где цифрам соотвтетсвуют буквы алфавита по индексу цифры.
        ПРИМ: 0 - считатется 'a' , 1 - 'b' и т.д.
        coder_01 - условное название данного алгоритма кодирования
        ПРИМ: Декодер должен быть таким: [ord(char) - 96 for char in input('Write Text: ').lower()]
        """    
        
        strDigitsSequence = str(digitsSequence)
        alphabetDigitsSequence = [chr(ord('`') + int(x)+1) for x in strDigitsSequence]
        alphabetDigitsSequence = "".join(alphabetDigitsSequence)
        
        return alphabetDigitsSequence
    
    
    
    
        
        
    
    
    
    
    
    
    
### END МЕТОДЫ КОНВЕРТИРОВАНИЯ  ------------------------


#### ОБЩИЕ -------------------




    @staticmethod
    def load_class_obj_from_file(filePath, className, **impParams):
        """
        FunctionsGeneralClass
        [05-01-2024] - последние изменения ?? или это старый ??
        Загружает класс как обьект по пути к файлу-модулю (классу)
		* https://stackoverflow.com/questions/49434118/python-how-to-create-a-class-object-using-importlib  !!
		* https://stackoverflow.com/questions/41678073/import-class-from-module-dynamically !! [SuperClass Parent ??]
        Category: 
        """
        
        print(f"PR_NC_110 --> START: load_class_obj_from_file()")

        spec = importlib.util.spec_from_file_location(className, filePath)
        
        # print(f"PR_NC_112 --> spec {spec}")
        
        module = importlib.util.module_from_spec(spec)
        
        # print(f"PR_NC_115 --> module {module}")
        
        # Verify contents of the module:
        # print(f"PR_NC_114 -->  импортированного модуля {dir(module)}")
        
        spec.loader.exec_module(module)

        # print(f"PR_NC_116 -->  POINT AFTER spec.loader.exec_module(module)")

        cls = getattr(module, className)

        # Создание обьекта класса
        objCls = cls(**impParams)
        
        print(f"PR_NC_111 --> END: load_class_obj_from_file()")

        return objCls
    
    
    


    
    


    @staticmethod
    def print_start_functions_by_id(listOfAllowdPrintsId, id, func = '', className = '', file = '', prefix = ''):
        """
        FunctionsGeneralClass
        РАспечатка в терминале логов старта  функций, либо чего- то еще
        Если в списке listOfAllowdPrintsId (которая в settings.py или передается напрямую в параметре) стоит '*' - то распечатываются все функции, 
        иначе - распечатываются только те, ID которых находится в этом списке. 
        id - идентификатор распечатки . ID могут быть любыми - цифры int или метки в стринговом варианте
        adrdressExt - метка адреса распечатки
        prefix - префикс-метка в начале распечатки, что бы было заметно в общем потоке в терминале
        Category: Распечатки
        """
        
        if '*' in listOfAllowdPrintsId: # Распечатываем всегда, если в listOfAllowdPrintsId есть '*'
            print(f"{prefix} id = {id}, START: {func} | {className} | {file}")
        elif id in listOfAllowdPrintsId: # Иначе распечатываем только тогда, когда в списке идентификаторов к распечатке есть id даннйо распечатки
            print(f"{prefix} id = {id}, START: {func} | {className} | {file}")
        
        
        
    @staticmethod
    def print_end_functions_by_id(listOfAllowdPrintsId, id, func = '', className = '', file = '', prefix = ''):
        """
        FunctionsGeneralClass
        РАспечатка в терминале логов завершения функций, либо чего- то еще
        Если в списке listOfAllowdPrintsId (которая в settings.py или передается напрямую в параметре) стоит '*' - то распечатываются все функции, 
        иначе - распечатываются только те, ID которых находится в этом списке. 
        id - идентификатор распечатки . ID могут быть любыми - цифры int или метки в стринговом варианте
        adrdressExt - метка адреса распечатки
        prefix - префикс-метка в начале распечатки, что бы было заметно в общем потоке в терминале
        Category: Распечатки
        """
        
        if '*' in listOfAllowdPrintsId: # Распечатываем всегда, если в listOfAllowdPrintsId есть '*'
            print(f"{prefix} id = {id}, END: {func} | {className} | {file}")
        elif id in listOfAllowdPrintsId: # Иначе распечатываем только тогда, когда в списке идентификаторов к распечатке есть id даннйо распечатки
            print(f"{prefix} id = {id}, END: {func} | {className} | {file}")
            
            
            
            
    @staticmethod
    def print_any_mark_by_id(listOfAllowdPrintsId, id, mark, markVal, func = '', className = '', classFile = inspect.stack()[0][1], prefix = ''):
        """
        FunctionsGeneralClass
        РАспечатка в терминале логов любых меток mark['name'] со значениями mark['val']
        Если в списке listOfAllowdPrintsId (которая в settings.py или передается напрямую в параметре) стоит '*' - то распечатываются все функции, 
        иначе - распечатываются только те, ID которых находится в этом списке. 
        id - идентификатор распечатки . ID могут быть любыми - цифры int или метки в стринговом варианте
        adrdressExt - метка адреса распечатки
        prefix - префикс-метка в начале распечатки, что бы было заметно в общем потоке в терминале
        
        ПРИМЕР:
            FunctionsGeneralClass.print_any_mark_by_id(
                PRINT_TERMINAL_START_END_FUNCTIONS_,
                'printPagin1',
                mark = {'name' : 'into PaginatorWithDataFrame.get_curr_paginator_from_gen()', 'val' : None},
                func = 'activate()',
                className = 'DSourceOutputCube',
                file = 'noocube/dsource_output_cube_v2.py',
                prefix = '@@@@@@@@@@@    $$$$$$$$$$$$4  '
            )
        Category: Распечатки
        """
        # print ('$$$$$$$$$$$$$$$$$$444 ' + inspect.stack()[0][1])
        if '*' in listOfAllowdPrintsId: # Распечатываем всегда, если в listOfAllowdPrintsId есть '*'
            print(f"\n|--> {prefix} LOG: id = {id}, \n|-->  mark: {mark} = \n\n|-->  VAL: \n{markVal} \n\n|--> Func: {func} | Class: {className} | File: {classFile}\n")
        elif id in listOfAllowdPrintsId: # Иначе распечатываем только тогда, когда в списке идентификаторов к распечатке есть id даннйо распечатки
            print(f"\n|--> {prefix} LOG: id = {id}, \n|-->  mark: {mark} = \n\n|-->  VAL: \n  {markVal} \n\n|--> Func: {func} | Class: {className} | File: {classFile}\n")
            


    @staticmethod
    def get_number_of_difits_in_numeric_fgc (valNumeric) : 
        """ 
        Получить разрядность числа или кол-во цифр в числе
        """
        
        n = abs(int(valNumeric))
        count = len(str(n))
        
        return count
        
        
        
        
        
        
        





    ### -- ФУНКЦИИ ДИНАМИЧЕСКОГО ФОРМИРОВАНИЯ КЛАССОВ И МЕТОДОВ КЛАССА
            
    @staticmethod
    def find_func_in_globals(fClassName, funcName):
        """
        FunctionsGeneralClass 
        Найти функцию по названию ее класса и имени , находящихся в области видимости
        Category: Глобальные функции
        """
        classObj = globals()[fClassName] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        funcObj = getattr(classObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        return funcObj
    
    
    
    @staticmethod
    def find_func_in_globals_by_func_path(methodPath, delim = '.'):
        """
        FunctionsGeneralClass 
        Найти функцию по названию ее класса и имени , находящихся в области видимости
        Category: Глобальные функции
        """
        from noocube.ds_table_output_cube_v2 import DsTableOutputCube
        
        className, funcName = FunctionsGeneralClass.get_class_and_method_name_from_path_to_function (methodPath, delim, type = 'visibleSpace')
        
        classObj = globals()[className] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        funcObj = getattr(classObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        return funcObj
    
    
    
    @staticmethod
    def get_func_obj_by_func_name_and_full_class_path_str(funcClassPathStr, delim = '.'):
        """
        FunctionsGeneralClass 
        Найти функцию по названию ее класса и имени , находящихся в области видимости
        funcClassPathStr: like '<FileClasspath>|<ClassName>|<FuncName>' ПРИМ: В старом варианте разделитель '.', поэтому не удалять метод
        Category: Глобальные функции
        """
        from noocube.ds_table_output_cube_v2 import DsTableOutputCube
        
        fileClassPath, expectedClass, funcName = FunctionsGeneralClass.get_class_and_method_name_from_path_to_function (funcClassPathStr, delim, type = 'invisibleSpace')
        
        print(f"PR_168 --> fileClassPath, expectedClass, funcName = {fileClassPath, expectedClass, funcName}")
        
        classObj, funcObj = FunctionsGeneralClass.get_func_obj_by_path_to_class_file_static(fileClassPath, expectedClass, funcName)
        
        return classObj, funcObj
    
    
    
    
    def get_class_and_method_name_from_path_to_function (methodPath, delim = '.', type = 'visibleSpace'):
        """
        Распарсить путь к методу , что бы получить название класса и имя метода
        В зависимости от области видимости могут быть два типа записи пути к методу.
        А так же может быть иной формат записи пути при необходимости сделать или обновить расчетную колонку. Все эти варианты определяются типом type
        methodPath - путь к методу (может быть в разных форматах, в зависимости от целей)
        delim -  делиметр
        Category: Глобальные функции
        """
        
        for case in Switch(type):
            
            if case('visibleSpace'): 
                
                parts = methodPath.split(delim) # Делим на Класс и название функции , которая создает вычисляемую колонку
                className = parts[0] # Название класса
                funcName = parts[1] # Название функции
                res = (className, funcName)
                
                
            if case('invisibleSpace'): 
                
                parts = methodPath.split(delim) # Делим на Класс и название функции , которая создает вычисляемую колонку
                classPath = parts[0] # Название класса
                className = parts[1] # Название функции
                funcName = parts[2] # Название функции
                res = (classPath, className, funcName)
                
                
            if case(): # default
                print('Другое число')
                break
        
        return res
        
    
            



        
    @staticmethod
    def find_func_in_globals_static_by_class_name_or_by_path_to_class(funcName = '', byClassFilePAth = False, expectedClass = '', classNameOrPath = ''):
        """
        FunctionsGeneralClass
        Найти функцию как обьект по названию ее класса и имени , находящихся в проекте
        (используется для создания функций динамическим образом)
        byClassFilePAth - флаг: либо ищем по названию класса, для тех классов, которая данная функция видит в своем пространстве пакета, где она расположена.
        Либо - ищет вне пространства по полному пути к модулю, содержащему класс. 
        funcName - название функции в модуле класса
        classObj 0 в теле функции - класс в виде обьекта
        classNameOrPath - Может быть в двух видах. В виде 'НазваниеКласса', Либо в виде 'ПутьККлассу' в зависимости от флага byClassFilePAth присваивается один из двух вариантов
        На выходе - функция в иде обьекта
        Category: Глобальные функции
        """
        
        if byClassFilePAth:
            classObj = FunctionsGeneralClass.load_class_obj_from_file(classNameOrPath, expectedClass) # В  случае , если модуль задается полным путем файла
        else:
            # Не доработано и не оттестировано
            classObj = globals()[classNameOrPath] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        
        funcObj = getattr(classObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        return funcObj
    
    
    
    @staticmethod
    def find_func_in_globals_static_by_class_name_or_by_path_to_class_v2(funcName = '', byClassFilePAth = False, expectedClass = '', className = '', filePath = ''):
        """
        FunctionsGeneralClass
        Найти функцию как обьект по названию ее класса и имени , находящихся в проекте
        Версия 2: Разделены classNameOrPath на className и modulePath
        (используется для создания функций динамическим образом)
        byClassFilePAth - флаг: либо ищем по названию класса, для тех классов, которая данная функция видит в своем пространстве пакета, где она расположена.
        Либо - ищет вне пространства по полному пути к модулю, содержащему класс. 
        funcName - название функции в модуле класса
        classObj 0 в теле функции - класс в виде обьекта
        classNameOrPath - Может быть в двух видах. В виде 'НазваниеКласса', Либо в виде 'ПутьККлассу' в зависимости от флага byClassFilePAth присваивается один из двух вариантов
        На выходе - функция в иде обьекта
        Category: Глобальные функции
        """
        
        if byClassFilePAth:
            classObj = FunctionsGeneralClass.load_class_obj_from_file(filePath, expectedClass) # В  случае , если модуль задается полным путем файла
        else:
            # Не доработано и не оттестировано
            classObj = globals()[className] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        
        funcObj = getattr(classObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        return funcObj
    
    
    
    @staticmethod
    def get_func_obj_by_path_to_class_file_static (fileClassPath, expectedClass, funcName):
        """
        FunctionsGeneralClass
        Найти функцию как обьект по пути к ее классу и имени функции
        funcName - название функции в модуле класса
        classObj 0 в теле функции - класс в виде обьекта
        classNameOrPath - Может быть в двух видах. В виде 'НазваниеКласса', Либо в виде 'ПутьККлассу' в зависимости от флага byClassFilePAth присваивается один из двух вариантов
        На выходе - функция в иде обьекта
        Category: Глобальные функции
        """
        
        print(f"PR_NC_109 --> START: FunctionsGeneralClass.get_func_obj_by_path_to_class_file_static()")
        
        classObj = FunctionsGeneralClass.load_class_obj_from_file(fileClassPath, expectedClass) # В  случае , если модуль задается полным путем файла
        funcObj = getattr(classObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        
        print(f"PR_NC_110 --> END: FunctionsGeneralClassget_func_obj_by_path_to_class_file_static()")

        
        
        return classObj, funcObj
    
        
            
    
    @staticmethod
    def parse_gen_func_name (fullFuncName):
        """
        FunctionsGeneralClass
        Распарсить общее название функции (используется для создания функций динамическим образом)
        TODO: Надо сделать два варианта парсинга по выбору - для классов, которые видны в пакете noocube и для них нужно только название класса (модуля) и функции искомой
        И для варианта, который не видим из пространства noocube, где надо путь к классу, название класса и название функции
        Category: Глобальные функции
        """

        parts = fullFuncName.split('|') # Делим на Класс и название функции , которая создает вычисляемую колонку
        classNameOrPath = parts[0] # Название класса или путь к нему
        modueName = parts[1] # Название модуля
        funcName = parts[2] # Название модуля
        # print(f"@@@@@@@@@@@@   55555555555   className = {className} / funcName = {funcName}")
        return classNameOrPath, modueName, funcName
        
        
        
        
    @staticmethod
    def get_func_obj_by_its_full_name (fullFuncName, byClassFilePAth = False):
        """
        FunctionsGeneralClass
        Вернуть функцию как обьект по ее полному названию ('НазваниеКласса.НазваниеФункции')
        fullFuncName - Полное название функции . Может быть в двух видах. В виде 'НазваниеКласса.Название функции'
        Либо в виде 'ПутьККлассу.НазваниеФункции' (вслучае , если функция вне видимости noocube или текущего проекта???)
        
        ПРИМЕР: 
        Создание обьекта функции по полному пути, когда она находится вне области видимости noocube
        
        prepareTableHtmlFunc = '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/local_templates_fa.py|LocalTemplatesFA|prepare_html_table_code_type1_v3', # Путь к методу, отвечающему за формирование html кода для выходной таблицы выода функций
        get_func_obj_by_its_full_name (prepareTableHtmlFunc, byClassFilePAth = True) 
        Category: Глобальные функции
        """

        classNameOrPath, modueName, funcName = FunctionsGeneralClass.parse_gen_func_name (fullFuncName)
        
        if byClassFilePAth:
            oFunc = FunctionsGeneralClass.find_func_in_globals_static_by_class_name_or_by_path_to_class(funcName = funcName, byClassFilePAth = True, expectedClass = modueName, classNameOrPath = classNameOrPath)
        else:
            # Этот вариант не доработан и неоттестирован
            oFunc = FunctionsGeneralClass.find_func_in_globals_static_by_class_name_or_by_path_to_class(funcName, False, classNameOrPath)

        return oFunc



    @staticmethod
    def wrap_df_with_cols_formatting_dict (df, dicFormatter):
        """
        FunctionsGeneralClass
        Форматирует данные в колонках фрейма df в соотвтетствии с заданными функциями в словаре-форматере dicFormatter
        Функциями в словаре определяют колонку и соотвтетсвующую функцию-обертку для значений в этой колонке
        Используется в частности для расчетных полей
        Если index = True,  то в функцию apply подается еще уникальный индекс строки заданного фрейма. По умолчанию, index = False и в apply подается 
        только само значение заданной колонки
        Пример:
        
        (обертка для значений названий функций (прибавление круглых скобок в конце) для класса FuncsAnalyzerManager, который не виден из noocube)
        
        COLS_WRAPS_FORMATTING_ = {
        'Название' : '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/funcs_analyzer_manager.py|FuncsAnalyzerManager|func_name_wrap', 
        }
        Category: Калькуляторы полей
        """
        
        
        
        # Обертывание значений по стобцам в соотвтетсвии с заданынми в settings.py (корневой) обертками в константе COLS_WRAPS_FORMATTING_
        for key, wrapFaunc in dicFormatter.items():
            
            # Получение обьекта функции заданного класса 
            oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (wrapFaunc, byClassFilePAth = True)
            # Применение обертки для соотвтетсвующих столбцов фрейма
            df[key] =  df.apply(lambda row: oFunc(row[key]), axis = 1)
            
        
        return df
        
        
    @staticmethod
    def wrap_df_with_cols_formatting_dict_indexed (df, **dkwargs):
        """
        ПРОВЕРЕНО
        FunctionsGeneralClass
        Форматирует данные в колонках фрейма df в соотвтетствии с заданными функциями в словаре-форматере dicFormatter с передачей индекса ряда в заданном фрейме df,
        что позволяет каждое значение в ряду через apply() обрабатывать с заданным индексом уникальности, что необходимо часто при формировании таблицы, если, к примеру,
        надо выводить какие-то данные с обращением в общий фрейм , из которого пагинацией сделана выборка (аможет быть это соотвтетсвует и индексу таблицы БД , только с +1 значенеим 
        внутреннего индекса таблицы, не поля 'id', а собственного индекса таблицы) 
        Функциями в словаре определяют колонку и соотвтетсвующую функцию-обертку для значений в этой колонке. А так эе необхдимо при оборачивании оформления колонок фрейма
        Используется в частности для расчетных полей
        В функцию apply подается еще уникальный индекс строки заданного фрейма, так как часто необхоимо формировать уникальные id для строк таблицы из фрейма
        В отличии от аналогичного декоратора wrap_df_with_cols_formatting_dict(), где подается только значение заданнйо колонки в рядах фрейма
        row.name в df.apply () - представляет индекс ряда. Если задано имя или без имени  ~ https://stackoverflow.com/questions/26658240/getting-the-index-of-a-row-in-a-pandas-apply-function
        Пример:
        
        (обертка для значений названий функций (прибавление круглых скобок в конце) для класса FuncsAnalyzerManager, который не виден из noocube)
        
        COLS_WRAPS_FORMATTING_ = {
        'Название' : '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/funcs_analyzer_manager.py|FuncsAnalyzerManager|func_name_wrap', 
        }
        Category: Калькуляторы полей
        """
        dicFormatter = dkwargs['column_decorator']

        
        # Обертывание значений по стобцам в соотвтетсвии с заданынми в settings.py (корневой) обертками в константе COLS_WRAPS_FORMATTING_
        for key, wrapFaunc in dicFormatter.items():
            
            # Получение обьекта функции заданного класса 
            oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (wrapFaunc, byClassFilePAth = True)
            # Применение обертки для соотвтетсвующих столбцов фрейма
            # row.name - представляет индекс ряда. Если задано имя или без имени ~ https://stackoverflow.com/questions/26658240/getting-the-index-of-a-row-in-a-pandas-apply-function
            df[key] =  df.apply(lambda row: oFunc(row[key], row.name, **dkwargs), axis = 1)
            
        
        return df
        

        
    @staticmethod
    def wrap_df_with_cols_formatting_dict_indexed_v2 (df, **dkwargs):
        """
        FunctionsGeneralClass
        Версия 2 от wrap_df_with_cols_formatting_dict_indexed(): Добавляется возможность задавать название колонки в df[key] =  df.apply ... Таким образом если название
        колонки новое для фрейма, то эта колонка добавиться. А если уже имеется такое название, то будет форматироваться старая коллонка
        Аргументом служит значение ячейки в ряду фрейма row[keyParts[0]] в функии ниже  df.apply(lambda row: oFunc(row[keyParts[0]], row.name, **dkwargs), axis = 1)
        
        Форматирует данные в колонках фрейма df в соотвтетствии с заданными функциями в словаре-форматере dicFormatter с передачей индекса ряда в заданном фрейме df,
        что позволяет каждое значение в ряду через apply() обрабатывать с заданным индексом уникальности, что необходимо часто при формировании таблицы, если, к примеру,
        надо выводить какие-то данные с обращением в общий фрейм , из которого пагинацией сделана выборка (аможет быть это соотвтетсвует и индексу таблицы БД , только с +1 значенеим 
        внутреннего индекса таблицы, не поля 'id', а собственного индекса таблицы) 
        Функциями в словаре определяют колонку и соотвтетсвующую функцию-обертку для значений в этой колонке. А так эе необхдимо при оборачивании оформления колонок фрейма
        Используется в частности для расчетных полей
        В функцию apply подается еще уникальный индекс строки заданного фрейма, так как часто необхоимо формировать уникальные id для строк таблицы из фрейма
        В отличии от аналогичного декоратора wrap_df_with_cols_formatting_dict(), где подается только значение заданнйо колонки в рядах фрейма
        row.name в df.apply () - представляет индекс ряда. Если задано имя или без имени  ~ https://stackoverflow.com/questions/26658240/getting-the-index-of-a-row-in-a-pandas-apply-function
        Пример:
        
        (обертка для значений названий функций (прибавление круглых скобок в конце) для класса FuncsAnalyzerManager, который не виден из noocube)
        
        COLS_WRAPS_FORMATTING_ = {
        'Название' : '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/funcs_analyzer_manager.py|FuncsAnalyzerManager|func_name_wrap', 
        }
        Category: Калькуляторы полей
        """
        dicFormatter = dkwargs['column_decorator']
        
        # print(f'@@@@@@@@@@@   %%%%%%%%%%%%%%%%%%   $$$$$$$$$$$$   dicFormatter = {dicFormatter}')
        # print(f"@@@@@@@@@@@   %%%%%%%%%%%%%%%%%%   $$$$$$$$$$$$   dkwargs['requestDic']  = {dkwargs['requestDic'] }")
        

        
        # Обертывание значений по стобцам в соотвтетсвии с заданынми в settings.py (корневой) обертками в константе COLS_WRAPS_FORMATTING_
        for key, wrapFaunc in dicFormatter.items():
            
            # Получение обьекта функции заданного класса 
            oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (wrapFaunc, byClassFilePAth = True)
            # Применение обертки для соотвтетсвующих столбцов фрейма
            # row.name - представляет индекс ряда. Если задано имя или без имени ~ https://stackoverflow.com/questions/26658240/getting-the-index-of-a-row-in-a-pandas-apply-function
            
            # Анализ ключевого названия колонки. Если есть второе имя через | то это значит заводить новую колонку с резултатом в нее. А аргументом служит первое название колонки
            keyParts = key.split('|')
            
            # TODO: Если было два имени и больше, то первые имена - это аргументы для функции, а последний - результирующая новая колонка . Пока лишь колонка аргумент | колонка результат, если есть
            if len(keyParts) > 1: 
                
                # Находим название новой колонки и ее необходимый порядок в фрейме. 
                newColParts = keyParts[1].split(':')
                print(f'%%%%%%%%%%  @@@@@@@@@@ ;;;;;;;;;;;  newColParts = {newColParts} ')
                
                # Если есть разделитель, то значит задан индекс порядка колонки в фрейме. и устанавливаем колонку по этому индексу. Иначе колонка просто остается в конце фрейма
                if len(newColParts) > 1: 
                    newColName = newColParts[0]
                    # ФОРМАТИРОВАНИЕ КОЛОНКИ. Подставляем в поле ключа - новое название колонки. И поэтмоу будет создана новая колонка. А аргументом выступает первое название колонки
                    df[newColName] =  df.apply(lambda row: oFunc(row[keyParts[0]], row.name, **dkwargs), axis = 1)
                    # Передвигаем колонку на нужное место
                    df = PandasManager.shift_col_by_name_in_df (df, newColParts[0], int(newColParts[1]))
                    
                else:
                    newColName = keyParts[1]
                    # ФОРМАТИРОВАНИЕ КОЛОНКИ. Подставляем в поле ключа - новое название колонки. И поэтмоу будет создана новая колонка. А аргументом выступает первое название колонки
                    df[keyParts[1]] =  df.apply(lambda row: oFunc(row[keyParts[0]], row.name, **dkwargs), axis = 1)
                    
                
            else: # Если одно ключевое название колонки, значит форматируется или декорируется сама эта колонка
                
                df[key] =  df.apply(lambda row: oFunc(row[key], row.name, **dkwargs), axis = 1)
            
            
            # print (f'#############   %%%%%%%%%%%%%%%%%%%    ************   df = \n{df}')
        
        return df
        
        
    @staticmethod
    def proccessing_df_by_dynamic_funcs_with_row_as_argument (df, **dkwargs):
        """
        FunctionsGeneralClass
        Форматирование колонок фрейма  на базе результатов динамически задаваемой функции, где входящим аргументом для динамичекой функции служит ряд фрейма 
        В этом случае в динамической функции можно использовать значения разных ячеек передаваемого ряда для вычисления необходимого результата
        (в не колонка. как ранее)
        Category: Калькуляторы полей
        """
        dicFormatter = dkwargs['column_decorator']
        
        # print(f'@@@@@@@@@@@   %%%%%%%%%%%%%%%%%%   $$$$$$$$$$$$   dicFormatter = {dicFormatter}')
        # print(f"@@@@@@@@@@@   %%%%%%%%%%%%%%%%%%   $$$$$$$$$$$$   dkwargs['requestDic']  = {dkwargs['requestDic'] }")
        

        
        # Обертывание значений по стобцам в соотвтетсвии с заданынми в settings.py (корневой) обертками в константе COLS_WRAPS_FORMATTING_
        for key, wrapFaunc in dicFormatter.items():
            
            # Получение обьекта функции заданного класса 
            oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (wrapFaunc, byClassFilePAth = True)
            # Применение обертки для соотвтетсвующих столбцов фрейма
            # row.name - представляет индекс ряда. Если задано имя или без имени ~ https://stackoverflow.com/questions/26658240/getting-the-index-of-a-row-in-a-pandas-apply-function
            
            # Анализ ключевого названия колонки. Если есть второе имя через | то это значит заводить новую колонку с резултатом в нее. А аргументом служит первое название колонки
            keyParts = key.split('|')
            
            # TODO: Если было два имени и больше, то первые имена - это аргументы для функции, а последний - результирующая новая колонка . Пока лишь колонка аргумент | колонка результат, если есть
            if len(keyParts) > 1: 
                
                # Находим название новой колонки и ее необходимый порядок в фрейме. 
                newColParts = keyParts[1].split(':')
                # print(f'%%%%%%%%%%  @@@@@@@@@@ ;;;;;;;;;;;  newColParts = {newColParts} ')
                
                # Если есть разделитель, то значит задан индекс порядка колонки в фрейме. и устанавливаем колонку по этому индексу. Иначе колонка просто остается в конце фрейма
                if len(newColParts) > 1: 
                    newColName = newColParts[0]
                    # ФОРМАТИРОВАНИЕ КОЛОНКИ. Подставляем в поле ключа - новое название колонки. И поэтмоу будет создана новая колонка. А аргументом выступает первое название колонки
                    df[newColName] =  df.apply(lambda row: oFunc(row, row.name, **dkwargs), axis = 1)
                    # Передвигаем колонку на нужное место
                    df = PandasManager.shift_col_by_name_in_df (df, newColParts[0], int(newColParts[1]))
                    
                else:
                    newColName = keyParts[1]
                    # ФОРМАТИРОВАНИЕ КОЛОНКИ. Подставляем в поле ключа - новое название колонки. И поэтмоу будет создана новая колонка. А аргументом выступает первое название колонки
                    df[keyParts[1]] =  df.apply(lambda row: oFunc(row, row.name, **dkwargs), axis = 1)
                    
                
            else: # Если одно ключевое название колонки, значит форматируется или декорируется сама эта колонка
                
                df[key] =  df.apply(lambda row: oFunc(row[key], row.name, **dkwargs), axis = 1)
            
            
            # print (f'#############   %%%%%%%%%%%%%%%%%%%    ************   df = \n{df}')
        
        return df

        
        
        
        
        
    # @staticmethod
    # def delete_df_rows_based_on_dynamic_function_result (df, **dkwargs):
    #     """
    #     FunctionsGeneralClass
    #     Удалить ряды фрейма на основе результатов заданной динамической функции
    #     Обработать не данные, а именно фрейм. Например, удалить такие-то ряды ... в зависимости от результата динамической функции на основе данных из яччеек фрейма и прочих
    #     дополнительных жданных, переданных через **kwargs
        
        
    #     Category: Калькуляторы полей
    #     """
        
    #     # Набор и последовательнойсть действий, задаваемых в настройках settings.py
    #     dicProccessing = dkwargs['df_proccessing']
        
    #     # print(f'@@@@@@@@@@@   %%%%%%%%%%%%%%%%%%   $$$$$$$$$$$$   dicFormatter = {dicFormatter}')
    #     # print(f"@@@@@@@@@@@   %%%%%%%%%%%%%%%%%%   $$$$$$$$$$$$   dkwargs['requestDic']  = {dkwargs['requestDic'] }")
        

    #     # Процессинг
    #     for key, proccess in dicProccessing.items():
            
    #         # Получение обьекта функции заданного класса 
    #         oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (proccess, byClassFilePAth = True)
    #         # Применение обертки для соотвтетсвующих столбцов фрейма
    #         # row.name - представляет индекс ряда. Если задано имя или без имени ~ https://stackoverflow.com/questions/26658240/getting-the-index-of-a-row-in-a-pandas-apply-function
            
    #         # Анализ ключевого названия колонки. Если есть второе имя через | то это значит заводить новую колонку с резултатом в нее. А аргументом служит первое название колонки
    #         keyParts = key.split('|')
            
    #         # TODO: Если было два имени и больше, то первые имена - это аргументы для функции, а последний - результирующая новая колонка . Пока лишь колонка аргумент | колонка результат, если есть
    #         if len(keyParts) > 1: 
                
    #             # Находим название новой колонки и ее необходимый порядок в фрейме. 
    #             newColParts = keyParts[1].split(':')
    #             print(f'%%%%%%%%%%  @@@@@@@@@@ ;;;;;;;;;;;  newColParts = {newColParts} ')
                
    #             # Если есть разделитель, то значит задан индекс порядка колонки в фрейме. и устанавливаем колонку по этому индексу. Иначе колонка просто остается в конце фрейма
    #             if len(newColParts) > 1: 
    #                 newColName = newColParts[0]
    #                 # ФОРМАТИРОВАНИЕ КОЛОНКИ. Подставляем в поле ключа - новое название колонки. И поэтмоу будет создана новая колонка. А аргументом выступает первое название колонки
    #                 df[newColName] =  df.apply(lambda row: oFunc(row[keyParts[0]], row.name, **dkwargs), axis = 1)
    #                 # Передвигаем колонку на нужное место
    #                 df = PandasManager.shift_col_by_name_in_df (df, newColParts[0], int(newColParts[1]))
                    
    #             else:
    #                 newColName = keyParts[1]
    #                 # ФОРМАТИРОВАНИЕ КОЛОНКИ. Подставляем в поле ключа - новое название колонки. И поэтмоу будет создана новая колонка. А аргументом выступает первое название колонки
    #                 df[keyParts[1]] =  df.apply(lambda row: oFunc(row[keyParts[0]], row.name, **dkwargs), axis = 1)
                    
                
    #         else: # Если одно ключевое название колонки, значит форматируется или декорируется сама эта колонка
                
    #             df[key] =  df.apply(lambda row: oFunc(row[key], row.name, **dkwargs), axis = 1)
            
            
    #         # print (f'#############   %%%%%%%%%%%%%%%%%%%    ************   df = \n{df}')
        
    #     return df
        
        
        
        
        
        
    @staticmethod
    def read_split_parts_with_dic_delimetr_to_dic(strInp, genDelim, dicDelim):
        """
        FunctionsGeneralClass
        Парсинг строки с общим делиметром частей , которые в свою очередь разделяются делиметром на ключ и значение. Превращение их в словарь
        Пример стринга типа словарь:
        'df,class_filt:sa,categ_filt:dd,file_filt:dv,descr_filt:dq', где ',' -  это общий делиметр, ':' - делиметр ключ-значение (словарный делиметр)
        RET: dictionary 
        Category: Парсинг
        """

        genParts = strInp.split(genDelim)
        
        # Удалить пустой член списка '' в genParts ,если он есть 
        if genParts[-1] =='':
            genParts.remove('')
        
        resDic = {}
        for dicKeyVal in genParts:
            partsDic = dicKeyVal.split(dicDelim)
            resDic[partsDic[0]] = partsDic[1]
        return resDic
            
        
        
        
        
        
        ### -- END ФУНКЦИИ ДИНАМИЧЕСКОГО ФОРМИРОВАНИЯ КЛАССОВ И МЕТОДОВ КЛАССА
        
        
        
    #### -- ВСПОМОГАТЕЛЬНЫЕ
    @staticmethod
    def upper_string(inpStr):
        """ 
        FunctionsGeneralClass
        Перевести все буквы в строке в заглавные
        Category: Вспомогательные
        """
        return inpStr.upper()

    
    
    #### -- END ВСПОМОГАТЕЛЬНЫЕ
        
        
        
        
        



#### END ОБЩИЕ --------------

    
    
    #### -- Даты
        
    @staticmethod
    def get_current_year():
        """ 
        Получить текущий год
        """
        today = datetime.date.today()
        currYear = today.year
        return currYear


    #### -- END Даты
    
    
    
    @staticmethod
    def minmax_from_list_gfc(listIntagers):
        """ 
        FunctionsGeneralClass
        Получить список из минимального и максимального значения из входного списка численных значений (может быть и из стринговых и 
        других классов обьектов списка, но не проверенео)
        ~ https://stackoverflow.com/questions/52354317/efficient-way-to-get-min-and-max-from-a-list
        
        """
        return functools.reduce(lambda mm,xx : ( min(mm[0],xx),max(mm[1],xx)) , listIntagers, ( listIntagers[0],listIntagers[0],))





    @staticmethod
    def get_min_max_from_list_of_int_lists (listOfintLists):
        """ 
        FunctionsGeneralClass
        Получить минимум и максимум значений из списка списков численных значений
        """
        
        totalList = []
        
        for intList in listOfintLists:
            
            totalList += intList 
            
        minMaxList = FunctionsGeneralClass.minmax_from_list_gfc(totalList)
        
        return minMaxList
            
            



        
        
        
        
    @staticmethod
    def replace_right_end_of_string_with_diigit_fragment_fgc (strLine, intVal):
        """ 
        FunctionsGeneralClass
        Подставить целое число в строковую переменную в конец справа
        """

        # Поулчить разрядность идентификационного номера 
        digitsCount = FunctionsGeneralClass.get_number_of_difits_in_numeric_fgc(intVal)
        
        zLiterGroup = strLine[:-digitsCount] + str(intVal)
        
        
        return zLiterGroup
        




    @staticmethod
    def obtain_list_elements_greater_than_given_val_fgc (listOfVals, compareVal):
        """ 
        Получить список тех элементов из заданного списка, Которые больше по величине , чем заданная величина для сравнения
        """
        
        listOfValsMoreThenGivenVal = [x for x in listOfVals if x > compareVal]
        
        return listOfValsMoreThenGivenVal


    
    
    
    
if __name__ == '__main__':
    pass



    # # # ПРОРАБОТКА: Получение днамического модуля по абсолютному файлу к модулю с использованием importlib библиотеки

    # #     # ~ https://docs.python.org/3.11/library/imp.html#module-imp 
    # #     # ~ https://stackoverflow.com/questions/301134/
    # #     # ~ https://docs.python.org/3.11/library/importlib.html#importlib-examples !!!

    # import importlib.util

    # file_path = '/home/lenovo/.virtualenvs/django_virt_env/lib/python3.12/site-packages/noocube/text_processor.py'
    # module_name = 'TextProcessor'

    # spec = importlib.util.spec_from_file_location(module_name, file_path)
    # module = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(module)

    # # Verify contents of the module:
    # print(dir(module))

    # testStr  = "[AAAAAA, BBBBBBB,   CCCCCCCC]"

    # cls = getattr(module, 'TextProcessor')

    # objCls = cls(testStr)

    # pList = objCls.string_in_square_brakets_to_list(',')

    # print(pList)



    
    
    
    
    