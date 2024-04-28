

from math import ceil


class Paginator2DimList (): # 
    """ 
   Класс  Пагинатора
    ds - массив, для вывода которого нуже пагинатор
    pgnGenSet - словарь с общими настройками пагинатора . Состоит из ключа ['maxPgsInRow'] - максимальное кол-во номеров страниц , показываемых в текущем активном ряду страниц пагинатора
    и ['rowsOnPage'] - число записей из входного массива, показываемых на одной странице

    currParams - словарь с текущими запросами на активацию : номера блока на активацию с ключем ['numBlActivate] и страницы из текущего блока на активацию с ключем ['pgAcivate']

    Создание текущего обьекта пагинатора на основе общего входного массива данных, параметра -словаря с общими настройками
    и параметра-словаря с текущими значениями атрибутов пагинатора, задающих его теекущее состояние
    """

    # TODO: !!! До смены собственнйо переменнйо текущего номера блока нумератора self.currPgsBlockNumber в методе compose_paginator_state_by_current_pgs_block_number !!!
    # При переходе на следующий блок, страница активная должна устанавливаться на первую страницу нового блока со сменой вырезки по массиву и кол-ву в этой выборке
    # При переходе на предыдущий блок, активная страница должна устанавливаться на крайний справа номер нумератора страниц нового блока со сменой вырезки по массиву и кол-ву в этой выборке

    # Создание текущего обьекта пагинатора на основе общего входного массива данных, параметра -словаря с общими настройками
    #  и параметра-словаря с текущими значениями атрибутов пагинатора, задающих его теекущее состояние
    # Конструктор
    def __init__(self, ds, pgnGenSet, currParams):
        self.ds = ds

        # Общие настроки пагинатора
        self.maxPgsInRow = pgnGenSet ['pagesRowMax'] # максимальное число показа нумерации страниц в ряду
        self.rowsOnPage = pgnGenSet ['dsRowsQnOnPage']  # число записей из входного массива, показываемых на одной странице

        # Анализ массива для слияния с пагинатором
        self.dsN = len(self.ds) # Общее кол-во рядов во входном массиве
        self.pagesNeededForDs = ceil(self.dsN/self.rowsOnPage) # всего необходимо будет страниц, чтобы вывести все записи массива с заданным кол-вом показа рядов на странице
        self.dsPages = [p+1 for p in range(self.pagesNeededForDs)] # текущий общий спиок нумерации для общего количества страниц, необходимы, что бы вывести все записи входного массива
        self.pagesBlocksMaxQn = ceil(self.pagesNeededForDs/self.maxPgsInRow) # Максимальное число блоков (эпох) для вывода всех расчитанных страниц , необходимых для вывода нумерации всех страниц с размером кол-ва номеров страниц, выводимых в ряду перечисления номеров страниц видимых в пагинаторе

        # Текущие параметры запроса для изменения или проверки состояния пагинатора
        # Номер блока для активации выводимых страниц в пагинаторе
        self.pgsBlockNumberCurr = currParams['numBlActivate'] # Номер блока для активации выводимых страниц в пагинаторе
        if self.pgsBlockNumberCurr =='' or self.pgsBlockNumberCurr == None: # Если не задано при инициализации пагинатораили задано и ошибка какя-то то устанавливаем дефолтно
            self.pgsBlockNumberCurr = 1 # Присваивание в собственную переменную текущего активного номера блока-эпохи выводимых номеров страниц в ряду пагинатора для нумерации страниц

        # Настройка предыдущег и последующего номеров блока нумератора выводимых в пагинаторе страниц
        self.pgsBlockNumberPrev = self.pgsBlockNumberCurr - 1  # ПРисваивание начального значения предыдущего текущего номера блока в собственную переменную для метки -ссылки <<
        if self.pgsBlockNumberPrev < 1: # ограничение по пределам возможных вариантов минимального номера блока нумератора (не может быть меньше 1)
            self.pgsBlockNumberPrev = 1

        self.pgsBlockNumberNext = self.pgsBlockNumberCurr + 1  # ПРисваивание начального значения следующего текущего номера блока в собственную переменную для метки -ссылки >>
        if self.pgsBlockNumberNext > self.pagesBlocksMaxQn: # ограничение по пределам возможных вариантов максимального номера блока нумератора (не может быть больше  self.pagesBlocksMaxQn)
            self.pgsBlockNumberNext = self.pagesBlocksMaxQn

        # Cтраница для активации состояния для вывода порции из входного массива
        self.currActivePgNumb = currParams['pgAcivate'] # Cтраница для активации состояния для вывода порции из входного массива
        if self.currActivePgNumb =='' or self.currActivePgNumb == None: # Если не задано при инициализации пагинатораили задано и ошибка какя-то то устанавливаем дефолтно
            self.currActivePgNumb = 1

        if self.currActivePgNumb <1 : # Ограничение по возможному минимальному номеру страницы
            self.currActivePgNumb = 1

        if self.currActivePgNumb > self.pagesNeededForDs: # Ограничение по возможному макимальному номеру страницы
            self.currActivePgNumb = self.pagesNeededForDs
 
        # Изменение текущего состояния пагинатора на основе входных текущих параметров (текущего номера блока нумератора пагинатора и текущей активной страницы)
        self.get_curr_pgs_row_list () # Получение и присваивание инициального автивного текущего списка номеров страниц для вывода в ряду номеров страниц пагинатора
        self.set_paged_limited_ds(self.currActivePgNumb) # Начальная выборка из входного массива на основе начальной инициальной активной страницы = 1
        self.compose_paginator_state_by_current_pgs_block_number(self.pgsBlockNumberCurr ) #  Инициализация начального состояния пагинатора и присвоение его состояние в собственную переменную-словарь self.curr_paginator_state_dict



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
        self.pgsNumeratorCurr = self.dsPages[(self.pgsBlockNumberCurr -1)  * self.maxPgsInRow  : (self.pgsBlockNumberCurr - 1)  * self.maxPgsInRow  + self.maxPgsInRow  ] # Массив для текущего вывода в рядо показываемых нумераторов страниц
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
        if self.pgActivateForNextNumerator > self.pagesNeededForDs: # Ограничения по возможнымзначениям номера страницы
            self.pgActivateForNextNumerator = self.pagesNeededForDs

        
        # Получение и присваивание новой вырезки из входного массива данных с новой устанваливаемой страницей 
        # TODO: Сделать вспомогательныйю функцию вычисления вырезки, так как этот же код используется и в set_paged_limited_ds ниже
        dsLimByPgNumb = self.ds[ (self.currActivePgNumb -1) * self.rowsOnPage  : (self.currActivePgNumb -1) * self.rowsOnPage + self.rowsOnPage ] # Вырезка из общего входного массива на основе входящего номера задаваемой страницы pgNumb
        self.dsLimByPgNumb = dsLimByPgNumb # Присвоение текущей вырезки из общего массива на основе входящего номера страницы в собственную переменную
        self.dsLimByPgNumbN = len(self.dsLimByPgNumb) # Кол-во в текущей вырезке из общег омассива в зависимости от страницы (Последняя страница может давать кол-во меньше, чем заданное кол-во self.rowsOnPage)

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
        print(f"paginator ds = {self.dsN} / Кол-во запсией в массиве") # Кол-во запсией в массиве
        print(f"paginator pagesNeededForDs = {self.pagesNeededForDs} / всего необходимо будет страниц, чтобы вывести все записи массива")  # всего необходимо будет страниц, чтобы вывести все записи массива
        print(f"paginator dsPages = {self.dsPages} / текущий общий спиок нумерации для общего количества страниц") #  текущий общий спиок нумерации для общего количества страниц
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
        ['pgsBlockNumberCurr'] - Текущий активный номер блока-эпохи выводимых страниц в нумераторе страниц
        ['pgsBlockNumberPrev'] - предыдущий текущий номер блока для вывода нумератора страниц
        ['pgsBlockNumberNext'] - последующий текущий номер блока для вывода нумератора страниц    
        Category: Пагинация    
         """
        curr_paginator_state_dict = {}
        curr_paginator_state_dict['maxPgsInRow'] = self.maxPgsInRow # максимальное число показа нумерации страниц в ряду
        curr_paginator_state_dict['rowsOnPage'] = self.rowsOnPage # число записей из входного массива, показываемых на одной странице
        curr_paginator_state_dict['dsN'] = self.dsN # Кол-во запсией в массиве
        curr_paginator_state_dict['pagesNeededForDs'] = self.pagesNeededForDs # всего необходимо будет страниц, чтобы вывести все записи массива
        curr_paginator_state_dict['dsPages'] = self.dsPages #  текущий общий спиок нумерации для общего количества страниц
        curr_paginator_state_dict['pagesBlocksMaxQn'] = self.pagesBlocksMaxQn # Максимальное число блоков (эпох) для вывода всех расчитанных страниц , необходимых для вывода нумерации всех страниц с размером кол-ва номеров страниц
        curr_paginator_state_dict['pgsBlockNumberCurr'] = self.pgsBlockNumberCurr # Текущий начальный номер блока выводимых страниц в пагинаторе
        curr_paginator_state_dict['pgsNumeratorCurr'] = self.pgsNumeratorCurr # текущий список активного нумератора страниц 
        curr_paginator_state_dict['pgsBlockNumberCurr'] = self.pgsBlockNumberCurr # Текущий активный номер блока-эпохи выводимых страниц в нумераторе страниц
        curr_paginator_state_dict['pgsBlockNumberPrev'] = self.pgsBlockNumberPrev  # предыдущий текущий номер блока для вывода нумератора страниц
        curr_paginator_state_dict['pgsBlockNumberNext'] = self.pgsBlockNumberNext # последующий текущий номер блока для вывода нумератора страниц
        curr_paginator_state_dict['currActivePgNumb'] = self.currActivePgNumb # Текущая переданная или инициальная страница для выборки из общего массива
        curr_paginator_state_dict['dsLimByPgNumbN'] = self.dsLimByPgNumbN # Кол-во в текущей вырезке из общег омассива в зависимости от страницы         
        curr_paginator_state_dict['dsLimByPgNumb'] = self.dsLimByPgNumb # Текущая вырезка из общего массива на основе входящего номера страницы в собственную переменную

        self.curr_paginator_state_dict = curr_paginator_state_dict # Присвоение текущего состояния пагинатора в собственную переменную - словарь curr_paginator_state_dict
        return self.curr_paginator_state_dict 



    def set_paged_limited_ds(self, pgNumb):
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
        if pgNumb > self.pagesNeededForDs:
            print (f"Активная страница не может быть больше {self.pagesNeededForDs}. Присваиваем ей {self.pagesNeededForDs}")
            pgNumb = {self.pagesNeededForDs}

        self.currActivePgNumb = pgNumb
        # TODO: Сделать вспомогательныйю функцию вычисления вырезки, так как этот же код используется и в compose_paginator_state_by_current_pgs_block_number         
        dsLimByPgNumb = self.ds[ (self.currActivePgNumb -1) * self.rowsOnPage  : (self.currActivePgNumb -1) * self.rowsOnPage + self.rowsOnPage ] # Вырезка из общего входного массива на основе входящего номера задаваемой страницы pgNumb
        self.dsLimByPgNumb = dsLimByPgNumb # Присвоение текущей вырезки из общего массива на основе входящего номера страницы в собственную переменную
        self.dsLimByPgNumbN = len(self.dsLimByPgNumb) # Кол-во в текущей вырезке из общег омассива в зависимости от страницы (Последняя страница может давать кол-во меньше, чем заданное кол-во self.rowsOnPage)

        # Изменить состояние пагинатора 
        self.compose_paginator_state_by_current_pgs_block_number(self.pgsBlockNumberCurr )
        return self.dsLimByPgNumb 



# УПАРВЛЕНИЕ TODO: 




if __name__ == '__main__':
    pass





