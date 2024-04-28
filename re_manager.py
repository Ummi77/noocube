
# import bonds.re_manager as RE
# from bonds.re_manager import ReManager

import re
from noocube.files_manager import FilesManager
# from bonds.re_constants import *
from noocube.structures import MarkFileParagraph
from noocube.text_formater import TextFormater
from noocube.mem_manager import MemManager
from noocube.re_constants import *


class ReManager():
    """Класс для методов работы с регулярными выражениями
    If you really need True or False, just use bool : bool(re.search("hi", "abcdefghijkl"))
    """

    def __init__(self): # По умолчанию ссылка = https://smart-lab.ru/q/bonds/
        pass

    @staticmethod
    def regex_filter(val, rExpr = '.*'):
        """
        Функция для использования для фильтрации по массивам или фреймам или просто стрингам
        myregex - регулярное выражение, которое по умолчанию задано для любой String
        https://stackoverflow.com/questions/15325182/how-to-filter-rows-in-pandas-by-regex/48884429#48884429
        Category: Регулярные выражения
        """
        # rExpr = 'http.*\d$'
        if val:
            mo = re.search(rExpr,val)
            if mo:
                return True
            else:
                return False
        else:
            return False        


    @staticmethod
    def regex_serarch(val, rExpr = '.*'):
        """
        Функция для использования для фильтрации по массивам или фреймам или просто стрингам. Находит первое совпадение ??
        myregex - регулярное выражение, которое по умолчанию задано для любой String
        https://stackoverflow.com/questions/15325182/how-to-filter-rows-in-pandas-by-regex/48884429#48884429
        Category: Регулярные выражения
        """
        # rExpr = 'http.*\d$'
        mo = re.search(rExpr,val)    
        return mo


    @staticmethod
    def find_pos_of_element_in_paranthes(strInp):
        """
        Найти положение элемента, заключенного в скобки
        Category: Регулярные выражения
        """
        # s = "qwop(8)(9) 5"
        regex = re.compile("\(\d\)")
        match = re.search(regex, strInp)
        return match


    @staticmethod
    def find_pos_of_element_in_single_quotes(strInp):
        """
        Найти положение элемента, заключенного в скобки
        Category: Регулярные выражения
        """

        regex = re.compile("\'\d\'")
        match = re.search(regex, strInp)
        return match

    @staticmethod
    def find_pos_of_element_in_double_quotes(strInp):
        """
        ReManagerНайти положение элемента, заключенного в скобки
        Category: Регулярные выражения
        """

        regex = re.compile("\"\d\"")
        match = re.search(regex, strInp)

        return match


    @staticmethod
    def find_all_matches_from_text (txtInp, regExp, unique = False):
        """
        ReManager
        Найти все совпадения выражения regExp в тексте и вернуть список. Альтернативно - вернуть список только уникальных
        найденных значений по выражению. unique = True 
        Category: Регулярные выражения
        """

        if unique: # Если нужны уникальные значения в списке
            res = list(set(re.findall(regExp, txtInp, re.MULTILINE)))
        else:
            res = re.findall(regExp, txtInp, re.MULTILINE)
        
        return res


    @staticmethod
    def find_all_matches_from_file_text (filePath, regExp, unique = False):
        """
        ReManager
        Найти все совпадения выражения regExp в тексте файла и вернуть список. Альтернативно - вернуть список только уникальных
        найденных значений по выражению. 
        unique = True 
        Category: Регулярные выражения
        """

        fm = FilesManager(filePath)

        ftxt = fm.read_file_data_txt() # текст файла


        if unique: # Если нужны уникальные значения в списке
            res = list(set(re.findall(regExp, ftxt)))
        else:
            res = re.findall(regExp, ftxt)
        
        return res
    
    
    @staticmethod
    def find_all_given_mark_matches_from_txt_file_with_its_paragraphs_html (filePath, regExpMark = MEMS_WITH_FIGUR, qnParagrLines = 5, mem = '*'):
        """ 
        ReManager
        Найти параграфы в текстовом файле, в которых будет найден стринговый маркер, заданный регулярным выражением  regExpMark, с HtML-оформлением найденных параграфов. 
        Количество строк в параграфе, которые следуют за той строкой, в которой найден стринговый маркер regExpMark, определяется параметром qnParagrLines по умолчанию = 5.
        И вернуть список структур типа MarkFileParagraph. Класс структуры задан в /home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/structures.py
        Список структур, В которых найдены маркеры по формату равне искомому регулярному выражению regExpMark
        
        mem - заданный ммем для выделения в текстовом блоке. по умолчанию '*' - это значит все мемы (то есть не выделять ни одного)
        
        В частности, это используется при поиске мемов типа {Заглавные буквы / Цифры}. Но могут быть любые маркеры. 
        По умолчанию регулярное выражение равно поиску именно мемов типа  {Заглавные буквы / Цифры}
        Category: Регулярные выражения
        """
        from noocube.html_renderer import HTMLRenderer
        
        fm = FilesManager(filePath)
        fLines = fm.read_file_txt_lines() # текст файла
        totalMemParagrs = [] # Общий список стркутру параграфов с найденными в файле мемами (в которых указывается мем, файл и параграф с заданным кол-вом строк)
        for index, txtLine in enumerate(fLines):
            currLineMemsFound = re.findall(regExpMark, txtLine) # Мемы , найденные в текущей по циклу строке
            if len(currLineMemsFound) > 0: # Если в строке найден хоть один мем (но их может быть несколько в строке)
                for mem in currLineMemsFound: # для каждого мема, найденного в строке (а их может быть не только один, но несколько в строке)
                    paragraphLines = fLines[index: index + qnParagrLines]
                    memParagrphStr = '' # Текущий набор строк , формирующих параграф для той строки, в котором найден любой мем 
                    for pLine in paragraphLines: # pLine - строка из выделенного параграфа (параграф определяется текущей строкой и заданным прибавлением дополнительных строк qnParagrLines)
                        pLine = pLine.replace('\t','')
                        if pLine == '\n' : # Пропуск пустых строк с переносом строки
                            pass
                        else:
                            memParagrphStr += pLine
                            
                    # F. Сформировать обьект структуры класса MarkFileParagraph для каждого найденного мема
                    txtBlock = TextFormater.convert_str_lines_to_text_static(memParagrphStr) # Переводим линии в один текстовый блок
                    # G. Рендеринг текстового блока в формат HTML
                    txtBlock = HTMLRenderer.convert_TLHblock_to_HTMLblock(txtBlock)
                    # D. Выделить заданный мем в найденных параграфах
                    txtBlock = MemManager.highlight_mems_in_txt_for_html(txtBlock, mem, '#FF9C00')
                    memCurrParagr = MarkFileParagraph(mem, filePath, txtBlock)
                    # H. Сделать конкатинейт струтур memCurrParagr в список totalMemParagrs
                    totalMemParagrs.append(memCurrParagr)
                    
            else: # Если не найдено ни одного маркера (?)
                pass
            
        return totalMemParagrs
    
    
    @staticmethod
    def replace_by_regex_in_txt (txt, regExp, replaceStr):
        """ 
        ReManager
        Заместить найденные регулярные выражения regExp заданным стринговым значением replaceStr
        Category: Регулярные выражения
        """
        txt = re.sub(regExp, 
            replaceStr, 
            txt
        )
        
        return txt
    
    
    @staticmethod
    def replace_url_for_txt_lines_by_its_html_link (txt, regExp):
        """ 
        Проверенео
        ReManager
        Заместить найденные URL в строке текста ссылками в формате HTML этими же URL
        Ограничение: В одной строке может быть только одна URL. Если в однйо строке - несколько URL, то эта функция не годится!!!
        Category: Регулярные выражения
        """
        
        lines = TextFormater.get_str_lines_of_text_static (txt)
        newlines = [] # Набор строк после обработки
        for line in lines:
            href = ReManager.find_all_matches_from_text (line, regExp)
            if len(href) > 0: # Если найдена URL
                replaceStr = f'<a href="{href[0]}" target = "_blank">{href[0]}<a/>'
                newLine = ReManager.replace_by_regex_in_txt (line, regExp, replaceStr)
                newlines.append(newLine)
            else:
                newlines.append(line)

        newTxt = TextFormater.convert_str_lines_to_text_static(newlines) # Переводим линии в один текстовый блок    
        
        return newTxt
            
        
    @staticmethod
    def find_line_with_marker(txt, marker):
        """
        ReManager
        Найти строку в тексте , в которой присутствует заданный маркер (? или только букв и цифр - ПРОТЕСТИРОВАТЬ)
        Category: Регулярные выражения
        """
        
        regExpr = LINE_WITH_WORD_.replace('%WORD%', marker)
        matches = ReManager.find_all_matches_from_text (txt, regExpr)
        
        return matches
    
    
    @staticmethod
    def find_line_with_marker_single_res(txt, marker):
        """
        ReManager
        Найти строку в тексте , в которой присутствует заданный маркер (? или только букв и цифр - ПРОТЕСТИРОВАТЬ)
        Category: Регулярные выражения
        """
        
        regExpr = LINE_WITH_WORD_.replace('%WORD%', marker)
        matches = ReManager.find_all_matches_from_text (txt, regExpr)
        
        if len(matches) > 0:
            return matches[0]
        else:
            return None
    
    
    
        
        
    @staticmethod    
    def replace_marker_inside_regex(regex, marker, replaceVal):
        """
        Заменить маркер marker внутри тэга на заданное значение replaceVal
        Category: Регулярные выражения
        """    
        regex = regex.replace(marker, replaceVal)
        return regex
        
        
    


# ФУНКЦИИ КОНКРЕТНОГО ПРИМЕНЕНИЯ REGEX 

    @staticmethod
    def find_url_in_string(str):
        """
        ReManager
        Найти URL в строке
        Category: Регулярные выражения
        """

        href = re.search("(?P<url>https?://[^\s]+)", str).group("url")

        return href
    
    
    


    @staticmethod
    def remove_comments_type1(string):
        """ 
        ReManager       
        Удаляет все коменты с решеткой 
        Category: Регулярные выражения
        """
        pattern = r"(#.*)"
        return re.sub(pattern, "", string)



# END ФУНКЦИИ КОНКРЕТНОГО ПРИМЕНЕНИЯ REGEX 



    @staticmethod
    def if_string_contqin_regexp(strInp, reExpression):
        """
        ReManager
        Содержит ли стринг regexp-pattern?
        Category: Регулярные выражения
        """

        regexp = re.compile(reExpression)
        if regexp.search(strInp):
            return True
        else:
            return False



    
    @staticmethod
    def get_first_word_special_019(s):
        """ 
        Получить первое слово из строки для получения названия поля в фильтре в проекте 019
        https://stackoverflow.com/questions/48093746/find-first-word-in-string-python
        ПРИМ: '_' нужен для скрытых полей и прочих вспомогательных полей, где название поля разделяется с дополнительными вспомогательными суффиксами
        Точка нужна для сложных названий полей типа 'Тек.НКД' и пр
        """
        
        # p = r"[a-zA-Zа-яА-Я'._]+" # Ранее почему-то была такая формула, с точкой внутри скобок. Хотя точка является разделителем вроде. Но может есть и другие варианты. Пока не удалять
        p = r"[a-zA-Zа-яА-Я'_]+"
        m = re.search(p,s)
        print(f"PR_894 --> Regular Expr m = {m}")
        return m.group(0)





    @staticmethod
    def replace_last_right_charicters_with_group_of_simbols_rm_stat (searchedGroup, substitudeGroup, initialStringModel):
        """ 
        ReManager
        Заместить в заданном стринге группупоследовательности символов замещающей группой символов
        initialStringModel - изначальная стринговая модель
        searchedGroup - искомая группа последовательности символов, которая ищется в моделе strIniModel и  при нахождении нескольких 
        вариантов таких последовательностей, выбирает самую правую группу задаваемой последовательности, которая будет замещена на задаваемую 
        замещающую последовательность символов, равных по кол-ву в группе
        substitudeGroup - набор стринговыхсимволов, которыми будет замещена группа символов, равная по размерности, справа 
        (то есть , если будут найдены несколько соотвтетсвий равных поиску, для замещения будет задана та последовательность, которая находится крайней справа)
        

        """
        
        resultString = re.sub(f'{searchedGroup}$', substitudeGroup, initialStringModel)
        
        return resultString








if __name__ == '__main__':
    pass


    
    
    # # ПРОРАБОТКА: Функция замещения URL в текстовой строке с одной ссылкой на HTML-ссылку 
    
    # txt = """
    # ;;;; @@@ #################################### {COURSE_SHELF_1_} ####################################
    # ;;;; Информатика первого года, ФМХФ - семестр 1, лекция 3
    # https://www.youtube.com/watch?v=EKJW2OF8Og8&list=PLRDzFCPr95fKqdZFJ2dMt0jjkNLn1vzU8
    # >>>
    # --
    # ;;;; Как называть переменные / Григорий Петров / Правила культурного кода
    # https://www.youtube.com/watch?v=z5WkDQVeYU4&list=FLQfwKTJdCmiA6cXAY0PNRJw
    # >>>
    # --
    # """
    # # Pars:
    # regExp = URL_RE_
    
    # newTxt = ReManager.replace_url_for_txt_lines_by_its_html_link (txt, regExp)
    
    # print(f"newTxt = {newTxt}")
            
            
            
            
            



    # # ПРОРАБОТКА: find_all_given_mark_matches_from_txt_file_with_its_paragraphs ()
    # # Найти параграфы в текстовом файле, в которых будет найден стринговый маркер, заданный регулярным выражением  regExpMark. 
    # # Количество строк в параграфе определяется параметром qnParagrLines по умолчанию = 5. И вернуть список структур типа MarkFileParagraph
    
    # # Pars:
    # filePath = '/home/ak/Yandex.Disk/MY_COURSES_TLH/MY_LABS/Lab16_GITHUB_Molchanov.txt' # Файл, в котором ищутся мемы
    # regExpMark = MEMS_WITH_FIGUR # Стринговая поискова метка в формате regExp, Которая ищется в текстовом файле
    # qnParagrLines = 5 # Кол-во строк в параграфе, следуемых за той строкой, в которой найден мем
    
    # # Список структур типа MarkFileParagraph, параграфов, в которых найдены маркеры регулярного выражения regExpMark (в данном случае - мемы с фигурными скобками, 
    # # с заглавными буквами, цифрами и разделением через _)
    # totalMemParagrs = ReManager.find_all_given_mark_matches_from_txt_file_with_its_paragraphs(filePath, regExpMark)
    
    # # ПРОВЕРКА: 
    
    # print(f"totalMemParagrs_N = {len(totalMemParagrs)}")
    
    # for paragr in totalMemParagrs:
        
    #     print(f"\nmem = {paragr.strMarker}")
    #     print(f"file = {paragr.file}")
    #     print(f"listParagraphLines = {paragr.listParagraphLines}\n")
    
    
    
    
    


    # # ПРИМЕР: Ссылки в поле link1

    # cLink1 = 'https://checko.ru/'
    # cLink2 = 'https://checko.ru/company/dom-rf-1027700262270'

    # rExpr = 'http.*\d$'

    # m = re.search(rExpr, cLink2)
    # print (m)


    # # ПРИМЕР:   https://spark-interfax.ru/moskva-krasnoselski/ao-biznes-nedvizhimost-inn-7708797121-ogrn-1137746850977-c2220c23028949a4962370cd14eda1ff

    # stringS = 'https://spark-interfax.ru/altaiski-krai-barnaul/ooo-gruppa-prodovolstvie-inn-0411137185-ogrn-1080411002055-317e587229cd4e50a4fb58a9a7301532'

    # rExpr = r"inn-(\d{9}|\d{10}|\d{11}|\d{12})"
    # m = re.search(rExpr, stringS)
    # innLink = m.groups(1)[0]
    # print (innLink)


    # # ПРИМЕР: 

    # stringS = 'ООО ХК ФИНАНС — ОГРН 1137746449257, ИНН 7743889590 | РБК Компании'

    # rExpr = r"ИНН (\d{10})"

    # m = re.search(rExpr, stringS)

    # print (m.groups(1)[0])



#


