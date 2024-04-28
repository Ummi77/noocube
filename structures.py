

class SelectUnionStructure ():
    """
    Структура для задания параметров для метода select_tbs_union() в sql_syntaxer.py
    Собственными переменными являются : название таблицы, название полей для выборки из этой таблицы и название типа записей, вытягиваемых из
    данной таблицы, уловия для части WHERE запроса
    """

    def __init__(self, tbName, selFields, whereCond, type):
        self.tbName = tbName
        self.selFields = selFields
        self.whereCond = whereCond
        self.type = type
        
        


class MarkFileParagraph ():
    """
Структура для обьектов , rоторые содержат стринговый поисковый фрагмент (strMarker) в тексте. Путь файла (file) , в котором содержится 
найденный фрагмент txtBlock.

Используются, в частности, при поиске мемов в текстовом файле и возвращении абзаца, в котором найден стринговый поисковый маркер
    """

    def __init__(self, strMarker, file, txtBlock):
        self.strMarker = strMarker
        self.file = file
        self.txtBlock = txtBlock

        




# class LambdaFunctionTbUpdateParams ():
#     """
#     Параметры для лфмбда -функции для обновления полей в таблице методом update_tb_col_by_lambda_pandas () в sqlite_pandas_processor.py
#     """

#     def __init__(self, lFunc, dictAssocArgs):
#         # self.tbName = tbName
#         # self.colUpd = colUpd
#         self.lFunc = lFunc
#         self.dictAssocArgs = dictAssocArgs



# class WhereStructure ():
#     """
#  ЗАГОТОВКА
#     Структура для задания параметров WHERE при формировании SQL-запроса в sql_syntaxer.py
#     Собственными переменными являются : 
#     """

#     def __init__(self):
#         pass
    
    
    
    

        # """
        # conds - список с условиями типа {
        #                                     'OR' : [['fieldName1', '<', 5], ['fieldName2', '>', 15]], 
        #                                     'AND' : [['fieldName3', '<', 5], ['fieldName4', '>', 15]], /
        #                                     'ONE'  : ['fieldName1', '<', 5],/
        #                                     'ALL or NO'   : None, / <или иначе - без всяких условий>
        #                                     'STR' : '(fieldName1 > 5 AND fieldName2 < 15) AND (...)'
        #                                     }# -- ЗАПРОСЫ JOIN ------
        #         Если conds = {} или не заданы вовсе (по умолчанию {}), то SELECT sql формируется без условий WHERE


        #     Returns:
        #         _type_: _description_
        #     """
        


# class OrderByStructure ():
#     """
#     Структура для задания параметров ORDER BY в SQL-запросах
#     """

#     def __init__(self, byFields, order = 'ASC'):
#         self.byFields = byFields
#         self.order = order
















