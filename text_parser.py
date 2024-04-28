

from noocube.re_manager import ReManager
from noocube.re_constants import *

class TextParser ():
    """ 
    Класс для парсинга текстов 
    """



    def __init__(self): # создание обьекта без конкретной ссылки 
        pass


    @staticmethod
    def get_mono_tags_parser(txt, tag, resDim = '*'):
        """
        TextParser
        Найти заданные одиночные тэги в тексте
        # ПРИМ: Тэг  не должен иметь пробелов вначале
        resDim - ограничение в размере выходного списка, целое число int. если '*' -  то все элементы. По умолчанию - все элементы. 
        Categ: Парсинг текста
        """ 
        
        # matches = ReManager.find_line_with_marker(txt, tag)
        regExpr = ReManager.replace_marker_inside_regex(INEER_OF_MONO_TAG_, '%TAG%', tag)
        matches = ReManager.find_all_matches_from_text(txt, regExpr)
        
        if isinstance(resDim,str) and '*' in resDim: # - значит стоит звездочка и значит показываем все элементы
            pass
        else: # Значит число - размер выходного списка совпадений matches
            matches = matches[:resDim]
        
        # print(f"$$$$$$$$$$$$$$$$ maches = {matches}")
        # tagInner = matches[0].replace(f'{tag}','').replace('<','').replace('>','').strip()
        
        return matches
    
    
    

    @staticmethod
    def get_double_tags_parser(txt, tag, resDim = '*'):
        """
        TextParser
        Найти заданные двойные тэги в тексте (в частности, допустим , тэг открытия и тэг закрытия типа <table> ... </table>)
        ПРИМ: Тэг открытия не должен иметь пробелов вначале, а тэг закрытия - вообще не должен иметь пробелов
        resDim - ограничение в размере выходного списка, целое число int. если '*' -  то все элементы. По умолчанию - все элементы. 

        Categ: Парсинг текста
        """ 
        
        # matches = ReManager.find_line_with_marker(txt, tag)
        regExpr = ReManager.replace_marker_inside_regex(INNER_CONTIN_OF_DOUBLE_TAG_, '%TAG%', tag)
        matches = ReManager.find_all_matches_from_text(txt, regExpr)
        
        if isinstance(resDim,str) and '*' in resDim: # - значит стоит звездочка и значит показываем все элементы
            pass
        else: # Значит число - размер выходного списка совпадений matches
            matches = matches[:resDim]
            
        # print(f"$$$$$$$$$$$$$$$$ maches = {matches}")
        # tagInner = matches[0].replace(f'{tag}','').replace('<','').replace('>','').strip()
        
        return matches
    
    
    
    def get_inside_of_mono_tags_result_dim_in_text_parser(txt, tag, resDim = '*'):
        """
        TextParser
        Получить содержаний внутренностей моно тэгов идущих по порядку в тксте. Размер списка определяется размерностью resDim
        resDim - ограничение в размере выходного списка, целое число int. если '*' -  то все элементы. По умолчанию - все элементы. 
        
        """
        
        tagMatches = TextParser.get_mono_tags_parser(txt, tag, resDim)
        
        tagInnerMatches = [x.replace(f'<{tag}','').replace('<','').replace('>','').strip() for x in tagMatches]
        
        return tagInnerMatches
        
        


    @staticmethod
    def get_contents_between_double_tags_parser(txt, tag, resDim = '*'):
        """
        НЕ ТЕСТИРОВАНО
        TextParser
        Найти конструкции из открывающего и закрывающего тэга 
        resDim - размерность вырезки из списка всех найденных конструкций. По умолчанию = 1, то есть из списка бкрется первый элемент
        Categ: Парсинг текста
        """ 
        
        tagMatches = TextParser.get_double_tags_parser(txt, tag, resDim)
        
        tagInnerMatches = [x.replace(f'<{tag}','').replace(f'{tag}>','').strip() for x in tagMatches]
        
        return tagInnerMatches
    
    
    @staticmethod
    def get_tds_in_first_row_of_tbody_from_table_html (tableHtmlWithTbody):
        """
        TextParser
        Получить тэги <td> с их содержимым в первой строке <tr> из тела таблицы <tbody>. А так же их кол-во
        tableHtmlWithTbody - полный код таблицы или ее часть , с полным содержимым между тэгами <tbody> ... </tbody>, включая тэги тела таблицы
        """

        tbodyMatchesHtml = TextParser.get_double_tags_parser(tableHtmlWithTbody, 'tbody')[0]
        
        trMatchesHtml = TextParser.get_double_tags_parser(tbodyMatchesHtml, 'tr')[0]
        
        tdList =  TextParser.get_double_tags_parser(trMatchesHtml, 'td')
        
        tdQn = len(tdList)
        
        return tdList, tdQn





if __name__ == "__main__":
    pass



    # # ПРОВЕРКА: Получение контента между открывающим и закрывающим одним и тем же тэгом (double tag)
    
    # txt = """<div class="table-responsive">
    #         <table class="table text-center table-bordered table-striped">
    #         <thead>
    #             <tr>
    #             <th style="width: 34%;"></th>
    #             <th style="width: 22%;">Free</th>
    #             <th style="width: 22%;">Pro</th>
    #             <th style="width: 22%;">Enterprise</th>
    #             </tr>
    #         </thead>
    #         <tbody>
    #             <tr>
    #             <th scope="row" class="text-start">Public</th>
    #             <td style = "text-align:left;font-weight: bold;"><svg class="bi" width="24" height="24"><use xlink:href="#check"/></svg></td>
    #             <td style = "text-align:left"><svg class="bi" width="24" height="24"><use xlink:href="#check"/></svg></td>
    #             <td style = "text-align:left"><svg class="bi" width="24" height="24"><use xlink:href="#check"/></svg></td>
    #             <td style = "text-align:left"><svg class="bi" width="24" height="24"><use xlink:href="#check"/></svg></td>
    #             <td style = "text-align:left"><svg class="bi" width="24" height="24"><use xlink:href="#check"/></svg></td>
    #             <td style = "text-align:left"><svg class="bi" width="24" height="24"><use xlink:href="#check"/></svg></td>
    #             </tr>
    #         </tbody>

    #         </table>
    #     </div>"""
    
    # tdList, tdQn = TextParser.get_tds_in_first_row_of_tbody_from_table_html(txt)

    # print(f"tdQn = {tdQn}")
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    








