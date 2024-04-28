


# from bonds.lo_calc_sheets import CalcSheets
# from bonds.sqlite_pandas_processor import SqlitePandasProcessor
# from bonds.settings import *
# import pandas as pd
from noocube.pandas_manager import PandasManager
from noocube.lo_calc_sheets import CalcSheets

class LibreCalcPandasDBSpeedup (CalcSheets, PandasManager):
    """ Для работы с таблицами c использованием Pandas и без использования старого неэффективного медленного подсоединения к БД через SqliteProcces  и пр.
    Использовать только менеджеры-классы с БД с расширением Speedup типа SqliteProccesSpeedup
    """

        # Конструктор
    def __init__(self):
        CalcSheets.__init__(self)  # Вызов родительского конструктора, чтобы можно было дополнять конструктор свой
        PandasManager.__init__(self)



# СТРАНИЦА ДЛЯ АКТИВИРОВАНИЯ И ФАЙЛ ЗАДАЮТСЯ КАК ПАРАМЕТРЫ МЕТОДОВ
    def create_df_from_calc_rng_name_of_given_file_and_sheet_speedup (self, file, sheetName, rngName, colNames = []):
        """
        Аналогичный метод к create_df_from_calc_rng_name, только документ Libre office активируется изнутри метода по названию файла. Так же активируется страница по названию
        изнутри. 
        Category: Excel
        """
        self.open_document(file)
        oSheet = self.get_sheet_by_name (sheetName) # Обьект страницы с именем sheetName
        dfRes = self.create_df_from_calc_rng_name (oSheet, rngName, colNames)
        return dfRes






# ВНЕШНЯЯ СТРАНИЦА УЖЕ АКТИВИРОВАНА И НЕ ЗАВИСИТ ОТ ПАРАМЕТРОВ МЕТОДОВ
    def create_df_from_calc_rng_name (self, oSheet, rngName, colNames = []):
        """
        Создать фрейм из зеденного региона таблицы Эксел на текущей активной странице libre Office (активная страница не зависит от параметров этого метода. Это  внешняя среда для этого метода)
        oSheet - обьект страницы с  которой идет взаимодействие в методе
        colNames - название колонок фрейма в соответствии с колонками задаваемого региона таблицы эксел. Если не заданы , то идет индексация колонок фрейма без названий
        Category: Excel
        """
        oRng = oSheet.get_rng_obj_by_names (rngName) # обьект range
        rngDataList = oSheet.get_full_data_from_range(oRng)
        # if DEBUG_:  # Не удалять !!!
        #     print(f"rngDataList = {rngDataList}")
        #     print (f"rngDataList_N = {len(rngDataList)}")
        if len(colNames) > 0: # если задан список с названиями колонок
            dfRes = self.get_pandas_data_frame(rngDataList, colNames)    
        else:
            dfRes = self.get_pandas_data_frame(rngDataList)  
        return dfRes






if __name__ == "__main__":
    pass



    # # ПРОРАБОТКА: Запись данных из фрейма в таблицу эксел 
    #     # ISINs из табл bonds_current

    # db_panda_proc = LibreCalcPandasDB()
    # dfISINCurrent= db_panda_proc.read_table_by_sql_to_df_pandas(TB_BONDS_CURRENT_, ['isin'])
    # if DEBUG_:
    #     print(f"dfISINCurrent = \n{dfISINCurrent}")
    #     print(f"dfISINCurrent_N = {len(dfISINCurrent)}")


    # # ISINs, bond_name, f3, f6  from bonds_archive
    # dfISINsArchive = db_panda_proc.read_table_by_sql_to_df_pandas(TB_BONDS_ARCIVE_, ['isin','bond_name','f3','f6','f5'])
    # if DEBUG_:
    #     print(f"dfISINsArchive = \n{dfISINsArchive}")
    #     print(f"dfISINsArchive_N = {len(dfISINsArchive)}")

    # # фильтруем , если f5 содержит 'BANKRUPT' - удаляем ряды
    # dfIsinNotBankrupt  = db_panda_proc.filter_df_with_str_fragm_by_one_col_and_one_cond (dfISINsArchive, 'f5', 'BANKRUPT', 'contain', invert = True)
    # if DEBUG_:
    #     print(f"dfIsinNotBankrupt = \n{dfIsinNotBankrupt}")
    #     print(f"dfIsinNotBankrupt_N = {len(dfIsinNotBankrupt)}")


    # # Фильтруем. оставляем только те isin, которые принадлежат множеству isin dfISINCurrent, находящихся в оперативной таблице bonds_curr
    # #  (с этой таблицей идут все действия по анализу текущих скаченных современных облигаций)
    # keyColAssocDic = {'isin':'isin'}
    # dfIsinNotBankruptCurr = db_panda_proc.drop_rows_from_df_by_ds_keys_pandas (dfIsinNotBankrupt, dfISINCurrent, keyColAssocDic, inverse = True )
    # if DEBUG_:
    #     print(f"dfIsinNotBankruptCurr = \n{dfIsinNotBankruptCurr}")
    #     print(f"dfIsinNotBankruptCurr_N = {len(dfIsinNotBankruptCurr)}")


    # # Фильтруем ряды. Оставляем те, в которых в поле f6 проставлен маркер NOT QUALIFIED
    # # фильтруем , если f5 содержит 'BANKRUPT' - удаляем ряды
    # dfIsinNotQualifed  = db_panda_proc.filter_df_with_str_fragm_by_one_col_and_one_cond (dfIsinNotBankruptCurr, 'f6', 'NOT QUALIFIED', 'contain')
    # if DEBUG_:
    #     print(f"dfIsinNotQualifed = \n{dfIsinNotQualifed}")
    #     print(f"dfIsinNotQualifed_N = {len(dfIsinNotQualifed)}")


    # path = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/proj_docs/test1.ods'

    # LibreCalcPandasDB.write_from_df_to_exel_pandas (dfIsinNotQualifed, path, startCell = [3,3])


    # # ПРОРАБОТКА: Считывание таблцы в pandas dataFrame

    # import pandas as pd
    # path = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/proj_docs/test1.ods'
    # sales = pd.read_excel(path, sheet_name = 'Sheet1')












    # # ПРОРАБОТКА create_df_from_calc_rng_name_of_given_file_and_sheet: Считывание данных из таблицы в фрейм
    
    # file = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/proj_docs/20221209-emidocs-default.xlsx'
    # shName = 'emidocs-default'
    # rngName = 'A2:C204'
    # colNames = ['name','inn', 'isin'] # Название колонок в фрейме

    # loCalcPandas = LibreCalcPandasDB()
    # dfInnBankrots = loCalcPandas.create_df_from_calc_rng_name_of_given_file_and_sheet (file, shName, rngName, colNames)
    # print(f"dfInnBankrots = \n{dfInnBankrots}")














