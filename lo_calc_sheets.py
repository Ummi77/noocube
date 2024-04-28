# https://wiki.documentfoundation.org/Macros/Python_Guide/Calc/Calc_sheets

import os
from noocube.lo_calc_sheet import CalcSheet
from noocube.lo_calc_sheet_sqlite import CalcSheetSqlite
from noocube.lo_document import LibreDocument
# import uno

import noocube.funcs_general as FG


class CalcSheets (LibreDocument):
    """ Основной класс для работы с Либре Calc sheets. Параметры: path - если пустой, то sheets открываются с пустым документом,
    подключенный к каналу сокета.     Если path =  абсолютный путь к файлу , то sheets открываются с документом из существующего файла calc , 
    подключенные к сокету. По умолчанию класс работает с Libre Calc и параметр  module = 'calc'. По умолчанию порт = 2002 """

        # Конструктор
    def __init__(self, path='', port='2002', module = 'calc'):
        self.module = module # Модуль, с которым будет работать родительский класс LibreOffice
        self.port = port # Порт для сокета, по которому будет открываться соединение в родительском классе LibreOffice
        self.path = path
        super().__init__(self.path, self.port, self.module)  # Вызов родительского конструктора, чтобы можно было дополнять конструктор свой
        # self.sheets = self.document.getSheets()

    

    # -- МЕТОДЫ ОТКРЫТИЯ И АКТИВАЦИИ СТРАНИЦ

    def open_sheet_with_db_connect (self, file, shName,db):
        """ 
        Запускает LibreCalc через сокет , открывает нужный документ, активирует заданную страницу в документе и расширяет активную 
        страницу для работы с БД 
        Category: Excel
        """
        self.open_document(file) # Открытие документа (в данном случае '/home/ak/MY_INVESTMENTS/ПОРТФОЛИО/CURR/БАЗОВЫЕ ДАННЫЕ ПО КОРПОРАТИВАМ_modif_006.ods')
        corpCalcSqliteSheet = self.get_sqlite_sheet_by_name(shName, db) # Создание обьекта страницы 'Корпоративные' с привязкой к БД sqlite 
        self.activate_sheet(corpCalcSqliteSheet.sheet) # Активация страницы 'Корпоративные'  



    def get_sheet_by_name (self, shName = 'Sheet1'):
        """ 
        Получить страницу (как  обьект оберточного класса CalcSheet) по названию страницы
        По умолчанию щиется и открываетсястраница с названием Sheet1 
        Category: Excel
        """
        unoSh = self.document.Sheets[shName]
        calcSheet = CalcSheet(self.document, unoSh)
        return calcSheet # Обьект класса CalcSheet, который содержит в self.sheet обьект unoSheet


    def get_sqlite_sheet_by_name (self, shName, dBase):
        """ Получить страницу (как  обьект оберточного класса CalcSheet) по названию страницы, интегрированную
        с БД sqlite"""
        unoSh = self.document.Sheets[shName]
        calcSqliteSheet = CalcSheetSqlite(self.document, unoSh, dBase)
        return calcSqliteSheet # Обьект класса CalcSheet, который содержит в self.sheet обьект unoSheet   

    def activate_sheet(self, sh):
        """ 
        Активировать страницу 
        Category: Excel
        """
        self.document.getCurrentController().setActiveSheet(sh)


    def open_document (self, path):
        """ 
        Открывает существующий  файл с абсолютным путем  и расширением файла , либо открывает  пустой Calc-документ, если путь пустой 
        Category: Excel
        """
        if len(path) == 0: # Если path пустой, то открываем новый пустой документ calc
            p = 'private:factory/scalc'
            self.document = self.desktop.loadComponentFromURL(p, '_default', 0, ())   
            self.documentName = ''
            self.dirName = ''
            
        else: # Если path не пустой, то считаем, что там абсолютный путь к файлу  calc и открываем тогда его
            self.document  = self.desktop.loadComponentFromURL(uno.systemPathToFileUrl(path), "_blank", 0, tuple([]))
            self.documentName = os.path.basename(path) # Присваиваем имя файла в собственную переменную
            self.dirName = os.path.dirname(path) # Присваиваем диреторию в собственную переменную

        self.sheets = self.document.getSheets()


    def close (self):
        """
        Закрыть докумен
        Category: Excel
        """
        self.document.close(True)




    # -- END МЕТОДЫ ОТКРЫТИЯ И АКТИВАЦИИ СТРАНИЦ

    def count(self):
        """ 
        Кол-во страниц открытых
        """
        count = self.sheets.Count
        return  count



    def get_names(self):
        """ 
        Получить названия открытых страниц
        Category: Excel
        """
        sheets_names = self.sheets.ElementNames
        return sheets_names


    # -- МЕТОДЫ РАБОТЫ С ТАБЛИЦЕЙ

    def get_data_from_range_positions (self, rngPos):
        """ 
        <Устарел для данного класса. Перенесен в класс CalcSheet в lo_calc_shhet.py>
        Получение данных из региона таблицы, определяемого позициями [x1, y1, x2, y2], в виде массива значений (в тапле таплов?)
        Извлекаются в виде: da()[1][0], индексами в регионе 
        Category: Excel
        """
        sh1 = self.sheets.getByIndex(0) 
        # loRange = sh1.getCellRangeByName( "E5:E15" )
        loRange = sh1.getCellRangeByPosition(rngPos[0],rngPos[1],rngPos[2],rngPos[3])
        da = loRange.getDataArray # массив с данными из столбца E ячеек  5:15
        return da
        #print (da()[1][0])


    def sort_region_by_column (self, listRange, sortCol, sortType = "descend" ):
        """ 
        Сортировка региона по столбцу. listRange - list 4х координат региона, sortCol - int, номер колонки
            в регионе!!,sortType - str, "descend"(по умолчанию)/ "ascend" 
        Category: Excel
        """

        # range to be sorted
        cellRange = self.sheets.getByIndex(0).getCellRangeByPosition(listRange[0],listRange[1],
                                                listRange[2], listRange[3]) # 1 и 3 позиции -  по колонкам
        # use the first column for the sort key 
        colDescr = uno.createUnoStruct('com.sun.star.table.TableSortField')
        colDescr.Field = sortCol  # Начальный индекс относится именно к range
        if sortType == "ascend":
            colDescr.IsAscending = True
        else:
            colDescr.IsAscending = False
        
        # sort descriptor
        sortDescr = cellRange.createSortDescriptor()
        # <!!!??? ПРИМ: почему-то необходимо сохрянять там, где начинается цикл for индентацию не 4, а 2 пробела. иначе идет ошибка !!!????>
        for x in sortDescr: 
          if x.Name == 'SortFields':
            x.Value = uno.Any('[]com.sun.star.table.TableSortField',(colDescr,))
            break
        else: 
          raise KeyError('SortFields')
                
        # sort ...
        cellRange.sort(sortDescr)


    def inseart_data_to_table (self, titlesTypes, tbData, tbXY):
        """ 
        tbData - Вставка данных из List рядов с List данных
        [ row1[ colCellVal1, colCellVal2,...],row1[ colCellVal1, colCellVal2,...], ...] в таблицу эксел
        и Dictionary названий колонок с их типом данных orded coresponding to Data above. startPosition - List[Xcol,Yrow]  
        Category: Excel
        """
        
        Xcol = tbXY[0] # Началная позиция по колонкам
        Yrow = tbXY[1] # Началная позиция по рядам

        r = len(tbData)
        c = len(tbData[1])

        # Вставка данных в таблицу эксел 
        sh1 = self.sheets.getByIndex(0)

        # A. Вставка заголовков
        j=0
        for val in titlesTypes:
            sh1.getCellByPosition( j+Xcol, Yrow).setString(val) # j - отступ по колонкам, j - по рядам в getCellByPosition. В bonds_tb_elements i+1 потому что первый ряд пустой пока. В нем наоборот ряды идут вначале
            j+=1

        j=0
        # B. Вставка данных
        keys = list(titlesTypes)
        for i in range(r): # r-1 потому что первая строка в bonds_tb_elements пустая строк не r, а r-1
            for j in range(c): # columns

                key = keys[j] # тип данных
                valType = titlesTypes[key] # задаваемый тип  величин в столбце

                # TODO: Сделать обязательно try на IndexError: list index out of range
                try:
                    val = tbData[i][j] # текущее значение ячейки
                except:
                    print("Проверить выход индекса за рамки или значение переменной NaN. M: lo_calc L: 95")
                


                if val != '' and ("F#" in valType or "int" in valType) : # проверка величины на float или   int 
                    #print ("F#")

                    if "%" in val :
                        val = FG.strip_for_digits_bytearray (val) # очистка от символов
                        val = float(val.strip('%')) # конвертация значения процентных велечин из строковой переменной во float
                        format(val, '.2f')
                        sh1.getCellByPosition( j+Xcol, i+Yrow+1).setValue(val)

                    else:
                        val = FG.strip_for_digits_bytearray (val) # очистка от символов
                        val = float(val) # конвертация значения числа из строковой переменной во float
                        format(val, '.2f')
                        sh1.getCellByPosition( j+Xcol, i+Yrow+1).setValue(val)                        
                else:
                    sh1.getCellByPosition( j+Xcol, i+Yrow+1).setString(val) # j - отступ по колонкам, j - по рядам в getCellByPosition. В bonds_tb_elements i+1 потому что первый ряд пустой пока. В нем наоборот ряды идут вначале



    

    # -- END МЕТОДЫ РАБОТЫ С ТАБЛИЦЕЙ



    
if __name__ == "__main__":
    pass



    # # ПРИМЕР: Получение обьединенного dataSet из считывания данных из разделенных (разных) регионов таблицы эксел
    # # file = '/home/ak/MY_INVESTMENTS/ПОРТФОЛИО/CURR/БАЗА_ОБЛИГАЦИИ_modif_011.ods'
    
    # file = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/proj_sources/20221209-emidocs-default.xlsx'
    # calcSheets = CalcSheets()
    # calcSheets.open_document(file)
    # # corpSh = calcSheets.document.Sheets['Корпоративные'] # 
    # corpSh = calcSheets.document.Sheets['Корпоративные'] # активировать страницу (но не визуально)
    # calcSheet = CalcSheet(calcSheets.document,corpSh)  
    # rgnName1 = 'C7:D9' # Имя первого региона, в котором будет осуществлятся поиск данных
    # rgnName2 = 'G7:I9' # Имя второго региона, в котором будет осуществлятся поиск данных
    # rngNames = [rgnName1, rgnName2]

    # ds = calcSheet.get_data_from_diffrent_ranges_by_names(rngNames)
   







    ### ------------- ПРИМЕРЫ -------------------------------




    # # ПРИМЕР: Получение обьединенного dataSet из считывания данных из разделенных (разных) регионов таблицы эксел
    # file = '/home/ak/MY_INVESTMENTS/ПОРТФОЛИО/CURR/БАЗА_ОБЛИГАЦИИ_modif_011.ods'
    # calcSheets = CalcSheets()
    # calcSheets.open_document(file)
    # # corpSh = calcSheets.document.Sheets['Корпоративные'] # 
    # corpSh = calcSheets.document.Sheets['Корпоративные'] # активировать страницу (но не визуально)
    # calcSheet = CalcSheet(calcSheets.document,corpSh)  
    # rgnName1 = 'C7:D9' # Имя первого региона, в котором будет осуществлятся поиск данных
    # rgnName2 = 'G7:I9' # Имя второго региона, в котором будет осуществлятся поиск данных
    # rngNames = [rgnName1, rgnName2]
    # ds = calcSheet.get_data_from_diffrent_ranges_by_names(rngNames)
   

    # # ПРИМЕР: Тестирование получение цветов региона ячеек таблицы и использования их для качественного анализа для кода в програме
    # file = '/home/ak/MY_INVESTMENTS/ПОРТФОЛИО/CURR/БАЗА_ОБЛИГАЦИИ_modif_011.ods'
    # calcSheets = CalcSheets()
    # calcSheets.open_document(file)
    # # corpSh = calcSheets.document.Sheets['Корпоративные'] # 
    # corpSh = calcSheets.document.Sheets['Корпоративные'] # активировать страницу (но не визуально)
    # calcSheet = CalcSheet(calcSheets.document,corpSh)  
    # rgnName = 'C7:D9' # Имя региона, в котором будет осуществлятся поиск
    # dsRngColors = calcSheet.get_range_color_list(rgnName)
    # print(dsRngColors)


    # # ПРИМЕР: Тестирование получение цветов ячейки таблицы и использования их для качественного анализа для кода в програме
    # file = '/home/ak/MY_INVESTMENTS/ПОРТФОЛИО/CURR/БАЗА_ОБЛИГАЦИИ_modif_011.ods'
    # calcSheets = CalcSheets()
    # calcSheets.open_document(file)
    # # corpSh = calcSheets.document.Sheets['Корпоративные'] # 
    # corpSh = calcSheets.document.Sheets['Корпоративные'] # активировать страницу (но не визуально)
    # calcSheet = CalcSheet(calcSheets.document,corpSh)  
    # rgnName = 'C7' # Имя региона, в котором будет осуществлятся поиск
    # oCell = calcSheet.get_rng_obj_by_names(rgnName) # Обьект регион, в котором будет осуществлятся поиск
    # colorProperty = oCell.getPropertyValue("CellBackColor")
    # hexStr = hex(colorProperty)



    # # ПРИМЕР: ПОИСК ЯЧЕЕК ПО ЗНАЧЕНИЮ В НИХ
    # file = '/home/ak/MY_INVESTMENTS/ПОРТФОЛИО/CURR/FIRST_COPY_FROM_SOURCES/БАЗА_ОБЛИГАЦИИ_first_source_001.ods'
    # calcSheets = CalcSheets()
    # calcSheets.open_document(file)
    # # corpSh = calcSheets.document.Sheets['Корпоративные'] # 
    # corpSh = calcSheets.document.Sheets['Корп БЗ Пред'] # активировать страницу (но не визуально)
    # calcSheet = CalcSheet(calcSheets.document,corpSh)  
    # rgnName = 'C7:BP10' # Имя региона, в котором будет осуществлятся поиск
    # oRange = calcSheet.get_rng_obj_by_names(rgnName) # Обьект регион, в котором будет осуществлятся поиск
    # srchVal = 'ПионЛизБП1' # искомое значение ячейки
    # foundCellAddrs = calcSheet.search_cell_addrs_by_value(oRange,srchVal) #  адрес ячейки, в которой найдено значение
    # if foundCellAddrs != -1: # # если найдена ячейка со значением
    #     calcSheet.activate_by_range_addrs (foundCellAddrs) # активация ячейки
    # else:
    #     print("Искомое значение не найдено в регионе")








    # # ПРИМЕР: Перевод индекса колонки таблицы в буквенное название и наоборот
    # file = '/home/ak/MY_INVESTMENTS/ПОРТФОЛИО/CURR/FIRST_COPY_FROM_SOURCES/БАЗА_ОБЛИГАЦИИ_first_source_001.ods'
    # calcSheets = CalcSheets()
    # calcSheets.open_document(file)
    # # corpSh = calcSheets.document.Sheets['Корпоративные'] # 
    # corpSh = calcSheets.document.Sheets['Корп БЗ Пред'] # 
    # calcSheet = CalcSheet(calcSheets.document,corpSh)
    # inx = 107
    # cName = calcSheet.get_col_name_from_col_inx(inx)
    # print(cName)
    # idx = calcSheet.get_inx_col_name(cName)
    # print(idx)





    # # ПРИМЕР : Скопировать заданный регион и вставить его в новый заданный равный регион
    # file = '/home/ak/MY_INVESTMENTS/ПОРТФОЛИО/CURR/FIRST_COPY_FROM_SOURCES/БАЗА_ОБЛИГАЦИИ_first_source_001.ods'
    # calcSheets = CalcSheets()
    # calcSheets.open_document(file)
    # corpSh = calcSheets.document.Sheets['Корпоративные'] # 
    # rgnName = 'E4:E907'
    # newRngName = 'B4:B907'    
    # calcSheet = CalcSheet(calcSheets.document,corpSh)
    # calcSheet.copypaste_range_name(rgnName,newRngName) # Скопировать и вставить


    # # ПРИМЕР 1: Открытие страницы эксел с подключением
    # file = '/home/ak/MY_INVESTMENTS/ПОРТФОЛИО/CURR/БАЗА_ОБЛИГАЦИИ_modif_011.ods'
    # calcSheets = CalcSheets()
    # calcSheets.open_document(file)
    # corpSh = calcSheets.document.Sheets['Корпоративные']
    # db = 'bonds.db'
    # corpSqliteSheet = CalcSheetSqlite(corpSh, calcSheets.document, db)
    # tb = 'comps'
    # fieldsVals = {'comp_name': 'FirstCompany LTD', 'inn': '1234567'}
    # corpSqliteSheet.insert_row_into_table(tb, fieldsVals)




### ------------- ПEND РИМЕРЫ -------------------------------











