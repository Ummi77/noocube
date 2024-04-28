
from project_tlh.projr.classes.search_manager_db import SearchManagerDB
import bonds.funcs_general as FG
from bonds.switch import Switch
from bonds.sqlite_pandas_processor import SqlitePandasProcessor
from project_bonds_html.projr.classes.paginator_data_frame import PaginatorWithDataFrame
from project_bonds_html.projr.classes.dsource_cube import DSourceCube
from project_bonds_html.projr.settings import *


# TODO: Продумать систему наследования этого класса и родителей. Так как в программирвоании с БД и пандой нужны не только конечные обьекты дял вывода таблиц на конечных ресурсах,
#  но и подобные обьекты вообще, до вывода на конечный ресурс
# 
class DSearchCube (DSourceCube):
    """Класс для организации поиска по источнику данных dsObj
    """

    def __init__(self, dbName, dataSrc, **kwargs):

        DSourceCube.__init__(self, dbName, dataSrc, **kwargs)
        
        self.kwargs = kwargs

        # Дефолтная установка собственных переменных, тех, которых необходимо устанавливать по умолчанию:



        # Параметры с сервера HTML
        self.request = None # Приходящая переменная  с параметрами от HTML-сервера 

        # переменные для поиска
        self.srchStr = '' # Поисковая строка
        self.srchInterpretor = '' # Тип интерпретатора поисковой строки (могут быть FTS5 , local и regex)

        self.set_cls_vars_from_kwargs_dsearchcube_ () # Настройка собственных переменных, которые соотвтетсвуют входным именнованным параметрам (именно этого DSearchCube класса)

        # Если установлены собственные переменные поиска при инициализации (если передается параметры поиска srchParams в **kwargs), то поиск осуществляется уже в конструкторе
        if "srchParams" in self.kwargs :
            self.srchParams = self.kwargs['srchParams'] 
            # self.ftsInterpretor = self.kwargs['ftsInterpretor']
            print(f"@#R%RGTT Параметры поиска переданы при создании обьекта класса DSearchCube / DSearchCube.__init__ <dsearch_cube.py>")
            print(f"@#R%RGTT self.srchStr = {self.srchStr}")
            print(f"@#R%RGTT self.srchInterpretor = {self.srchInterpretor}") 

            # Осуществить поиск
            self.search()  

        # Запуск сортировки в этом конструкторе тоже по задаваемым в self.sortCols  колонкам , если флаг сортировки self.sortFlag = True
        # Иметь ввиду, что поиск перегружает self.outputDf, который получается в родительском классе. И даже, если там происходит сортировка, это сортировка над старым self.outputDf 
        # и не имеет значения для self.outputDf после получения результатов поиска в self.outputDf в этом классе. И значит фрем нужно сортировать заново
        if self.sortFlag:
            self.sort()


    def set_search_infor(self, srchParams):
        """
        Установка поисковых атрибутов для осуществления поиска
        Category: Поиск
        """
        self.srchParams = srchParams
        # Расшифровка и присвоение параметров поиска, которые сами хранятся в параметре-словаре self.srchParams 
        # @@@ Настройка сортировки по колонкам и их порядку, задаваемые в словаре 
        if "srchStr" in self.srchParams :
            self.srchStr = self.srchParams['srchStr'] 
        else:
            self.srchStr = ''

        # Расшифровка и присвоение параметров поиска, которые сами хранятся в параметре-словаре self.srchParams 
        # @@@ Тип поиска или интерпретатора поискового выражения
        if "srchInterpretor" in self.srchParams :
            self.srchInterpretor = self.srchParams['srchInterpretor'] 
        else:
            self.srchInterpretor = ''



    def set_cls_vars_from_kwargs_dsearchcube_ (self):
        """
        установка собственных переменных в зависимости от переданных переметров **kwargs с соответствующими ключами , предназаначенных, кроме всего, для настройки собственных
        соотвтетсвующих прееменных
        Category: Вспомогательные
        """


        # переменная инициализации
        # @@@ Выводимые поля при полнотекстовом запросе SQL
        if "getFields" in self.kwargs :
            self.getFields = self.kwargs['getFields'] 


        ## ПЕРЕМЕННЫЕ ПОИСКА:
        # @@@  self.srchParams - Параметры поиска, расшифровывающиеся и присваемые ниже
        if "srchParams" in self.kwargs :
            self.srchParams = self.kwargs['srchParams'] 
            print(f"WE#$@$#@RRRR self.srchParams = {self.srchParams}")

            # Расшифровка и присвоение параметров поиска, которые сами хранятся в параметре-словаре self.srchParams 
            # @@@ Настройка сортировки по колонкам и их порядку, задаваемые в словаре 
            if "srchStr" in self.srchParams :
                self.srchStr = self.srchParams['srchStr'] 
                print(f"WE#$@$#@RRRR self.srchStr = {self.srchStr}")
            else:
                self.srchStr = ''

            # Расшифровка и присвоение параметров поиска, которые сами хранятся в параметре-словаре self.srchParams 
            # @@@ Тип поиска или интерпретатора поискового выражения
            if "srchInterpretor" in self.srchParams :
                self.srchInterpretor = self.srchParams['srchInterpretor'] 
                print(f"WE#$@$#@RRRR self.srchInterpretor = {self.srchInterpretor}")
            else:
                self.srchInterpretor = ''

        else:
            self.sortParams = {}





    def search(self):
        """
        Осуществить поиск
        Category: Поиск
        """

        print(f"СТАРТ ПОИСКА / DSearchCube.search <dsearch_cube.py>")

        # Переключатель в зависимости от маркера интерпретатора
        for case in Switch(self.srchInterpretor):

            if case('FTS'): 
                print (f"Interpetator : FTS")
                self.search_with_FTS_() # Полнотекстовый поиск по заданными параметрами поиска
                break
            
            if case('regex'): 
                pass
                break

            if case('local'): 
                print('Число от 1 до 3')
                pass
                break

            if case('usualDB'): 
                pass
                break

            if case(): # default
                print('Не найдено')
                break





    ## Внутренние служебные методы класса




    def create_fts_table_(self):
        """ЗАГТОВКА
        Создать виртуальную таблицу для данного источника данных
        Category: Заготовки
        """

        # # Считать данные из таблицы comps_descr (БД: bonds) в фрейм
        # db_bonds_proc = SqlitePandasProcessor(DB_BONDS_) # Процессор для БД bonds
        # # Получить SQL запрос на создание виртуальной FTS таблицы по прообразу обычной таблицы
        # virtTbName = 'comps_descr_fts' # название новой виртуальной таблицы
        # baseTabl = TB_COMPS_DESCR_ # Название базовой таблицы
        # virtTbSQLCreate = db_bonds_proc.get_fts_virt_table_create_sql_ram(baseTabl, virtTbName)
        # # Создать виртуальную таблицу virtTbName в БД с использованием технологии FTS5
        # db_bonds_proc.execute_sql(virtTbSQLCreate)




    def fill_fts_table_(self):
        """ЗАГТОВКА
        Cкопировать данные из контентной табл comps_descr в виртуальную таблицу comps_descr_fts для FULНАстройка списка колонок к выводу на странице L TEXT SEARCH с предварительным очищение виртуальной таблицы
        Category: Заготовки
        """
        # db_bonds_proc = SqlitePandasProcessor(DB_BONDS_) # Процессор для БД bonds
        # virtTbName = 'comps_descr_fts'
        # # Создать выиртуальную таблицу и заполнить ее данными из базовой таблицы 
        # baseTbName = 'comps_descr'
        # db_bonds_proc.create_and_fill_virt_table_ram( baseTbName, virtTbName)






    def search_with_FTS_(self):
        """
        Полнотекстовый поиск по источнику данных
        Может проводится по разному для разных первичных источников данных
        Первичные данные - это то, что подается на вход при построении обьекта dsObj класса DSourceCube (который в свою очередь является входным параметром для этого класса) 
        Если первичный  источник данных - название таблицы , то для этой таблицы возможно уже существует дочерняя    FTS-таблица. Либо ее нужно создать независимо
        (предпочтительно создать независимую, а не связанную с таблицей. Иначе нужны триггеры обновления и пр. и так как зависимоая давала ошибки )
        Если первичным источником данных являются все прочие варианты, то тогда независисмая FTS-таблица на основе фрейма с этими данными должна быть создана и наполнена
        Далее по вышеуказанной FTS -  таблице осуществляется полнотекстовый поиск FTS5 (пока проработано только для БД sqlite)
        Category: Поиск
        """
        print(f"Full Text Search / DSearchCube.search_with_FTS_ <dsearch_cube.py>")
        srchMngrDB = SearchManagerDB(self.dbname) # Поисковый помощник с  функциями FTS и пр
        # @@@ ПРИСВОЕНИЕ
        self.outputDf = srchMngrDB.full_text_search_in_FTS_DB_with_df(TB_COMPS_DESCR_FTS_,  self.srchStr, self.getFields, self.srchInterpretor)  # Выводит поля ['id', 'bl_title', 'bl_rest', 'full_path']  

        dfResFTS_N = len(self.outputDf )
        if DEBUG_:
            print(f"dfResFTS_N = {dfResFTS_N} / DSearchCube.search_with_FTS_ <dsearch_cube.py>")



    ## END Внутренние служебные методы класса


if __name__ == '__main__':
    pass




    # ПРОРАБОТКА: Фильтрация фрейма обьекта


    

    # # Поиск по компаниям
    # # Pars search:
    # srchParams = {}
    # srchParams['srchStr'] = "ювелир*"
    # srchParams['srchInterpretor'] = "FTS"
    # # Pars Ini:
    # getFields = ['inn']

    # # Формирование **kwargs
    # kwargs = {}
    # kwargs['srchParams'] = srchParams
    # kwargs['getFields'] = getFields

    # dscCompsDescr = DSearchCube(DB_BONDS_, TB_COMPS_DESCR_, **kwargs) # Найденные по поиску компании 

    # # # <PRINT>
    # # db_proc = SqlitePandasProcessor(DB_BONDS_)
    # # db_proc.print_df_gen_info_pandas_IF_DEBUG(dscCompsDescr.outputDf, True, dfId = '&&&&&&&&&&&&&', srcId = '')


    # # Pars filtration
    # filterParams ={}
    # filterParams['filterFlag'] = True
    # filterParams['filterKeys'] = { 'inn_ref' : dscCompsDescr.outputDf } # Ключи фильтрации по колонке 'inn_ref' в фрейме dscCompsDescr.outputDf 
    # filterParams['filtKeysAssoc'] = {'inn_ref': 'inn'} # Словарь соотвтетвий между полями в базовом фрейме и полями в фрейме для ключей фильтрации {поле в базовом фрейме : поле в фрейме ключей фильтрации}
    # dscBondsCurrent = DSourceCube(DB_BONDS_, TB_BONDS_CURRENT_, filterParams = filterParams) # Облигации 



    # # <PRINT>
    # db_proc = SqlitePandasProcessor(DB_BONDS_)
    # db_proc.print_df_gen_info_pandas_IF_DEBUG(dscBondsCurrent.outputDf, True, dfId = '&&&&&&&&&&&&&', srcId = '')







    # # ПРИМЕР:  Проработка класса

    # # Разные типы источников данных для тестирования и подачи на вход коструктора класса
    # dataSrclist = [['dfsdf', 'sd']]
    # srcListTitles = ['Title1', 'Title2']
    # dataSrcTbname = 'comps_descr'
    # dataSrcSQL = 'SELECT * FROM comps_descr'
    # db_proc = SqlitePandasProcessor(DB_BONDS_)
    # dataSrcFrame = db_proc.read_table_by_sql_to_df_pandas('comps_descr')

    # sortParams = {}
    # sortParams['ascTrue'] = True  # Установка флага направления сортировки
    # sortParams['sortCols'] = {} # Установка колонок сортировки
    # sortParams['sortFlag'] = False # Установка флага сортировки
    # sortParams['sortColInx'] =  0 # Начальная колонка для сортировки

    # # dbTabOutput = DSourceCube(DB_BONDS_, dataSrcTbname, sortParams = sortParams)

    # # db_proc.print_df_gen_info_pandas_IF_DEBUG(dbTabOutput.outputDf, True, dfId = 'genDf', srcId = '')

    # # print(f"sortParams = {sortParams}")
    # # print(f"sortFlag = {dbTabOutput.sortFlag}")
    # # print(f"sortCols = {dbTabOutput.sortCols}")
    # # print(f"ascTrue = {dbTabOutput.ascTrue}")
    # # print(f"sortColInx = {dbTabOutput.sortColInx}")

    # # Pars:
    # # srchStr = "ювелир*"
    # # srchInterpretor = 'FTS' # Интерпретатор или вид поиска

    # srchParams = {}
    # srchParams['srchStr'] = "ювелир*"
    # srchParams['srchInterpretor'] = "FTS"

    # dSearchCb = DSearchCube(DB_BONDS_, dataSrcTbname, sortParams = sortParams, srchParams = srchParams)

    # db_proc.print_df_gen_info_pandas_IF_DEBUG(dSearchCb.outputDf, True, dfId = '&&&&&&&&&&&&&', srcId = '')

    # # print (f"%%%%%  dSearchCb.dbname = {dSearchCb.dbname}")































