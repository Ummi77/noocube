# Для ошибок from bonds.exceptions import *

def exception_factory(exception, message):
    """Метод обработки ошибок / from bonds.exceptions import *
    
    ПРИМЕР использования:
    
    try:
        prevColsNames = list(map(dfColsNames.__getitem__, changeIndices))
    except Exception as err:
        raise  exception_factory(AssocDicConversionIndicesToNamesAssocDic, "method() / module/ relative_file / project_name_dir")
            
    """
    
    return exception(message)



class AddCalculatedColumnErr(Exception):
    """Ошибка,связанная с добавлением калькулируемой колонки в dataFrame"""
    pass



class AssocDicConversionIndicesToNamesAssocDic(Exception):
    """Ошибка,связанная с конвертированием словаря соответствий , основанного на индексах колонок в фрейме и их новыми названиями в словарь , основанный на именах колонок и новых названий
    в методе convert_assoc_dic_from_indices_to_name_based_pandas() / OutputPandasManager
    /home/ak/projects/3_Proj_Bonds_HTML_Center/project_bonds_html/projr/classes/output_pandas_manager.py"""
    pass



class AssocDicToRenameNotEqualByStructure(Exception):
    """Ошибка возможно связанная с неравенством элементов в двух словарях для переименования колонок в фрейме
    в методе rename_cols_by_associate_dic_type2_pandas() | /home/ak/projects/3_Proj_Bonds_HTML_Center/project_bonds_html/projr/classes/pandas_manager.py
    """
    pass




class SQLInsert(Exception):
    """
    Ошибка INSERT SQL execution to BD
    """

    def __init__(self, message):
        print("PR_497 --> Ошибка выполнения SQL - запроса типа INSERT ...")
        print(f"PR_498 --> {message}")





class SQLExec(Exception):
    """
    Ошибка выполнения SQL-запроса
    """

    def __init__(self, message):
        print("PR_504 --> Ошибка выполнения SQL-запроса")
        print(f"PR_505 --> {message}")












