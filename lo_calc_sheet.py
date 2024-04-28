# https://wiki.openoffice.org/wiki/Spreadsheet_common

from openpyxl.utils import get_column_letter, column_index_from_string
# from bonds.lo_calc_sheets import CalcSheets # Для переводов индексов в символы и наоборот в экселовских таблицах https://habr.com/ru/company/otus/blog/331998/
import noocube.funcs_general as FG
import numpy as np

class CalcSheet():
    """ Класс - обертка для обьекта Sheet: набор методов для более гибкой работы с листами LibreCalc """

    # Конструктор
    def __init__(self, unoDocument, unoSheet):
        """ Передаются unoDocument  и  unoSheet (обьекты loUNO) """
        # self.sheet = sheet 
        self.document = unoDocument
        self.sheet = unoSheet


# DOCUMENT-MODEL METHODS




# VIEW METHODS

    def activate_sheet(self):
        """ 
        Активировать страницу self.sheet
        Category: Excel
        """
        self.document.getCurrentController().setActiveSheet(self.sheet)


    def activate_by_range_name (self, rngName):
        """ 
        Активировать контроллер на заданный регион 
        Ориентировочно пока для заданной ячейки. Проверить для региона работает ли 
        Category: Excel
        """
        oRange = self.sheet.getCellRangeByName(rngName)
        # oCell = self.sheet.getCellRangeByPosition(foundCellAddrs) # по позиции
        controller = self.document.getCurrentController()
        controller.select(oRange) 

        return controller # Вернуть активный текущий контроллер

    def activate_by_range_addrs (self, rangeAddrs):
        """ 
        Активировать контроллер на заданный адресом ячейку 
        Ориентировочно пока для заданной ячейки. Проверить для региона работает ли
        Category: Excel
        """
        # oRange = self.sheet.getCellRangeByName(rngName)
        x1 = rangeAddrs[0]
        y1 = rangeAddrs[1]
        x2 = rangeAddrs[2]
        y2 = rangeAddrs[3]        
        oRange = self.sheet.getCellRangeByPosition(x1,y1,x2,y2) # по позиции
        controller = self.document.getCurrentController()
        controller.select(oRange) 

        return controller # Вернуть активный текущий контроллер


    def copypaste_range_name (self, rngName,newRngName):
        """ 
        Скопировать заданный регион и вставить в другой заданный равный регион 
        Category: Excel
        """
        curController = self.activate_by_range_name(rngName) # Выделить регион
        o = curController.getTransferable() # Скопировать в обьект
        curController = self.activate_by_range_name(newRngName) # Выделить новый равный регион
        curController.insertTransferable(o) # Вставить скопированный обьект в новый регион
        return curController # Вернуть активный текущий контроллер


    def copy_range_name (self, rngName):
        """ 
        TODO: Метод не проверен на практике
        Скопировать заданный регион и вставить в другой заданный равный регион 
        Category: Excel
        """
        curController = self.activate_by_range_name(rngName) # Выделить регион
        o = curController.getTransferable() # Скопировать в обьект
        return o, curController


    def paste_range_name (self, newRngName, o):
        #
        """ 
        TODO: Метод не проверен на практике
        Вставить скопированный регион (обьект) в заданный регион  
        Category: Excel
        """
        curController = self.activate_by_range_name(newRngName) # Выделить новый равный регион
        curController.insertTransferable(o) # Вставить скопированный обьект в новый регион
        return curController # Вернуть активный текущий контроллер



# INTERACTIVE METHODS

    def remove_col_by_index(self,cInx, count):
        """ 
        Удалить колонку по индексу
        Category: Excel
        """
        oColumns = self.sheet.Columns
        oColumns.removeByIndex(cInx, count) 



    def remove_col_by_name(self, cName, count):
        """ 
        Удалить колонку по названию
        Category: Excel
        """
        rName = f"{cName}:{cName}" # название колонки в ввиде региона
        rngSource = self.sheet.getCellRangeByName(rName)
        addr = rngSource.RangeAddress
        cInx = addr.StartColumn
        oColumns = self.sheet.Columns
        oColumns.removeByIndex(cInx, count)   
        

    def clear_range(self, viewElement, cellFlag):
        """ 
        Очистить регин в таблице
        cellFlag * https://www.openoffice.org/api/docs/common/ref/com/sun/star/sheet/CellFlags.html 
        Category: Excel
        """
        viewElement.clearContents(cellFlag)


    def cursor(self):
        """ 
        Получить курсор
        Category: Excel
        """
        cursor = self.sheet.createCursor()
        cursor.getCellByPosition(0, 0)


    def move_region (self, oCellDest, oRangeSource):
        """ 
        переместить регион
        Category: Excel
        """
        cellDest_addrss = oCellDest.CellAddress
        rngSource_addrss = oRangeSource.RangeAddress
        self.sheet.moveRange(cellDest_addrss, rngSource_addrss)





# STYLE METHODS

    def drow_range_outborder(self, tbRng, wdths):
        """ 
        Создает внешнюю оконтовку региона 
        Category: Excel
        """

        currSh = self.sheet

        addr = tbRng.RangeAddress
        startColumn = addr.StartColumn
        startRow = addr.StartRow            
        endColumn = addr.EndColumn
        endRow = addr.EndRow     

        prevWdth = wdths[0]
        newWdth = wdths[1]

        # Левая сторона таблицы
        # rng = currSh.getCellRangeByName("C6:C606")
        rng = currSh.getCellRangeByPosition(startColumn, startRow, startColumn, endRow)
        wds = [newWdth,prevWdth,prevWdth,prevWdth]
        self.set_rng_borders(rng,wds)

        # Верхняя сторона
        # rng = currSh.getCellRangeByName("C6:W6")
        rng = currSh.getCellRangeByPosition(startColumn, startRow, endColumn, startRow)
        wds = [prevWdth,prevWdth,newWdth,prevWdth]
        self.set_rng_borders(rng,wds)

        # Правая сторона
        # rng = currSh.getCellRangeByName("W6:W606")
        rng = currSh.getCellRangeByPosition(endColumn, startRow, endColumn, endRow)
        wds = [prevWdth,newWdth,prevWdth,prevWdth]
        self.set_rng_borders(rng,wds)   

        # Нижняя сторона сторона
        # rng = currSh.getCellRangeByName("C606:W606")
        rng = currSh.getCellRangeByPosition(startColumn, endRow, endColumn, endRow)
        wds = [prevWdth,prevWdth,prevWdth,newWdth]
        self.set_rng_borders(rng,wds)  


    def set_rng_borders(self, rngCell, listBordWidths):
        """ 
        Устанавливает огранку в заданном регионе по вертикалям и горизонталям. listBordWidths - список с тольщиной линий для всех 4х ребер
        [LeftBorder,RightBorder, TopBorder, BottomBorder ].  rngCell - заданный регион эксела
        Category: Excel
        """

        borderNames = {"LeftBorder": rngCell.LeftBorder, "RightBorder" : rngCell.RightBorder, 
        "TopBorder" : rngCell.TopBorder, "BottomBorder": rngCell.BottomBorder}
        i = 0
        for  key,value in borderNames.items():
            p_border = value
            p_border.OuterLineWidth = listBordWidths[i]
            p_border.LineWidth = listBordWidths[i] # ?? Автоматом возможно выставляется при установке OuterLineWidth. То есть ее тоэе надо изменять
            rngCell.setPropertyValue(key, p_border)
            i+=1


    def set_rng_background(self, rng, hexColor):
        """ 
        Устанавливает background color для региона эксел 
        Category: Excel
        """
        colorProp = rng.getPropertyValue("CellBackColor")
        rng.setPropertyValue("CellBackColor", hexColor)	



    def set_col_width(self, colName, mm):
        """  
        Установка фиксированной ширины колонки в милимметрах 
        Category: Excel
        """
        w = mm * 167
        # oColumn = self.sheet.getColumns.getByIndex(col)
        oColumns = self.sheet.getColumns()
        oColumn = oColumns.getByName(colName) 
        oColumn.setPropertyValue("Width", w)


    def autosize_col (self, colName):
        """ 
        Автосайзинг колонки
        Category: Excel
        """
        oColumns = self.sheet.getColumns()
        oColumn = oColumns.getByName(colName)         
        oColumn.OptimalWidth = True 


    def set_cell_color(self, oCell, hexColor):
        """ 
        Установка фона ячейки по шеснадцатиричному формату цвета 
        Category: Excel
        """
        # cell = self.sheet.getCellByPosition( 4, 5 )
        # cell.CellBackColor =0x9acd32
        oCell.CellBackColor =hexColor

        

    def get_cell_obj_bg_color(self, oCell):
        """ 
        Получение цвета фона ячейки-обьекта oCell в шеснадцатиричном виде string  
        Category: Excel
        """
        bgColor = oCell.getPropertyValue("CellBackColor")
        hexColor = hex(bgColor)
        return hexColor


    def get_cell_by_index_bg_color(self, cellInxs):
        """ 
        Получение цвета фона ячейки-обьекта oCell в шеснадцатиричном виде string  
        Category: Excel
        """

        oCell = self.sheet.getCellRangeByPosition(cellInxs[0],cellInxs[1],cellInxs[0],cellInxs[1])
        bgColor = oCell.getPropertyValue("CellBackColor")
        hexColor = hex(bgColor)
        return hexColor





# --- METHODS FOR WORKING WITH TABLES

    def get_data_from_range(self, rng):
        """ 
        Получение одномерных данных из обьекта column range - столбец на странице эксел
        Извлекаются в виде: da()[1][0], индексами в регионе. Проверить структуру можно print (da()[1][0])  и т.д.  Трансформируются в обычный лист одномерный!!!
        Используются только для первой колонки!!! и трансформируются в обычный одномерный лист со значениями из первой колонки по рядам региона
        Category: Excel
        """
        da = rng.getDataArray # массив с данными из региона <непонятный формат немного>
        # Формирование обычного list из dataArr()
        cVals = [] 
        for val in da(): 
            cVals.append(val[0]) # извлекаются данные по первому нулевому индексу. Если регион состоит из нескольких столбцов, то значения хранятся в следующих индексах 1, 2, ...
        return cVals


    def get_full_data_from_range(self, rng):
        """ 
        Получение многомерных данных из обьекта range - регион на странице эксел
        Извлекаются в виде: da()[1][0], индексами в регионе. Проверить структуру можно print (da()[1][0])  и т.д. 
        Переводятся в список таплов (?) всех значений в регионе по рядам 
        Category: Excel
        """
        da = rng.getDataArray # массив с данными из региона <непонятный формат немного>
        # Формирование обычного list из dataArr()
        cVals = [] 
        for val in da(): 
            cVals.append(val) # извлекаются данные по первому нулевому индексу. Если регион состоит из нескольких столбцов, то значения хранятся в следующих индексах 1, 2, ...
        return cVals


    def get_data_from_diffrent_ranges_by_names (self, rngNames):  # !!! 
        """ 
        Получение данных из таблицы эксел из разных регионов таблицы с обьединением с обьединением в результирующем DataSet вдоль столбцов (кол-во рядов разных регионов должно быть равным)
        То есть, допустим, соединение данных из разных столбцов (что бы не считывать весь массив диапазона колонок)
        rngNames = [rng1,rng2, ...]
        Category: Excel
        """
        dsLists = [] 
        for rngName in rngNames: # Цикл по списку регионов

            oRange = self.get_rng_obj_by_names (rngName) # получение обьекта oRange
            dsCurTup = self.get_full_data_from_range(oRange) # получение массива данных по региону обьекта oRange
            dsCur = FG.convert_tuple_of_tuples_to_list_of_lists(dsCurTup)
            dsLists.append(dsCur) # Формирование списка из массивов, равных по количеству рядов, но потенциально отличающихся по количеству колонок

        dsRes = FG.concat_several_ds_by_colmns_to_list(dsLists) # составление обьединенного по колонкам массива из множества массивов с одинаковым количеством рядов

        return dsRes



    def get_range_list_of_parameter_function_PF(self,rngName, PF):
        """ 
        Получение двумерного списка значений параметрической функции PF по ОДНОМУ региону, в которой аргументом является каждая ячейка задаваемого региона 
        PF - функция -параметр, где аргументом является каждая ячейка в каждом передаваемом в параметрах регионе таблицы эксел
        TODO: Сделать получение списка со множества разных регионов, равных по кол-ву рядов
        Category: Excel
        """
        # PF - функция -параметр
        addrsList = self.get_inx_addrs_of_reg_name (rngName)
        print(addrsList)
        m = addrsList[3] - addrsList[1] + 1 # кол-во рядов региона
        n = addrsList[2] - addrsList[0] + 1 # кол-во колонок региона
        # deltaX = # Смещение по оси Х (то есть смещение начала отсчета региона от левой кромки экрана экскел)
        # deltaY = m-1 # Смещение по оси  Y (то есть смещение начала отсчета региона от верхней кромки экрана экскел) - по рядам
        resList = [] # список для списка цветов  по колонкам в одном ряду
        for i in range(m): # цикл по рядам
            
            Colmnlist = [] # список значений ячеек колонок в одном ряду
            for j in range(n): # цикл по  столбцам

                cellInxs = addrsList[0] + j,addrsList[1]+i ,addrsList[0]+j,addrsList[1]+i 
                oCell = self.sheet.getCellByPosition(cellInxs[0],cellInxs[1])                
                val = PF (oCell) # Функция - параметр с аргументом в виде обьекта ячейки таблицы эксел
             
                Colmnlist.append(val)

            resList.append(Colmnlist)

        return resList       



    def get_data_from_diffrent_ranges_by_names_for_parameter_function_ubiversal_PF (self, rngNames, PF):  # !!! 
        """  
        Универсальное Получение данных из таблицы эксел из НЕСКОЛЬКИХ регионов таблицы для функции-параметра, где аргументом является обьект ячейки,
        с обьединением с обьединением в результирующем DataSet вдоль столбцов (кол-во рядов разных регионов должно быть равным)
        То есть, допустим, соединение данных из разных столбцов (что бы не считывать весь массив диапазона колонок)
        rngNames = [rngName1,rngName2, ...]
        PF - функция -параметр, где аргументом является каждая ячейка в каждом передаваемом в параметрах регионе таблицы эксел
        Category: Excel
        """
        dsLists = [] 
        for rngName in rngNames: # Цикл по списку регионов

            dsCurTup = self.get_range_list_of_parameter_function_PF(rngName, PF)
            dsCur = FG.convert_tuple_of_tuples_to_list_of_lists(dsCurTup)
            dsLists.append(dsCur) # Формирование списка из массивов, равных по количеству рядов, но потенциально отличающихся по количеству колонок

        dsRes = FG.concat_several_ds_by_colmns_to_list(dsLists) # составление обьединенного по колонкам массива из множества массивов с одинаковым количеством рядов

        return dsRes
      


    def get_rng_obj_by_indices (self, sh, inxRange):
        """ 
        получение обьекта range на активной странице экскл по заданным индексным координатам границ региона
        Параметры: inxRange -> [x1, y1, x2, y2] 
        Category: Excel
        """
        rng = sh.getCellRangeByPosition(inxRange[0],inxRange[1],inxRange[2],inxRange[3])
        return rng


    def get_rng_obj_by_names (self,  nameRange):
        """ 
        получение обьекта range на активной странице экскл по заданным стандартным названиям колонок и рядов границ региона
        Параметры: inxRange -> 'E5:E15' 
        Category: Excel
        """
        rng = self.sheet.getCellRangeByName( nameRange )
        return rng



    def search_cell_addrs_by_value(self, oRange,srchVal):
        """ 
        Поиск адреса ячейки по значению в заданном регионе
        Возвращает адрес ячейки или [-1,-1], если ничего не найдено 
        Category: Excel
        """
       
        data = self.get_full_data_from_range(oRange)
        y, x = FG.m_array_index(data, srchVal) # координаты найденного элемента в массиве (y - ряд, x - столбец)
        # print (y, x)
        regAddrs = self.get_addrs_of_range (oRange) # получение адреса региона
        # print(regAddrs)
        deltaX1 = regAddrs[0] # смещение по координате Х (по колонкам) за счет того, что индексы в массиве приравниваются к нулю в начале заданного региона
        deltaY1 = regAddrs[1]

        if x != -1: # если координата x в массиве не равна -1 (то есть , найдена)
            foundX1 = x + deltaX1 # координата Х найденной ячейки
            foundY1 = y + deltaY1 # координата Y найденной ячейки
            foundCellAddrs = [foundX1,foundY1,foundX1,foundY1] # адрес ячейки повторяется потому что у региона края ячейки равны друг другу
        else: # если не найдено значение, возвращает -1
            foundCellAddrs = -1
        # print (foundCellAddrs)
        # foundCellName = self.get_cell_name_from_indx_cell_address(foundCellAddrs)
        # print (foundCellName)
        # self.activate_by_range_name (foundCellName)   
        # oCell = self.sheet.getCellRangeByPosition(foundCellAddrs)

        return  foundCellAddrs    


    def get_range_color_list(self,rngName):
        """ 
        Получение двумерного списка цветов фона ячеек региона в шестнадцатиричном виде (матрица стрингов шестнадцатиричного формата) 
        Category: Excel
        """
        
        addrsList = self.get_inx_addrs_of_reg_name (rngName)
        print(addrsList)
        m = addrsList[3] - addrsList[1] + 1 # кол-во рядов региона
        n = addrsList[2] - addrsList[0] + 1 # кол-во колонок региона
        rowsColors = [] # список для списка цветов  по колонкам в одном ряду
        for i in range(m): # цикл по рядам
            
            clmnsColors = [] # список цветов ячеек колонок в одном ряду
            for j in range(n): # цикл по  столбцам

                cellInxs = addrsList[0] + j,addrsList[1]+i,addrsList[0]+j,addrsList[1]+i
                hColor = self.get_cell_by_index_bg_color(cellInxs).replace('0x','')
                clmnsColors.append(hColor)

            rowsColors.append(clmnsColors)

        return rowsColors




    def get_annotation_from_cell (self, oCell):
        """ 
        Получить значчение комментария (аннотации) ячейки 
        Category: Excel
        """   
        oCmt = oCell.getAnnotation()
        oCmtStr = oCmt.getString()   
        return   oCmtStr   





# --- END METHODS FOR WORKING WITH TABLES


# -- ADDRESS METHODS

    def get_addrs_of_range (self,oRng):
        """ 
        Получение адреса региона из обьекта range в виде списка позиционныз координат [x1, y1, x2, y2] в экселе 
        Category: Excel
        """
        addr = oRng.RangeAddress
        startColumn = addr.StartColumn
        startRow = addr.StartRow            
        endColumn = addr.EndColumn
        endRow = addr.EndRow 
        addrsList = [startColumn, startRow, endColumn, endRow]
        return addrsList


    def get_inx_col_name(self,ch):
        """ 
        Возвращает индекс буквенного названия колонки в системе Libre Calc (максимум 2 буквенных разряда)
        Category: Excel
        """

        nLen = len(ch) # кол-во буквенных разрядов

        if nLen == 1:
            inx = ord(ch) - 65
        elif nLen ==2:
            demFirst = ch[0]
            demSecond = ch[1]
            inxP1 = ord(demFirst) - 65
            inxP2 = ord(demSecond) - 65
            inx = (inxP1 +1) * 26 + inxP2 # 26 букв-колонок
        else:
            raise ValueError("Разрядность не соотвествует. M: lo_calc_sheet L: 201")
       
        return inx



    def get_col_name_from_col_inx (self, inx):
        """ 
        Возвращает символ названия колонки по ее индексу в системе spreadsheet эксела 
        Используется пока метод из пакета для экселовских таблиц MS Office  
        Category: Excel
        """
        # TODO: Потом придумать метод без использования библиотеки для эксела MsOffice Excel

        inx = inx + 1 # Так как в системе LibreOffice нумерация колонок начинаются с 0, а в Эксел - с 1
        colName = get_column_letter(inx)
        return colName


    def get_inx_addrs_of_reg_name (self,rgnName):
        """ 
        Возарвщает набор индексов-координат региона,  задаваемого символьным значением 
        Category: Excel
        """
        oRange = self.get_rng_obj_by_names(rgnName)
        addrsList = self.get_addrs_of_range (oRange)
        return addrsList



    def get_reg_name_from_indx_reg_address(self,listAddress):
        """  
        Возвращает символьное название региона, заданного его индексным адресом 
        Category: Excel
        """
        x1 = listAddress[0]
        x1ch = self.get_col_name_from_col_inx (x1)
        y1 = str(listAddress[1] + 1) # +1 потому что ряд 1 имеет индекс 0 в системе Libre Spreadsheet
        x2 = listAddress[2]
        x2ch = self.get_col_name_from_col_inx (x2)
        y2 = str(listAddress[3] + 1) # +1 потому что ряд 1 имеет индекс 0 в системе Libre Spreadsheet
        rngName = f"{x1ch}{y1}:{x2ch}{y2}" 
        return rngName



    def get_cell_name_from_indx_cell_address(self,listAddress):
        """  
        Возвращает символьное название ячейки, заданного его индексным адресом 
        Category: Excel
        """
        x1 = listAddress[0]
        x1ch = self.get_col_name_from_col_inx (x1)
        y1 = str(listAddress[1] + 1) # +1 потому что ряд 1 имеет индекс 0 в системе Libre Spreadsheet
        rngName = f"{x1ch}{y1}" 
        return rngName        


# -- END ADDRESS METHODS





if __name__ == "__main__":
    pass









  # --- ПРИМЕРЫ --------------








