from project_bonds_html.projr.classes.html_manager import HTMLSiteManager
from project_bonds_html.projr.settings import *


class PseudoRequest (dict):
    """Класс для созданий обьектов , несущих в себе смысл псевдо-request , возвращаемый с сайта во Flask
    Служит для тестирования алгоритмолв и блоков, участвующих в обработке информации, возвращаемой с сервера саайта в обьекте request
    pseudo-request object (PRO) для тестирования тех алгоритмов, где используются атрибуты возвратных параметров с сервера сайта
    """
    #TODO: Изучить дескриптор @property и как его использовать . Нюансы

    def __init__(self):
        pass


    # # @form.setter
    # def set(self, key, val):
    #     """Устанвка аргументов"""
    #     self.form[key] = val

    # # @form.getter
    # def get(self, key, default = None, type = None):
    #     """Получение аргумента"""
    #     try:
    #         rv = self[key]
    #     except KeyError:
    #         return default
    #     if type is not None:
    #         try:
    #             rv = type(rv)
    #         except ValueError:
    #             rv = default
    #     return rv


    @property
    def args(self) :
        """
        The parsed URL parameters (the part in the URL after the question
        mark).

        By default an
        :class:`~werkzeug.datastructures.ImmutableMultiDict`
        is returned from this function.  This can be changed by setting
        :attr:`parameter_storage_class` to a different type.  This might
        be necessary if the order of the form data is important.
        Category: Вспомогательные
        """
        return self





    @property
    def form(self) :
        """
        The parsed URL parameters (the part in the URL after the question
        mark).

        By default an
        :class:`~werkzeug.datastructures.ImmutableMultiDict`
        is returned from this function.  This can be changed by setting
        :attr:`parameter_storage_class` to a different type.  This might
        be necessary if the order of the form data is important.
        Category: Вспомогательные
        """
        return self



    def set(self, key, val):
        """
        Устанвка аргументов
        Category: Вспомогательные
        """
        self.self[key] = val


    def get(self, key, default = None, type = None):
        """
        Получение аргумента
        Category: Вспомогательные
        """
        try:
            rv = self[key]
        except KeyError:
            return default
        if type is not None:
            try:
                rv = type(rv)
            except ValueError:
                rv = default
        return rv





    @staticmethod
    def print_pseudo_request_IF_DEBUG (pseuRequest):
        """
        OBSOLETED: Преернесено в класс самого псевдо-request
        HTMLSiteManager
        Распечатка параметров псевдо-request
        Category: Распечатки
        """
        if DEBUG_:
            for key,val in pseuRequest.items():
                print(f"key = {key} : val = {val}")






if __name__ == '__main__':
    pass

    # pseudoDic = PseudoRequest ()

    # print(type(pseudoDic))

    # pseudoDic['A'] = 'AAA' 
    # pseudoDic['B'] = 'BBB' 
    # pseudoDic['C'] = 'CCC' 

    # print(pseudoDic.get('A'))

    # form_getA = pseudoDic.get('A')


    # print(pseudoDic.get('B'))

    # form_getB = pseudoDic.form.get('B', type=str , default='')



    # print(pseudoDic.get('C'))

    # args_getC = pseudoDic.args.get('C')