
from noocube.bonds_main_manager import BondsMainManager
from noocube.files_manager import FilesManager
import time

class DataFrameFieldsCalcFuncs():
    """Класс для функций калькулции полей в разных проектах для фреймов"""

    def __init__(self): 
        pass

    @staticmethod
    def calc_convert_col_class_id_to_class_name (df, **lambOutArgs):
        """
        DataFrameFieldsCalcFuncs
        Конвертация колонки classId (в фрейме имя - 'Класс' в название класса функции в ту же коллонку) (Конвертация - псевдо. Сначала создается новая колонка, затем перемещается на
        место исходной. Таким образом чуть сокращается время процедуры. Примерно на 0.2 сек)
        Project: Анализ функций в пакете ~ /home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/funcs_analyzer_manager.py
        ПРИМ: Для нового подхода в расчетных колонках фрейма

        Если  поставить в colTrg = 'Класс' название новой колокни, например, 'Название класса', то должна появиться новая колонка с этим названием (НЕ ПРОТЕСТИРОВАНО)
        Category: Калькуляторы полей
        """

        print('------START: calc_convert_col_class_id_to_class_name() | noocube/df_fields_calc_funcs.py')
        
        # start_time = time.time()
        
        dBase = '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/db.sqlite3'
        bmm = BondsMainManager(dBase)
        tbClasses = 'funcs_analyzer_classes'
        dfClasses = bmm.read_table_by_sql_to_df_pandas(tbClasses, ['id', 'class_name'])
        # bmm.print_df_gen_info_pandas_IF_DEBUG(dfClasses, True)
    
        def get_class_by_id_ (classId):
            """Получить класс через его id
            ПРИМ: !!! эта вспомогательная функция в частности для того, то бы первести classId в classId[0], так как в лямбда-функции выдается список !!!
            TODO: Придумать, как переходить от списка к самой велечине от classId в classId[0]
            """

            # pars:
            keyColName = 'id'
            resColName = 'class_name'
            className = bmm.get_col_name_val_by_key_col_name_val_pandas (dfClasses, keyColName, classId[0], resColName)
            return className
        
        colTrg = 'Класс' # Если тут поставить название новой колокни, например, 'Название класса', то должна появиться новая колонка с этим названием (НЕ ПРОТЕСТИРОВАНО)
        lambFunc = get_class_by_id_
        listLambArgs = ['Класс']
        lambOutArgs ={}
        
        df = bmm.convert_or_add_calc_col_in_df_by_lambda_func_with_args_pandas_v2(df, colTrg, lambFunc, listLambArgs, **lambOutArgs)
        
        # ПОКА НЕ УДАЛЯТЬ !!! Переместить новую колонку, которая в конце, на место исходной колонки 'Класс' и затем удалить последнюю. И переименовать новую в изначальнео имя 'Класс'
        # df = BondsMainManager.replace_col_name_by_last_col_in_df (df, 'Класс')


        # import pandas as pd
        # pd.set_option('display.max_columns', None)
        # print (f"$$$$$$$$$$$$$$$$$    @@@@@@@@@@@@@2222      %%%%%%%%%%%%%%%%%%%%%   df = {df}")
        
        # print("---TTTTTTTTTTTTTTTTTTTTTTT ------ calc_convert_col_class_id_to_class_name() | noocube/df_fields_calc_funcs.py %s seconds ---" % (time.time() - start_time))
        
        print('------END: calc_convert_col_class_id_to_class_name() | noocube/df_fields_calc_funcs.py')
        return df



    @staticmethod
    def calc_convert_col_categ_id_to_categ_name (df, **lambOutArgs):
        """
        DataFrameFieldsCalcFuncs
        Конвертация колонки category_id_id c id категории в название категории из табл funcs_analyzer_categories 
        Project: Анализ функций в пакете ~ /home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/funcs_analyzer_manager.py
        ПРИМ: Для нового подхода в расчетных колонках фрейма

        Если  поставить в colTrg = 'Класс' название новой колокни, например, 'Название класса', то должна появиться новая колонка с этим названием (НЕ ПРОТЕСТИРОВАНО)
        Category: Калькуляторы полей
        """

        print('------START: calc_convert_col_class_id_to_class_name() | noocube/df_fields_calc_funcs.py')
        
        dBase = '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/db.sqlite3'
        bmm = BondsMainManager(dBase)
        tbCategs = 'funcs_analyzer_categories' # должны быть абсолютные навания таблиц, так как этот класс - в пакете Noocube
        dfCategs = bmm.read_table_by_sql_to_df_pandas(tbCategs, ['id', 'category'])
        # bmm.print_df_gen_info_pandas_IF_DEBUG(dfClasses, True)
    
        def get_categ_by_id_ (categId):
            """Получить категорию через его id
            ПРИМ: !!! эта вспомогательная функция в частности для того, то бы первести classId в classId[0], так как в лямбда-функции выдается список !!!
            TODO: Придумать, как переходить от списка к самой велечине от classId в classId[0]
            """

            # pars:
            keyColName = 'id'
            resColName = 'category'
            categName = bmm.get_col_name_val_by_key_col_name_val_pandas (dfCategs, keyColName, categId[0], resColName)
            return categName
        
        colTrg = 'Категория' # Если тут поставить название новой колокни, например, 'Название класса', то должна появиться новая колонка с этим названием (НЕ ПРОТЕСТИРОВАНО)
        lambFunc = get_categ_by_id_
        listLambArgs = ['Категория']
        lambOutArgs ={}
        
        df = bmm.convert_or_add_calc_col_in_df_by_lambda_func_with_args_pandas_v2(df, colTrg, lambFunc, listLambArgs, **lambOutArgs)
        
        # ПОКА НЕ УДАЛЯТЬ !!! Переместить новую колонку, которая в конце, на место исходной колонки 'Класс' и затем удалить последнюю. И переименовать новую в изначальнео имя 'Класс'
        # df = BondsMainManager.replace_col_name_by_last_col_in_df (df, 'Класс')


        # import pandas as pd
        # pd.set_option('display.max_columns', None)
        # print (f"$$$$$$$$$$$$$$$$$    @@@@@@@@@@@@@2222      %%%%%%%%%%%%%%%%%%%%%   df = {df}")
        
        # print("---TTTTTTTTTTTTTTTTTTTTTTT ------ calc_convert_col_class_id_to_class_name() | noocube/df_fields_calc_funcs.py %s seconds ---" % (time.time() - start_time))
        
        print('------END: calc_convert_col_class_id_to_class_name() | noocube/df_fields_calc_funcs.py')
        return df







    @staticmethod
    def calc_convert_col_with_full_path_to_file_name(df, **lambOutArgs):
        """
        DataFrameFieldsCalcFuncs
        Конвертация колонки fpath (в фрейме имя - 'Файл' в имя файла в ту же коллонку)
        Project: Анализ функций в пакете ~ /home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/funcs_analyzer_manager.py
        ПРИМ: Для нового подхода в расчетных колонках фрейма
        Если  поставить в colTrg = 'Файл' название новой колокни, например, 'Название файла', то должна появиться новая колонка с этим названием (НЕ ПРОТЕСТИРОВАНО)
        Category: Калькуляторы полей
        """

        print('------START: calc_convert_col_with_full_path_to_just_file_name() | noocube/df_fields_calc_funcs.py')
        
        dBase = '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/db.sqlite3'
        bmm = BondsMainManager(dBase)
        
        def get_file_name_from_path_ (path):
            """Получить название файла из пути к нему
            ПРИМ: !!! эта вспомогательная функция в частности для того, то бы первести path в path[0], так как в лямбда-функции выдается список !!!
            TODO: Придумать, как переходить от списка к самой велечине от path в path[0]
            """
            
            fileName = FilesManager.get_file_name_from_path(path[0])
            
            return fileName

        # Pars:
        colTrg = 'Файл' # Если тут поставить название новой колокни, например, 'Название файла', то должна появиться новая колонка с этим названием (НЕ ПРОТЕСТИРОВАНО)
        lambFunc = get_file_name_from_path_
        listLambArgs = ['Файл']
        lambOutArgs ={}

        df = bmm.convert_or_add_calc_col_in_df_by_lambda_func_with_args_pandas_v2(df, colTrg, lambFunc, listLambArgs, **lambOutArgs)
        
        print('------END: calc_convert_col_with_full_path_to_just_file_name() | noocube/df_fields_calc_funcs.py')
        return df



    @staticmethod
    def calc_convert_col_with_atributes_delete_apostrophs(df, **lambOutArgs):
        """
        DataFrameFieldsCalcFuncs
        Конвертация колонки 'Аргументы' (удаление апострофов в названии аргументов)
        ПРИМ: Для нового подхода в расчетных колонках фрейма
        Project: Анализ функций в пакете ~ /home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/funcs_analyzer_manager.py
        Если  поставить в colTrg = 'Файл' название новой колокни, например, 'Название файла', то должна появиться новая колонка с этим названием (НЕ ПРОТЕСТИРОВАНО)
        Category: Калькуляторы полей
        """

        print('------START: calc_convert_col_with_atributes_delete_apostrophs() | noocube/df_fields_calc_funcs.py')
        
        dBase = '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/db.sqlite3'
        bmm = BondsMainManager(dBase)
        
        def clear_apostrophes_in_arguments_ (atrubutes):
            """Получить название файла из пути к нему
            ПРИМ: !!! эта вспомогательная функция в частности для того, то бы первести path в path[0], так как в лямбда-функции выдается список !!!
            TODO: Придумать, как переходить от списка к самой велечине от path в path[0]
            """
            
            atrubutes = atrubutes[0].replace("'","")
            
            return atrubutes

        # Pars:
        colTrg = 'Аргументы' # Если тут поставить название новой колокни, например, 'Название файла', то должна появиться новая колонка с этим названием (НЕ ПРОТЕСТИРОВАНО)
        lambFunc = clear_apostrophes_in_arguments_
        listLambArgs = ['Аргументы']
        lambOutArgs ={}

        df = bmm.convert_or_add_calc_col_in_df_by_lambda_func_with_args_pandas_v2(df, colTrg, lambFunc, listLambArgs, **lambOutArgs)
        
        print('------END: calc_convert_col_with_atributes_delete_apostrophs() | noocube/df_fields_calc_funcs.py')
        return df





    @staticmethod
    def calc_convert_col_with_class_first_class_make_bold(df, **lambOutArgs):
        """
        DataFrameFieldsCalcFuncs
        Конвертация колонки 'Классы' (сделать первый класс - bold)
        ПРИМ: Для нового подхода в расчетных колонках фрейма
        Project: Анализ функций в пакете ~ /home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/funcs_analyzer_manager.py
        Если  поставить в colTrg = 'Файл' название новой колокни, например, 'Название файла', то должна появиться новая колонка с этим названием (НЕ ПРОТЕСТИРОВАНО)
        Category: Калькуляторы полей
        """

        print('------START: calc_convert_col_with_class_first_class_make_bold() | noocube/df_fields_calc_funcs.py')
        
        dBase = '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/db.sqlite3'
        bmm = BondsMainManager(dBase)
        
        def diff_first_calss_and_parent_class_by_bold_ (classes):
            """Получить название файла из пути к нему
            ПРИМ: !!! эта вспомогательная функция в частности для того, то бы первести path в path[0], так как в лямбда-функции выдается список !!!
            TODO: Придумать, как переходить от списка к самой велечине от path в path[0]
            """
            
            classesParts = classes[0].split(',')
            firstClass = '<b>' + classesParts[0] + '</b>'
            
            # print(f"@@@@@@@@@@@@@@@@@@@@@@@@ firstClass = {firstClass}")
            
            otherClassesLine = ''
            for otherClass in classesParts [1:]:
                otherClassesLine += otherClass +  '<br>'
                
            resClasses = firstClass + '<br>' + otherClassesLine
            
            # print(f"@@@@@@@@@@@@@@@@@@@@@@@@ resClasses = {resClasses}")

            return resClasses

        # Pars:
        colTrg = 'Класс' # Если тут поставить название новой колокни, например, 'Название файла', то должна появиться новая колонка с этим названием (НЕ ПРОТЕСТИРОВАНО)
        lambFunc = diff_first_calss_and_parent_class_by_bold_
        listLambArgs = ['Класс']
        lambOutArgs ={}

        df = bmm.convert_or_add_calc_col_in_df_by_lambda_func_with_args_pandas_v2(df, colTrg, lambFunc, listLambArgs, **lambOutArgs)
        
        print('------END: calc_convert_col_with_class_first_class_make_bold() | noocube/df_fields_calc_funcs.py')
        return df







if __name__ == '__main__':
    pass


