
# from bonds.lo_office import LibreOffice
# import pyoo
# import uno
# import funcs_general as FG


# class LibreCalc (LibreOffice):
#     """ Управление Либре эксел <Устаревший класс!!!> """

#         # Конструктор
#     def __init__(self, port='2002'):
#         self.module = 'calc'
#         self.port = port
#         self.open_connection()
#         self.currTbPos = [] # Ячейка для задания текущей позиции таблицы
#         #self.libreDirector = libreDirector # Обьект класса LibreDirector()
#         # self.document = self.desctop.getCurrentComponent() # the current LibreOffice document
#         self.document = self.desctop.getCurrentComponent() # the current LibreOffice document
#     #     self.document  = self.desktop.loadComponentFromURL( \
#     # uno.systemPathToFileUrl('/home/ak/MY_INVESTMENTS/ПОРТФОЛИО/CURR/БАЗОВЫЕ ДАННЫЕ ПО КОРПОРАТИВАМ.ods'), "_blank", 0, tuple([]))
#         self.sheets = self.document.getSheets() # активный документ офиса


#     def get_data_from_range_positions (self, rngPos):
#         """ Получение данных из региона таблицы, определяемого позициями [x1, y1, x2, y2], в виде массива значений (в тапле таплов?)
#         Извлекаются в виде: da()[1][0], индексами в регионе """
#         sh1 = self.sheets.getByIndex(0) 
#         # loRange = sh1.getCellRangeByName( "E5:E15" )
#         loRange = sh1.getCellRangeByPosition(rngPos[0],rngPos[1],rngPos[2],rngPos[3])
#         da = loRange.getDataArray # массив с данными из столбца E ячеек  5:15
#         return da
#         #print (da()[1][0])


#     def sort_region_by_column (self, listRange, sortCol, sortType = "descend" ):
#         """ Сортировка региона по столбцу. listRange - list 4х координат региона, sortCol - int, номер колонки
#             в регионе!!,sortType - str, "descend"(по умолчанию)/ "ascend" """

#         # range to be sorted
#         cellRange = self.sheets.getByIndex(0).getCellRangeByPosition(listRange[0],listRange[1],
#                                                 listRange[2], listRange[3]) # 1 и 3 позиции -  по колонкам
#         # use the first column for the sort key 
#         colDescr = uno.createUnoStruct('com.sun.star.table.TableSortField')
#         colDescr.Field = sortCol  # Начальный индекс относится именно к range
#         if sortType == "ascend":
#             colDescr.IsAscending = True
#         else:
#             colDescr.IsAscending = False
        
#         # sort descriptor
#         sortDescr = cellRange.createSortDescriptor()
#         # <!!!??? ПРИМ: почему-то необходимо сохрянять там, где начинается цикл for индентацию не 4, а 2 пробела. иначе идет ошибка !!!????>
#         for x in sortDescr: 
#           if x.Name == 'SortFields':
#             x.Value = uno.Any('[]com.sun.star.table.TableSortField',(colDescr,))
#             break
#         else: 
#           raise KeyError('SortFields')
                
#         # sort ...
#         cellRange.sort(sortDescr)


#     def inseart_data_to_table (self, titlesTypes, tbData, tbXY):
#         """ tbData - Вставка данных из List рядов с List данных
#         [ row1[ colCellVal1, colCellVal2,...],row1[ colCellVal1, colCellVal2,...], ...] в таблицу эксел
#         и Dictionary названий колонок с их типом данных orded coresponding to Data above. startPosition - List[Xcol,Yrow]  """
        
#         Xcol = tbXY[0] # Началная позиция по колонкам
#         Yrow = tbXY[1] # Началная позиция по рядам

#         r = len(tbData)
#         c = len(tbData[1])

#         # Вставка данных в таблицу эксел 
#         sh1 = self.sheets.getByIndex(0)

#         # A. Вставка заголовков
#         j=0
#         for val in titlesTypes:
#             sh1.getCellByPosition( j+Xcol, Yrow).setString(val) # j - отступ по колонкам, j - по рядам в getCellByPosition. В bonds_tb_elements i+1 потому что первый ряд пустой пока. В нем наоборот ряды идут вначале
#             j+=1

#         j=0
#         # B. Вставка данных
#         keys = list(titlesTypes)
#         for i in range(r): # r-1 потому что первая строка в bonds_tb_elements пустая строк не r, а r-1
#             for j in range(c): # columns

#                 key = keys[j] # тип данных
#                 valType = titlesTypes[key] # задаваемый тип  величин в столбце

#                 # TODO: Сделать обязательно try на IndexError: list index out of range
#                 try:
#                     val = tbData[i][j] # текущее значение ячейки
#                 except:
#                     print("Проверить выход индекса за рамки или значение переменной NaN. M: lo_calc L: 95")
                


#                 if val != '' and ("F#" in valType or "int" in valType) : # проверка величины на float или   int 
#                     #print ("F#")

#                     if "%" in val :
#                         val = FG.strip_for_digits_bytearray (val) # очистка от символов
#                         val = float(val.strip('%')) # конвертация значения процентных велечин из строковой переменной во float
#                         format(val, '.2f')
#                         sh1.getCellByPosition( j+Xcol, i+Yrow+1).setValue(val)

#                     else:
#                         val = FG.strip_for_digits_bytearray (val) # очистка от символов
#                         val = float(val) # конвертация значения числа из строковой переменной во float
#                         format(val, '.2f')
#                         sh1.getCellByPosition( j+Xcol, i+Yrow+1).setValue(val)                        
#                 else:
#                     sh1.getCellByPosition( j+Xcol, i+Yrow+1).setString(val) # j - отступ по колонкам, j - по рядам в getCellByPosition. В bonds_tb_elements i+1 потому что первый ряд пустой пока. В нем наоборот ряды идут вначале



#     # # get title of a document
#     # def get_doc_title (self, curr_doc):
#     #     title = curr_doc.getTitle()
#     #     return title

#     # # get all sheets
#     # def get_all_sheets(self):
#     #     sheets = self.document.getSheets()
#     #     return sheets

#     # # get sheet by index
#     # def get_sheet_by_idx (self, doc_sheets):
#     #     sheet = doc_sheets.getByIndex(0)





# def main():
#     pass


# if __name__ == "__main__":
#     # Модуль коннектора
#     calc = LibreCalc()
#     document = calc.document
#     title = document.getTitle()
#     sheets = document.getSheets()

#     # end Модуль коннектора

#     # sh1 = sheets.getByIndex(0)
#     # cell = sh1.getCellRangeByName("B2")
#     # cell.setString("HELLO!") 
#     # sheet = sheets[0]
#     # sheet[1:3,0:2].values = [[3, 4], [5, 6]]
#     # cells = sheet[:4,:3]
#     # sheet = document.getSheets().getByIndex(0)
#     # row = 0
#     # col = 0
#     # text = sheet.getCellByPosition(row, col).getFormula()
#     # sheet.getCellByPosition( 0, 0 ).setString( "Month" ) 
#     # desktop = pyoo.Desktop('localhost', 2002)
#     # doc = desktop.open_spreadsheet("/home/ak/MY_INVESTMENTS/ПОРТФОЛИО/Анализ своих инвестиций 01.ods")


#     # ----- Модуль алгоритма вставки таблицы и приведения ее к базовому виду ----



#     # ----- END Модуль алгоритма вставки таблицы и приведения ее к базовому виду ----

































