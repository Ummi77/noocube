

from noocube.files_manager import FilesManager
import noocube.funcs_general as FG
import sys

class ClassIni ():
    """
    ЗАГОТОВКА: В частности для распечатки в коде при тестировании при выводе данных переменно информацию о названии переменной , текущем методе и классе,
    в участке кода, гдк выводится значение переменно. Что бы можно было быстро находить место в коде при проверке печатаемых логов, откуда идет распечатка 
    родоначальник всех классов
    
    """

    def __init__(self):
        self.cls_file =  __file__
        self.cls_name = self.__class__.__name__
        self.method = sys._getframe().f_code.co_name



    def print_var_with_class_module_info_if_DEBUG_clsini(self, var):
        """
        Получить стринговые данные по названию класса и модуля (файла)
        Category: Распечатки
        """
        varStrName = FG.name_of_variable_as_string_retrieve (var)
        fbasename = FilesManager.basename_from_filepath_retrieve  (self.cls_file)
        print (f"{varStrName} = {var} / {self.cls_name}.{self.method} <{fbasename}>")












