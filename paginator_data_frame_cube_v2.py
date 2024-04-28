

from math import ceil
import sys
from noocube.files_manager import FilesManager


sys.path.append('/home/ak/projects/3_Proj_Bonds_HTML_Center/project_bonds_html') # Прописываем path в системную переменную Python, что бы можно было запускать функции из данного модуля напрямую

# from projr.classes.bonds_manager_html import BondsManagerHTML
# from projr.classes.pandas_manager import PandasManager
# from projr.settings import PAGIN_BONDS_CURR_SET_

class PaginatorWithDataFrame (): # 
    """ 
   Класс  Пагинатора
    ds - массив, для вывода которого нуже пагинатор
    pgnGenSet - словарь с общими настройками пагинатора . Состоит из ключа ['maxPgsInRow'] - максимальное кол-во номеров страниц , показываемых в текущем активном ряду страниц пагинатора
    и ['rowsOnPage'] - число записей из входного массива, показываемых на одной странице
    currParams - словарь с текущими запросами на активацию : номера блока на активацию с ключем ['numBlActivate] и страницы из текущего блока на активацию с ключем ['pgAcivate']
    Создание текущего обьекта пагинатора на основе общего входного массива данных, параметра -словаря с общими настройками
    и параметра-словаря с текущими значениями атрибутов пагинатора, задающих его теекущее состояние
    """

    # Создание текущего обьекта пагинатора на основе общего входного массива данных, параметра -словаря с общими настройками
    #  и параметра-словаря с текущими значениями атрибутов пагинатора, задающих его теекущее состояние
    # Конструктор
    def __init__(self, df, pgnGenSet):
        self.df = df
        self.dfInput = df
        
        # Общие настроки пагинатора
        if len(pgnGenSet) > 0: # Если заданы общие настройки пагинатора
            self.maxPgsInRow = pgnGenSet ['pagesRowMax'] # максимальное число показа нумерации страниц в ряду
            self.rowsOnPage = pgnGenSet ['dsRowsQnOnPage']  # число записей из входного массива, показываемых на одной странице
        else: # Если не заданы общие настройки пагинатора, то устанавливаем дефолтное значение
            self.maxPgsInRow = 3 # максимальное число показа нумерации страниц в ряду
            self.rowsOnPage = 20  # число записей из входного массива, показываемых на одной странице

        # Анализ массива для слияния с пагинатором
        self.dfN = len(self.df) # Общее кол-во рядов во входном массиве
        self.pagesNeededForDf = ceil(self.dfN/self.rowsOnPage) # всего необходимо будет страниц, чтобы вывести все записи массива с заданным кол-вом показа рядов на странице
        self.dfPages = [p+1 for p in range(self.pagesNeededForDf)] # текущий общий спиок нумерации для общего количества страниц, необходимы, что бы вывести все записи входного массива
        self.pagesBlocksMaxQn = ceil(self.pagesNeededForDf/self.maxPgsInRow) # Максимальное число блоков (эпох) для вывода всех расчитанных страниц , необходимых для вывода нумерации всех страниц с размером кол-ва номеров страниц, выводимых в ряду перечисления номеров страниц видимых в пагинаторе

        

        # Индексирвоанный Словарь необходимых блоков нумераторов для всего входящего dFrame
        self.numeratorsBlDict = {}
        for numerInx in range(self.pagesBlocksMaxQn):
            numeratorRow = self.dfPages[numerInx * self.maxPgsInRow : numerInx * self.maxPgsInRow + self.maxPgsInRow]
            self.numeratorsBlDict[numerInx+1] = numeratorRow
            
        # # Шаблон пагинатора
        # self.paginTemplateFile = paginTemplateFile
        
        # # !!! HTML-пагинатор код в зависимости от активной страницы
        # # Если задан какой-то файл шаблона в self.paginTemplateFile, то пока подставляем этот шабло (в будущем должен быть анализатор шаблона с конвертацией в текущее состояние по активной странице)
        # if len(self.paginTemplateFile) > 0: 
        #     paginHtml = FilesManager.read_file_data_txt_static(self.paginTemplateFile)
        # else: # Иначе paginHtml = ''
        #     paginHtml = ''
            
        # self.currentPaginHTML = paginHtml

        self.set_curr_active_obj_paginator(1) # Первичная активация превой страницы выборки из общего массива данных
        
        
    # def prepare_pagin_html(self):
    #     """ЗАГОТОВКА. ? Формирование HTML-кода пагинатора"""


    def activate_paginator_state(self, currParams):
        """
        Активирует текущее общее состояние пагинатора по общим настройкам в конкретное состояние , зависящее от страницы к активации и блока нумератора к активации
        Category: Пагинация
        """
        # Текущие параметры запроса для изменения или проверки состояния пагинатора
        # Номер блока для активации выводимых страниц в пагинаторе
        self.pgsBlockNumberCurr = currParams['numBlActivate'] # Номер блока для активации выводимых страниц в пагинаторе
        if self.pgsBlockNumberCurr =='' or self.pgsBlockNumberCurr == None: # Если не задано при инициализации пагинатораили задано и ошибка какя-то то устанавливаем дефолтно
            self.pgsBlockNumberCurr = 1 # Присваивание в собственную переменную текущего активного номера блока-эпохи выводимых номеров страниц в ряду пагинатора для нумерации страниц

        # Cтраница для активации состояния для вывода порции из входного массива
        self.currActivePgNumb = currParams['pgAcivate'] # Cтраница для активации состояния для вывода порции из входного массива
        if self.currActivePgNumb =='' or self.currActivePgNumb == None: # Если не задано при инициализации пагинатораили задано и ошибка какя-то то устанавливаем дефолтно
            self.currActivePgNumb = 1

        # Настройка предыдущег и последующего номеров блока нумератора выводимых в пагинаторе страниц
        self.pgsBlockNumberPrev = self.pgsBlockNumberCurr - 1  # ПРисваивание начального значения предыдущего текущего номера блока в собственную переменную для метки -ссылки <<
        if self.pgsBlockNumberPrev < 1: # ограничение по пределам возможных вариантов минимального номера блока нумератора (не может быть меньше 1)
            self.pgsBlockNumberPrev = 1

        self.pgsBlockNumberNext = self.pgsBlockNumberCurr + 1  # ПРисваивание начального значения следующего текущего номера блока в собственную переменную для метки -ссылки >>
        if self.pgsBlockNumberNext > self.pagesBlocksMaxQn: # ограничение по пределам возможных вариантов максимального номера блока нумератора (не может быть больше  self.pagesBlocksMaxQn)
            self.pgsBlockNumberNext = self.pagesBlocksMaxQn

        if self.currActivePgNumb <1 : # Ограничение по возможному минимальному номеру страницы
            self.currActivePgNumb = 1


        # !!!!!! Защита. Если номер активной страницы превышает максимум страниц  в пагинаторе self.dfPages, то активную страницу нужно обнулить до pg = 1
        if int(self.currActivePgNumb) > self.pagesNeededForDf: # Ограничение по возможному макимальному номеру страницы
            # self.currActivePgNumb = self.pagesNeededForDf
            self.currActivePgNumb = 1

        self.get_curr_pgs_row_list () # Получение и присваивание инициального автивного текущего списка номеров страниц для вывода в ряду номеров страниц пагинатора
        self.set_paged_limited_df(self.currActivePgNumb) # Начальная выборка из входного массива на основе начальной инициальной активной страницы = 1
        self.compose_paginator_state_by_current_pgs_block_number(self.pgsBlockNumberCurr ) #  Инициализация начального состояния пагинатора и присвоение его состояние в собственную переменную-словарь self.curr_paginator_state_dict
        
        return self

    def get_prev_pgs_block_number (self):
        """
        Получевние и присваивание в собственную переменную предыдущего номера блока выводимых страниц (для метки <<)
        currPgsBlockNumber - текущий номер блока (эпохи) вывода страниц в показываемом рфду страниц пагинатора
        RET: pgsBlockNumberPrev - предыдущий номер блока выводимых страниц для перехода по метке <<
        Category: Пагинация
        """
        pgsBlockNumberPrev = self.pgsBlockNumberCurr  - 1 # Предыдущий номер блока выводимых страниц (для метки <<)
        if pgsBlockNumberPrev < 1 : # Если предыдущий номер блока меньше 0, то устанавливаем его в 0 (так как это предел по Previous Block Number)
            pgsBlockNumberPrev = 1     
        self.pgsBlockNumberPrev = pgsBlockNumberPrev # ПРисваивание значения предыдущего текущего номера блока в собственную переменную для метки -ссылки <<
        return pgsBlockNumberPrev # предыдущий номер блока выводимых страниц для перехода по метке <<


    def get_next_pgs_block_number (self):
        """
        Получение и присваивание в собственную переменную следующего номера блока выводимых страниц (для метки >>)
        currPgsBlockNumber - текущий номер блока (эпохи) вывода страниц в показываемом рфду страниц пагинатора
        RET: pgsBlockNumberNext - следующий номер блока выводимых страниц для перехода по метке >>
        Category: Пагинация
        """
        pgsBlockNumberNext = self.pgsBlockNumberCurr  + 1 # Следующий номер блока выводимых страниц в показе
        if pgsBlockNumberNext > self.pagesBlocksMaxQn: # Если следующий номер блока выводимых страниц > необходимого числа блоков страниц pagesNeededForDs, то устанавливаем его = pagesNeededForDs (так как это макимально возможный номер блока выводимых страниц)
            pgsBlockNumberNext = self.pagesBlocksMaxQn   

        self.pgsBlockNumberNext = pgsBlockNumberNext # ПРисваивание значения следующего текущего номера блока в собственную переменную для метки -ссылки >>
        return pgsBlockNumberNext # следующий номер блока выводимых страниц для перехода по метке >>


    def get_curr_pgs_row_list (self):
        """
        Получение текущего списка номеров показываемых страниц в ряду пагинатора
        pgsBlockNumberCurr - текущий номер блока (эпохи) вывода страниц в показываемом рфду страниц пагинатора
        RET: pgsNumeratorCurr - текущий спиок активного нумератора страниц 
        страниц для вывода в ряду пагинатора) передается
        Category: Пагинация
        """
        self.pgsNumeratorCurr = self.dfPages[(self.pgsBlockNumberCurr -1)  * self.maxPgsInRow  : (self.pgsBlockNumberCurr - 1)  * self.maxPgsInRow  + self.maxPgsInRow  ] # Массив для текущего вывода в рядо показываемых нумераторов страниц
        return self.pgsNumeratorCurr # текущий спиок активного нумератора страниц 


    def compose_paginator_state_by_current_pgs_block_number(self, pgsBlockNumberCurr):
        """
        Сформировать состояние пагинатора в зависимости от текущего номера блока-эпохи выводимых номеров страниц в пагинаторе на основе поступающего значения pgsBlockNumberCurr
        Получение нового состояния пагинатора при смене блока нумерации (блок нумерации - это блок показываемых страниц в нумераторе . Переход по блоку осуществляется при нажатии на ссылки >> или <<)
        Меняются Нумератор страниц пагинатора, а так же Prev и Next ссылки. Так же меняется активная страница (либо первая в новом следующем блоке, либо последняя - при переходе на предыдущий блок нумерации страниц)
        При смене активной страницы , соответственно, меняется вырезка из общего массива данных. Все это присваивается собственным переменным обьекта класса

        currPgsBlockNumber - текущий поступающий номер блока-эпохи выводимых в ряду номеров страниц
        Category: Пагинация
        """
        # Ограничения для текущего номера блока в зависитмости от минимального и максимального значения возможных номеров блоков
        # TODO: Нужно ли это ограничение? или лучше выдать ошибку?
        if pgsBlockNumberCurr < 1 : # Если предыдущий номер блока меньше 0, то устанавливаем его в 0 (так как это предел по Previous Block Number)
            pgsBlockNumberCurr = 1   
        if pgsBlockNumberCurr > self.pagesBlocksMaxQn: # Если следующий номер блока выводимых страниц > необходимого числа блоков страниц pagesNeededForDs, то устанавливаем его = pagesNeededForDs (так как это макимально возможный номер блока выводимых страниц)
            pgsBlockNumberCurr = self.pagesBlocksMaxQn           

        nowPgsBlockNumb = self.pgsBlockNumberCurr # Номер блока до смены (предыдущий)
        if nowPgsBlockNumb  > pgsBlockNumberCurr: # Если номер блока до предстоящей смены номера был больше того, который сейчас передается для изменения, то значит идет смена блока на предыдущий
            pass  # При переходе на предыдущий блок, активная страница должна устанавливаться на крайний справа номер нумератора страниц нового блока со сменой вырезки по массиву и кол-ву в этой выборке или на единицу меньше крайнего левого значения текущего нумератора страниц
            firstLeftPgNumbOfNowNumerator = self.pgsNumeratorCurr[0] # Крайний слева номер текущего нумератора страниц
            newActivePage = firstLeftPgNumbOfNowNumerator - 1 # Новая активная страница при смене блока на предыдущий блок нумератора будет меньше на 1 , Чем карйний левый номер текущего нумератора
            self.currActivePgNumb = newActivePage

        elif nowPgsBlockNumb  < pgsBlockNumberCurr: # Если номер блока до предстоящей смены номера был меньше того, который сейчас передается для изменения, то значит идет смена блока на следующий
            pass # При переходе на следующий блок, страница активная должна устанавливаться на первую страницу нового блока со сменой вырезки по массиву и кол-ву в этой выборке
            lastRightPgNumbOfNowNumerator = self.pgsNumeratorCurr[-1] # Крайний справа номер текущего нумератора страниц
            newActivePage = lastRightPgNumbOfNowNumerator + 1 # Новая активная страница при смене блока на следующий блок нумератора будет больше на 1 , Чем карйний справа номер текущего нумератора
            self.currActivePgNumb = newActivePage

        # Вычисление страниц активации при переходе по блокам нумератора
        # При переходе на предыдущий блок нумератора страница активации при этом должна быть:
        firstLeftPgNumbOfNowNumerator = self.pgsNumeratorCurr[0] # Крайний слева номер текущего нумератора страниц
        self.pgActivateForPrevNumerator = firstLeftPgNumbOfNowNumerator - 1 # Новая активная страница при смене блока на предыдущий блок нумератора будет меньше на 1 , Чем карйний левый номер текущего нумератора
        if self.pgActivateForPrevNumerator < 1: # Ограничения по возможнымзначениям номера страницы
            self.pgActivateForPrevNumerator = 1


        # При переходе на следующий блок нумератора страница активации при этом должна быть:
        lastRightPgNumbOfNowNumerator = self.pgsNumeratorCurr[-1] # Крайний справа номер текущего нумератора страниц
        self.pgActivateForNextNumerator = lastRightPgNumbOfNowNumerator + 1 # Новая активная страница при смене блока на следующий блок нумератора будет больше на 1 , Чем карйний справа номер текущего нумератора
        if self.pgActivateForNextNumerator > self.pagesNeededForDf: # Ограничения по возможнымзначениям номера страницы
            self.pgActivateForNextNumerator = self.pagesNeededForDf

        
        # Получение и присваивание новой вырезки из входного массива данных с новой устанваливаемой страницей 
        # TODO: Сделать вспомогательныйю функцию вычисления вырезки, так как этот же код используется и в set_paged_limited_ds ниже
        dfLimByPgNumb = self.df[ (self.currActivePgNumb -1) * self.rowsOnPage  : (self.currActivePgNumb -1) * self.rowsOnPage + self.rowsOnPage ] # Вырезка из общего входного массива на основе входящего номера задаваемой страницы pgNumb
        self.dfLimByPgNumb = dfLimByPgNumb # Присвоение текущей вырезки из общего массива на основе входящего номера страницы в собственную переменную
        self.dfLimByPgNumbN = len(self.dfLimByPgNumb) # Кол-во в текущей вырезке из общег омассива в зависимости от страницы (Последняя страница может давать кол-во меньше, чем заданное кол-во self.rowsOnPage)

        self.pgsBlockNumberCurr = pgsBlockNumberCurr # Присваивание в собственную переменную нового номера блока выводимых номеров страниц в ряду страниц пагинатора
        self.get_prev_pgs_block_number () # Получение и присваивание нового номера для предвдущего номера блока для ссылки <<
        self.get_next_pgs_block_number () # Получение и присваивание нового номера для следующего  номера блока для ссылки <<
        self.get_curr_pgs_row_list () # Получение и присваивание нового автивного текущего списка номеров страниц для вывода в ряду номеров страниц пагинатора

        self.set_curr_paginator_state_dict() # Фиксирование текущего состояния словаря в собственной переменной  self.curr_paginator_state_dict  



    def show_curr_paginator_state(self):
        """
        Показать текущее состояние пагинатора
        Category: Пагинация
        """
        print(f"paginator maxPgsInRow = {self.maxPgsInRow} / максимальное число показа нумерации страниц в ряду") # максимальное число показа нумерации страниц в ряду
        print(f"paginator rowsOnPage = {self.rowsOnPage} / число записей из входного массива, показываемых на одной странице") # число записей из входного массива, показываемых на одной странице
        print(f"paginator ds = {self.dfN} / Кол-во запсией в массиве") # Кол-во запсией в массиве
        print(f"paginator pagesNeededForDs = {self.pagesNeededForDf} / всего необходимо будет страниц, чтобы вывести все записи массива")  # всего необходимо будет страниц, чтобы вывести все записи массива
        print(f"paginator dsPages = {self.dfPages} / текущий общий спиок нумерации для общего количества страниц") #  текущий общий спиок нумерации для общего количества страниц
        print(f"paginator pagesBlocksMaxQn = {self.pagesBlocksMaxQn} / Максимальное число блоков (эпох) для вывода всех расчитанных страниц") # Максимальное число блоков (эпох) для вывода всех расчитанных страниц , необходимых для вывода нумерации всех страниц с размером кол-ва номеров страниц
        print(f"paginator pgsBlockNumberCurr = {self.pgsBlockNumberCurr} / Текущий начальный номер блока выводимых страниц в пагинаторе") # Текущий начальный номер блока выводимых страниц в пагинаторе
        print(f"paginator pgsNumeratorCurr = {self.pgsNumeratorCurr} / текущий спиок активного нумератора страниц ") # текущий спиок активного нумератора страниц 
        print(f"paginator pgsBlockNumberCurr = {self.pgsBlockNumberCurr} / Текущий активный номер блока-эпохи выводимых страниц в нумераторе страниц") # Текущий активный номер блока-эпохи выводимых страниц в нумераторе страниц
        print(f"paginator pgsBlockNumberPrev = {self.pgsBlockNumberPrev} / предыдущий текущий номер блока для вывода нумератора страниц")  # предыдущий текущий номер блока для вывода нумератора страниц
        print(f"paginator pgsBlockNumberNext = {self.pgsBlockNumberNext} / последующий текущий номер блока для вывода нумератора страниц") # последующий текущий номер блока для вывода нумератора страниц
        print(f"paginator dsLimByPgNumbN = {self.dsLimByPgNumbN} / Кол-во в текущей вырезке из общего массива в зависимости от страницы") # Кол-во в текущей вырезке из общег омассива в зависимости от страницы (Последняя страница может давать кол-во меньше, чем заданное кол-во self.rowsOnPage)
        print(f"paginator currActivePgNumb = {self.currActivePgNumb} /Текущая переданная или инициальная страница для выборки из общего массива") # Текущая переданная или инициальная страница для выборки из общего массива


    def set_curr_paginator_state_dict(self):
        """
        Формирует новое  текущее состояние пагинатора в виде словаря и присвоить в собственную переменную self.curr_paginator_state_dict
        RET: curr_paginator_state_dict - словарь текущего состояния пагинатора с ключами
        ['maxPgsInRow'] - максимальное число показа нумерации страниц в ряду
        ['rowsOnPage'] - число записей из входного массива, показываемых на одной странице
        ['dsN']- Кол-во запсией в массиве
        ['pagesNeededForDs'] - всего необходимо будет страниц, чтобы вывести все записи массива
        ['dsPages'] -  текущий общий спиок нумерации для общего количества страниц
        ['pagesBlocksMaxQn'] - Максимальное число блоков (эпох) для вывода всех расчитанных страниц , необходимых для вывода нумерации всех страниц с размером кол-ва номеров страниц
        ['pgsBlockNumberCurr']- Текущий начальный номер блока выводимых страниц в пагинаторе
        ['pgsNumeratorCurr'] - текущий спиок активного нумератора страниц 
        ['pgsBlockNumberPrev'] - предыдущий текущий номер блока для вывода нумератора страниц
        ['pgsBlockNumberNext'] - последующий текущий номер блока для вывода нумератора страниц   
        Category: Пагинация     
        """
        curr_paginator_state_dict = {}
        curr_paginator_state_dict['maxPgsInRow'] = self.maxPgsInRow # максимальное число показа нумерации страниц в ряду
        curr_paginator_state_dict['rowsOnPage'] = self.rowsOnPage # число записей из входного массива, показываемых на одной странице
        curr_paginator_state_dict['dfN'] = self.dfN # Кол-во запсией в массиве
        curr_paginator_state_dict['pagesNeededForDf'] = self.pagesNeededForDf # всего необходимо будет страниц, чтобы вывести все записи массива
        curr_paginator_state_dict['dfPages'] = self.dfPages #  текущий общий спиок нумерации для общего количества страниц
        curr_paginator_state_dict['pagesBlocksMaxQn'] = self.pagesBlocksMaxQn # Максимальное число блоков (эпох) для вывода всех расчитанных страниц , необходимых для вывода нумерации всех страниц с размером кол-ва номеров страниц
        curr_paginator_state_dict['pagesBlockInx'] = self.pgsBlockNumberCurr # Текущий начальный номер блока выводимых страниц в пагинаторе
        curr_paginator_state_dict['pagesList'] = self.pgsNumeratorCurr # текущий список активного нумератора страниц 
        curr_paginator_state_dict['pagesBlockInxPrev'] = self.pgsBlockNumberPrev  # предыдущий текущий номер блока для вывода нумератора страниц
        curr_paginator_state_dict['pagesBlockInxNext'] = self.pgsBlockNumberNext # последующий текущий номер блока для вывода нумератора страниц
        curr_paginator_state_dict['pgToActivate'] = self.currActivePgNumb # Текущая переданная или инициальная страница для выборки из общего массива
        curr_paginator_state_dict['dfLimByPgNumbN'] = self.dfLimByPgNumbN # Кол-во в текущей вырезке из общег омассива в зависимости от страницы         
        curr_paginator_state_dict['dfLimByPgNumb'] = self.dfLimByPgNumb # Текущая вырезка из общего массива на основе входящего номера страницы в собственную переменную
        curr_paginator_state_dict['prevBlockPageToActivate'] = self.pgActivateForPrevNumerator # Новая активная страница при смене блока на предыдущий блок нумератора
        curr_paginator_state_dict['nextBlockPageToActivate'] = self.pgActivateForNextNumerator # Новая активная страница при смене блока на следующий блок нумератора   



        self.curr_paginator_state_dict = curr_paginator_state_dict # Присвоение текущего состояния пагинатора в собственную переменную - словарь curr_paginator_state_dict
        return self.curr_paginator_state_dict 



    def set_paged_limited_df(self, pgNumb):
        """
        Получить ограниченную количеством self.rowsOnPage выборку-эпоху из исходного массива данных self.ds = ds на основе приходящего номера страницы pgNumb
        И зафиксировать изменения в новом состоянии Пагинатора (меняется активная страница и соответственно вырезка из общего массива данных)
        pgNumb - входящий номер задаваемой страницы для вывода части из общего массива (всего может быть self.rowsOnPage записей, отображаемых при текущей странице)
        RET: self.dsLimByPgNumb  - Вырезка из общего входного массива на основе входящего номера задаваемой страницы pgNumb
        Category: Пагинация
        """
        # Проверка номера страницы, который не может быть меньше 1 и больше максимального вычисленного кол-ва страниц self.pagesNeededForDs
        if pgNumb < 1:
            print (f"Активная страница не может быть меньше 1. Присваиваем ей 1")
            pgNumb = 1
        if pgNumb > self.pagesNeededForDf:
            print (f"Активная страница не может быть больше {self.pagesNeededForDf}. Присваиваем ей {self.pagesNeededForDf}")
            pgNumb = {self.pagesNeededForDf}

        self.currActivePgNumb = pgNumb
        # TODO: Сделать вспомогательныйю функцию вычисления вырезки, так как этот же код используется и в compose_paginator_state_by_current_pgs_block_number         
        dfLimByPgNumb = self.df.iloc[ (self.currActivePgNumb -1) * self.rowsOnPage  : (self.currActivePgNumb -1) * self.rowsOnPage + self.rowsOnPage ] # Вырезка из общего входного массива на основе входящего номера задаваемой страницы pgNumb
        self.dfLimByPgNumb = dfLimByPgNumb # Присвоение текущей вырезки из общего массива на основе входящего номера страницы в собственную переменную
        self.dfLimByPgNumbN = len(self.dfLimByPgNumb) # Кол-во в текущей вырезке из общег омассива в зависимости от страницы (Последняя страница может давать кол-во меньше, чем заданное кол-во self.rowsOnPage)

        # Изменить состояние пагинатора 
        # self.compose_paginator_state_by_current_pgs_block_number(self.pgsBlockNumberCurr )
        return self.dfLimByPgNumb 



# Вспомогательные


    @staticmethod
    def get_curr_paginator_from_gen (genPaginator,  pgAcivate):
        """ 
        PaginatorWithDataFrame
        ПОлучение текущего пагинатора на основе потупающих запросов из страницы сайта по запрашиваемой страницы к активации и текущему блоку нумератора к активации
        numBlActivate - номер блока нумератора , получаемой из запроса request, (списка страниц для нажатия) к активации
        pageToActivate - номер страницы , получаемой из запроса request, из страницы сайта к активации
        df - вырезка из общего массива данных dataFrame по запрашиваемой странице к активации
        Category: Пагинация
        """
        # Определение индекса блока нумератора страниц к активации на основе приходящей страницы к активации
        currParams = {} # Текущие параметры пагинатора, определяющие его состояние

        # ПОлучение параметра pg - запрашиваемой с сайта страницы из request
        if pgAcivate =='' or pgAcivate == None:
            pgAcivate = '1'

        # Получение индекса блока нумератора на основе запрашиваемой страницы к активации
        numBlActivate = genPaginator._get_numerator_block_inx_by_page(pgAcivate)

        # Формирование параметра-словаря для переменных, управляющих состоянием пагинатора
        currParams['numBlActivate'] = int(numBlActivate) # Номер нумератора для активации состочния пагинатора
        currParams['pgAcivate'] = int(pgAcivate) # Номер страницы для активации состочния пагинатора
        # END ТЕКУЩИЕ ПАРАМЕТРЫПАГИНАТОРА лпределяющие его состояние
        
        # Создание текущего обьекта пагинатора на основе общего входного массива данных и параметров настройки и текущего состояния
        # paginator = genPaginator  
        currStatePaginator = genPaginator.activate_paginator_state(currParams)

        return   currStatePaginator  








    def set_curr_active_obj_paginator(self,  pgAcivate):
        """ 
        PaginatorWithDataFrame
        ПОлучение текущего пагинатора на основе потупающих запросов из страницы сайта по запрашиваемой страницы к активации и текущему блоку нумератора к активации
        numBlActivate - номер блока нумератора , получаемой из запроса request, (списка страниц для нажатия) к активации
        pageToActivate - номер страницы , получаемой из запроса request, из страницы сайта к активации
        df - вырезка из общего массива данных dataFrame по запрашиваемой странице к активации
        Category: Пагинация
        """
        # Определение индекса блока нумератора страниц к активации на основе приходящей страницы к активации
        currParams = {} # Текущие параметры пагинатора, определяющие его состояние

        # ПОлучение параметра pg - запрашиваемой с сайта страницы из request
        if pgAcivate =='' or pgAcivate == None:
            pgAcivate = '1'

        # Получение индекса блока нумератора на основе запрашиваемой страницы к активации
        numBlActivate = self._get_numerator_block_inx_by_page(pgAcivate)

        # Формирование параметра-словаря для переменных, управляющих состоянием пагинатора
        currParams['numBlActivate'] = int(numBlActivate) # Номер нумератора для активации состочния пагинатора
        currParams['pgAcivate'] = int(pgAcivate) # Номер страницы для активации состочния пагинатора
        # END ТЕКУЩИЕ ПАРАМЕТРЫПАГИНАТОРА лпределяющие его состояние
        
        # Создание текущего обьекта пагинатора на основе общего входного массива данных и параметров настройки и текущего состояния
        # paginator = genPaginator  
        self.activate_paginator_state(currParams)

 




    def _get_numerator_block_inx_by_page(self, pgToActivate):
        """
        Получить индекс блока нумератора из словаря self.numeratorsBlDict в котором находится запрашиваемая страница к активации
        Category: Пагинация
        """
        # !!!!!! Защита. Если номер активной страницы превышает максимум страниц  в пагинаторе self.dfPages, то активную страницу нужно обнулить до pg = 1
        if int(pgToActivate) > self.pagesNeededForDf: # Ограничение по возможному макимальному номеру страницы
            pgToActivate = '1'
        
        
        for key,val in self.numeratorsBlDict.items():
            if int(pgToActivate) in val: # Если в ряду списка находится номер страницы к активайии, то выдать индекс этого блока нумератора
                numeratorBlinx = key
        return numeratorBlinx




# END Вспомогательные








if __name__ == '__main__':
    pass




    # # ПРИМЕР: Проработка получения индекса блока нумератора на основе запрашиваемой страницы к ативации
    # # Массив текущих облигаций из таблицы bonds_current BD = /home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/bonds.db
    # bondsMngr = BondsManagerHTML() # При этом в файле func_general.py в проекте bonds были заблокированы употребление библиотеки pyautogui (почему то не видит ее отсюда)
    # dsBondsCurr = bondsMngr.get_bonds_current () # Массив облигаций с полями в соответствии с таблицей bonds_current    

    # # Получить Pandas dataFrame
    # pandMangr = PandasManager()
    # tbBondsCurr = 'bonds_current'
    # tbFields = bondsMngr.get_tb_fields(tbBondsCurr) # Получение спсика полей таблицы bonds_current
    # dfBonds = pandMangr.get_pandas_data_frame(dsBondsCurr, tbFields)  # dataFrame      

    # # Текущий пагинатор на основе запрашиваемых индекса блока нумератора страниц к активации и страницы к активации и вырезки из массива dataFrame облигаций по запрашиваемой страницы к активации
    # paginatorGen = PaginatorWithDataFrame(dfBonds, PAGIN_BONDS_CURR_SET_) # инициализация общего пагинатора на основе общих настроек PAGIN_BONDS_CURR_SET_ и входного массива dfSorted

    # # Определение ключа словаря numeratorsBlList , в котором находится переданная страница к активации
    # pgAcivate = 6

    # # Получение текущего пагинатора из общего, через получение параметров активации: страницы к активации и блока
    # currPaginator = PaginatorWithDataFrame.get_curr_paginator_from_gen (paginatorGen,  pgAcivate)




    # # ПРИМЕР: Инициализация пагинаора

    # # Массив текущих облигаций из таблицы bonds_current BD = /home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/bonds.db
    # bondsMngr = BondsManagerHTML() # При этом в файле func_general.py в проекте bonds были заблокированы употребление библиотеки pyautogui (почему то не видит ее отсюда)
    # dsBondsCurr = bondsMngr.get_bonds_current () # Массив облигаций с полями в соответствии с таблицей bonds_current    


    # # Получить Pandas dataFrame
    # pandMangr = PandasManager()
    #  # # # Получение спсика полей таблицы bonds_current
    # tbBondsCurr = 'bonds_current'
    # tbFields = bondsMngr.get_tb_fields(tbBondsCurr)

    # dfBonds = pandMangr.get_pandas_data_frame(dsBondsCurr, tbFields)   

    # # Общие настройки пагинатора
    # pagesRowMax  = 5 # максимальное число показа нумерации страниц в ряду
    # dsRowsQnOnPage = 20 # число записей из входного массива, показываемых на одной странице  
    # pgnGenSet = {} # общие настрйоки пагинатора
    # pgnGenSet['pagesRowMax'] = pagesRowMax
    # pgnGenSet['dsRowsQnOnPage'] = dsRowsQnOnPage    


    # # Текущие параметры пагинатора, определяющие его состояние
    # currParams = {} # Текущие параметры пагинатора, лпределяющие его состояние

    # # Формирование параметра-словаря для переменных, управляющих состоянием пагинатора
    # currParams['numBlActivate'] = 1 # Номер нумератора для активации состочния пагинатора
    # currParams['pgAcivate'] = 1 # Номер страницы для активации состочния пагинатора


    # paginator = PaginatorWithDataFrame(dfBonds, pgnGenSet, currParams)
