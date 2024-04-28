


import inspect
import noocube.funcs_general as FG
from noocube.switch import Switch
from noocube.sqlite_pandas_processor import SqlitePandasProcessor
from noocube.settings import *



class DSourceCube ():
    """Кубиковый  класс (относящийся к базовому фреймворку CUBE, система кубиков) для организации фреймов из разных источников данных
    Источником данных, входным параметром, dataSrc обьекта можгут быть разные типы данных
    srcListTitles = [] - дополнительный параметр - список названий колонок в случае, если обьект строится на основе двумерного списка (аналога данных таблицы) и если необходимы названия колонок..
                        В других источниках названия колонок присутствуют в самих источниках
    Предусмотрены возможности фильтрации и сортировки , если заданы соотвтетствующие именные параметры в **kwargs и включены флаги: self.sortFlag  и self.filterFlag (по умолчанию - выключены)
    """

    def __init__(self, dbName, dataSrc, **kwargs):
        
        self.iniConstr = True # Флаг инициации обьекта. Только один раз True, когда проходит инициализацию в констроукторе обьект

        self.dataSrc = dataSrc
        self.srcDataType = ''
        self.dbname = dbName # БД
        self.srcListTitles = []
        self.kwargs = kwargs # Входные именнованные параметры **kwargs

        # Устанавливает: 
        # Переменные для сортировки:
        # @@@  self.sortParams - Параметры сортировки
        # @@@ self.sortFlag -  
        # @@@ self.sortCols - 
        # @@@ self.ascTrue - Направление сортировки sortDict['desc'] или self.sortDirection:  False или True. По умолчанию ascending=True
        # @@@ self.sortColInx индекс колонки для сортировки, если задана. По умолчанию сортировки нет. По умолчанию стоит индекс колонки  = 0
        
        # ДЕФОЛТНАЯ УСТАНОВКА СОБСТВЕННЫХ ПЕРЕМЕННЫХ, тех, которых необходимо устанавливать по умолчанию:
        self.sortFlag = False # Включатель сотрировки при True
        self.sortColInx = 0 # Колонка для сортировки по умолчанию
        self.ascTrue = True
        self.getFields = ['*'] # Получаемые коллонки таблицы из запроса SQL, если первичным источником является название таблицы БД (дополнительный параметр, если необходимо, к источнику дяанных - Таблица)

        # Переменные для фильтрации фрейма
        # Переменная для фильтрации по ключам , находящихся в словаре, где ключами словаря служат названия полей фрейма,
        #  а последовательность ключей словаря является последовательностью полей в фильтрации
        self.filterKeys = {} 
        self.filterFlag = False # Флаг включения фильтрации
        self.filtKeysAssoc = {} # Словарь соотвтетвий между полями в базовом фрейме и полями в фрейме для ключей фильтрации {поле в базовом фрейме : поле в фрейме ключей фильтрации}

        # Настройка собственных переменных, которые соотвтетсвуют входным именнованным параметрам
        self.set_cls_vars_from_kwargs_dsourcecube_ ()   # Настройка собственных переменных, которые соотвтетсвуют входным именнованным параметрам (именно этого родительского класса)





        self.genDf = None # Полный начальный Прообраз таблицы в виде фрейма
        self.dbPandaProc = SqlitePandasProcessor(DB_BONDS_) # Процедурный обьект (отвечает за подклчение к БД и всякие опрерации с БД , включая с использованием фреймов )
        self.prepare_gen_df () # Получаем общий фрейм на основе таблицы <ПОЛУЧЕНИЕ КОНЕЧНОГО ФРЕЙМА С ДАНЫНМИ>

        # переменные настройки выходного массива
        self.outputDf = self.genDf # конечный вариант фрейма для вывода на внешний ресурс (с готовым пагинатором, заанными колонкми и их названиями на внешнем ресурсе)
                                    # Изначально приравнивается проинициализированному входному массиву self.genDf
        self.outputCols = []  # Названия выводимых колонок в конечной таблице
        self.remainColsInxs = [] # Колонки оставляемые из общего фрейма - прообраза таблицы tbName

        # Запуск сортировки по задаваемым в self.sortCols  колонкам , если флаг сортировки self.sortFlag = True
        if self.sortFlag:
            self.sort()

        # Запуск фильтрации, если она предполагается
        if self.filterFlag:
            self.filter_by_values()


        self.iniConstr = False # Флаг инициации обьекта. Только один раз True, когда проходит инициализацию в констроукторе обьект. В конце __init__ выключаем флаг инициализации



    def  filter_by_values (self):
        """
        фильтрация колонок фрейма по заданным для них массивами с величинами для фильтрации  
        Возможна фильтрация по нескольким колонкам <но пока не проверено в тестировании>
        Category: Фильтрация
        """

        # dsBase = TB_BONDS_CURRENT_  # Базовый источник данных - таблица bonds_current
        # dsKeys = dfCompsFTS # Ключи для идентификации нужных записей в базовой таблице находятся в фрейме найденных компаний и ими является колонка с inn как реферальный ключ
        # dicKeysAssoc ={'inn_ref': 'inn'} # словарь соответствия названия ключа в базе(key) и названия колонки (val) ключей в dsKeys

        # Цикл по словарю полей и ключей филльтрации 
        for kField, vKeysFilt in self.filterKeys.items():
            dicKeysAssoc = { kField : self.filtKeysAssoc[kField] }  # Словарь соотвтетвий между полями в базовом фрейме и полями в фрейме для ключей фильтрации {поле в базовом фрейме : поле в фрейме ключей фильтрации}
            # @@@ ПРИСВОЕНИЕ self.outputDf
            self.outputDf = self.dbPandaProc.select_rows_from_data_source_by_values_source_pandas (self.dataSrc, vKeysFilt, dicKeysAssoc)




    # def get_data_source_type (self, ds):
    #     """ ЗАГОТОВКА: Анализ и получение типа источника данных"""
    #     # Анализ типа источника данных и присвоение метки , соотвтетсвеннной этому типу переменной
    #     if  'list' in str(type(ds)):
    #         dsType = 'srcList'
    #     elif 'DataFrame' in str(type(ds)):
    #         dsType = 'srcDf'
    #     elif 'str' in str(type(ds)) and 'SELECT' in ds:
    #         dsType = 'srsSQL'
    #     elif 'str' in str(type(ds)) and 'SELECT' not in ds:
    #         dsType = 'srcTbName'  
    #     else:
    #         dsType = None
            
    #     return dsType



    def prepare_gen_df (self):
        """ TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>
        Подготовить и присвоить первичный фрейм с данными на основе одного из источников (собственные переменные с первиксом 'src')
        тот источник, который не None, значит является источником данных для построения фрейма. Остальные строго д.б. равны None
        # TODO: Сделать автоматическое определени источника. Ввести входной параметр с источником данных. И автоматом определить, что это за источник (какую-то универсальную функцию(?))
        Category: Фреймы
        """
        # Анализ типа источника данных и присвоение метки , соотвтетсвеннной этому типу переменной
        if  'list' in str(type(self.dataSrc)):
            self.srcDataType = 'srcList'
        elif 'DataFrame' in str(type(self.dataSrc)):
            self.srcDataType = 'srcDf'
        elif 'str' in str(type(self.dataSrc)) and 'SELECT' in self.dataSrc:
            self.srcDataType = 'srsSQL'
        elif 'str' in str(type(self.dataSrc)) and 'SELECT' not in self.dataSrc:
            self.srcDataType = 'srcTbName'  
        else:
            self.srcDataType = None


        # Переключатель SWITCH ... CASE для запуска формирования общего фрема с данными на основе входного источника данных и в зависимости от него по разному формируется фрейм
        for case in Switch(self.srcDataType):
            if case('srcTbName'): 
                if DEBUG_: print('Тип источника данных: srcTbName / TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>')
                self.create_df_from_dbase_tabl_ () # Создание общего фрейма с данными ,считанными из таблицы с названием, заданным во входном параметре источника данных dataSrc
                break
            if case('srsSQL'): 
                if DEBUG_: print('Тип источника данных: srsSQL / TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>')
                self.create_df_from_SQL_ () # Создание общего фрейма с данными из запроса SQL , задаинного во входном  dataSrc
                break
            if case('srcDf'): 
                if DEBUG_: print('Тип источника данных: srcDf / TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>')
                self.create_df_from_data_frame_ () # Создание общего фрейма с данными из входного фрейма, заданного во входном параметре dataSrc
                break
            if case('srcList'): 
                if DEBUG_: print('Тип источника данных: srcList / TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>')
                self.create_df_from_list_ () # Создание общего фрейма с данными из двумерного списка, заданным во входном параметре источника данных dataSrc
                break
            if case(): # default
                if DEBUG_: print('Не задано ни одного источника данных / TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>')
                break

    # МЕТОДЫ ДЛЯ СТАТИЧЕСКОГО ИСПОЛЬЗОВАНИЯ 
    
    # @staticmethod
    # def get_df_from_data_source_dsc (ds):
    #     """ TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>
    #     Подготовить и присвоить первичный фрейм с данными на основе одного из источников (собственные переменные с первиксом 'src')
    #     тот источник, который не None, значит является источником данных для построения фрейма. Остальные строго д.б. равны None
    #     TODO: Унифицировать для использования в самом классе. Иначе два раза одно и то же почти для обьекта класса и для статичного использования
    #     """
    #     # Анализ и получение типа источника данных
    #     if  'list' in str(type(ds)):
    #         dsType = 'srcList'
    #     elif 'DataFrame' in str(type(ds)):
    #         dsType = 'srcDf'
    #     elif 'str' in str(type(ds)) and 'SELECT' in ds:
    #         dsType = 'srsSQL'
    #     elif 'str' in str(type(ds)) and 'SELECT' not in ds:
    #         dsType = 'srcTbName'  
    #     else:
    #         dsType = None
            

    #     # Переключатель SWITCH ... CASE для запуска формирования общего фрема с данными на основе входного источника данных и в зависимости от него по разному формируется фрейм
    #     for case in Switch(dsType):
    #         if case('srcTbName'): 
    #             if DEBUG_: print('Тип источника данных: srcTbName / TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>')
    #             self.create_df_from_dbase_tabl_ () # Создание общего фрейма с данными ,считанными из таблицы с названием, заданным во входном параметре источника данных dataSrc
    #             break
    #         if case('srsSQL'): 
    #             if DEBUG_: print('Тип источника данных: srsSQL / TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>')
    #             self.create_df_from_SQL_ () # Создание общего фрейма с данными из запроса SQL , задаинного во входном  dataSrc
    #             break
    #         if case('srcDf'): 
    #             if DEBUG_: print('Тип источника данных: srcDf / TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>')
    #             self.create_df_from_data_frame_ () # Создание общего фрейма с данными из входного фрейма, заданного во входном параметре dataSrc
    #             break
    #         if case('srcList'): 
    #             if DEBUG_: print('Тип источника данных: srcList / TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>')
    #             self.create_df_from_list_ () # Создание общего фрейма с данными из двумерного списка, заданным во входном параметре источника данных dataSrc
    #             break
    #         if case(): # default
    #             if DEBUG_: print('Не задано ни одного источника данных / TableDbdfOutput.prepare_gen_df()  <table_dbdf_output.py>')
    #             break


    # END МЕТОДЫ ДЛЯ СТАТИЧЕСКОГО ИСПОЛЬЗОВАНИЯ 



    def prepare_output_df (self):
        """ 
        ЗАГОТОВКА
        Подготовить конечный вариант фрейма длdataSrcя вывода на внешний ресурс (с готовым пагинатором, заанными колонкми и их названиями на внешнем ресурсе)
        Category: Заготовки
        """



    def sort(self):
        """ 
        Для сортировки фрейма @@@ self.outputDf 
        Уже должны быть значения В собственных переменных:
        self.outputDf - сам фрейм с данынми
        self.sortColInx - индекс колонки, по которой необходимо провести сортировку
        self.sortFlag - флаг сортировки (включатель сортировки)
        sortDirection - Направление сортировки sortDict['desc'] или self.sortDirection:  False или True. По умолчанию ascending=True
        Category: Фреймы
        """

        self.outputDf = self.dbPandaProc.get_df_sorted_by_col_index(self.outputDf, self.sortColInx, self.ascTrue)





    def sort_by_sys_indx():
        """
        ЗАГОТОВКА
        Category: Заготовки
        """



    ## Внутренние служебные методы класса

    def create_df_from_dbase_tabl_ (self):
        """
        Создание общего фрейма с данными ,считанными из таблицы с названием, заданным во входном параметре источника данных dataSrc
        Category: Фреймы
        """
        print ("START: create_df_from_dbase_tabl_()")
        if DEBUG_: print(f'create_df_from_dbase_tabl_ / TableDbdfOutput.create_df_from_dbase_tabl_()  <table_dbdf_output.py>')
        if self.iniConstr: # Если запуск метода идет из конструктора, то есть идет инициализация обьекта, тогда  self.genDf наполняем данными, которые тождественны будут с self.dfOutput после конструктора
            self.genDf = self.dbPandaProc.read_table_by_sql_to_df_pandas(self.dataSrc, getFields = self.getFields) # @@@ Присвоение созданного фрейма из таблицы БД в собств. переменную
        else:
            self.outputDf = self.dbPandaProc.read_table_by_sql_to_df_pandas(self.dataSrc, getFields = self.getFields) # @@@ Присвоение созданного фрейма из таблицы БД в собств. переменную
        self.dbPandaProc.print_df_gen_info_pandas_IF_DEBUG(self.genDf, dfId = 'genDf', srcId = '/ TableDbdfOutput.create_df_from_dbase_tabl_ <table_dbdf_output.py>')

    def create_df_from_SQL_ (self):
        """
        Создание общего фрейма с данными из запроса SQL , задаинного во входном  dataSrc
        Category: Фреймы
        """
        print ("START: create_df_from_SQL_()")
        if DEBUG_: print(f'create_df_from_SQL_ / TableDbdfOutput.create_df_from_SQL_()  <table_dbdf_output.py>')
        if self.iniConstr: # Если запуск метода идет из конструктора, то есть идет инициализация обьекта, тогда  self.genDf наполняем данными, которые тождественны будут с self.dfOutput после конструктора
            self.genDf = self.dbPandaProc.read_sql_to_df_pandas(self.dataSrc)  # @@@ Присвоение созданного фрейма из SQL в собств. переменную
        else:
            self.outputDf = self.dbPandaProc.read_sql_to_df_pandas(self.dataSrc)  # @@@ Присвоение созданного фрейма из SQL в собств. переменную
        self.dbPandaProc.print_df_gen_info_pandas_IF_DEBUG(self.genDf, dfId = 'genDf', srcId = '/ TableDbdfOutput.create_df_from_SQL_ <table_dbdf_output.py>')


    def create_df_from_data_frame_ (self):
        """
        Создание общего фрейма с данными из входного фрейма, заданного во входном параметре dataSrc
        Category: Фреймы
        """
        print ("START: create_df_from_data_frame_()")
        if DEBUG_: print(f'create_df_from_data_ftame_ / TableDbdfOutput.create_df_from_data_ftame_()  <table_dbdf_output.py>')
        if self.iniConstr: # Если запуск метода идет из конструктора, то есть идет инициализация обьекта, тогда  self.genDf наполняем данными, которые тождественны будут с self.dfOutput после конструктора
            self.genDf = self.dataSrc  # @@@ Присвоение входящего фрейма в собств. переменную 
        else:
            self.outputDf = self.dataSrc  # @@@ Присвоение входящего фрейма в собств. переменную 
        self.dbPandaProc.print_df_gen_info_pandas_IF_DEBUG(self.genDf, dfId = 'genDf', srcId = '/ TableDbdfOutput.create_df_from_data_frame_ <table_dbdf_output.py>')

    def create_df_from_list_ (self):
        """
        Создание общего фрейма с данными из двумерного списка, заданным во входном параметре источника данных dataSrc
        Category: Фреймы
        """
        if DEBUG_: print(f'create_df_from_list_() / dsource_cube.py')
        if self.iniConstr: # Если запуск метода идет из конструктора, то есть идет инициализация обьекта, тогда  self.genDf наполняем данными
            self.genDf = self.dbPandaProc.get_data_frame_from_2dim_list_pandas (self.dataSrc, self.srcListTitles)
        else:
            self.outputDf = self.dbPandaProc.get_data_frame_from_2dim_list_pandas (self.dataSrc, self.srcListTitles)
        self.dbPandaProc.print_df_gen_info_pandas_IF_DEBUG(self.genDf, ifPrintDF = True, dfId = 'genDf', srcId = '/ TableDbdfOutput.create_df_from_list_ <table_dbdf_output.py>')


    def set_cls_vars_from_kwargs_dsourcecube_ (self):
        """
        установка собственных переменных в зависимости от переданных переметров **kwargs с соответствующими ключами , предназаначенных, кроме всего, для настройки собственных
        соотвтетсвующих прееменных
        Category: Вспомогательные
        """

        # @@@ список названий колонок в случае, если обьект строится на основе двумерного списка (аналога данных таблицы) и если необходимы названия колонок.
        if "srcListTitles" in self.kwargs :
            self.srcListTitles = self.kwargs['srcListTitles'] 
        else:
            self.srcListTitles = []

        # @@@ self.getFields Получаемые коллонки таблицы из запроса SQL, если первичным источником является название таблицы БД (дополнительный параметр, если необходимо, к источнику дяанных - Таблица)
        if "getFields" in self.kwargs :
            self.getFields = self.kwargs['getFields'] 


        ##ПЕРЕМЕННЫЕ ФИЛЬТРАЦИИ
        # @@@  self.sortParams - Параметры сортировки, расшифровывающиеся и присваемые ниже
        if "filterParams" in self.kwargs :
            self.filterParams = self.kwargs['filterParams'] 
            print(f"self.filterParams = {self.filterParams}")

            # Расшифровка и присвоение параметров сортировки, которые сами хранятся в параметре-словаре self.sortParams 
            # @@@ Флаг включения фильтрации
            if "filterFlag" in self.filterParams :
                self.filterFlag = self.filterParams['filterFlag'] 

            # @@@ Ключи фильтрации по колонкам в виде словаря {колонка : ключи фильтрации}
            if "filterKeys" in self.filterParams :
                self.filterKeys = self.filterParams['filterKeys'] 

            # @@@ Словарь соотвтетвий между полями в базовом фрейме и полями в фрейме для ключей фильтрации {поле в базовом фрейме : поле в фрейме ключей фильтрации}
            # {поле в базовом фрейме : поле в фрейме ключей фильтрации}
            if "filtKeysAssoc" in self.filterParams :
                self.filtKeysAssoc = self.filterParams['filtKeysAssoc'] 


        ## ПЕРЕМЕННЫЕ СОРТИРОВКИ:
        # @@@  self.sortParams - Параметры сортировки, расшифровывающиеся и присваемые ниже
        if "sortParams" in self.kwargs :
            self.sortParams = self.kwargs['sortParams'] 
            print(f"self.sortParams = {self.sortParams}")

            # Расшифровка и присвоение параметров сортировки, которые сами хранятся в параметре-словаре self.sortParams 
            # @@@ Настройка сортировки по колонкам и их порядку, задаваемые в словаре 
            if "sortCols" in self.sortParams :
                self.sortCols = self.sortParams['sortCols'] 
            else:
                self.sortCols = {}

            # @@@  Флаг запуска сорировки. По умолчанию - False, т.е. без сортировки вообще
            if "sortFlag" in self.sortParams :
                self.sortFlag = self.sortParams['sortFlag'] 
            else:
                self.sortFlag = False

            # @@@  Направление сортировки sortDict['desc'] или self.sortDirection:  False или True. По умолчанию ascending=True
            if "ascTrue" in self.sortParams :
                self.ascTrue = self.sortParams['ascTrue'] 
            else:
                self.ascTrue = True

            # @@@  self.sortColInx индекс колонки для сортировки, если задана. По умолчанию сортировки нет. По умолчанию стоит индекс колонки  = 0
            if "sortColInx" in self.sortParams :
                self.sortColInx = self.sortParams['sortColInx'] 
            else:
                self.sortColInx = 0
        else:
            self.sortParams = {}

        ## END ПЕРЕМЕННЫЕ СОРТИРОВКИ:
        




    ## END Внутренние служебные методы класса



if __name__ == '__main__':
    pass




    # ПРОРАБОТКА: Сохранение и исполозование Excel как хранитель информации быстрого доступа 

    





    # # ПРИМЕР: Работа с обьектом TableDbdfOutput ()

    # # Разные типы источников данных для тестирования и подачи на вход коструктора класса
    # dataSrclist = [['dfsdf', 'sd']]
    # srcListTitles = ['Title1', 'Title2']
    # dataSrcTbname = 'comps_descr'
    # dataSrcSQL = 'SELECT * FROM comps_descr'
    # db_proc = SqlitePandasProcessor(DB_BONDS_)
    # dataSrcFrame = db_proc.read_table_by_sql_to_df_pandas('comps_descr')

    # # Обьект класса TableDbdfOutput !!!
    # # dbTabOutput = TableDfCube(DB_BONDS_, dataSrcSQL, paginGenSet = PAGIN_BONDS_CURR_SET_)
    # # dbTabOutput = TableDfCube(DB_BONDS_, dataSrcTbname)False

    # # # Работа с пагинатором
    # # paginator = dbTabOutput.paginator
    # # firstPgDf = dbTabOutput.paginator.dfLimByPgNumb
    # # db_proc.print_df_gen_info_pandas_IF_DEBUG(dbTabOutput.paginator.dfLimByPgNumb, True, dfId = 'genDf', srcId = '')
    # # pg = 5
    # # paginator.set_curr_active_obj_paginator(pg)
    # # db_proc.print_df_gen_info_pandas_IF_DEBUG(dbTabOutput.paginator.dfLimByPgNumb, True, dfId = 'genDf', srcId = '')



    # # Работа с сортировкой
    # # Pars параметры сортировки:

    # sortParams = {}
    # sortParams['ascTrue'] = False  # Установка флага направления сортировки
    # sortParams['sortCols'] = {} # Установка колонок сортировки
    # sortParams['sortFlag'] = True # Установка флага сортировки
    # sortParams['sortColInx'] =  0 # Начальная колонка для сортировки

    # dbTabOutput = DSourceCube(DB_BONDS_, dataSrcTbname, sortParams = sortParams)


    # db_proc.print_df_gen_info_pandas_IF_DEBUG(dbTabOutput.outputDf, True, dfId = 'genDf', srcId = '')


    # print(f"sortParams = {sortParams}")
    # print(f"sortFlag = {dbTabOutput.sortFlag}")
    # print(f"sortCols = {dbTabOutput.sortCols}")
    # print(f"ascTrue = {dbTabOutput.ascTrue}")
    # print(f"sortColInx = {dbTabOutput.sortColInx}")









































