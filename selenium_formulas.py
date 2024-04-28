

from ast import Str
from noocube.switch import Switch
from selenium.webdriver.common.by import By
from noocube.settings import *

class SeleniumFormulas ():
    """ Класс для работы с формулами Селениум """



    def __init__(self, driver): # создание обьекта без конкретной ссылки 
        self.driver = driver


## -- GENERAL SEL SEARCH FUNC  ---
    def __sel_general_srch_func(self,  byParams):
        """ STATE_OF_ART. общая функция поиска по принципам селениум
        ByParams['selFuncName'] - символическое название метода поиска в селениум для операции switch ... case 
        ByParams - конкретные параметры для составления строки поиска селениум {'selObj': selObj,'objTag' : objTag}
        debug - Если True, то будут выведены некоторые принты для режима отладки
        """

        for case in Switch(byParams['selFuncName']):
            
            if case('_sel_find_next_obj_of_equal_lv_for_genF'): # Найти равные  обьекту selObj обьекты с тэегом objTag с задаваемым 
                objs = byParams['selObj'].find_elements(By.XPATH, f".//following-sibling::{byParams['objTag']}" )
                notFoundStr = f"Не найден следующий обьект равного уровня с тэгом {byParams['objTag']}" # Строка для печати в случае не нахождения обьектов
                break

            if case('_sel_find_direct_child_objs_genF'): # Находит прямые дочерние обьекты заданного selObj
                objs = byParams['selObj'].find_elements(By.XPATH, f"./{byParams['objTag']}" )
                notFoundStr = f"Не найден дочерний обьект с тэгом <{byParams['objTag']}>" # Строка для печати в случае не нахождения обьектов
                break

            if case('_sel_find_direct_parent_objs_genF'): # Находит прямые дочерние обьекты заданного selObj
                objs = byParams['selObj'].find_elements(By.XPATH, f".//parent::{byParams['objParTag']}" )
                notFoundStr = f"Не найден родительский обьект  с тэгом {byParams['objParTag']}" # Строка для печати в случае не нахождения обьектов
                break            

            if case('_sel_find_direct_child_objs_with_class_genF'): #Найти прямые DIRECT дочерние обьекты с тэгом objTag и классом  по отношению к обьекту  selObj
                parStr = f"./{byParams['objTag']}[@class='" + f"{byParams['tagCls']}" + "']" # Параметрическая строка с условиями
                objs = byParams['selObj'].find_elements(By.XPATH, parStr )
                notFoundStr = f"Не найден следующий обьект равного уровня с тэгом {byParams['objTag']}" # Строка для печати в случае не нахождения обьектов
                break            

            if case('_sel_find_any_child_objs_with_class_genF'): # Найти любые ANY дочерние обьекты с тэгом objTag и классом  по отношению к обьекту  selObj
                parStr = f".//{byParams['objTag']}[@class='" + f"{byParams['tagCls']}" + "']" # Параметрическая строка с условиями
                objs = byParams['selObj'].find_elements(By.XPATH, parStr)
                notFoundStr = f"Не найден ни один дочерний обьект с тэгом  {byParams['objTag']} и классом {byParams['tagCls']}" # Строка для печати в случае не нахождения обьектов
                break 

            if case('_sel_find_objs_with_given_attribute_genF'): # Найти дочерние обьекты по отношению к selObj, в котором есть атрибут attrName со значением attrVal
                parStr = f".//{byParams['objTag']}[@" + f"{byParams['attrName']}" + "='" + f"{byParams['attrVal']}" + "']" # Параметрическая строка с условиями
                if DEBUG_:
                    print (f"parStr of _sel_find_objs_with_given_attribute_genF = {parStr}")
                objs = byParams['selObj'].find_elements(By.XPATH, parStr)
                notFoundStr = f"Не найден ни один дочерний обьект с тэгом  {byParams['objTag']} , в котором  атрибут {byParams['attrName']} равен {byParams['attrVal']}" # Строка для печати в случае не нахождения обьектов
                break             

            if case('_sel_srch_by_txt_in_obj_genF'): # Найти обьекты в документе или обьекте, содержащие фрагмент текста
                parStr = f".//*[contains(text(),'{byParams['srchStr']}')]" # Параметрическая строка с условиями

                if type(byParams['selObj']) == str : # если обьектом является весь документ и задан стринг 'DOM'
                    objs = self.driver.find_elements(By.XPATH, parStr)
                else: # если передан обьект, а не стрин 'DOM'
                    objs = byParams['selObj'].find_elements(By.XPATH, parStr)

                notFoundStr = f"Не найден ни один  обьект содержащий текст: {byParams['srchStr']}" # Строка для печати в случае не нахождения обьектов
                break 

            if case('_sel_srch_by_exact_txt_in_obj_genF'): # Найти обьекты в документе или обьекте, в точности равные фрагменту текста
                parStr = f".//*[text()='{byParams['srchStr']}']" # Параметрическая строка с условиями

                if type(byParams['selObj']) == str : # если обьектом является весь документ и задан стринг 'DOM'
                    objs = self.driver.find_elements(By.XPATH, parStr)
                else: # если передан обьект, а не стрин 'DOM'
                    objs = byParams['selObj'].find_elements(By.XPATH, parStr)

                notFoundStr = f"Не найден ни один  обьект в точности равный тексту: {byParams['srchStr']}" # Строка для печати в случае не нахождения обьектов
                break             


            if case(): # default   # Если не найдена символическое название функции в switch ... case
                objs = 'Не найдена функция'
                break        

        if 'Не найдена' in objs:
            print (f"Функция {byParams['selFuncName']} не найдена в sqitch .. case ")
            n = -1
            obj = f"Не найдена базовая функция {byParams['selFuncName']}"
            objs = f"Не найдена базовая функция {byParams['selFuncName']}"

        else: 

            n = len(objs)
            if n == 1:
                obj = objs[0] # следующий элемент одного уровня  
                # objs = None
            elif n > 1:
                obj = objs[0]
                # objs = objs
            else: # Если не найдены обьекты
                if DEBUG_: # Если в модуле seetings.py стоит True, то отображается. И наоборот
                    print (notFoundStr) # Вывод строки ненахождения обьекта , индивидуальной для каждой функции - сел
                objs = None            
                obj = None

        return [n, obj, objs]


    def _sel_find_next_obj_of_equal_lv_for_genF (self, selObj , objTag) :
        """ 
        Найти равные  обьекту selObj обьекты с тэегом objTag с задаваемым 
        Функция для использования с общей функцией селениум-поиска _sel_general_srch_func
         """   
        # Подготовка параметров:         
        byParams = { 
            'selFuncName' : '_sel_find_next_obj_of_equal_lv_for_genF',
            'selObj' : selObj,
            'objTag' : objTag
        }
        res = self.__sel_general_srch_func(byParams)
        return res


    def _sel_find_direct_child_objs_genF(self, selObj, objTag):
        """ Найти прямые дочерние обьекты с тэгом objTag по отношению к обьекту  selObj
        Тэг обьекта. Может быть * - тогда все тэги
        """
        # Подготовка параметров:
        byParams = { 
            'selFuncName' : '_sel_find_direct_child_objs_genF',
            'selObj' : selObj,
            'objTag' : objTag
        }
        res = self.__sel_general_srch_func(byParams)
        return res

    def _sel_find_direct_parent_objs_genF(self, selObj, objParTag):
        """ Найти прямые родительский обьект с тэгом objTag по отношению к обьекту  selObj
        Тэг обьекта. Может быть * - тогда все тэги
        """
        # Подготовка параметров:
        byParams = { 
            'selFuncName' : '_sel_find_direct_parent_objs_genF',
            'selObj' : selObj,
            'objParTag' : objParTag
        }
        res = self.__sel_general_srch_func(byParams)
        return res        


    def _sel_find_direct_child_objs_with_class_genF(self, selObj, objTag, tagCls):
        """
        TODO: ?? Не работает поиск по классу почему-то
         Найти прямые DIRECT дочерние обьекты с тэгом objTag и классом  по отношению к обьекту  selObj
        tagCls - !!! Полное название класса (не фрагмента)
        """
        # Подготовка параметров:
        byParams = { 
            'selFuncName' : '_sel_find_direct_child_objs_with_class_genF',
            'selObj' : selObj,
            'objTag' : objTag,
            'tagCls' : tagCls
        }
        res = self.__sel_general_srch_func(byParams)
        return res

    def _sel_find_any_child_objs_with_class_genF(self, selObj, objTag, tagCls):
        """
        TODO: ?? Не работает поиск по классу почему-то
         Найти любые ANY дочерние обьекты с тэгом objTag и классом  по отношению к обьекту  selObj
        tagCls - !!! Полное название класса (не фрагмента)
        """
        # Подготовка параметров:
        byParams = { 
            'selFuncName' : '_sel_find_any_child_objs_with_class_genF',
            'selObj' : selObj,
            'objTag' : objTag,
            'tagCls' : tagCls
        }
        res = self.__sel_general_srch_func(byParams)
        return res


    def _sel_srch_by_txt_in_obj_genF (self,selObj, srchStr):
        """ Найти обьекты в документе или обьекте, содержащие фрагмент текста
        Если selObj = 'DOM', то поиск по всему документу. Иначе только в обьекте selObj
         """
        # Подготовка параметров:
        byParams = { 
            'selFuncName' : '_sel_srch_by_txt_in_obj_genF',
            'selObj' : selObj,
            'srchStr' : srchStr
        }
        res = self.__sel_general_srch_func(byParams)
        return res


    def _sel_srch_by_exact_txt_in_obj_genF (self,selObj, srchStr):
        """ Найти обьекты в документе или обьекте, в точности равные фрагменту текста (а не содержащие его)
        Если selObj = 'DOM', то поиск по всему документу. Иначе только в обьекте selObj
         """
        # Подготовка параметров:
        byParams = { 
            'selFuncName' : '_sel_srch_by_exact_txt_in_obj_genF',
            'selObj' : selObj,
            'srchStr' : srchStr
        }
        res = self.__sel_general_srch_func(byParams)
        return res

    
    def _sel_find_objs_with_given_attribute_genF(self,selObj,objTag, attrName, attrVal):
        """Найти дочерние обьекты по отношению к selObj, в котором есть атрибут attrName со значением attrVal"""

        # Подготовка параметров:
        byParams = { 
            'selFuncName' : '_sel_find_objs_with_given_attribute_genF',
            'selObj' : selObj,
            'objTag' : objTag, 
            'attrName' : attrName,
            'attrVal' : attrVal
        }
        res = self.__sel_general_srch_func(byParams)    
        return res

  

## -- END GENERAL SEL SEARCH FUNC  ---


## -- ОБЫЧНЫЕ НЕЗАВИСИМЫЕ ФУНКЦИИ ---------------------------

    def _sel_get_tds_sibling_of_one_given_td_obj(self, tdObj, print = False):
        """ Находит все соседские однуровневые td-элементы по заданному td обьекту-селениум
            tdObj - Обькт-ключ поле, по которому надо найти рядом стоящие одноуровневые в ряду другие ячейки-поля таблицы
            print - Распечатка настроечных лог сообщений. По умолчанию = False
        """

        tds = self._sel_find_next_obj_of_equal_lv_for_genF (tdObj , 'td') # Одноуровневые td, где хранятся показатели Revenue

        if print: # Распечатка настроечных лог сообщений
            if tds[0]>0 : # Если найдены соседние tds
                print ("Соседние tds найдены")
            else:
                print ("Соседние tds не найдены")

        res = tds
        return res





## -- END ОБЫЧНЫЕ НЕЗАВИСИМЫЕ ФУНКЦИИ ---------------------------


    # --- Вспомогательные функции --------
    def _get_united_data_from_two_columns_selenium_objs_list(self, oRows, rowTag):
        """ Получение обьединенных данных из ряда, состоящих из двух колонок одинаковых по тэгу селениум-обьектов (прототип таблицы из 2х колонок) """
        infText = ''
        rows = oRows
        for row in rows: # обрабатываем ряды по циклу
            resRowCol = self._sel_find_direct_child_objs_genF(row, rowTag) # колонки в текущем ряду (их две : название и значение)
            rowName = resRowCol[2][0].text
            rowVal = resRowCol[2][1].text
            infText += f'{rowName} : {rowVal} | '

        return infText




    def _if_element_exists(self, objs):
        """Проверка наличия элемента"""
        if len(objs) > 0:
            flagExists = True
        else:
            flagExists = False
        return flagExists






    # --- END Вспомогательные функции --------



    # -- ОБРАБОТКА ТАБЛИЧНЫХ ДАННЫХ  --------------
    
    
    def read_tb_standart_data_with_heads_to_list_SF (self, tb):
        """Считать стандартную таблицу со стандартными заголовками
        ЗАГОТОВКА: Не оттестирована
        """
        
        trs= tb.find_elements(By.TAG_NAME, "tr")

        # Заголовки
        ths = trs[0].find_elements(By.TAG_NAME, "th")
        titles = []
        for i, th in enumerate(ths):

            if i == 2: # Ячейка с ссылкой и названием облигации, где указан isin
                titles.append('ISIN') # ISIN - 3й элемент в ряду массива заголовок для ISIN

            titles.append(th.text)
        
        trs.pop(0) # Удаляем первый ряд, который для заголовков и выходит пустым в результате

        # Данные
        elements = []

        #iterate over the rows                        for index, row in df.iterrows():
        for tr in trs:
            # row data set to 0 each time in list
            row = []
            #iterate over the columns
            tds = tr.find_elements(By.TAG_NAME, "td") 
            for i,td in enumerate(tds):
                # getting text from the ith row and jth column
                if i == 2: # Ячейка с ссылкой и названием облигации, где указан isin
                    href = td.find_element(By.TAG_NAME, "a").get_attribute('href') 
                    hrefParts = href.split('/')
                    isin = hrefParts[-2]
                    row.append(isin) # ISIN - 3й элемент в ряду массива

                row.append(td.text)
            #finally store and print the list in console
            elements.append(row)
            

    def read_tb_standart_data_to_list_SF (self, tbSel, heads  = False):
        """Считать данные тела таблицы без заголовков, таблица стандартная
        tbSel - Обьект Selenium , в данном случае - таблица
        heads - флаг считывания заголовков
        """
        
        trs= tbSel.find_elements(By.TAG_NAME, "tr")
        
        if heads: # Если нужны заголовки так же
            # Заголовки
            ths = trs[0].find_elements(By.TAG_NAME, "th")
            titles = []
            for i, th in enumerate(ths):
                titles.append(th.text)

        
        # trs.pop(0) # Удаляем первый ряд, который для заголовков и выходит пустым в результате
        elements = []
        for tr in trs:
            row = []
            tds = tr.find_elements(By.TAG_NAME, "td") 
            for i,td in enumerate(tds):
                row.append(td.text)
            elements.append(row)

        if heads:
            return titles, elements
        else:
            return elements
    
    
    def read_tb_standart_data_without_heads_with_columns_links_to_list_SF (self, tbSel, linkFieldsFormatsDic):
        """Считать данные тела таблицы без заголовков, таблица стандартная. 
        Считать  так же Дополнительные информационные значения каких-то велечин по заданным колонкам, кроме текста колонки (например, ссылки)
        tbSel - Обьект Selenium , в данном случае - таблица
        linkFieldsFormatsDic - индекс полей с сылками и формат их обработки в виде словаря : { fieldInx : r'RegexpFormstMatch'}. Если RegexpFormstMatch = '*' , 
        то считываем не обработанное (полное ) значение
        
        Пример:
        
        linkFieldsFormatsDic = { 1 : r'([A-Z0-9]{12})'} - если нужно из ссылки вычислить значение ISIN
          или
        linkFieldsFormatsDic = { 1 : '*'} - если полная ссылка
        
        """
        
        from bonds.re_manager import ReManager
        trs= tbSel.find_elements(By.TAG_NAME, "tr")
        # Данные
        fieldInxs = list(linkFieldsFormatsDic.keys())
       
        elements = []

        for tr in trs:
            row = []
            rowGivenColsVals = [] # Дополнительные считавыемые значения каких-то велечин по заданным колонкам, кроме текста колонки
            #iterate over the columns
            tds = tr.find_elements(By.TAG_NAME, "td") 
            for i,td in enumerate(tds):
                # АНализ заданных колонок 
                if i in fieldInxs: # Если индекс колонки есть в списке заданных колонок fieldInxs из словаря с параметрами linkFieldsFormatsDic, то ...
                    href = td.find_element(By.TAG_NAME, "a").get_attribute('href') 
          
                    if linkFieldsFormatsDic[i] == '*': # Если надо взять всю ссылку 
                        rowGivenColsVals.append(href)
                    else: # Обрабатываем ссылку через RegExp
                        reMnger = ReManager()
                        # Применить соответствующий этой коллонке формат для анализа ссылки (в случае необходимости вычислить из ссылки какое-то значение)
                        res = reMnger.find_all_matches_from_text(href, linkFieldsFormatsDic[i]) 

                        if len(res) > 0:
                            rowGivenColsVals.append(res[0]) # 

                row.append(td.text) # Присвоение текста обычной колонки
                
            row += rowGivenColsVals # Добавление к ряду со значениями по колонкам дополнительных ячеек с прочими информационными величинами, считанными по задланным колонкам
            #finally store and print the list in console
            elements.append(row)
        
        return elements
    
    
    # -- END ОБРАБОТКА ТАБЛИЧНЫХ ДАННЫХ  -------------- 






if __name__ == "__main__":
    pass




