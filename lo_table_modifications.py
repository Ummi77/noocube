
class BondTabModifications():
    """ Класс для управления различными модицикациями таблиц """




    def bonds_tb_modif_001(self, objSheet):
        """ 
        Очистка колонки С. Перенос таблицы по новому адресу с началом в "C6".  Size of columns. оформление таблицы
        PAR: calcSheets - SpreadSheets; corpSh  - рабочая страница
        Category: Excel
        """

        currSh = objSheet.sheet # рабочая страница эксела

        # Очистка колонки С
        oColumns = currSh.getColumns()
        oCol_С = oColumns.getByName("C")
        objSheet.clear_range(oCol_С, 4)
        objSheet.clear_range(oCol_С, 1)


        # Перенос таблицы по новому адресу с началом в "C6"
        cellDest = currSh.getCellRangeByName("C6")
        rngSource = currSh.getCellRangeByName("A4:V604")
        objSheet.move_region(cellDest, rngSource)


        # Size of columns
        objSheet.autosize_col('D') # Autoresize column D
        objSheet.set_col_width('C', 10) # Установка фиксированной ширины колонки C в милимметрах


        # оформление таблицы
        rng = currSh.getCellRangeByName("C6:X606")
        brdWidths = [12,12,12,12]
        objSheet.set_rng_borders(rng,brdWidths)

        objSheet.remove_col_by_name('E',1)

        objSheet.remove_col_by_name("V", 2) # Удаление последних 2х столбцов

        objSheet.remove_col_by_name("G", 1) # Удаление G колонки

        # Окантовка  таблицы и ряда заголовков
        tbRng = currSh.getCellRangeByName("C6:U606")
        # tbRng = currSh.getCellRangeByPosition(2, 0, 3, 1)
        wdths = [12,44]
        objSheet.drow_range_outborder(tbRng, wdths)

        # Оконтовка заголовков
        tbRng = currSh.getCellRangeByName("C6:W6")
        wdths = [12,44]
        objSheet.drow_range_outborder(tbRng, wdths)

