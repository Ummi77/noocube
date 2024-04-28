

from noocube.sql_syntaxer import SQLSyntaxer
# from project_tlh.projr.classes.sqlite_proc_tlh import SqliteProcessorTLH  
import re
from noocube.sqlite_pandas_processor import SqlitePandasProcessor
# from bonds.sqlite_pandas_processor import SqliteProcessor # PREVIOUS
from noocube.re_manager import ReManager
from noocube.re_constants import *
# from project_tlh.projr.settings import DB_TLH_

# class SearchManagerDB (SqliteProcessor): # PREVIOUS
class SearchManagerDB (SqlitePandasProcessor):
    """Класс для осуществеления различных вариантов поиска по БД"""




    def __init__(self, dbName):
        # SqliteProcessor.__init__(self,dbName) # PREVIOUS
        SqlitePandasProcessor.__init__(self,dbName)





    def full_text_search_in_FTS_DB_with_df(self, tbFTS, srchStr, getFields, ftsInterpretor, regexFields = None):
        """
        SearchManagerDB
        Осуществляет полнотекстовый поиск (FULL TEXT SEARCH, FTS) по виртуальной таблице в оперативной памяти по искомому выражению с MATCH оператором в SELECT
        criterias - список полей, в которых осуществляется поиск srchStr в заданной таблице
        srchStr - поисковая строка
        getFields - список выводимых полей
        Category: Full Text Search поиск
        """
        #TODO: Пока простое выражение = входной поисковой строке с сайта. Сделать класс FullTextSearch, в котором входная поисковая строка будет трансформироваться 
        # в полноценное выражение для MATCH со своим микро-языком (типа, + - и т.д.  будут расшифровываться для формирования полноценного выражения для MATCH)

        print (f"InterpretorFTS in  full_text_search_in_FTS_DB ()= {ftsInterpretor}")
        # Переключаем Интерпретатор поисковой строки в зависимости от выбранной радио-батон на странице 
        if ftsInterpretor == 'local': # Если нажата опция локального интерпретатора

            srchStrCleared = srchStr.replace('AND', '+').replace('NOT','-') # Защита, если перепутаны форматы

            matchExpr = self.FTS_search_str_interpretor_v01(srchStr)
        elif ftsInterpretor == 'FTS': # Если вывбран встроенный интерпретатор FTS5

            srchStrCleared = srchStr.replace('+', 'AND').replace('-','NOT') # Защита, если перепутаны форматы
            matchExpr = srchStrCleared


        else: # Если опшибка или не выбрана По умолчанию вывбирается локальный интерпертатор
            matchExpr = self.FTS_search_str_interpretor_v01(srchStr) 

        print (f"matchExpr = {matchExpr}")
        # matchExpr = srchStr
        
        # Pars: 
        # getFields = ['id', 'bl_title', 'bl_rest', 'full_path']
        # selFirstPart = f"highlight({tbFTS}, 5, '<b>', '</b>')"
        conds = {'ONE' : [tbFTS,'MATCH', matchExpr]}




        if ftsInterpretor == 'regex': # Если интерпретатор regexp, то подключаем поисковик REGEX
            #TODO: Потом унверсализировать для любых БД, таблиц и полей 
            matchExpr = srchStr
            # Подключение поисковика REGEXP
            # regexFields = ['bl_title','bl_rest']
            conds = {'OR' : [['bl_title','REGEXP', matchExpr], ['bl_rest','REGEXP', matchExpr]]}

        else: # Если интерпретатор не regexp, во всех остальных случаях идет поиск по FTS Match
            # selFirstPart = f"highlight({tbFTS}, 5, '<b>', '</b>')"
            conds = {'ONE' : [tbFTS,'MATCH', matchExpr]}


        # TODO: Сделать получение фрейма по SQL запросу !!! Инае приходит list
        # dsRes = self.select_from_table_with_where_condition(tbFTS, getFields, conds) # Выборка по заданным парамметрам  # PREVIOUS
        sql = SQLSyntaxer.select_from_table_with_where_condition_sql(tbFTS, getFields, conds)

        dfRes = self.read_sql_to_df_pandas(sql)  # NEW

        return dfRes



    def full_text_search_in_FTS_DB(self, tbFTS, srchStr, getFields, ftsInterpretor, regexFields = None):
        """
        OBSOLETED. используется в проекте TLH 
        SearchManagerDB
        Осуществляет полнотекстовый поиск (FULL TEXT SEARCH, FTS) по виртуальной таблице в оперативной памяти по искомому выражению с MATCH оператором в SELECT
        criterias - список полей, в которых осуществляется поиск srchStr в заданной таблице
        srchStr - поисковая строка
        getFields - список выводимых полей
        Category: Full Text Search поиск
        """
        #TODO: Пока простое выражение = входной поисковой строке с сайта. Сделать класс FullTextSearch, в котором входная поисковая строка будет трансформироваться 
        # в полноценное выражение для MATCH со своим микро-языком (типа, + - и т.д.  будут расшифровываться для формирования полноценного выражения для MATCH)

        print (f"InterpretorFTS in  full_text_search_in_FTS_DB ()= {ftsInterpretor}")
        # Переключаем Интерпретатор поисковой строки в зависимости от выбранной радио-батон на странице 
        if ftsInterpretor == 'local': # Если нажата опция локального интерпретатора

            srchStrCleared = srchStr.replace('AND', '+').replace('NOT','-') # Защита, если перепутаны форматы

            matchExpr = self.FTS_search_str_interpretor_v01(srchStr)
        elif ftsInterpretor == 'FTS': # Если вывбран встроенный интерпретатор FTS5

            srchStrCleared = srchStr.replace('+', 'AND').replace('-','NOT') # Защита, если перепутаны форматы
            matchExpr = srchStrCleared


        else: # Если опшибка или не выбрана По умолчанию вывбирается локальный интерпертатор
            matchExpr = self.FTS_search_str_interpretor_v01(srchStr) 

        print (f"matchExpr = {matchExpr}")
        # matchExpr = srchStr
        
        # Pars: 
        # getFields = ['id', 'bl_title', 'bl_rest', 'full_path']
        # selFirstPart = f"highlight({tbFTS}, 5, '<b>', '</b>')"
        conds = {'ONE' : [tbFTS,'MATCH', matchExpr]}




        if ftsInterpretor == 'regex': # Если интерпретатор regexp, то подключаем поисковик REGEX
            #TODO: Потом унверсализировать для любых БД, таблиц и полей 
            matchExpr = srchStr
            # Подключение поисковика REGEXP
            # regexFields = ['bl_title','bl_rest']
            conds = {'OR' : [['bl_title','REGEXP', matchExpr], ['bl_rest','REGEXP', matchExpr]]}

        else: # Если интерпретатор не regexp, во всех остальных случаях идет поиск по FTS Match
            # selFirstPart = f"highlight({tbFTS}, 5, '<b>', '</b>')"
            conds = {'ONE' : [tbFTS,'MATCH', matchExpr]}


        # TODO: Сделать получение фрейма по SQL запросу !!! Инае приходит list
        dsRes = self.select_from_table_with_where_condition(tbFTS, getFields, conds) # Выборка по заданным парамметрам  # PREVIOUS
        # sql = SQLSyntaxer.select_from_table_with_where_condition_sql(tbFTS, getFields, conds)

        # dfRes = self.read_sql_to_df_pandas(sql)  # NEW

        return dsRes





    def FTS_search_str_interpretor_v01 (self, srchStr):
        """
        Интерпретатор поисковой строки srchStr с сайта для составления выражения для match на основе
        Правила для локального интерпретатора на данный момент разработки:
        1. Если нет разделителей и групп . заключенных в куругдые скобки, то весь набор слов считается одной фразой и ищется полное ее соответствие
        2. Если есть хоть один разделитель- логическая связка из множества [+-], то все слова в фразе становятся независимыми и разделители трансформируются в 
        соотвтествующие логические операторы FTS5 [AND, NOT] <OR пока не реализовано>
        3. Если найдены круглые скобки , то ничего не происходит. Просто распечатка <реализовать>
        
        Category: Full Text Search поиск
        
        """

        # Анализируем поисковую строку, вводя свои правила преобразования этой строки для последующего поиска через MATCH оператор
        # Правило 1. Если просто слова с пробелами. Пробелы рассматриваются как соединение слов в одну поисковую фразую
        # Анализируем разделители, которые возможны Это - (+, - , &, AND, |, OR и круглые скобки)

        # 1. Поиск скобок
        # ЗАГОТОВКА - https://stackoverflow.com/questions/24696715/regex-for-match-parentheses-in-python

        # 2. Обьедлинение фразы с пробелами в выражение с несколькими токенами (выражение должно быть заключено в двойные кавычки, тогда MATCH будет искать полный комплекс токенов)

        re_mangr = ReManager()

        if_paranthis = re_mangr.regex_filter(srchStr, PARANTHIS_EXPR_) # Есть ли скобки (*)
        print (f"if_paranthis = {if_paranthis}")
        # A. Анализ на наличие круглых скобок
        if not if_paranthis: # Если в поисковой строке srchStr нет круглых скобок, то анализируем разделители только токенов (логических обьединений значит нет)

            pass
            # B. Анализ разделителей между токенами
            # mo = re.search(NOT_FTS_DELIMETERS_,srchStr)
            if_fts_delimiters = re_mangr.regex_filter(srchStr, FTS_DELIMETERS_) # Есть нет разделителей FTS

            # print (f"mo={mo}")

            # if mo:
            #     return True
            # else:
            #     return False

            if not if_fts_delimiters : # Если нет разделителей FTS locale. Пока : (+-)

                print (f"if_fts_delimiters = {if_fts_delimiters}")
                print(f"Найдены шруппы в круглых скобках")

                match_expr = f"\"{srchStr}\"" # Просто  добавляем двойные кавычки и MATCH расшифровывает фразу внутри двойных кавычек как единый токен

                return match_expr



            else: # если обнаружены FTS разделители [+-]

                print (f"if_fts_delimiters = {if_fts_delimiters}")
                print(f"Обнаружены разделители [+-]")


                # Дальнейший анализ и парсинг поискового слова
                print (f"Необходим дальнейший парсинг поискового выражения")

                # Заменяем [+-] на [AND NOT ]
                match_expr = srchStr.replace('+', '').replace('-', 'NOT') # Просто не добавляем двойные кавычки и MATCH расшифровывает пробелы как AND, разделяя каждое слово в фразе как отдельный токен
                return match_expr
                


        else: # Если обнаружены скобки
            print(f"Обнаружены группы в круглых скобках")



if __name__ == '__main__':
    pass



    # # ПРИМЕР: Проработка FTS_match_locale_syntax

    #     # Проверка круглых скобок
    #     srchStr = "dsjng84  kjnds  (sdg)  oiefj"
    #     re_mangr = ReManager()
    #     if_paranthis = re_mangr.regex_filter(srchStr, PARANTHIS_EXPR_) # Есть ли скобки (*)
    #     print (f"if_paranthis = {if_paranthis}")



    # srchMngrDB = SearchManagerDB(DB_TLH_)
    # # srchStr = "a + copy + of"
    # srchStr = "a copy of"


    # srchMngrDB.FTS_search_str_interpretor_v01(srchStr)

    # # match_expr = srchMngrDB.FTS_match_locale_syntax_expr_for_srch_str(srchStr)
    # # print (match_expr)













