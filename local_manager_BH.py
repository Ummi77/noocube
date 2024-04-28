


from noocube.decorators import Decorators
from noocube.settings import *


class LocalManager():
    """Класс для реализации локальных специализированных методов, связанных только с этим локальны проектом"""




    # СИСТЕМНЫЕ ФУНКЦИИ CUBE


    def find_func_in_globals_HM(funcDescr):
        """LocalManager
        Найти функцию по названию ее класса и имени , находящихся в проекте
        funcDescr - описание функции в виде 'className.funcName'
        """
        parts = funcDescr.split('.') # Вычисление названий класса в которой находится АИФП и  имени атомарной поисковой функции
        fClassName = parts[0] # названий класса в которой находится АИФП 
        funcName = parts[1] # имени атомарной поисковой функции

        algClassObj = globals()[fClassName] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
        algFuncObj = getattr(algClassObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
        return algFuncObj



    # END СИСТЕМНЫЕ ФУНКЦИИ CUBE




    # КАЧЕСТВЕННЫЕ МЕТОДВ ДЛЯ СТРУКТУР HTML 


    @staticmethod
    @Decorators.get_color_due_to_boolean_input_args_maker('RAEX_WITHDROWN_ROWS_COLORS_') # RAEX_WITHDROWN_ROWS_COLORS_ - константа в settings проекта Bonds_HTML  Proj 3
    def if_comp_in_raex_comps_withdrawn_tb(currRow, inList):
        """LocalManager
        Boolean дифференциация рядов в таблицах в зависисмости от нахождения компании в таблице отозванных компаний по рейтингу RAEX в задаваемом списке inList, где находятся ИНН из таблицы 
        Идентификация проходит по ключу inn
        currRow -  row из цикла , формирующего тело таблицы с рядами 
        """
        inn = currRow['ИНН']
        if inn in inList: # Если есть inn в таблице raex_comps_withdrawn
            ifInnExists = True

        else:
            ifInnExists = False # Усли inn нет, то возвращаем False (хотя это меняет искуственно ситуацию и неправильно. Временная заплатка)

        return ifInnExists



    @staticmethod
    @Decorators.get_color_due_to_boolean_input_args_maker('BUNKRUPT_ROWS_COLORS_') # BUNKRUPT_ROWS_COLORS_ - константа в settings проекта Bonds_HTML  Proj 3
    def if_comp_in_bunkrupt_bonds_tb(currRow, inList, keyField):
        """LocalManager
        Boolean дифференциация рядов в таблицах в зависисмости от нахождения компании в таблице отозванных компаний по рейтингу RAEX в задаваемом списке inList, где находятся ИНН из таблицы 
        Идентификация проходит по ключу inn
        currRow -  row из цикла , формирующего тело таблицы с рядами 
        """
        inn = currRow[keyField]
        if inn in inList: # Если есть inn в таблице raex_comps_withdrawn
            ifInnExists = True

        else:
            ifInnExists = False # Усли inn нет, то возвращаем False (хотя это меняет искуственно ситуацию и неправильно. Временная заплатка)

        return ifInnExists




    @staticmethod
    def if_comp_in_inn_list(currRow, inList, keyField):
        """LocalManager
        Общая функция. Используется в циклах, создающих ряды для HTML таблицы для вывода на странице сайта
        Boolean дифференциация рядов в таблицах в зависисмости от нахождения значения по ключу keyField в передаваемом в параметрах списке значений inList
        currRow -  row из цикла , формирующего тело таблицы с рядами 
        keyField - поле в таблице, по которому производится сверка
        """
        inn = currRow[keyField]
        if inn in inList: # Если есть inn в таблице raex_comps_withdrawn
            ifInnExists = True

        else:
            ifInnExists = False # Усли inn нет, то возвращаем False (хотя это меняет искуственно ситуацию и неправильно. Временная заплатка)

        return ifInnExists


    # END КАЧЕСТВЕННЫЕ МЕТОДВ ДЛЯ СТРУКТУР HTML 







































