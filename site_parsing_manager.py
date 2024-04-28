
from bonds.html_pars_manager import HTMLSeleniumManager
from selenium.webdriver.common.by import By

class SiteParserManager(HTMLSeleniumManager):
    """ Класс для парсинга контента сайтов
    Библиотеки: phonenumbers  -  https://rukovodstvo.net/posts/id_575/, https://pypi.org/project/phonenumbers/4.8b1/
    # TODO: Этот модуль предназначен для парсинга сайтов. А родительский - для подсоединения к драйверу и прочими тех.методами. Но в названии есть парсинг, что не должно соответствовать. Потом постепенно изменить структуру

     """

    # Конструктор
    def __init__(self):
        pass


    # Конструктор класа по ссылке или просто по системному драйверу внутри системы
    @classmethod
    def ini_from_iside(cls, openLinkFlag = True):
        """инициализация драйвера изнутри программы через драйвер Firefox"""
        HTMLSeleniumManager.ini_from_iside()  # Вызов родительского конструктора
        if openLinkFlag: # загрузить дефолтную ссылку, если флаг-параметр openLinkFlag = True (по умолчанию True)
            cls.dr_link = 'https://www.google.com' # деволтная ссылка
            cls.open_link()

    # Конструктор класcа по драйверу, полученному вне системы
    @classmethod
    def ini_from_remote(cls, ffxDriver):
        """Инициализация обьекта класса по драйверу, полученному извне системы"""
        HTMLSeleniumManager.ini_from_remote(ffxDriver)  # Вызов родительского конструктора



    
## -- Функции анализа контента 

    def get_title_of_active_page(self):
        """Получает титульное название страницы
        Этот метод есть в родительском классе. Его используют несколько алгоритмолв , но он устарел там
        """
        pgTitle = self.driver.title
        return pgTitle

    def get_html_source_of_active_page(self):
        """Получить html-код страницы"""
        htmlSrc = self.driver.page_source
        return htmlSrc


    def get_whole_text_of_active_page(self):
        """Получить текстовое наполнение активной страницы"""
        pgText = self.driver.find_element(By.XPATH, "/html/body").text
        return pgText


    def get_URL_of_active_page (self):
        """получить URL активнйо страницы"""
        pgUrl = self.driver.current_url
        return pgUrl


## -- END Функции анализа контента 


# Прикладные и специфические функции

    # Для работы с библиотекой phonenumbers

    def get_phone_from_res_match_of_phonenumbers(self, match):
        """Выделить и получить чисто номер из результатов парсинга библиотеки phonenumbers
        match - тип данных от phonenumbers, в котором хранится номер телефона
        """
        strMatch = str(match) # перевод типа match в стринг
        phnMatchlineParts = strMatch.split('+') # разделяем по символу '+'
        phoneNmb = phnMatchlineParts[-1] # Последняя является номером
        return phoneNmb




    



    # END Для работы с библиотекой phonenumbers








# END Прикладные и специфические функции











































if __name__ == '__main__':
    pass



