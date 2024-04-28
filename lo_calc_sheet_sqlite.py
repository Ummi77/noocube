# Класс предназначен для работы со страницей calc spreadshhet и базой данных sqlite

from noocube.lo_calc_sheet import CalcSheet
from noocube.sqlite_processor import SqliteProcessor


class CalcSheetSqlite (CalcSheet):
    """ Класс предназначен для работы со страницей calc spreadshhet и интегрированной с ней базой данных sqlite """

    def __init__(self,unoDocument, unoSheet, dbName):
        CalcSheet.__init__(self,unoDocument, unoSheet)    
        self.db_processor = SqliteProcessor(dbName)


        


    def update_data_in_db_from_calc(self, dbTableName, sheetRgnName, fieldsAcordAbs, uniqueColNames):
        """ 
        Обновление данных в таблице БД на основе данных в заданном регионе таблицы эксел\n
        ПАРАМЕТРЫ:\n
        fieldsAcordAbs = {'G': 'okpo', 'V' : 'reg_year', 'F':'comp_name'} \n
        uniqueColNames = ['U','inn']
        Category: Excel
        """

        dataRgnArr = self.sheet.getCellRangeByName(sheetRgnName) # Формирование общего пула данных из заданного региона таблицы эксел в виде массива таплов по рядам
        rngDataSet = self.get_full_data_from_range(dataRgnArr) # преобразованные данные по всему региону, переведенные в вид списка рядов из общего пула данных dataRgnArr - таплов со значениями из источника данных (например, таблицы эксел)

        unqColExelName = uniqueColNames[0] # Название колонки-ключа в пространстве Exel
        uniqColInx = self.get_rel_inx_by_abs_name_in_range (sheetRgnName, unqColExelName) # Получение относительного индекса в dataSet колонки уникального ключа

        fieldsAcordRel = self.name_inx_dict_for_dataset_transition(fieldsAcordAbs, sheetRgnName) # Преобразование словаря с абсолютными буквенными колонками в относит индекс словарь в пространстве dataSet трансофрминг
        unqColTbName = uniqueColNames[1] # Название колонки-ключа в таблице БД

        unqInxColVal = [uniqColInx, unqColTbName] # соответствие инждекса ключевой колонки в dataSet  и названия ключевой колонки в таблице БД

        # Обновление полей в таблице БД на основе данных из массива dataSet
        self.db_processor.update_rows_from_ds(dbTableName, rngDataSet, fieldsAcordRel, unqInxColVal)



    
    def insert_data_from_calc_to_DB (self, dbTableName, sheetRgnName, fieldsAcordAbs, uniqueColName):
        """ 
        Cчитывание данных из региона таблицы эксел из задаваемых колонок и внесение их в определенную таблицу БД sqlite в заданные колонки (универсальная функция должна быть) \n
        ПАРАМЕТРЫ:\n
        dbTableName - название таблицы из активной БД (БД активируется зараниее через connect_mngr).\n
        sheetRgnName - задаваемый абсолютными буквенно-цифровыми значениями регион источника данных на активной странице эксел (calc-страница активируется заранее). \n
        fieldsAcordAbs - словарь соответствий между буквенными названиями колонок - источников данных на активной странице эксела и названиями колонок - приемников данных в таблице БД sqlite. Колонки отбираются те, из которых необходимо считать данные из общего региона-источника.\n
        uniqueColName - абсолютное буквенное название колонки в задаваемом регионе эксел, по которому проводится проверка на уникальность вносимых записей, что бы выполнить условие UNIQUE таблицы-приемника БД\n
        ПРИМЕРЫ ПАРМЕТРОВ:\n
        dbTableName = 'comps' \n
        sheetRgnName = 'D7:BP9'\n
        fieldsAcordAbs = {'U':'inn', 'F': 'comp_name', 'G': 'okpo', 'V' : 'reg_year', 'W' : 'www', 'X' : 'location' } \n
        prKeyField = 'U'
        Category: Excel
        """
        dataRgnArr = self.sheet.getCellRangeByName(sheetRgnName) # Формирование общего пула данных из заданного региона таблицы эксел в виде массива таплов по рядам

        rngDataSet = self.get_full_data_from_range(dataRgnArr) # преобразованные данные по всему региону, переведенные в вид списка рядов из общего пула данных dataRgnArr - таплов со значениями из источника данных (например, таблицы эксел)

        prKeyInx = self.get_rel_inx_by_abs_name_in_range(sheetRgnName,uniqueColName) # относительный индекс UNIQUE колонки в массиве региона dataSet на основе соответствия колонке с абсолютным названием в регионе эксел, источнике общего массива данных

        # Абс в относит индекс словарь трансофрминг
        fieldsAcordRel = self.name_inx_dict_for_dataset_transition(fieldsAcordAbs, sheetRgnName)

        # Вставить данные из общего массива данных dataSet региона таблицы эксел в таблицу БД , по заданным полям - соответствиям между колонками эксела и полями таблицы БД
        self.db_processor.insert_rows_from_ds (dbTableName, rngDataSet, fieldsAcordRel, prKeyInx)        







    def name_inx_dict_for_dataset_transition (self, fieldsAccordAbs, dataRgnName):
        """ 
        Трасформация абсолютного именного словаря fieldsAccordDic соответствий заданных колонок в источнике данных dataSet колонкам таблицы БД, в которую будут вноситься данные из источника,
        в относительный индексный словарь соответствий. dataRgnName - абсолютное буквенное имя региона, их которого были взяты данные для
        dataSet . Возвращает  fieldsAccordRel - словарь соответствий абсолютных индексов колонок в общем dataSet источника и колонок в таблице БД 
        Category: Excel
        """

        fieldsAccordRel = {} # словарь соответствий абсолютных индексов колонок в общем dataSet источника и колонок в таблице БД
        for key, value in  fieldsAccordAbs.items(): # цикл по ключам словаря fieldsAccordAbs
            relFieldInx = self.get_rel_inx_by_abs_name_in_range(dataRgnName, key) # относительный индекс колонки в массиве региона dataSet
            fieldsAccordRel[relFieldInx] = value

        return fieldsAccordRel # словарь соответствий абсолютных индексов колонок в общем dataSet источника и колонок в таблице БД


    def get_rel_inx_by_abs_name_in_range (self, dataRgnName, absColname):
        """ 
        относительный индекс колонки в массиве региона dataSet(список рядов данных из таблицы эксел по заданному региону, где первая колонка 
        теперь это - нулевой индекс, а в экселе - это буквенное обозначение колонки на странице sheet), если все колокни изначально выраженны 
        абсолютными буквенными значениями 
        Category: Excel
        """

        regFirstColInx = self.get_inx_col_name(dataRgnName[0]) # Индекс первой колонки задаваемого региона dataRgnName. TODO: сделать вычисление индекса для двойных буквенных наименований колонок также
        fieldAbsInx = self.get_inx_col_name(absColname) # Абсолютный Индекс колонки текущего поля в цикле по словарю задаваемых колонок fields
        relFieldInx =  fieldAbsInx - regFirstColInx # Относительный индекс текущей по циклу колонки в массиве - общем источнике данных dataSet
        return relFieldInx



    def insert_row_from_calc_to_BD(self, tb, row, fieldsDict):
        """ 
        вставить определенные поля из строки таблицы эксел, определяемые названиями столбцов, в соответственные поля строки  задаваемой таблицы 
        в БД. Connection с БД уже открыт. fieldsDict = {'U.s':'inn', 'F.s': 'comp_name', 'G.s': 'okpo'} # Словарь соответсвий названий колонок в эксел и названий колонок в БД.
        U.s - Колонка U (.s - string/ .i - int/ .f - real)  
        Category: Excel
        """

        # Формирвоание словаря {'fieldName':'fieldValue'} для использования функции insert_row_into_table_sql (self, tb_name, fieldsVals) в синтаксере
        # для одной строки в таблице
        fieldsVals = {}
        for key,value in fieldsDict.items():

            fieldType = key.split('.') 
            field = fieldType[0] # название столбца в эксел
            fType = fieldType[1] # тип записей в столбце (.s - string/ .i - int/ .f - real) 
            if 's' in fType: # если строковый тип полей
                fieldsVals[value] = self.sheet.getCellRangeByName(f'{field}{row}').getString()
            elif 'f' in fType or 'i' in fType: # если числовой тип полей
                fieldsVals[value] = self.sheet.getCellRangeByName(f'{field}{row}').getValue()

        # Использование insert_row_into_table (self, tbName, fieldsVals) в sqlite_processor !!
        self.db_processor.insert_row_into_table(tb, fieldsVals)

        






















