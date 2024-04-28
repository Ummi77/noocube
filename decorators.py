""" Декораторы """

from noocube.settings import *

class Decorators():
    """Хранилище для декораторов"""

    def get_color_due_to_boolean_input_args_maker(colors):
        """
        Создает decorator maker с возможностью передачт агргументов в сам декоратор
        Category: Декораторы
        """

        def get_color_due_to_boolean_input(func_to_decorate):
            """Выдает один из двух заданных цветов в зависимости от входного булиновского параметра
            Цветовая дифференциация в зависимости от входного параметра True or False
            """
            def wrapper(self, *args, **kwargs):

                boolVal = func_to_decorate(self,*args, **kwargs)

                if boolVal:
                    res = colors[1]

                else: # Значит функция sql возвращает один курсор cur
                    res = colors[0]

                return res

            return wrapper

        return get_color_due_to_boolean_input




    def get_color_from_DB_differeciator_by_boolean_input_args_maker(marker):
        """
        Создает decorator maker с возможностью передачт агргументов в сам декоратор
        Category: Декораторы
        """
        

        # A. Получить список цветов дифференциации по названию маркера marker из табл 'differenciztor'

        
        def get_color_due_to_boolean_input(func_to_decorate):
            """Выдает один из двух заданных в БД табл differenciztor по названиею маркера в этой таблице цветов в зависимости от входного булиновского параметра
            Цветовая дифференциация в зависимости от входного параметра True or False
            """
            def wrapper(self, *args, **kwargs):

                boolVal = func_to_decorate(self,*args, **kwargs)

                if boolVal:
                    res = colors[1]

                else: # Значит функция sql возвращает один курсор cur
                    res = colors[0]

                return res

            return wrapper

        return get_color_due_to_boolean_input





