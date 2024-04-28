# КЛАСС : ReadWriteFile
# read_write_file_v3.py
# ВСЕ, ЧТО СВЯЗАНО СО СЧИТЫВАНИЕМ ИЛИ ЗАПИСЬЮ В ТЕКСТОВЫЕ ФАЙЛЫ

# import
# from Module import Class
# from gen_serv_data_v3 import GenServerData

from noocube.text_formater import TextFormater
import noocube.funcs_general as FG



# from distutils.dir_util import copy_tree # НЕ УДАЛЯТЬ, НАЙТИ ЗАМЕНУ ДЛЯ МЕТОДА copy_dir_tree_to_another_dir()
import datetime
import os
import io
import re
import glob
import shutil

import subprocess
import sys
from noocube.re_constants import *
# from .settings import *
# from bonds.re_manager import ReManager
from pathlib import Path
import pathlib


# КЛАСС
class FilesManager ():
    
    # КОНСТРУКТОР
    def __init__(self, file):
        
        self.file = file         



### FILE INFOR

    @staticmethod
    def basename_from_filepath_retrieve  (self, filepath):
        """Получить имя файла с расширением из пути к нему"""
        return os.path.basename(filepath)
        


#




### END FILE INFOR



### PRINTS 

    def print_list(dsList):
        """Распечатывает список в столбец"""
        
        for x in dsList:
            print(x)


### END PRINTS



        
    # Считывание текста из файла в виде списка строк
    def read_file_txt_lines (self):
        """Считывание содержимого файла в виде набора строк"""
        f = open(self.file, "r" , encoding='utf-8', errors='ignore')
        return f.readlines()   


    def read_file_data_txt(self):
        """Считывание текста файла в виде стринга"""
        # Read in the file
        with  open(self.file, "r", encoding='utf-8', errors='ignore') as f :
            fieldataStr = f.read()       
        return fieldataStr

    @staticmethod
    def read_file_data_txt_static(fPath):
        """ Class: FilesManager
        Считывание текста файла в виде стринга без создания обьекта, статический метод"""
        # Read in the file
        with  open(fPath, "r", encoding='utf-8', errors='ignore') as f :
            fieldataStr = f.read()   
                
        return fieldataStr


    # Создаем файл, если его нет. Если есть, проверяем пустой или нет и выставляем флаг: fileEmpty
    # Если пустой, то fileEmpty = True. Если не пустой, то fileEmpty = False
    # ERR: UnicodeDecodeError: 'charmap' codec can't decode byte 0x98 in position 19: character maps to <undefined>
    def create_txtfile_or_check_its_emptiness (self) :
        """Проверяем наличие файла. Если его нет - то создаем. Если есть, то проверяем пустой ли он или нет"""
        # if os.path.isfile("./" + self.file):
        if os.path.isfile(self.file):

            print ("PR_NC_143 --> Файл есть M: FilesManager.create_txtfile_or_check_its_emptiness")
            # Если существует, проверяем пустой он или нет
            f = open(self.file, "r")
            if len(f.readlines()) == 0:
                print ("PR_NC_142 --> Файл - пустой")
                fileEmpty = True # Выставляем флаг - Пустой
                f.close()
            else:
                print("PR_NC_141 --> Файл - не пустой")
                fileEmpty = False # Выставляем флаг - Не пустой
                f.close()
        else:
            print ("PR_NC_140 --> Файла нет. Создаем его  M: FilesManager.create_txtfile_or_check_its_emptiness")  
            # Если файла нет, то создаем его
            f = open(self.file, "w", encoding='utf-8', errors='ignore')
            fileEmpty = True # Выставляем флаг - Пустой
            f.close()
        return fileEmpty    
    
    # ------------

    # Запись данных в лог-файл
    # src - данные по источнику лог-операции - M: Ln:
    def write_log_in_file (self,  massage, startMark = "", src = "", time = "", endMark = ""):
        fullStr = startMark + "\n" + massage + "\n" +  src + "\nTime: " + time  + "\n" + endMark  + "\n"
        f = open(self.file, "w", encoding='utf-8', errors='ignore')
        f.write(fullStr)
        f.close() 

    # ------------

    # Полная очистка файла
    def  clear_file (self):
        """Удалить содержимое файла и сохранить"""
        f = open(self.file, "w", encoding='utf-8', errors='ignore')
        f.truncate()  # Clear previous content
        f.close() 

    # ------------

    # Отчищение и Запись в тектовый файл
    def write_in_file (self,  text):
        """Записать текст в файл"""
        f = open(self.file, "w", encoding='utf-8', errors='ignore')
        f.write(text)
        f.close() 
        
        
        
    # Отчищение и Запись в тектовый файл статика
    @staticmethod
    def write_in_file_static (file, text):
        """Записать текст в файл"""
        f = open(file, "w", encoding='utf-8', errors='ignore')
        f.write(text)
        f.close() 
        
        
        
        

    # ------------

    # Проверка пустой ли файл
    def check_if_file_empty (self):
        """Проверка пустой файл или нет"""
        # Если существует, проверяем пустой он или нет
        f = open(self.file, "r")
        if len(f.readlines()) == 0:
            print ("PR_NC_139 --> Файл - пустой")
            fileEmpty = True # Выставляем флаг - Пустой
            f.close()
        else:
            print("PR_NC_138 --> Файл - не пустой")
            fileEmpty = False # Выставляем флаг - Не пустой
            f.close()    
        return fileEmpty

        
    # Поиск в строках текствого файла определенного текста
    def find_txt_in_file (self, srchTxt):
        
        f = io.open(self.file,'r', encoding='utf-8')
        textInFile = f.read()
        if srchTxt in textInFile:
            print ( "PR_NC_137 --> Найден текст: " + srchTxt + " M: def_gen_funcs F: find_txt_in_file Ln: 142")
            found = True
            
        else:
            found = False
            
        return found    
    
    # ------------

    # Нахождение блока текста в текстовом файле или строке по начальному фрагменту и конечному
    # ret: txtBlock - найденный текстовый блок, startidx - индекс старта блока в файле, endIdx - индекс конца блока в файле
    # TODO: Проверить эту функцию. Возможно - глюк
    def find_fragment_by_start_end_marks (self, startMark, endMark) :
        
        # Read in the file
        with  open(self.file, "r", encoding='utf-8', errors='ignore') as f :
            fieldata = f.read()
    
        # Нахождение индексов начала и конца блока тескстового в общем тексте
        startIdx = fieldata.index(startMark)
        endIdx = fieldata.index( endMark, startIdx)
        txtBlock = fieldata[startIdx : endIdx]  
    
        return txtBlock, startIdx, endIdx

    # ------------




    # Замещение фрагмента в тестовом файле новым фрагментом
    def replace_text_fragment_in_file (self, initialFragment, newFragment):
        with  open(self.file, "r", encoding='utf-8', errors='ignore') as f :
          filedata = f.read()
        # Replace the target string
        filedata = filedata.replace(initialFragment, newFragment)  
        # Write the file out again
        with open(self.file, 'w' , encoding='utf-8', errors='ignore') as f:
          f.write(filedata) 

    # ------------



    def insert_txt_fragm_to_txt_file_before_str_fragm_first_occurence (self, strFragm , txtInsert ):
        """OBSOLETED: Новый вариант ниже insert_to_file_text_block_by_inx_relative_to_srch_fragm_first_occurence (self, srchFragm , txtInsert, relInx )
        Всавить фрагмент текста в базовый  текстовый файл. Текст вставляется в предыдущую строчку в том месте, где было найдено первое совпадение в базовом тексте с
         искомым фрагментом текста  """
        # fileManager = FilesManager(txtFilePath)
        textFormatter = TextFormater()
        txtFileLines = self.read_file_txt_lines () # Получаем спиок строк
        # Находим индекс строки, в которой есть 
        indexFound = textFormatter.find_inx_of_text_list_lines_containing_fragm (txtFileLines, strFragm)
        # Переводим текст в список строк
        txtInsertLines = textFormatter.get_str_lines_of_text (txtInsert)
        # Вставить txtInsert в pageLines перед индексом indexIfName
        newFinalTextLines = FG.insert_list_to_another_list_by_inx (txtFileLines, txtInsertLines, indexFound)
        # Перевести список строк обратно в текст
        newFinalText = textFormatter.convert_str_lines_to_text (newFinalTextLines)
        # Очистить файл filePath
        self.clear_file ()
        # Записать новый текст с новым кодом в файл
        self.write_in_file (newFinalText)
        return newFinalText



    def insert_txt_fragm_to_txt_file_by_relative_inx_to_str_fragm_first_occurence (self, srchFragm , txtInsert, relInx ):
        """ <НЕ ТЕСТИРОВАН>
        Вставить блок текста в   текстовый файл до или после первого совпадения искомого стрингового фрагмента в тексте
        baseTxtInLines - текст в виде списка строк
        relInx : -1 вставить до найденного фрагмента/ 1 вставить после найденного фрагмента 
        srchFragm - искомый фрагмент в тексте
        """
        textFormatter = TextFormater()
        txtFileLines = self.read_file_txt_lines () # Получаем спиок строк
        # Находим индекс строки, в которой есть 
        indexFound = textFormatter.find_inx_of_text_list_lines_containing_fragm (txtFileLines, srchFragm)
        # Переводим текст в список строк
        txtInsertLines = textFormatter.get_str_lines_of_text (txtInsert)
        # Вставить txtInsert в pageLines перед индексом indexIfName
        if relInx < 0:
            indexFound = indexFound - 1 # Индекс для вставки до искомого фрагмента
        else:
            indexFound = indexFound + 1 # Индекс для вставки после искомого фрагмента
        newFinalTextLines = FG.insert_list_to_another_list_by_inx (txtFileLines, txtInsertLines, indexFound)
        # Перевести список строк обратно в текст
        newFinalText = textFormatter.convert_str_lines_to_text (newFinalTextLines)
        # Очистить файл filePath
        self.clear_file ()
        # Записать новый текст с новым кодом в файл
        self.write_in_file (newFinalText)
        return newFinalText




    def insert_block_to_txt_file_by_relative_inx_to_srch_block_first_occurence (self, srchBlockStartMarker , srchBlockFinalMarker, txtBlockInsert, relInx ):
        """ 
        Вставить блок текста в   текстовый файл до или после тексового блока, найденного по начальному и конечному маркеру (по их первому совпадению)
        relInx : -1 вставить до найденного блока/ 1 вставить после найденного блока 
        srchFragm - искомый фрагмент в тексте
        """
        textFormatter = TextFormater()
        txtFileLines = self.read_file_txt_lines () # Получаем спиок строк
        # НАходим адрес (начальный и конечный индексы строк) искомого блока в списке строк заданного текста
        srchBlockAddress = textFormatter.find_txt_block_in_txt_lines_by_begin_end_markers (txtFileLines, srchBlockStartMarker, srchBlockFinalMarker)
        # Переводим текст для вставки в список строк
        txtBlockInsertLines = textFormatter.get_str_lines_of_text (txtBlockInsert)
        # Вставить txtInsert в pageLines перед индексом indexIfName
        if relInx < 0:
            indexToInsert= srchBlockAddress[0] - 1 # Индекс для вставки до искомого блока
        else:
            indexToInsert = srchBlockAddress[1] + 1 # Индекс для вставки после искомого блока
        newFinalTextLines = FG.insert_list_to_another_list_by_inx (txtFileLines, txtBlockInsertLines, indexToInsert)
        # Перевести список строк обратно в текст
        newFinalText = textFormatter.convert_str_lines_to_text (newFinalTextLines)
        # Очистить файл filePath
        self.clear_file ()
        # Записать новый текст с новым кодом в файл
        self.write_in_file (newFinalText)
        return newFinalText



    # Считывание групп в виде списка из файла установок fileName
    def get_set_groups (self, fileName) :
        
        try:
            fileTxt = open(fileName, encoding='utf-8', errors='ignore').read()
            self.setupGroups = fileTxt.split("$$")
            # print(len(self.setupGroups))
            # self.setGroups = setupGroups
        except Exception as e:
            print(str(e))
            print("PR_NC_136 --> Ошибка считывания файла: " + fileName + " или разделения его текста по группам $$ M: setup_data_v3 ln: 44")



    # Получение строки конкретной переменной в тексте заданной группы или масив этой строки, разделенной по делиметру delim (по умолчанию ',') если таковой существует в строке переменной
    # Если нужно получить возможный массив, то указываем 3й параметр делиметр delim, который по умолчанию равен None. Иначе получаем просто значение переменной (не список)
    # Если нужно получить просто значение переменной в фигурных скобках, то пропускаем 3й параметр delim
    def get_setup_var_value (self, groupName, varName, delim = None):
        try:
            groupTxt =  [x for x in self.setupGroups if groupName + ":" in x.replace(" ","")][0]
        except Exception as e:
            print(str(e))
            print("PR_NC_135 --> Ошибка считывания текста группы: " + groupName + " M: setup_data_v3 ln: 62")
        groupLines = groupTxt.splitlines()
        try :
            # Строка в тексте группы, содержащая заданную переменную varName
            varLineStr = [x for x in groupLines if varName in x][0]
        except Exception as e:
            print(str(e))
            print("PR_NC_134 --> Не найдена переменная " + varName + " в группе " + groupName+ " M: setup_data_v3 ln: 70")
        # Получаем то, что содержится между фигурных скобок в varLineStr {} с очисткой пробелов
        self.varValue = varLineStr[varLineStr.find("{") + len("{"):varLineStr.find("}")].strip() 

        # Анализ на разбиение по делиметру
        if delim:
            # $$ list comprehansion
            varValueArr = self.varValue.split(delim)
            varValueArr = [x.strip() for x in varValueArr] # удаляем пробелы вначале и в конце
            
            return varValueArr
        
        else:
            return self.varValue




    # СЧИТЫВАЕМ ТЕКСТ В ФАЙЛЕ В ВИДЕ СПИСКА СТРОК
    def read_file_txt_to_list_of_lines (self):
        
        f = open(self.file, "r" , encoding='utf-8', errors='ignore')
        
        return f.readlines()



    # СЧИТЫВАЕМ ТЕКСТ В ФАЙЛЕ В ВИДЕ СПИСКА СТРОК статика
    def read_file_txt_to_list_of_lines_stat (filePathFull):
        """ 
        FilesManager
        Считать текст файла в список строк текста
        """
        
        f = open(filePathFull, "r" , encoding='utf-8', errors='ignore')
        
        return f.readlines()




    # ВЫТЯЖКА ИЗ СТРОКИ ЦИФР И НЕФОРМАТНЫХ ЗНАКОВ, ВКЛЮЧАЯ НЕГАТИВНЫЕ
    # return: digs - ф фрме list
    def digits_from_string_with_negatives (string) :
        
        digs = re.findall("[-\d]+", string) # с негативными цифрами в строке
        
        return digs # list




    # очистка от всяких знаков 
    def clear_from_empty_unicode(s):
        
        newString = (s.encode('ascii', 'ignore')).decode("unicode_escape")
        return newString


    # НАХОЖДЕНИЕ БЛОКА ТЕКСТА В ТЕКСТОВОМ ФАЙЛЕ ИЛИ СТРОКЕ ПО НАЧАЛЬНОМУ ФРАГМЕНТУ И КОНЕЧНОМУ
    # ret: txtBlock - найденный текстовый блок, startidx - индекс старта блока в файле, endIdx - индекс конца блока в файле
    def find_textblock_by_start_end_strings (self, file, startStr, endStr) :
        
        # Read in the file
        with  open(file, "r", encoding='utf-8', errors='ignore') as file :
            filedata = file.read()

        # Нахождение индексов начала и конца блока тескстового в общем тексте
        startidx = filedata.index(startStr)
        endIdx = filedata.index( endStr, startidx)
        txtBlock = filedata[startidx : endIdx]  

        return txtBlock, startidx, endIdx


    # ЗАМЕЩЕНИЕ В ТЕКСТОВОМ ФАЙЛЕ БЛОКА НОВЫМ БЛОКОМ
    @staticmethod
    def replace_in_file_txtblock_with_newblock (fileName, oldBlock, newBlock):
        
        with  open(fileName, "r", encoding='utf-8', errors='ignore') as file :
            filedata = file.read()
            
        # Replace the target string
        filedata = filedata.replace(oldBlock, newBlock)  

        # print (filedata)    
        
        # Write the file out again
        with open(fileName, 'w' , encoding='utf-8', errors='ignore') as file:
            file.write(filedata)      


    # ОЧИСТКА БЛОКА, ВЫЧИСЛЯЕМОГО ПО СТАРТОВОМУ ТЭГУ И КОНЕЧНОМУ ТЭГУ (конечный тэг не изменяется пока
    def clear_block_in_file_by_start_and_end_fragments (self,file, startStr, endStr):
        
        txtBlock, startIdx, endIdx = self.find_textblock_by_start_end_strings (file, startStr, endStr)

        newBlock = startStr + '\n'
        
        # replace_in_file_txtblock_with_newblock (file, txtBlock, newBlock)



    # ПОИСК СТАРТОВОГО ФРАГМЕНТА В ТЕКСТЕ ФАЙЛА И ВОЗВРАЩЕНИЕ ИНДЕКСА, ЕСЛИ НАЙДЕН
    def find_str_fragment_in_file (self,  strFragment):
        
        with  open(self.file, "r", encoding='utf-8', errors='ignore') as f :
            filedata = f.read() 
        
        try:
            
            startIdx = filedata.index(strFragment)
            
        except ValueError: # substring not found   
            
            print ("PR_NC_133 --> Не найдено совпадение")
            startIdx = -1
            
        
        return startIdx
    
    
    @staticmethod
    def find_paragrphs_in_txt_file_where_re_string_marker_found (filePath, regExpMark = MEMS_WITH_FIGUR, qnParagrLines = 5):
        """Найти параграфы в текстовом файле, в которых будет найден стринговый маркер, заданный регулярным выражением  regExpMark. 
        Количество строк в параграфе, которые следуют за той строкой, в которой найден стринговый маркер regExpMark, определяется параметром qnParagrLines по умолчанию = 5.
        И вернуть список структур типа MarkFileParagraph. Класс структуры задан в /home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/structures.py
        Список структур, В которых найдены маркеры по формату равне искомому регулярному выражению regExpMark
        
        htmlSep - знак html-тэга, который разделяет найденные линии в параграфах
        """
        
        from noocube.re_manager import ReManager
        
        totalMemParagrs = ReManager.find_all_given_mark_matches_from_txt_file_with_its_paragraphs_html (filePath, regExpMark = regExpMark, qnParagrLines = qnParagrLines)
        
        return totalMemParagrs
        

    @staticmethod
    def filter_objs_list_of_type_mark_file_paragraph_by_given_marker(paragraphsList, marker):
        """ ПРОТЕСТИРОВАН
        Отфильтровать список найденных параграфов из текстового файла по заданнму формату регулярного выражения regExpMark по заданному маркеру marker
        paragraphsList - список параграфов-обьектов  класса MarkFileParagraph (/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/structures.py)
        marker - маркер, по которому ищуться параграфы из заданного списка найденных параграфов по атрибуту obj.strMarker
        """
        
        # A. Найти в списке totalMemParagrs те элементы, у которых obj.strMarker в списке обьектов со структурой типа MarkFileParagraph равен заданному strMarker (поисковому маркеру или мему)
        paragraphsFiltered = [x for x in paragraphsList if x.strMarker == f'{marker}']
        # print(f"listFilt_N = {len(listFilt)}")
        return paragraphsFiltered


    @staticmethod
    def find_paragraphs_in_list_files_where_re_string_marker_found(listFilesInp, listExludeFiles, regExpMark = MEMS_WITH_FIGUR, qnParagrLines = 5):
        """Найти параграфы в списке фалов (не в одном файле, а в спике), в которых будет найден стринговый маркер, заданынй регулярным выражением regExpMark,
        с исключением из заданног осписка файлов, которые надо исключить из анализа 
        Количество строк в параграфе, которые следуют за той строкой, в которой найден стринговый маркер regExpMark, определяется параметром qnParagrLines по умолчанию = 5.
        И вернуть список структур типа MarkFileParagraph. Класс структуры задан в /home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/structures.py
        Список структур, В которых найдены маркеры по формату равне искомому регулярному выражению regExpMark
        
        qnParagrLines - кол-во строк в параграфе, в котормо найдено совпадение с искомым regExpMark
        htmlSep - знак html-тэга, который разделяет найденные линии в параграфах
        
        RET: generalMemParagr - список всех параграфов во всех файлах из списка listFilesInp, в коорых найден маркер regExpMark (регулярное выражение)
        """
        
        # regExpMark = MEMS_WITH_FIGUR # Стринговая поискова метка в формате regExp, Которая ищется в текстовом файле
        # qnParagrLines = 5 # Кол-во строк в параграфе, следуемых за той строкой, в которой найден мем

        generalMemParagr = [] # Общая совокупность параграфов, полученная из спика заданных файлов listFilesInp
        
        for file in listFilesInp:
            
            if file in listExludeFiles: # Иcключить из цикла, если файл задан в списке исключения listExludeFiles
                totalMemParagrs = []
            else:
                totalMemParagrs = FilesManager.find_paragrphs_in_txt_file_where_re_string_marker_found(file, regExpMark, qnParagrLines)
            
            generalMemParagr += totalMemParagrs
            
        # print(f"generalMemParagr_N = {len(generalMemParagr)}")
        
        return generalMemParagr



    @staticmethod
    def filter_paragraphs_from_file_list_with_exlude_by_marker (listFilesInp, listExludeFiles, regExpMark,  marker, qnParagrLines):
        """НАхождение параграфов с заданным маркером из спика фалов с исключением в виде списка файлов исключений
        listFilesInp - список вхдящих файлов
        listExludeFiles - списко фалов, которые надо исключить из рассмотрения
        regExpMark - регулярное выражение, по которому ищуться совпадения в файлах и вытяжка параграфов, в которых они найдены
        qnParagrLines - кол-во строк, Которые определяют параграф, нижесоящий от строки с найденным маркером
        marker - поисковая строка уже для найденног общего списка параграфов , найденных по регулярному выражению regExpMark
        htmlSep - знак html-тэга, который разделяет найденные линии в параграфах
        
        ПРИМЕР ПАРАМЕТРОВ:
        
        listFilesInp = [ 
            '/home/ak/Yandex.Disk/MY_COURSES_TLH/MY_LABS/Lab16_GITHUB_Molchanov.txt',
            '/home/ak/Yandex.Disk/MY_COURSES_TLH/MY_LABS/Lab15_Library_site_Django.txt',
            '/home/ak/Yandex.Disk/MY_IT_TLH/PYTHON_2.txt'
            ]
        
        # Список фалов для исключения
        listExludeFiles = [ 
            '/home/ak/Yandex.Disk/MY_IT_TLH/PYTHON_2.txt'
        ]
        
        regExpMark = MEMS_WITH_FIGUR # Стринговая поискова метка в формате regExp, Которая ищется в текстовом файле
        qnParagrLines = 5 # Кол-во строк в параграфе, следуемых за той строкой, в которой найден мем
        marker = '{PYTHON_INSTALL}'
            
        """
        
        # Список параграфов из спсика файлов  listFilesInpс исключениями из списка фалов исключений listExludeFiles
        generalMemParagrs = FilesManager.find_paragraphs_in_list_files_where_re_string_marker_found (listFilesInp, listExludeFiles, regExpMark, qnParagrLines)
        
        # A. отфильтровать спсиок параграфов из общего списка файлов с исключением по спику фалов по заданному маркеру 
        # pars:
        # marker = '{PYTHON_INSTALL}'
        paragraphsFiltered = FilesManager.filter_objs_list_of_type_mark_file_paragraph_by_given_marker(generalMemParagrs, marker)
        
        print(f"PR_NC_132 --> paragraphsFiltered_N = {len(paragraphsFiltered)}")
        
        return paragraphsFiltered


        

    def add_text_to_end_of_file_data(self, addTxt):
        """Добавить заданный текст в конец данных файла
        Вернуть конечный вариант данных в файле
        """

        with  open(self.file, "r", encoding='utf-8', errors='ignore') as f :
            filedata = f.read() 

        filedata += addTxt

        with open(self.file, 'w' , encoding='utf-8', errors='ignore') as f:
          f.write(filedata) 

        return filedata




    ##ПОЛУЧИТЬ ТЕКУЩЕЕ ВРЕМЯ ПЛЮС ДЕЛЬТА_СЕКУНД

    def get_curr_time_plus_secs (deltaSecs):
        
        nextTime = datetime.now() + datetime.timedelta(seconds=deltaSecs)
        
        return nextTime



    # ТРАНСФОРМАЦИЯ СТРИНГОВОГО ВРЕМЕНИ ТИПА 00:00:00 В СЕКУНДЫ
    def time_str_to_sec (strTime):
        
        timeParts = strTime.split(":")
        
        totalSecs = int(timeParts[0].replace(" ","")) * 60 * 60 + int(timeParts[1].replace(" ","")) * 60 + int(timeParts[2].replace(" ",""))

        return totalSecs


    # ПОИСК В СТРОКАХ ТЕКСТОВОГО ФАЙЛА ОПРЕДЕЛЕННГО ТЕКСТА
    def find_txt_in_file (file, txt):
        
        f = io.open(file,'r', encoding='utf-8')
        textInFile = f.read()
        if txt in textInFile:
            print ( "PR_NC_131 --> Найден текст: " + txt + " M: def_gen_funcs F: find_txt_in_file Ln: 142")
            found = True
            
        else:
            found = False
            
        return found

    
        # очистка от всяких пустых знаков 
    def clear_from_empty_unicode(self):
        newString = (self.string.encode('ascii', 'ignore')).decode("unicode_escape")
        return newString    

    # ------------



    # РАБОТА С ДИРЕТОРИМИ И ФАЙЛАМИ


    @staticmethod
    def get_dir_files( cdir, fileFormat = '*.*', subdirDeep =''):
        """ Class: FilesManager
        OBSOLETED: ИСпользовать get_dir_files_full ниже
        Получает список полных путей файлов директория с возаможной настройкой вариантов форматов  для поиска файлов и  глубины считывания поддиректорий
        fileFormat - формат искомых файлов, типа "*.txt". По умолчанию '*.*' - файлы со всеми расширениями
        subdirDeep - глубина считывания поддиректорий. Задается дополнительной вставкой после заданной диреткории , типа '/*/*.txt'. По умолчанию глубина нулевая
        RET: Список полных путей файлов диреткория
        Src: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
        """
        # print(f"%%%%%%%%%%%%************ cdir = {cdir}")
        # print(f"%%%%%%%%%%%%************  subdirDeep = {subdirDeep} | 1_Proj_Obligations_Analitic_Base/infor_assembling_center/files_manager.py | get_dir_files() ")
        
        fileSrchFormat = cdir + '/' + subdirDeep + fileFormat
        # print (fileSrchFormat)
        dirFiles = glob.glob(fileSrchFormat)
        
        # print (f"%%%%%%%%%%%%************ dirFiles = {dirFiles}")
        
        return dirFiles


    @staticmethod
    def get_dir_files_full( cdir, fileFormat = '*.*', subdirDeep = 0, totalSubdir = True):
        """ Class: FilesManager
        Получает список полных путей файлов директория с возаможной настройкой вариантов форматов  для поиска файлов и  глубины считывания поддиректорий
        fileFormat - формат искомых файлов, типа "*.txt". По умолчанию '*.*' - файлы со всеми расширениями
        subdirDeep - глубина считывания поддиректорий , задается числом. Задается дополнительной вставкой после заданной диреткории , типа '/*/*'. По умолчанию глубина нулевая и 
        считывает только в заданном диреткории, не углубляясь. Каждая новая глубина задается новым дополнением '/*' и файлы плюсуются в общий список (должны плюсоваться. пока - НЕ СДЕЛАНО)
        totalSubdir - флаг считывания. Если True, то считываются все файлы во всех поддиректориях глубины. Если - False - то считывается только по директориям заданной глубины
        
        RET: Список полных путей файлов диреткория
        Src: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
        """
        print(f"------ PR_NC_146 --> START: get_dir_files_full()")
        
        # print(f"%%%%%%%%%%%%************ cdir = {cdir}")
        
        # print(f"%%%%%%%%%%%%************  subdirDeep = {subdirDeep} | 1_Proj_Obligations_Analitic_Base/infor_assembling_center/files_manager.py | get_dir_files() ")
        
        deepDir = '/'
        dirFiles = []
        
        if subdirDeep == 0:
            fileSrchFormat = cdir + '/' + fileFormat
            
        if subdirDeep == 0 and totalSubdir:
            dirFiles = glob.glob(fileSrchFormat)

            
        
        if totalSubdir:
        
            for deep in range(subdirDeep): # Цикл по заданной цифре глубины считывания директорий
                deepDir += '*/'
                fileSrchFormat = cdir + deepDir + fileFormat
                # Найти файлы с заданынм форматом и глубиной fileSrchFormat
                # print (f"%%%%%%%%%%%%************ fileSrchFormat = {fileSrchFormat}")   
                dirFiles += glob.glob(fileSrchFormat)
                
        else:
            for deep in range(subdirDeep): # Цикл по заданной цифре глубины считывания директорий
                deepDir += '*/'
                fileSrchFormat = cdir + deepDir + fileFormat
                # Найти файлы с заданынм форматом и глубиной fileSrchFormat
                
            # print (f"%%%%%%%%%%%%************ fileSrchFormat = {fileSrchFormat}")   
            dirFiles = glob.glob(fileSrchFormat)
            
                
        # FG.print_list(dirFiles) # Распечатка спика в столбец
        
        print(f"------ PR_NC_145 --> END: get_dir_files_full()")

        
        return dirFiles


    @staticmethod
    def find_files_in_list_of_dirs_recursively (listDirs, fileExt):
        """Найти все файлы в заданных директориях рекурсивно (то есть по всем субдиректориям любой вложенности)
        Тип файла задается fileExt формата: '.txt' """

        totalFiles = []
        for dir in listDirs:
            totalFiles += Path(dir).rglob(f"*{fileExt}")
            
        return totalFiles
            
        



    @staticmethod
    def find_file_in_dir_by_name_recursively (dir, fileName):
        """
        Найти файл по имени в директории рекурсивно
        Не доработана до конца. Надо проработать вывод Не найдено и т.д.
        result - список полных путей найденных по имени файлов в заданной главной директории. 
        Так как на выходе - генератор по которому должна идти итерация по идее, поэтому переводим ее в список по любому. Сам по себе генератор не принтуется
        """
                
        listFiles = Path(dir).rglob(fileName)
        listFiles = list(listFiles)
        
        return listFiles




    
    @staticmethod
    def get_dirs_files_dict (dirsTLHList, fileFormat = '*.*', subdirDeep = ''):
        """Class: FilesManager
        ПОлучить словарь с ключами в виде задаваемых в списке на вход диреториями, а в значениях по ключам - списки файлов заданного формата и глубины проникновения в поддиректории,
        принадлежащим директориям
        subdirDeep - глубина считывания поддиректорий. Задается дополнительной вставкой после заданной диреткории , типа '/*/*.txt'. По умолчанию глубина нулевая
        fileFormat - формат искомых файлов, типа "*.txt". По умолчанию '*.*' - файлы со всеми расширениями
        dirsTLHList - список диреткорий в которых ищутся файлы
        """

        tlhDirsFiles = {}
        for tlhDir in dirsTLHList: # цикл по списку TLH - диреторий
            currDirFiles = FilesManager.get_dir_files( tlhDir, fileFormat, subdirDeep ) # Получение полных путей всех txt-файлоа текущей по циклу директории
            tlhDirsFiles[tlhDir] = currDirFiles  

        return tlhDirsFiles




    def get_list_of_all_files_in_all_dirs_of_list (dirsList, fileFormat = '*.*', subdirDeep = ''):
        """FilesManager
        Получить полный список всех файлов из суб-директорий, в названии которых есть фрагмент '_TLH' и которые принадлежат базовым родительским установочным диреткориям из 
        константы settings. 
        subdirDeep - глубина проникновения в поддиретории текущего диреткория, определяемая вставкой типа '/*/*.txt'
        """
        totalFilesList = [] # Полный список всех файлов  из списка диреторий dirsList с расширением fileFormat и глубиной по суб-диреториям subdirDeep
        for tlhDir in dirsList: # цикл по списку TLH - диреторий
            currDirFiles = FilesManager.get_dir_files( tlhDir, fileFormat, subdirDeep ) # Получение полных путей всех txt-файлоа текущей по циклу директории
            totalFilesList += currDirFiles  

        return totalFilesList


    @staticmethod
    def get_last_loaded_file_name_from_dir (dirPath):
        """FilesManager
        Получить название последнего загруженного файла в заданной диретории
        dirPath - должна быть такого формата '/home/ak/Downloads'"""
        filename = max([dirPath + '/' + f for f in os.listdir(dirPath)], key=os.path.getctime)
        return filename


    # КОПИРОВАНИЕ ПЕРЕНОС СОЗДАНИЕ

    @staticmethod
    def rename_move_file_shutil (srcFilePath, newFilePath):
        """FilesManager
        Переименование и/или перенос файла с использованием системной библиотеки shutil"""    

        shutil.move(srcFilePath,newFilePath)
        print(f"PR_NC_130 --> Файл {srcFilePath} переименован  и перенесен в новую диреторию : {newFilePath}")



    @staticmethod
    def copy_file_shutil (src, dst):
        """
        FilesManager
        Копирование файла в директорий
        Ели файл с таким именем уже существует в целевом лиректории, то он заменяется новым файлом
        
        """
        shutil.copy(src, dst) 
        print(f"PR_NC_129 --> Файл {src} скопирован в новый диреторий : {dst}") 




    @staticmethod
    def move_file_to_another_dir_if_exists_in_this_dir(fullFilePath, newFullFilePath):
        """ 
        [27-01-2024]
        Если файл существует в заданной директории в его названии, то переносим тот файл в другую диреторию
        Если такой директории не существует, то она создается автоматом
        """
        
        if FilesManager.if_file_exist (fullFilePath):
            
            # Перенести файл в локальную урну newFilePath
            FilesManager.rename_move_file_shutil (fullFilePath, newFullFilePath)
            
        else:
            
            pass





    @staticmethod
    def copy_dir_tree_to_another_dir(dirFrom, dirTo):
        """Скопировать содержимое директория в новый диреторий"""
        copy_tree(dirFrom, dirTo)
        print(f"PR_550 --> Папка {dirFrom} скопирована в новую папку : {dirTo}") 



    @staticmethod
    def copy_dirs_to_its_arch_dirs(projsDirsArchDic):
        """Копирует проект в его архивный директорий по циклу словаря 
        projsDirsArchDic - словарь соотвтетвий проекта и архива, куда нужно архивировать проект с добавкой текущего времени для унификации названия {projPath: pathToItsArcive}
        """
        for kproj, varchdir in projsDirsArchDic.items(): # цикл по словарю соотвтетвий проектов - архивов
            FilesManager.copy_dir_tree_to_another_dir(kproj, varchdir)



    @staticmethod
    def create_dir(path):
        """Создать директорий"""
        os.umask(0)
        os.mkdir(path, mode=0o777)





    @staticmethod
    def get_last_dir_name_from_path(path):
        """Получить название последней папки в пути без файла в конце пути"""
        dirParts = path.split('/')
        lastDirName = dirParts[-1]
        return lastDirName


    # END КОПИРОВАНИЕ ПЕРЕНОС СОЗДАНИЕ


    @staticmethod
    def get_dir_from_file(filePath):
        """FilesManager
        Получить путь директория к файлу"""
        dirPath = os.path.dirname(filePath)
        return dirPath



    def get_current_dir():
        """Получить текущую диреторию проекта"""
        currDir = os.getcwd()
        return currDir




    # END РАБОТА С ДИРЕТОРИМИ И ФАЙЛАМИ


    # ВСПОМОГАТЕЛЬНЫЕ 


    @staticmethod
    def get_names_list_from_abs_files_list (absFilesList):
        """ Class: FilesManager
        Получить список названий из списка файлов с абсолютными путями"""

        fNames = [x.split('/')[-1].rstrip('.txt') for x in absFilesList] # Получение списка названий файлов
        return fNames







    # END ВСПОМОГАТЕЛЬНЫЕ 


    # Методы с диреториями

    @staticmethod
    def find_all_subdirs_with_fragment_in_name(mainDir, nameFragment):
        """ Class: FilesManager
        Нахождение субдиректорий в заданной основной mainDir с фрагментом в названии nameFragment
        mainDir  - Диретория поиска поддиреторий с фрагментом nameFragment в названии
        RETURN: subDirs - список субдиректорий в заданной mainDir, которые имеют фрагмент nameFragment в названии
        https://fanwangecon.github.io/Py4Econ/support/inout/htmlpdfr/fp_folders.html
        """
        subDirs = FilesManager.get_subdirs(mainDir) # перечень поддиректорий в заданной основной директории поиска mainDir
        subDirs = [mainDir + spt 
                        for spt in subDirs
                        if nameFragment in spt]
        return subDirs



    @staticmethod
    def get_subdirs (mainDir):
        """Class: FilesManager
        Получение списка поддиректорий в заданной mainDir"""
        subDirs = os.listdir(mainDir) # перечень поддиректорий в заданной основной директории поиска mainDir
        return subDirs


    @staticmethod
    def get_all_dirs_from_given_base_dirs_with_strfargm_in_name(baseDirsList, strFragm):
        """Class: FilesTLHManager
        Получить все директории со стринговым фрагментом nameFragment в названии директорий из списка заданных бызовых диреторий в виде  обьединенного списка 
        strFragm - стринговый фрагмент, который ищется в названиях директорий
        baseDirsList - список базовых диреторий, в которых могут хранится диретории с заданным фрагментом в имени
        RET: dirsList - обьединенный список всех директорий с заданным фрагментом в заданных базовых диреториях из списка baseDirsList
        """
        # Поиск поддиректорий в заданных  в TLH_SEARCH_DIRS диреториях, в названии которых присутствует фрагмент '_TLH' 
        dirsList = [] # Список для обединения найденных субдиреткорий, в названии которых есть фрагмент '_TLH' , в один
        for sDir in baseDirsList:
            subDirs = FilesManager.find_all_subdirs_with_fragment_in_name(sDir, strFragm) # список
            dirsList += subDirs # Сложение одномерных списков 

        return dirsList








    @staticmethod
    def open_dir(d):
        """From: http://stackoverflow.com/a/1795849/965332"""
        if sys.platform == 'win32':
            os.startfile(d)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', d])
        else:
            subprocess.Popen(['xdg-open', d]) 

            # subprocess.Popen(['xdg-select-file', '/home/ak/Yandex.Disk/MY_MED2_TLH/ОРТОПЕД КРЕСЛА.txt']) 




    # END    Методы с диреториями


    # Методы с файлами



    @staticmethod
    def if_file_exist (fullFilePath):
        """ Class: FilesManager
        Возвращает True or False в зависимости от того существует ли файл или нет"""
        if os.path.isfile(fullFilePath):
            return True
        else:
            return False





    @staticmethod
    def find_all_files_with_str_fragment_in_name(fileslist, strFragment):
        """ 
        Class: FilesManager
        Найти файлы из списка, в названии которых присутствует заданный стринговый фрагмент
        https://fanwangecon.github.io/Py4Econ/support/inout/htmlpdfr/fp_folders.html
        
        """
        fileslistFiltered = [x  
                        for x in fileslist
                        if strFragment in x]
        return fileslistFiltered





    @staticmethod
    def stat_file_size(fullPathFile):
        """ 
        FilesManager
        >> [29-01-2024]
        
        """
        
        return Path(fullPathFile).stat().st_size




    @staticmethod
    def get_file_name_from_path (fullPathFile):
        """ 
        FilesManager
        ~ https://stackoverflow.com/questions/66837158/get-just-the-filename-from-a-file-path-stored-as-a-string
        >> [29-01-2024]
        
        """
        
        return Path(fullPathFile).name
    
    
    @staticmethod
    def copy_files_of_given_ext_from_src_to_dest_dir_with_exist_and_size_checking (srcDir, destDir, filtExt = '*', limitSize = 500 ):
        """ 
        FilesManager
        >> [29-01-2024]
            
        Скопировать файлы из исходного директорий в целевой с проверкой наличия файлов по их названию и проверкой размеров файлов. 
        Если файлы из источника меньше заданного размера по ограничению, то копирование не происходит (файл-источник считается в этом случае нулевым или неправильным)
        Если в целевом директории уже существует файл с названием файла - источника, то проверяется его размер. Если размер существующего файла меньше заданного ограничения по минимуму, то файл
        удаляется, а файл - источник копируется
        крмое того. можно задавать файлы, которые предполагается скопировать из директории-источника по расширению, который отфильтрует файлы от других и попытается скопировать эти файлы 
        и целевой директорйи
        
        RET: copiedFilesList - список скопированных файлов в целевой директории
        
        """
        
        print(f"PR_NC_181 --> START: copy_files_of_given_ext_from_src_to_dest_dir_with_exist_and_size_checking()")
        
        # список скопированных файлов
        copiedFilesList = []
        
        # TODO: Сделать метод более гибким: что бы можно было задавать список фильруемых файлов по расширению. Так же сделать исключения, то есть какие файлы не отюираем по расширению
        jpgFilesListSrc = FilesManager.get_dir_files_full( srcDir, fileFormat = f'*.{filtExt}', subdirDeep = 0, totalSubdir = False)
        
        
        for jpgFileSrc in jpgFilesListSrc: 
            
            
            fsizeSrc = FilesManager.stat_file_size(jpgFileSrc)
            
            # Проверка файла-источника на размер. Если меньше заданного размера, то файл считается нулевым и не копируется, а цикл пропускается
            if fsizeSrc < limitSize:
                # !!! ПРОПУСКАЕМ цикл
                
                print(f"PR_NC_147 --> SYS LOG: Размер файла-источника  {jpgFileSrc} меньше минимального ограничения а {limitSize} байт.\nПоэтому не копируем файл и пропускаем цикл")
                continue 
            
            fileName = FilesManager.get_file_name_from_path (jpgFileSrc)
            
            dstPathFileFull = destDir + '/' + fileName
            
            # print(f"PR_A164 --> dstPathFile = {dstPathFileFull}")
            
            # Проверяем файл на существование уже в целевом директории
            if FilesManager.if_file_exist (dstPathFileFull): 
                
                fsizeDst = FilesManager.stat_file_size(dstPathFileFull)
                
                # В случае наличия файла с таким именем уже в целевом директории, этот уже существующий файл проверяется на размер. Если его размер больше заданной границы по размеру, 
                # то файл оставляется нетронутым , а цикл пропускается
                if fsizeDst > limitSize:
                    # !!! ПРОПУСКАЕМ цикл
                    
                    print(f"PR_NC_148 --> SYS LOG: Файл с названием {fileName} уже присутствует с целевом директории и его размер больше минимального ограничения а {limitSize} байт. \nПоэтому не копируем файл и пропускаем цикл")
                    continue 
                

            # Копируем файл 
            
            FilesManager.copy_file_shutil (jpgFileSrc, dstPathFileFull)
            
            copiedFilesList.append(dstPathFileFull)
            
        print(f"PR_NC_182 --> END: copy_files_of_given_ext_from_src_to_dest_dir_with_exist_and_size_checking()")

            
        return copiedFilesList
                
                


    



    # END Методы с файлами
    
    
    
    
    @staticmethod
    def get_full_file_path_formed_from_absolute_one_and_relative_given_right_resedue(absoluteFullPath, rightResedueRelativeFilePath):
        """ 
        Метод вычисления конечного пути файла по заданному абсолютному первичному пути (например, какой-то репозиторий файлов) absoluteFullPath и правой относителльной части
        пути какого-то файла с любым количеством секций-доменов, включая название файла с расширением, rightResedueRelativeFilePath
        
        Получить абсолютный путь для редактируемого относительного пути файла, который описывается чеециями-доменами пути файла с правого конца
        
        Формула: absoluteFullPath - <кол-во секций во вторичном файле rightResedueRelativeFilePath, включая название файла с его рсширением> + rightResedueRelativeFilePath 
        То есть , есть какая-то фиксированная часть пути, а правая часть, относительная, может менятся. Причем менятся с любым иерархическим кол-вом секций справа 
        вверх по директории заданного абсолютного пути
        """
        
        # Относительный оконечный справа путь файла, переданного из модуля редактирования, включая последний домен с названием файла с его расширением
        partsOfRelativePath = rightResedueRelativeFilePath.split('/')
        
        # Кол-во сегментов-доменов в относителльном оконечном справа пути файла, переданного из модуля редактирования, включая последний домен с названием файла с его расширением
        partsOfRelativePathQn = len(partsOfRelativePath)
        
        # Делим стандартный проектный путь для картинок книг по секциям-доменам
        partsOfAbsoluteFullPath = absoluteFullPath.split('/')
        
        
        # Кол-во доменов в пути к исходного проектного репозитория для картинок к описаниям книг - projImgBookFolder, за минусом кол-ва 
        # разделов-поддоменов той части пути с файлом, которая передается из редактора описания книги
        fixedAbsolutePartOfPrimePath = partsOfAbsoluteFullPath[:-(partsOfRelativePathQn-1)] # -1 потому что последняя секция - это само название файла  с его расширением
        
        # Отминучовав кол-во сегментов-доменов от конца стандартного пути к директорию с картинками для книг прибавляем переданный из модуля редактирования 
        # оконцовку пути к файлу-картинке
        fileFullPath = '/'.join(fixedAbsolutePartOfPrimePath) + '/' + rightResedueRelativeFilePath
        
        return fileFullPath

    
    
    @staticmethod
    def get_relative_right_path_from_full_file_path_by_given_section_name_fm (fileFullPath, sectionSliceSubdir):
        """ 
        Получить относительный путь редактируемого файла с правого конца до начала секции-маркера sectionSliceSubdir (какая-то заданная поддиректория в полном пути fileFullPath, 
        начиная с которой нам надо получить оставшийся путь справа без названия самого файла)
        """
        
        # Парсим абсолютный путь по маркеру = конечной точке Хранилища картинок книг ('books_images')
        parts = fileFullPath.split(sectionSliceSubdir)
        
        # Парсим относительный правй путь к файлу - нужно вычислить только путь без названия файла
        relRightPathParts = parts[-1].strip('/').split('/')
        
        relRightPath = '/'.join(relRightPathParts[:-1])
        
        return relRightPath



    @staticmethod
    def get_file_extension_from_file_path_fm (filePath):
        """ 
        Поулчить расширение файла из его названия или полного пути
        """
        
        fExt = pathlib.Path(filePath).suffix
    
        return fExt
    
    
    
    
    
    
        
    @staticmethod
    def devide_text_in_file_by_given_marker_and_save_to_another_file_static (textSourceFile, srchMarker, targetFile, breakLine = '\n', linetimes = 1, before = True, textReplaceDic = []):
        """ 
        РАзделить тектовый файл после-перед найденными маркерами определеннымми линиями-разделителями
        """

        # srchMarker = 'CREATE'
        
        # fPath = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/ARCHIVE_MYSQL_PROJS_DB/PRJ_021/LOGIC_BACKUP/labba__Дамп_структуры_БД_локального_PC_27_04_2024_07_29.struct'
        
        
        # fileTarget = '/home/ak/projects/P029_book_lib_site_simple_tg_django/PRJ029_DB_Structures/PRJ029_BD_structures.txt'
        
        
        iniText = FilesManager.read_file_data_txt_static(textSourceFile)
        
        newText = TextFormater.devide_text_with_markers_by_line_blocks_static (iniText, srchMarker, breakLine = breakLine, linetimes = linetimes, textReplaceDic = textReplaceDic)
        
        # parts = textPr.split(srchMarker)
        
        
        # newText = breakLine*linetimes + f'{srchMarker}'.join(parts)
        
        
        FilesManager.write_in_file_static(targetFile, newText)
        

    
    
    
    
    
    
    
    
    
    



# ВХОД ПО МОДУЛЮ
if __name__ == '__main__':

    pass



    # ПРОРАБОТКА:
    
    import pathlib
    
    file = '20. ТЕКСТ. ПБС 20_ch1_gsmegbc_gr1_audio_volume.fb2'

    fExt = pathlib.Path(file).suffix
    
    print(fExt)




    # # TEST: Проверка работы метода FilesManager.if_file_exist (fullFilePath)

    # fullFilePath = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN_!!!/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1/ch1_m4283_gr1_book_descr_photo.jpg'
    # ifExit = FilesManager.if_file_exist (fullFilePath)
    
    # print(f"PR_A400 --> ifExit = {ifExit}")



    # # ПРОРАБОТКА: НАхождение параграфов с заданным маркером из спика файлов
    
    # # Pars: 
    # # Список файлов заданный
    # listFilesInp = [ 
    #     '/home/ak/Yandex.Disk/MY_COURSES_TLH/MY_LABS/Lab16_GITHUB_Molchanov.txt',
    #     '/home/ak/Yandex.Disk/MY_COURSES_TLH/MY_LABS/Lab15_Library_site_Django.txt',
    #     '/home/ak/Yandex.Disk/MY_IT_TLH/PYTHON_2.txt'
    #     ]
    
    # # Список фалов для исключения
    # listExludeFiles = [ 
    #     '/home/ak/Yandex.Disk/MY_IT_TLH/PYTHON_2.txt'
    # ]
    
    # regExpMark = MEMS_WITH_FIGUR # Стринговая поискова метка в формате regExp, Которая ищется в текстовом файле
    # qnParagrLines = 5 # Кол-во строк в параграфе, следуемых за той строкой, в которой найден мем
    # marker = '{PYTHON_INSTALL}'
    
    # paragraphsFiltered = FilesManager.filter_paragraphs_from_file_list_with_exlude_by_marker (listFilesInp, listExludeFiles, regExpMark,  marker, qnParagrLines)
    
    
    # for paragraph in paragraphsFiltered:
        
    #     print(f"\nmem = {paragraph.strMarker}")
    #     print(f"file = {paragraph.file}")
    #     print(f"listParagraphLines = {paragraph.listParagraphLines}\n")

    

    
    # # ПРОРАБОТКА: Считывание директорий и файлов с любой глубиной, а так же с задаваемой глубиной
    
    # # deepDir = '/'
    # # dirFiles = []
    # # dir = '/home/ak/'
    
    # from pathlib import Path
    
    # strFragm = '_TLH'
    # subdirs = FilesManager.get_all_dirs_from_given_base_dirs_with_strfargm_in_name(TLH_SEARCH_DIRS, strFragm)
    
    # # print(f"subdirs = {subdirs}")
    
    # totalFiles = []
    # for dirTlh in subdirs:
    #     totalFiles += Path(dirTlh).rglob("*.txt")
    #     # print(f" DIR = {dirTlh}")
    #     # print(f" totalFiles = {totalFiles}")
        
    

        
    # print(f"totalFiles_N = {len(totalFiles)}")
    
    # file = str(totalFiles[0])
    
    # print(file)
    
    
    # files = sorted(Path(dir).rglob("*.py"))
    
    # print(f"files_N = {len(files)}")
    
    # if subdirDeep == 0:
    #     fileSrchFormat = cdir + '/' + fileFormat
        
    # if subdirDeep == 0 and totalSubdir:
    #     dirFiles = glob.glob(fileSrchFormat)

        
    
    # if totalSubdir:
    
    #     for deep in range(subdirDeep): # Цикл по заданной цифре глубины считывания директорий
    #         deepDir += '*/'
    #         fileSrchFormat = cdir + deepDir + fileFormat
    #         # Найти файлы с заданынм форматом и глубиной fileSrchFormat
    #         # print (f"%%%%%%%%%%%%************ fileSrchFormat = {fileSrchFormat}")   
    #         dirFiles += glob.glob(fileSrchFormat)
            
    # else:
    #     for deep in range(subdirDeep): # Цикл по заданной цифре глубины считывания директорий
    #         deepDir += '*/'
    #         fileSrchFormat = cdir + deepDir + fileFormat
    #         # Найти файлы с заданынм форматом и глубиной fileSrchFormat
            
    #     # print (f"%%%%%%%%%%%%************ fileSrchFormat = {fileSrchFormat}")   
    #     dirFiles = glob.glob(fileSrchFormat)
        

    
    
    
    
    

    # # ПРОРАБОТКА: Нахождение общего списка параграфов, в которых находится заданынное регулярное выражение, из списка файлов. Свозможностью исключения файлов из исключающего списка
    
    # # Pars: 
    # # Список файлов заданный
    # listFilesInp = [ 
    #     '/home/ak/Yandex.Disk/MY_COURSES_TLH/MY_LABS/Lab16_GITHUB_Molchanov.txt',
    #     '/home/ak/Yandex.Disk/MY_COURSES_TLH/MY_LABS/Lab15_Library_site_Django.txt',
    #     '/home/ak/Yandex.Disk/MY_IT_TLH/PYTHON_2.txt'
    #     ]
    
    # # Список фалов для исключения
    # listExludeFiles = [ 
    #     '/home/ak/Yandex.Disk/MY_IT_TLH/PYTHON_2.txt'
    # ]
    
    # regExpMark = MEMS_WITH_FIGUR # Стринговая поискова метка в формате regExp, Которая ищется в текстовом файле
    # qnParagrLines = 5 # Кол-во строк в параграфе, следуемых за той строкой, в которой найден мем
    
    # generalMemParagr = FilesManager.find_paragraphs_in_list_files_where_re_string_marker_found (listFilesInp, listExludeFiles, regExpMark, qnParagrLines )
    
    # print (f"generalMemParagr_N = {len(generalMemParagr)}")
    
    



    # # ПРОРАБОТКА: Найти в спиcке параграфов , найденных по стринговому маркеру через функцию find_paragrphs_in_txt_file_where_re_string_marker_found () , параграфы
    # # с заданным маркером
    
    # # Pars:
    # filePath = '/home/ak/Yandex.Disk/MY_COURSES_TLH/MY_LABS/Lab16_GITHUB_Molchanov.txt' # Файл, в котором ищутся мемы
    # regExpMark = MEMS_WITH_FIGUR # Стринговая поискова метка в формате regExp, Которая ищется в текстовом файле
    # qnParagrLines = 5 # Кол-во строк в параграфе, следуемых за той строкой, в которой найден мем
    
    # # Список структур типа MarkFileParagraph, параграфов, в которых найдены маркеры регулярного выражения regExpMark (в данном случае - мемы с фигурными скобками, 
    # # с заглавными буквами, цифрами и разделением через _), 
    # totalMemParagrs = FilesManager.find_paragrphs_in_txt_file_where_re_string_marker_found(filePath, regExpMark, qnParagrLines)
    
    
    # # A. Найти в списке totalMemParagrs те элементы, у которых obj.strMarker в списке обьектов со структурой типа MarkFileParagraph равен заданному strMarker (поисковому маркеру или мему)
    # # pars:
    # marker = '{PYTHON_TESTS_TDD_}'
    # paragraphsFiltered = FilesManager.filter_objs_list_of_type_mark_file_paragraph_by_given_marker(totalMemParagrs, marker)
    
    # print(f"paragraphsFiltered_N = {len(paragraphsFiltered)}")
    
    # for paragraph in paragraphsFiltered:
        
    #     print(f"\nmem = {paragraph.strMarker}")
    #     print(f"file = {paragraph.file}")
    #     print(f"listParagraphLines = {paragraph.listParagraphLines}\n")
    
    





    # # ПРОВЕРКА: find_paragrphs_in_txt_file_where_re_string_marker_found ()
    # # Найти параграфы в текстовом файле, в которых будет найден стринговый маркер, заданный регулярным выражением  regExpMark. 
    # # Количество строк в параграфе определяется параметром qnParagrLines по умолчанию = 5. И вернуть список структур типа MarkFileParagraph
    
    # # Pars:
    # filePath = '/home/ak/Yandex.Disk/MY_COURSES_TLH/MY_LABS/Lab16_GITHUB_Molchanov.txt' # Файл, в котором ищутся мемы
    # regExpMark = MEMS_WITH_FIGUR # Стринговая поискова метка в формате regExp, Которая ищется в текстовом файле
    # qnParagrLines = 5 # Кол-во строк в параграфе, следуемых за той строкой, в которой найден мем
    
    # # Список структур типа MarkFileParagraph, параграфов, в которых найдены маркеры регулярного выражения regExpMark (в данном случае - мемы с фигурными скобками, 
    # # с заглавными буквами, цифрами и разделением через _)
    
    # totalMemParagrs = FilesManager.find_paragrphs_in_txt_file_where_re_string_marker_found(filePath, regExpMark)
    
    # # ПРОВЕРКА: 
    
    # print(f"totalMemParagrs_N = {len(totalMemParagrs)}")
    
    # for paragr in totalMemParagrs:
        
    #     print(f"\nmem = {paragr.strMarker}")
    #     print(f"file = {paragr.file}")
    #     print(f"listParagraphLines = {paragr.listParagraphLines}\n")
    
    


    # ПРОРАБОТКА : 

    # # ПРМЕР: Проверка наличия файла по полному пути if_file_exist()
    # fullFilePath = '~/Yandex.Disk_/MY_MED2/Стомтология центральный район СПБ.txt'
    # ifExist = FilesManager.if_file_exist(fullFilePath)
    # print(f"ifExist = {ifExist}")


    # # ПРИМЕР: Проверка создания файла 

    # fullFilePath = '~/Yandex.Disk_/MY_MED2/Стомтология центральный район СПБ.txt'
    # dir = '/home/ak/Yandex.Disk_/MY_MED2/'

    # # fileMngr = FilesManager(fullFilePath)
    # # fileMngr.create_txtfile_or_check_its_emptiness ()

    # ifDirExist = os.path.isdir(dir)

    # # ПРИМЕР: Нахождение файлов директории

    # files = FilesManager.get_dir_files('/home/ak/Yandex.Disk_/MY_MED2_TLH', '*.txt')
    # # print(glob.glob("/home/ak/Yandex.Disk_/MY_MED2_TLH/*.txt"))

    # # # ПРИМЕР: Нахождение субдиректорий в заданной основной с фрагментом в названии 

    # # mainDir = '/home/ak' # Диретория поиска поддиреторий с фрагментом в названии
    # # nameFragment = '_TLH'

    # # listDirs = FilesManager.find_all_subdirs_with_fragment_in_name(mainDir, nameFragment)


    









