import math
from multiprocessing import Pool
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from noocube.selenium_formulas import SeleniumFormulas
from noocube.sqlite_processor import SqliteProcessor

from noocube.switch import Switch
from noocube.settings import *
import noocube.funcs_general as FG

from selenium.webdriver.common.by import By
import random
import datetime
import abc

from noocube.re_manager import ReManager
from noocube.files_manager import FilesManager
import urllib.request


class HTMLSeleniumManager (SeleniumFormulas):
    """ TODO: Этот модуль не предназначен для парсинга сайтов, хоть в названии есть. Он - для подсоединения к драйверу и прочими тех.методами. 
    Но в названии есть парсинг, что не должно соответствовать. Потом постепенно изменить структуру. Парсинг в этом модуле - OBSOLETED. Тспользовать для этого класс SiteParserManager,
    а этот переназвать и перенести парсинговые функции в класс SiteParserManager
"""

    # TODO: Сделать автоматическую сохранениие сессии в БД, специально для этого предназначенную и системную !!!


    def __init__(self): # создание обьекта без конкретной ссылки 
        pass

    # Конструктор класа по инициализации системного драйвера внутри системыс открытием окна
    @classmethod
    def ini_from_iside(cls):
        """ 
        Инициализация изнутри
        Category: Конструктор класса
        """
        self = cls()
        # self.driver = webdriver.Firefox('/home/ak/geckodriver/')
        self.driver = webdriver.Firefox()
        self.get_session_and_url_selen_sys() # ПОлучение параметров сессии открывшегося браузера
        # TODO: Сохранять параметры сессии еще и в лог-файле системном !!! log_sys_sessions.txt
        self.autosave_session_to_sys_db() # Автосохранение сессии в БД 'sys_db.db' табл ''sessions
        # self.dr_link = '' 
        self.brWindows = [] # лист для учета открывающихся окон, фолдеров в браузере
        return self


    # # Конструктор класа по драйверу, полученному вне системы
    # @classmethod
    # def ini_from_remote(cls, ffxFriver): # создание обьекта по драйверу, найденному извне обьекта
    #     cls.driver = ffxFriver
    #     cls.get_session_and_url_selen_sys(cls)
    #     #TODO: Сохранять заново, только если нет ключа [session_id, session_url]
    #     cls.autosave_session_to_sys_db(cls)
    #     # self.dr_link = '' 
    #     cls.brWindows = [] # лист для учета открывающихся окон, фолдеров в браузере



    # Конструктор класа по драйверу, полученному вне системы
    @classmethod
    def ini_from_remote(cls, ffxFriver): # создание обьекта по драйверу, найденному извне обьекта
        """ 
        Конструктор класа по драйверу, полученному вне системы
        Category: Конструктор класса
        """
        self = cls()
        self.driver = ffxFriver
        self.get_session_and_url_selen_sys()
        #TODO: Сохранять заново, только если нет ключа [session_id, session_url]
        self.autosave_session_to_sys_db()
        # self.dr_link = '' 
        self.brWindows = [] # лист для учета открывающихся окон, фолдеров в браузере
        return self





    def initialize_driver (self):
        """
        Инициализирует обьект класса  - создает драйвер
        Category: Конструктор класса
        """
        self.driver = webdriver.Firefox()
        self.get_session_and_url_selen_sys() # ПОлучение параметров сессии открывшегося браузера
        # TODO: Сохранять параметры сессии еще и в лог-файле системном !!! log_sys_sessions.txt
        self.autosave_session_to_sys_db() # Автосохранение сессии в БД 'sys_db.db' табл ''sessions
        # self.dr_link = '' 
        self.brWindows = [] # лист для учета открывающихся окон, фолдеров в браузере
        
        
    def initialize_and_link (self, link):
        """
        Инициализирует обьект класса  - создает драйвер
        Category: Конструктор класса
        """
        self.driver = webdriver.Firefox()
        self.get_session_and_url_selen_sys() # ПОлучение параметров сессии открывшегося браузера
        # TODO: Сохранять параметры сессии еще и в лог-файле системном !!! log_sys_sessions.txt
        self.autosave_session_to_sys_db() # Автосохранение сессии в БД 'sys_db.db' табл ''sessions

        self.driver.get(link)
        self.brWindows = [] # лист для учета открывающихся окон, фолдеров в браузере
        
        

# -- Методы для работы с сессиями браузера Firefox 

    def get_session_and_url_selen_sys(self):
        """
        Получить сессию и url обьекта класса и присвоить в переменную обьекта. Функция для сохранения параметров сессии в собственных переменных обьекта класса
        https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session/70088095#70088095
        Category: Сессии
        """
        self.url = self.driver.command_executor._url       
        self.session_id = self.driver.session_id      
        

    def autosave_session_to_sys_db (self):
        """
        Автосохранение сессии при любом открытии браузера в локальной системной БД sys_db.db <sqlite> в таблице sessions
        Category: Сессии
        """
        time_format2 = FG.get_current_time_format2()
        sessName = f'SessFfx: {time_format2}'
        db = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/sys_db.db'
        tbSess = 'sessions'
        # Подготовка параметров для INSERT
        db_proc = SqliteProcessor(db)
        # Вставка полей из текущей строки общего массива данных региона 
        fieldsVals = {
                        'session_id' : self.session_id,
                        'url' : self.url,
                        'name' : sessName,
                        'time' : time_format2,
                        'module' : 'FFX driver'   # Firexox driver
                        }  
        db_proc.insert_row_into_table (tbSess, fieldsVals) 


    def clear_sys_session_table(self):
        """ 
        HTMLSeleniumManager
        Удаление всех записей из таблицы sessions в системной БД sys_db.db
        Category: Сессии
        """
        db = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/sys_db.db'
        tbSession = 'sessions'
        db_proc = SqliteProcessor(db)
        db_proc.delete_from_table_with_where_condition(tbSession, {}) # Удаление без всяких условий, то есть всех записей



    @staticmethod
    def read_sys_session_from_db(sessName ='') :
        """ 
        HTMLSeleniumManager
        Считывание сессии, url и ее параметров из БД
        Таблица обязательно должна иметь поле 'name', в котором хранится уникальное рукодельное имя сессии при ее сохранении
        Category: Сессии
        """      
        db = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/sys_db.db'
        tbSession = 'sessions'        
        db_proc = SqliteProcessor(db)

        # Если параметр sessName - пустой, то считываем последнюю записанную сессию
        if len(sessName) == 0:
            getFields = ['*']
            conds = {}
            ds = db_proc.select_from_table_with_where_condition(tbSession, getFields, conds)

            res = FG.get_inx_and_val_of_row_with_max_val_in_col_of_2dim_list (ds, 0) # Получение индекса ряда, где находится макисмальное значение по колонке 0 (это и есть последний автоинкремент внесенной сессии)
            maxRowinx = res[0]
            resDs = ds[maxRowinx]

        else: # Если задано имя сессии, которую нужно вывести
            getFields = ['*']
            conds = {'ONE':['name','=',sessName]}
            ds = db_proc.select_from_table_with_where_condition(tbSession, getFields, conds)

            resDs = ds[0]
            # ds = db_proc.get_ds_from_cursor(cur)

        return resDs


    @staticmethod
    def save_session_and_url_to_db(db, tbSessions, fieldsVals, uniqueCheckDict):
        """ 
        HTMLSeleniumManager
        Сохранение сессии и URL в БД в таблицу sessions
        Поле 'name' в таблице tbSessions - обязательно к заполнению. Сессия не может не иметь уникального имени
        TODO: ПРи сохранении сессии с именем, которое уже есть в в БД _ предыдущую сессию нужно автоматом переименовать или спросить разрешение удалить <пока удаляем просто>
        Пример : Словарь полей и значений для вставки INSERT
        fieldsVals = {
        'session_id' : '98435jf98j',
        'url' : 'http//...',
        'name' : 'Нейрохирурги СПБ',
        'time' : '23_34_...',
        'descript' : 'Нейрохирурги СПб',
        'module' : 'GoogleManager'  
        }  
        Пример: uniqueCheckDict = {'link': 'http:// ...', 'name' : 'Нейрохирургия'} - множественные ключи со значениямми, которые надо проверить на UBIQUE   
        Category: Сессии   
        """
        sessName = fieldsVals['name']
        # Подготовка параметров для INSERT
        db_proc = SqliteProcessor(db)
        uniqueCheckDict = {'name' : sessName} # Уникальный ключ на проверку по UBIQUE
        boolRes, messageStr = db_proc.if_exist_in_tb_by_multiple_keys_by_dict(tbSessions,uniqueCheckDict) # Проверка на UNIQUE
        if (boolRes) :
            if DEBUG_:
                print("\n" + messageStr + f" уже СУЩЕСТВУЕТ в заданных динамически ключевых полях таблицы {tbSessions} -> Не вносим\n")
                print (f"\nНеобходимо удалить сессию с подобным именем (!!! тогда не будет доступа, если браузер с этой сессией открыт). Либо переименовать сохраняемую сессию")
                # TODO: ПРи сохранении сессии с именем, которое уже есть в в БД _ предыдущую сессию нужно автоматом переименовать или спросить разрешение удалить
                HTMLSeleniumManager.clear_session_in_DB_by_name(db, tbSessions, sessName)
                # Вставка полей из текущей строки общего массива данных региона 
                db_proc.insert_row_into_table (tbSessions, fieldsVals)                 

        else:
            if DEBUG_:
                print ("\n" + messageStr + f"  НЕТ в заданных динамически ключевых полях таблицы {tbSessions} -> Вносим\n")
            # Вставка полей из текущей строки общего массива данных региона 
            db_proc.insert_row_into_table (tbSessions, fieldsVals) 


    @staticmethod
    def clear_session_table(db, tbSession):
        """ 
        HTMLSeleniumManager
        Удаление всех записей из таблицы tbSession
        Category: Сессии
        """
        db_proc = SqliteProcessor(db)
        db_proc.delete_from_table_with_where_condition(tbSession, {}) # Удаление без всяких условий, то есть всех записей




    @staticmethod
    def read_session_from_db_by_name(db, tbSessions, sessName) :
        """ 
        HTMLSeleniumManager
        Считывание сессии, url и ее параметров из БД
        Таблица обязательно должна иметь поле 'name', в котором хранится уникальное рукодельное имя сессии при ее сохранении
        Category: Сессии
        """      
        db_proc = SqliteProcessor(db)

        getFields = ['*']
        conds = {'ONE':['name','=',sessName]}
        ds = db_proc.select_from_table_with_where_condition(tbSessions, getFields, conds)
        # ds = db_proc.get_ds_from_cursor(cur)
        print (f"dsSessRes = {ds}")
        return ds[0]

    
    @staticmethod
    def clear_session_in_DB_by_name(db, tbSessions, sessName):
        """ 
        HTMLSeleniumManager
        Очистка таблицы tbSessions от возможных прошлых сессий с подобным уникальным именем. В таблице сессий не может находиться две сессии с одним и тем же именем
        Category: Сессии
        """

        db_proc = SqliteProcessor(db)
        conds = {'ONE':['name','=',sessName]}
        db_proc.delete_from_table_with_where_condition (tbSessions, conds)





    # def connect_to_remote_browser(self, browsUrl, browsSession):
    #     """Присоединится к броузеру независимо, зная его сессию и url
    #     https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session/70088095#70088095
    #     """
    #     driver = webdriver.Remote(command_executor=browsUrl,desired_capabilities={})
    #     driver.close()   # this prevents the dummy browser
    #     driver.session_id = browsSession     


    @staticmethod
    def attach_to_session(executor_url, session_id):
        """ 
        HTMLSeleniumManager
        Присоединится к открытому браузеру Firefox, зная его session_id и URL
        Пример: brouser_driver = attach_to_session(url, session_id)
        Category: Сессии
        """

        original_execute = WebDriver.execute
        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return original_execute(self, command, params)
        # Patch the function before creating the driver object
        WebDriver.execute = new_command_execute
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.session_id = session_id
        # Replace the patched function with original function
        WebDriver.execute = original_execute
        return driver

# -- End Методы для работы с сессиями браузера Firefox



    def create_hyperlink_formula(self, href):
        """ 
        CALC Formulas: Создание формулы для вставки гиперлинка в ячейку Calc 
        Category: Excel
        """
        hrefF = f'=HYPERLINK("{href}")' 
        return hrefF




    def get_elements_from_tb (self,tb):
        """ 
        считывает элементы из ячеек таблицы в текствовом виде и возвращает массив elements[] 
        Category: Selenium
        """

        trs= tb.find_elements(By.TAG_NAME, "tr")

        # Заголовки
        ths = trs[0].find_elements(By.TAG_NAME, "th")
        titles = []
        for th in ths:
            titles.append(th.text)

        # Данные
        elements = []

        #iterate over the rows
        for tr in trs:
            # row data set to 0 each time in list
            row = []
            #iterate over the columns
            tds = tr.find_elements(By.TAG_NAME, "td") 
            for td in tds:
                # getting text from the ith row and jth column
                row.append(td.text)
            #finally store and print the list in console
            elements.append(row)

        return elements

# Методы обработки окон и фолдеров браузера

    def register_brWindow(self):
        """ 
        Регестрирует открытое окно в браузере в лист учета окон self.brWindows.
        Возвращает индекс нового зарегестрированного окна в списке учета
        Category: Selenium
        """
        window = self.driver.window_handles[-1]
        self.brWindows.append(window)
        return len(self.brWindows) # Возвращает индекс нового зарегестрированного окна в списке учета


    def unregister_brWindow (self, ordInx=-1):
        """ 
        Снимает с регистрации из листа учета окон self.brWindows. По умолчанию удаляет последний 
        Category: Selenium
        """
        del self.brWindows[ordInx]

    
    def get_last_wind_handle (self):
        """
        Возвращает handle последнего открытого окна
        Category: Selenium
        """
        windowLast = self.driver.window_handles[-1]
        return windowLast


    def get_sys_inx_of_last_open_wind_handle (self):
        """
        Возвращает системный индекс последнего открытого окна (на уровне системы)
        Category: Selenium
        """
        lastHInx = len(self.driver.window_handles) - 1 # Системный индекс последнего открытого окна в браузере
        return lastHInx


    def activate_brWindow(self,ordInx = -1):
        """ 
        Активация (передача управление окном текущему драйверу!!!, а не визуальная активация видимости окна)
        по порядковому номеру учтенных окон в браузере. По умолчанию активируется последнее зарегестрированное окно 
        Category: Selenium
        """
        wHandler = self.brWindows[ordInx]
        self.driver.switch_to.window(wHandler)



    def close_brWindow(self, ordInx = -1):
        """ 
        Закрывает учтенное окно с порядковым номеров в брацзере. По умолчанию закрывает последнее открывшееся окно 
        Category: Selenium
        """
        self.activate_brWindow(ordInx)
        self.driver.close()
        self.unregister_brWindow (ordInx) # удаляет хендлер из списка учета окон


    def get_active_url(self):
        """
        Получает URL активной страницы браузера
        Category: Selenium
        """
        url = self.driver.current_url
        return url


    def get_all_browser_pages_urls(self):
        """
        Считывает в список все URLs страниц, открытых в браузере
        Category: Selenium
        """
        windHandles = self.driver.window_handles
        dsURL = []
        for wHandler in windHandles: # цикл по хендлерам окон браузера
            self.driver.switch_to.window(wHandler)
            sleep(1)
            url = self.get_active_url() # считывает url активной страницы браузера
            dsURL.append(url)   
        return dsURL


    def get_all_browser_pages_urls_and_titles(self):
        """
        Считывает в список все URLs страниц, открытых в браузере
        Category: Selenium
        """
        windHandles = self.driver.window_handles
        dsURLTitle = []
        for wHandler in windHandles: # цикл по хендлерам окон браузера
            self.driver.switch_to.window(wHandler)
            sleep(1)
            url = self.get_active_url() # считывает url активной страницы браузера
            title = self.get_title_of_page()
            dsURLTitle.append([url,title])   
        return dsURLTitle    



    def get_br_winds_handlers(self):
        """
        Получить список хендлов открытых окон в браузере
        Category: Selenium
        """
        wHandlers = self.driver.window_handles
        return wHandlers



    def switch_to_br_wind_by_handler(self, wHandler):
        """
        Переключение на страницу по значению хендла окна
        Category: Selenium
        """
        self.driver.switch_to.window(wHandler)


# END Методы обработки окон и фолдеров браузера

    # -- Картинки
    
    @staticmethod
    def load_img_from_sel_img_static (imgSelObj, absPathToSave, imgNameToSave):
        """
        HTMLSeleniumManager
        загрузить картинку из обьекта Selenium тэга  <img> imgSelObj в директорий , заданный абсолютным путем absPathToSave и именем нового сохраняемого файла-картинки imgNameToSave
        """
        if absPathToSave[-1] != '/':
            absPathToSave = absPathToSave + '/'
        # Полный путь с именем нового файла с картинкой
        pathFull = absPathToSave + imgNameToSave 
        src = imgSelObj.get_attribute('src')
        urllib.request.urlretrieve(src, pathFull)
        
        return pathFull
    
    
    
    @staticmethod
    def get_selenium_img_extention (selImg):
        """ 
        HTMLSeleniumManager
        Получить расширение картинки из селениум-обьекта картинки
        """
        
        imgExt = selImg.get_attribute('src').split('.')[-1]
        return imgExt
    
    
    
    # -- END Картинки


    # Проверка , есть ли в обьекте метод pass_barriers
    # https://stackoverflow.com/questions/7580532/how-to-check-whether-a-method-exists-in-python  - Проверка существования метода в обьекте
    def has_method(self, o, name):
        """
        Проверка, есть ли в классе обьекта метод pass_barriers прохождения барьеров 
        Category: Аналитические методы
        """
        return callable(getattr(o, name, None)) # ??? Возможно надо один параметр убрать, если  self и является обьектом, в котором надо проверить наичие метода


    def open_link(self, passBarrier = True) :    
        """ 
        Открывает ссылку в браузере с анализом есть ли заданный барьер
        После открытия ссылки запусает метод pass_barriers дочернего класса. То есть метод с  этим названием должен быть (при необходимости)  определен и реализован в каждом дочернем классе так, как нужно
        passBarrier - флаг прохождения барьеров по умолчанию True (проходить)
        Category: Selenium
        """
        # self.driver = webdriver.Firefox()
        # self.dr_link = link
        self.driver.get(self.dr_link) # переход на ссылку в браузере
        sleep(2)
        if passBarrier: # Если флаг прохождения барьеров = True # TODO: Сделать два условия в одном if через AND if self.has_method(self, 'pass_barriers')
            if self.has_method(self, 'pass_barriers') : # Проверка , есть ли в обьекте метод pass_barriers  # CHANGED ??? Два self в параметрах ???
                self.pass_barriers()     # Запуск метода прохождения возможных барьеров, если он есть в классе обьекта  self
                sleep(1)
                
        self.register_brWindow() # CHANGED ???? Не понятно зачем передается параметр self


    def open_link_with_stop_load(self, passBarrier = True):
        """ 
        Открывает ссылку в браузере с принудительной остановкой загрузки по истечению заданного времени
        Используется для страниц, которые долго загружаются из-за подгрузоу AJAX и пр.
        После открытия ссылки запусает метод pass_barriers дочернего класса. То есть метод с  этим названием должен быть (при необходимости)  определен и реализован в каждом дочернем классе так, как нужно
        passBarrier - флаг прохождения барьеров по умолчанию True (проходить)
        Category: Selenium
        """
        timeWait = TIME_WAIGHT_
        try:
            self.driver.set_page_load_timeout(timeWait)
            self.driver.get(self.dr_link)
            sleep(3)
        except Exception: # ловит и обрабатывает ошибку timeout
                print (f'time is out: {timeWait} c')
                
        if passBarrier: # Если флаг прохождения барьеров = True # TODO: Сделать два условия в одном if через AND if self.has_method(self, 'pass_barriers')
            if self.has_method(self, 'pass_barriers') : # Проверка , есть ли в обьекте метод pass_barriers  # CHANGED ??? Два self в параметрах ???
                self.pass_barriers()     # Запуск метода прохождения возможных барьеров, если он есть в классе обьекта  self
                sleep(1)

        self.register_brWindow()



    def open_new_link(self,link) :    
        """ 
        Открывает ссылку в браузере без анализа барьеров
        Category: Selenium
        """
        # self.driver = webdriver.Firefox()
        self.dr_link = link
        self.driver.get(self.dr_link) # переход на ссылку в браузере
        sleep(3)
        winHandle = self.register_brWindow()
        return winHandle
        
        
        
        
        
    def open_links_from_ds(self, ds, timeWait):
        """
        Открыть в браузере последовательно ссылки в новых фодерах из массива (список или прочий массив)
        timeWait - максимальное ограничение ожидания времени загрузки нового окна со ссылкой, до следующего открытия следующего окна в сек
        Category: Selenium
        """   
        i = 0 # счетчик
        for link in ds: # Цикл открытия ссылок по массиву
            if i > 0: # Для первой загрузки не открывает фолдера, так как фолдер уже есть при запуске драйвера Firefox
                self.driver.execute_script('window.open('');')
            lastHInx= self.get_sys_inx_of_last_open_wind_handle () # системный индекс последнего открытого окна в браузере
            self.driver.switch_to.window(self.driver.window_handles[lastHInx])   
            self.dr_link =  link        
            self.open_link_with_stop_load() # Загрузка окна с ограничением времени загрузки
            i += 1




    def open_link_in_new_folder(self, href):
        """
        Открыть ссылку в новом фолдере браузера
        RET: resHndls - список хендла начальной страницы и новой открытой страницы
        Category: Selenium
        """
        pH = self.driver.current_window_handle # Хендл текущей открытой страницы

        self.driver.execute_script('window.open('');')
        newH = self.driver.window_handles[-1] # Хендл нового открытого фолдера страницы

        self.driver.switch_to.window(newH) 
        self.driver.get(href) # переход на ссылку в браузере
        sleep(2)
        resHndls = [pH, newH] # список хендла начальной страницы и новой открытой страницы
        return resHndls


        

    def get_whole_html_and_autosave (self,ext):
        """ 
        Автосохранение кода HTML в файл в текущую диреторию проекта 
        Category: Selenium
        """
        
        whtml = self.driver.page_source # Получить код файла (текст sourcr code html-страницы)
        dt = datetime.datetime.now()
        t_string = dt.strftime("%H_%M_%S")
        randm = random.randint(1,10000000)
        fName = f"auto_{randm}_{t_string}.{ext}"

        currPath = os.path.dirname(os.path.abspath(__file__))
        
        print(f"PR_NC_149 --> SYS LOG: Директорий автосохранения кода HTML-страницы = {currPath}")
        
        fullPath = f"{currPath}/{fName}" # абсолютный путь с названием файла

        curr_path = FG.save_to_file(fullPath,whtml)
        sleep(2)
        absolute_path = f"{curr_path}/{fName}" # абсолютный путь с названием файла
        ftp = f"file://{curr_path}/{fName}"  # ftp адрес сохраненного html файла
        return absolute_path, ftp




    def get_whole_html_and_autosave_v2 (self, dirToSave, ext):
        """ 
        Автосохранение кода HTML в файл в текущую диреторию проекта 
        ИЗМ: 1. Добавлена возможность передавть параметр проектного директория, куда будет сохранятся файл авто-сохранения с кодом. 
        Этот фал должен быть внутри проекта
        
        Category: Selenium
        """
        
        whtml = self.driver.page_source # Получить код файла (текст sourcr code html-страницы)
        dt = datetime.datetime.now()
        t_string = dt.strftime("%H_%M_%S")
        randm = random.randint(1,10000000)
        fName = f"auto_{randm}_{t_string}.{ext}"

        # currPath = os.path.dirname(os.path.abspath(__file__))
        
        print(f"PR_NC_149 --> SYS LOG: Директорий автосохранения кода HTML-страницы = {dirToSave}")
        
        fullPath = f"{dirToSave}/{fName}" # абсолютный путь с названием файла
        
        print(f"PR_NC_152 --> fullPath = {fullPath}")

        # Создать файл с заданынм именем в пути и сохранить в нем код HTML-страницы
        FG.create_and_save_to_file_v2(fullPath,whtml)
        sleep(2)
        # absolute_path = f"{curr_path}/{fName}" # абсолютный путь с названием файла
        ftp = f"file://{fullPath}"  # ftp адрес сохраненного html файла
        
        print(f"PR_NC_151 --> ftp = {ftp}")
        
        return fullPath, ftp





    def maximize_window(self, pause=3):
        """ 
        Максимизирует окно брацзера и ожидает время pause 
        Category: Selenium
        """
        self.driver.maximize_window()
        sleep(pause)


    @abc.abstractmethod
    def switch_between_folders(self):
        """ 
        Помогает управлять открытыми фолдерами 
        Category: Операции с браузером
        """
        return 'Should never reach here'

        
## -- Функции анализа контента OBSOLTETED . Использовать SiteParserManager

    def get_title_of_page(self):
        """
        ODSOLETED. Использовать SiteParserManager.get_title_of_active_page
        Получает титульное название страницы
        Category: Selenium
        """
        pgTitle = self.driver.title
        return pgTitle


## -- END Функции анализа контента 



# -- ВСПОМОГАТЕЛЬЫНЕ ФУНКЦИИ


    @staticmethod
    def download_file_from_site_page(downloadDir = '/home/ak/Downloads', timeSleep = 1, filePattern = '\..*$'):
        """ 
        ЗАГОТОВКА.  копия из класса MoexManager . Загрузка файла с сайта.
        # TODO: Сделать родительскую функцию загрузки файла Download с сайта через Selenium/ Продумать параметры. Может передавать обьект селениума кнопку при нажатии на которую идет 
        загрузка файла. или передавать функцию нахождения ссылки на странице для загрузки файла
        Скаичвает эксел файл с данными по банкротным облигациям и компаниям со страницы https://www.moex.com/ru/listing/emidocs.aspx?type=4&pageNumber=1 MOEX
        в системную папку Downloads
        downloadDir - Директория в которую загружается файл. По умолчанию системная папка '/home/ak/Downloads'
        timeSleep - время задержки для полной загрузки файла
        rePattern = '\..*$' - патерн для того, чтобы на выходе при проверке был файл того формата , которые подразумевается при скачивании. А не какой-нибудь другой из заданнйо диретории
                    Если такого формата не найдено выдает -1
        RET: Возвращает название последнего сгруженного файла в заданной диретории downloadDir (соотвтетсвенно выдает название файла, загруженного этой функцией в данный момент времени ее использования)
        Category: Прикладные интерактивные Selenium
        """
        cLink = 'https://www.moex.com/ru/listing/emidocs.aspx?type=4&pageNumber=1'
        moexMngr = MoexManager().ini_from_link(cLink)    

        aFileDownloadRes = moexMngr._sel_srch_by_txt_in_DOM_new('Скачать данные в формате Excel') # Ссылка на скачиваемый файл
        if aFileDownloadRes[0] == 1: # Если найдена единственная ссылка на файл
            aFileDownloadRes[1].get_attribute('href')

            aFileDownloadRes[1].click()
            sleep(timeSleep)

            # Название загруженного файла 
            lastFilename = FilesManager.get_last_loaded_file_name_from_dir (downloadDir)

            # Проверка найденного последнего сгруженного файла на соответствие формату подразумеваемого файла при загрузке из известного сайта и с возможной известным 
            # форматом сгружаемого файла
            # regExp = r'default\.xlsx$' # для проверки формата файла, что бы предотваратить удалени и переименование последнего загруженного файла, не целевого
            ifComply = ReManager.regex_filter (lastFilename, filePattern) # Флаг соответствия файла искомому загруженному последнему

            if ifComply: # Если файл соотвтетсвует по формату искомому
                print(f"Файл соответствует по формату искомому")
                print(f"Файл {lastFilename} заружен по умолчанию в директорию  {downloadDir} <MoexManager.download_bancropcy_bonds_file_moex>")
                return lastFilename
                
            else: # Если файл не соотвтетсвует по формату искомому
                msg = "Файл не соответствует заданному искомому формату, поэтому игнорируется"
                if DEBUG_:
                    print (f"Файл не соответствует заданному искомому формату, поэтому игнорируется")
                res = [-1, msg]
                return res

        else:
            msg = "Найдена неоднозначная ссылка на загрузочный файл"
            print(f"Найдена неоднозначная ссылка на загрузочный файл : Проверить <MoexManager.download_bancropcy_bonds_file_moex>")
            res = [-1, msg]
            return res



# END ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ







    ### --- SELENIUM SEARCH FUNCS TODO: Все функции OBSOLETED и реализованы в классе SeleniumFormulas по новому подходу-------------

    def _sel_srch_by_txt_in_DOM (self,  srchStr):
        """ 
        DEPRECIATED. (New: _sel_srch_by_txt_in_DOM_new) Поиск по фрагменту текста во всем документе 
        Поиск по фрагмету текста в селениум-обьекте
        Category: Selenium
        """

        objsFound = self.driver.find_elements(By.XPATH,f".//*[contains(text(),'{srchStr}')]")
        if len(objsFound) > 0:
            obj = self.driver.find_element(By.XPATH,f".//*[contains(text(),'{srchStr}')]")
        else:
            print (f" В обьекте не найдены суб-обьекты , содержащие фрагмент: {srchStr}")
            obj = None
        return obj    


    def _sel_srch_by_txt_in_DOM_new (self,  srchStr):
        """ 
        Поиск по фрагменту текста во всем документе 
        Поиск по фрагмету текста в селениум-обьекте
        Category: Selenium
        """
        objs= self.driver.find_elements(By.XPATH,f".//*[contains(text(),'{srchStr}')]")
        n = len(objs)
        if n == 1:
            obj = objs[0]
            objs = None
        elif n > 1:
            obj = objs[0]
            # objs = objs               
        else:
            print (f" В обьекте не найдены суб-обьекты , содержащие фрагмент: {srchStr}")
            obj = None
            objs = None
        return [n, obj, objs]



    def _sel_srch_by_txt_in_obj (self,selObj, srchStr):
        """ 
        Поиск по фрагмету текста в селениум-обьекте 
        Category: Selenium
        """
        # selSrch = f".//*[contains(text(),'{srchStr}')]"
        objs = selObj.find_elements(By.XPATH, f".//*[contains(text(),'{srchStr}')]")
        n = len(objs)
        if n == 1:
            obj = objs[0]
            objs = None
        elif n > 1:
            obj = objs[0]
            # objs = objs              
        else:
            print (f" В обьекте не найдены суб-обьекты , содержащие фрагмент: {srchStr}")
            obj = None
            objs = None
        return [n, obj, objs]


    def _sel_srch_by_cls_in_DOM (self,  clsName):
        """ 
        Поиск по фрагменту (первому?) в названии класса во всем документе 
        Category: Selenium
        """
        # selSrchPar = f'{clsName}'
        objs = self.driver.find_elements(By.CLASS_NAME, f'{clsName}')
        n = len(objs)
        if n == 1:
            obj = objs[0]
            objs = None
        elif n > 1:
            obj = objs[0]
            # objs = objs            
        else:
            print (f" В документе не найдены суб-обьекты с классом: {clsName}")
            obj = None    
            objs = None                
        return [n, obj, objs]


    def _sel_srch_by_cls_in_obj (self,selObj, clsName):
        """ 
        Поиск по классу суб-обьектов  в селениум-обьекте 
        Category: Selenium
        """
        objs = selObj.find_elements(By.CLASS_NAME,f'{clsName}')
        n = len(objs)
        if n == 1:
            obj = selObj.find_element(By.CLASS_NAME,f'{clsName}')
            objs = None
        elif n > 1:
            obj = objs[0]
            # objs = objs
        else:
            print (f" В обьекте не найдены суб-обьекты , содержащие класс: {clsName}")
            objs = None
            obj = None
        return [n, obj, objs]


    def _sel_find_next_obj_of_equal_lv (self, selObj, objTag) :
        """  
        Найти следующий обьект в ряду обьектов с одинакового уровня c с тэгом objTag 
        Category: Selenium
        """   
        objs = selObj.find_elements(By.XPATH, f".//following-sibling::{objTag}" )
        n = len(objs)
        if n == 1:
            obj = objs[0] # следующий элемент одного уровня  
            objs = None
        elif n > 1:
            obj = objs[0]
            # objs = objs
        else:
            print (f"Не найден следующий обьект равного уровня с тэгом {objTag}")
            objs = None            
            obj = None
        return [n, obj, objs]


        ## -- GENERAL SEL SEARCH FUNC 
    def __sel_general_srch_func(self,  byParams):
        """ 
        STATE_OF_ART. общая функция поиска по принципам селениум
        ByParams['selFuncName'] - символическое название метода поиска в селениум для операции switch ... case 
        ByParams - конкретные параметры для составления строки поиска селениум
        Category: Selenium
        """

        for case in Switch(byParams['selFuncName']):
            
            if case('_sel_find_next_obj_of_equal_lv'):
                # Params selObj, objTag
                # ByParams = {'selObj': selObj,'objTag' : objTag}
                objs = byParams['selObj'].find_elements(By.XPATH, f".//following-sibling::{byParams['objTag']}" )
                notFoundStr = f"Не найден следующий обьект равного уровня с тэгом {byParams['objTag']}" # Строка для печати в случае не нахождения обьектов
                break

            if case('2'):
                pass
            if case('3'): 
                print('Число от 1 до 3')
                break
            if case('4'): 
                print('Число 4')
            if case(): # default
                print('Другое число')
                break        

        n = len(objs)
        if n == 1:
            obj = objs[0] # следующий элемент одного уровня  
            objs = None
        elif n > 1:
            obj = objs[0]
            # objs = objs
        else: # Если не найдены обьекты
            print (notFoundStr) # Вывод строки ненахождения обьекта , индивидуальной для каждой функции - сел
            objs = None            
            obj = None
        return [n, obj, objs]


    def _sel_find_next_obj_of_equal_lv_for_genF (self, selObj , objTag) :
        """ 
        Найти равные  обьекту selObj обьекты с тэегом objTag с задаваемым 
        Функция для использования с общей функцией селениум-поиска _sel_general_srch_func
        Category: Selenium
        """   
        byParams = { # Поиск обьектов с тэгом objTag, находящихся на одном уровне со входящим обьектом selObj
            'selFuncName' : '_sel_find_next_obj_of_equal_lv',
            'selObj' : selObj,
            'objTag' : objTag
        }
        res = self.__sel_general_srch_func(byParams)
        return res




### --- END SELENIUM SEARCH FUNCS -------------


### UNIVERSAL INTERACTIVE PARAMENTR AND OTHER FUNC !!!-------------
### Не удалять !!!! Эта функция - обработчик ЦИКЛА из CHECKO

    @staticmethod    
    def save_comps_links_from_ds_set1_to_tb_comps_descr_PF (dsInput, args = {}):
        """
        Универсальная функция (УФ) для интерактивного получения ссылок страниц компаний из различных источников с дальнейшей обработкой результатов и внесения в БД
        Функция -параметр для обработки выходных данных в формате set1 атомарной функции pif_comp_link_by_inn_PF 
        которые обраховались в результате обработки эпохи в функции принудительного цикла WWWInteractiveUniversal.universal_get_interactive_data_by_epoch_using_universal_while_PF
        в виде списка списков (двумерного массива выходных данных после интерактивного поиска)
        Задается в словаре outputFuncDic для функции принудительного цикла (ФПЦ) universal_get_interactive_data_by_epoch_using_universal_while_PF
        dsLinks - массив найденных в цикле принудительного интерактивного поиска ссылок в формате pif_comp_link_by_inn_PF должен быть в таком формате [[inn1, link1],[inn2, link2]...]

        fieldCompsDescr - Название поля в таблице comps_descr, в который будут всталятся данные при обработке массива входного массива с ссылками
        fieldGlobalA - название поля в таблице global_A, в который будет ставится маркер 'INSERTED', фиксирующий то, что для данной ИНН компании запись ссылки в таблице comps_descr выполнена
        Category: Прикладные интерактивные Selenium
        """
        print("ФНКЦИЯ ОБРАБОТКИ ВЫХОДА: WWWInteractiveUniversal.save_comps_links_from_ds_set1_to_tb_comps_descr_PF")
        db = DB_BONDS_
        db_proc = SqliteProcessor(db)   
        db_proc
        tbCompsDescr = 'comps_descr'  

        # Расшифровка параметров
        cdField = args['fieldInCompsDescr']
        gaField = args['fieldInGlobalA']
        # A. Вставка данных (в массиве по эпохам) по checko.ru в поле descr1 таблицы 
        # pars UPDATE
        fieldsInxAccordList = {1: cdField}
        unqInxColVal = [0,'inn']  

        # for epochDsSet1 in dsInput: # Обработка эпох входного массива dsSet1, так как он был определен 3х мерным, значит это - список результатов эпох

        dsSet1Str = FG.convert_two_dim_list_with_dicts_to_same_list_with_str(dsInput, 1) # преобразование данных в виде dictionary в формат JSON-string
        sqlUpd = db_proc.update_rows_from_ds( tbCompsDescr, dsSet1Str, fieldsInxAccordList, unqInxColVal) # Втавка в поле descr1 таблицы  comps_descr
        # Апргрейд полей в таблице global_A , для checko - это поле d1, так как ссылка на компанию для checko находится в link1 , а описание в descr1, таблицы comps_descr
        # Апгред по ключевым полям inn, простановка значения = 'INSERTED'. Говорит о том, что в поле descr1 таблицы comps_descr вставлены данные с checko по соответствующи ИНН
        # Получение списка ИНН, по которым прошли вставки описаний в поле descr1 таблицы comps_descr
        innInsertedToCompsDecr = FG.convert_list_of_list_to_one_dim_list (dsSet1Str, 0) # одномерный простой список тех ИНН, по которым прошла вставка описания копании в таблице comps_descr по сайту checko
        # print (innInsertedToCompsDecr)
        # Pars:
        # update_where_in_simple_sql (tb, updFields,  updVals, whereConds)
        tbName = 'global_A'
        markerField = gaField
        markerStr = 'INSERTED'
        print (f"Список ИНН по которым надо прописать маркер  в global_A по полю {cdField} : {innInsertedToCompsDecr}  ")
        HTMLSeleniumManager.update_mark_to_global_table (innInsertedToCompsDecr, tbName, markerField, markerStr) # Вставка маркера 





    @staticmethod  
    def update_mark_to_global_table (dsIN, tbName, markerField, markerStr):
        """ 
        Вспомогательная универсальная функция, вставляющий (update) маркер в таблицу глобальных переменных или глобальную таблицу
        dsIN - входной массив ключей, по которым будет проставлен маркер markerStr в поле markerField таблицы tbName
        markerStr - стринговый маркер
        markerField - поле для вставки маркера в таблице tbName
        Category: Прикладные интерактивные Selenium
        """
        db = DB_BONDS_
        db_proc = SqliteProcessor(db)
        updFields = [markerField]
        updVals = [markerStr]
        # keyInField = ['x_str']
        # inDS = 'SELECT FROM * '
        whereConds = {'ONE': ['x_str','IN', dsIN]}
        sql = db_proc.update_where_in_simple_exec (tbName, updFields,  updVals, whereConds)
        # print (sql)  


    


### END UNIVERSAL INTERACTIVE PARAMENTR AND OTHER FUNC !!!-------------








if __name__ == "__main__":
    pass

    

    
    # # ПРИМЕР: Запуска драйыера селениума для Firefox

    # dr = HTMLSeleniumManager.ini_from_iside()
    # dr.dr_link = "https://www.google.com/webhp?hl=ru&sa=X&ved=0ahUKEwiW_vj2vs7-AhUB_SoKHReoCDwQPAgI"
    # dr.open_link()
    # # import selenium
    # # print (selenium.__version__)








