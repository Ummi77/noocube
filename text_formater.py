
import noocube.funcs_general as FG

class TextFormater():
    """ Класс для форматирования текста для любых прикладных модулей """

#


#  Вспомогателльные разные функции


    @staticmethod
    def create_name_with_time_from_given_name(name):
        """Создать стринговое имя с указанием времени создания в заданном изначально базовом названии """

        timeStr = FG.get_current_time_format1_d_m_y_h_m_s

        nameWithTime = name + timeStr

        return nameWithTime




#  Вспомогателльные разные функции



## TLH формат: Методы для работы с форматирвоанием текста для IAC (Information Assembling Center - центр управления информацией в текстовфх файлах компьюиера, для сохранения различной информации
#   по формату [ ;;;; Title -> * link (or FTP link) -> >>> hints ]. Аббревиатура формата: TLH)



    def create_inf_block_dictionary_TLH(self, title, link, hintRes = ''):
        """Формирование форматного словаря инф.блока,  на оснвое  title, link, hintRes
        hintRes - резуюме с быстрой информацией (hints ). это могут быть например телефоны, адреса и т.д.
        """

        # Составление форматного словаря инф.блока blockDict
        infBlockDict = {
            'infBlTitle' : title, # название блока - титульное название веб-страницы
            'link' : link, # ссылка веб-страницы
            'hintRes' : hintRes
            }

        return infBlockDict


    def create_inf_block_by_inf_bloc_dictionary_TLH(self, infBlockDict):
        """Формирование тектового информационного начального блока на базе форматного словаря блока"""
        titlePrefMarker = ';;;;' # префикс-метка названия блока 
        linkPrefMarker = '         * '  # перфикс-метка ссылки веб-страницы

        
        # Сотсавление инф.блока
        infBlock = '\n'
        infBlock += f"{titlePrefMarker} {infBlockDict['infBlTitle']} \n"
        infBlock += f"{linkPrefMarker} {infBlockDict['link']}"
        infBlock += '\n'

        return infBlock



    def get_inf_blocks_of_txt_TLH (self, tlhTxt):
        """Разбить TLH текст на информационные блоки и передать их в словаре , где ключ - ссылка
        tlhTxt - текст в формате TLH (Title - Href - Hints)
        RETURN: массив информационных блоков, на которые разбивается текст в формате TLH по делиметру ';;;;'
        """
        infBlocks = tlhTxt.split(';;;;') # Разбиение текста TLH на блоки по делиметру ';;;;'
        infBlocks = infBlocks[1:] # Обрубаем нудевую часть. Нулевая часть разбиения - не является инф.блоком, а string перед первым делиметром ';;;;'
        # # Цикл по инф.блокам
        # for infBlock in infBlocks:

        #     # Разбить на линии по делиметру '\n' и получить строки блока
        #     infBlockLines = self.split_tlh_inf_block_into_string_lines(infBlock)
        #     print(f"infBlockLinesN = {len(infBlockLines)}")

        return infBlocks





    def get_str_lines_of_inf_block_TLH (self, infBlock):
        """Разбить infBlock на строки по делиметру '\n' и получить массив строк блока"""

        # Разбить на линии по делиметру '\n' и получить строки блока
        infBlockLines = infBlock.split('\n') # получаем строки текста блока
        # Добавить '\n' к каждой линии в конце, что бы восстановить оригинальные строки, разделенные делиметром '\n'
        infBlockLines = [(x+'\n') for x in infBlockLines] # восстанавливаем split - делиметр
        # Удаляем последнюю, так как она - остаточная от split по '\n'
        infBlockLines = infBlockLines[:-1]
        
        return infBlockLines



    def add_inf_hints_to_tlh_block_lines(self, infBlockLines:list, dsInfHints:list) -> list:
        """Добавить новые строки с хинтами (быстрой вспомогательной информацие, типа , телефоны и пр.) в массив строк блока 
        через делимитр hint ('>>>' , новая строка с отступом Tab -> infHINT) по русле формата TLH
        infBlockLines - массив строк информационного блока TLH  <list>
        dsInfHints - спсок информационных элементов (strings) , которые нужно добавить в виде строк HINT в ракурсе формата TLH <list>
        RETURN: Возвращаем инф.блок infBlockLines с добавленными хинтами 
        """
        # Формируем строковый массив HINTS на базе dsInfHints (информационные hints)
        hintMark = '                >>>\n' # Кол-во пробелов = 16
        for infHint in dsInfHints: # цикл по массиву информационных хинтов
            infHintLine = f"                    {infHint}\n" # Кол-во пробелов = 20
            # Проверка дублирования
            if not infHintLine in infBlockLines:
                infBlockLines.append(hintMark) # добавляем в массив строк инф.блока метку хинта hintMark с необходимыми intend                
                infBlockLines.append(infHintLine) # добавляем строку с инф.хинтом
        return infBlockLines # Возвращаем инф.блок с добавленными хинтами






    def find_inx_of_inf_block_in_ds_with_given_str_fragment(self, dsInfBlocks, strSrchFragm):
        """Найти индекс информационного блока, в котором обнаружен искомый стринговый фрагмент (например, ссылка в качестве ключа)
        dsinfBlocks - массив информационных блоков в формате TLH
        strSrchFragm - стринговый фрагмент, который ищется в тексте блока
        RETURN: Если найден, то возвращает индекс в массиве блока, в котормо найдено значение
                Если ни в одном не найдено совпадение возвращает -1
        """
        for i, item in enumerate(dsInfBlocks):
            if strSrchFragm in item:
                return i # индекс вряда в массиве, в котором найдено совпадение
            
        return -1 # Если вообще не найдено совпадения ни в одном блоке


    def find_inx_of_text_list_lines_containing_fragm (self, textListLines, strFragm):
        """Находим индекс строки, в которой есть 'if __name__ == '__main__''"""
        index =  [idx for idx, s in enumerate(textListLines) if strFragm in s][0]
        return index




    def insert_txt_fragm_by_inx_relative_to_srch_fragm_first_occurence (self, baseTxtInLines, srchFragm , txtInsert, relInx ):
        """ <НЕ ТЕСТИРОВАН>
        Вставить блок текста в   текстовый файл до или после первого совпадения искомого стрингового фрагмента в тексте
        baseTxtInLines - текст в виде списка строк
        relInx : -1 вставить до найденного фрагмента/ 1 вставить после найденного фрагмента 
        srchFragm - искомый фрагмент в тексте
        """
        # Находим индекс строки, в которой есть 
        indexFound = self.find_inx_of_text_list_lines_containing_fragm (baseTxtInLines, srchFragm)
        # Переводим текст в список строк
        txtInsertLines = self.get_str_lines_of_text (txtInsert)
        # Вставить txtInsert в pageLines перед индексом indexIfName

        if relInx < 0:
            indexFound = indexFound - 1 # Индекс для вставки до искомого фрагмента
        else:
            indexFound = indexFound + 1 # Индекс для вставки после искомого фрагмента

        newFinalTextLines = FG.insert_list_to_another_list_by_inx (baseTxtInLines, txtInsertLines, indexFound)
        return newFinalTextLines







    @staticmethod
    def devide_text_with_markers_by_line_blocks_static (iniText, srchMarker, breakLine = '\n', linetimes = 1, before = True, textReplaceDic = []):
        """ 
        РАзделить тектовый файл после-перед найденными маркерами определеннымм  текстовым блоком (линиями-разделителями)
        before - пока не реализован. Вставлять блок-разделитель до или после найденных маркеров в тексте
        textReplaceDic - Словарь замещений в конечном тексте 
        """


        
        
        parts = iniText.split(srchMarker)
        
        divBlock = breakLine*linetimes
        
        newText =  f'{divBlock}{srchMarker}'.join(parts)
        
        # 
        
        for key, val in textReplaceDic.items():
            
            print(f"PR_B501 --> key = {key}")
            
            newText = newText.replace(key, val)
        
        
        return   newText      














    def find_txt_block_in_txt_lines_by_begin_end_markers (self, baseTxtLines, beginMark, finalMark):
        """Найти блок текста по заданным начальному и конечному маркеру в тексте, переведенному в список строк с выходными данными начала
        и конца искомого блока в виде начального и конечного индеста в списке строк. ищет первое слвпадение начальной и конечной меток так, что бы между ними не  было
        других подобных им меток. То есть именно кратчайший блок, а не блок, который определяется верхней и нижней метками, а внутри могут быть другие стартовые метки. """
        #  цикл по строкам
        adress = []
        adress.append(0) # инициализация первым элементом, в котором будут хранится адрес первой метки блока
        flgBeginFound = 0 # Флаг нахождения первой метки в строке по циклу
        for inx, line in enumerate(baseTxtLines):

            if beginMark in line : # flgBeginFound == 0 условие, которое ограничивает только первым совпадением, все другие - пропускаются
                # adress.append(inx)
                adress[0] = inx -1
                flgBeginFound = 1

            if finalMark in line and flgBeginFound == 1:
                adress.append(inx)
                return adress

            
    @staticmethod
    def find_txt_block_in_txt_lines_by_begin_end_markers_stat (baseTxtLines, beginMark, finalMark):
        """Найти блок текста по заданным начальному и конечному маркеру в тексте, переведенному в список строк с выходными данными начала
        и конца искомого блока в виде начального и конечного индеста в списке строк. ищет первое слвпадение начальной и конечной меток так, что бы между ними не  было
        других подобных им меток. То есть именно кратчайший блок, а не блок, который определяется верхней и нижней метками, а внутри могут быть другие стартовые метки. """
        #  цикл по строкам
        listAdresses = []
        listAdresses.append(0) # инициализация первым элементом, в котором будут хранится адрес первой метки блока
        flgBeginFound = 0 # Флаг нахождения первой метки в строке по циклу
        for inx, line in enumerate(baseTxtLines):

            if beginMark in line : # flgBeginFound == 0 условие, которое ограничивает только первым совпадением, все другие - пропускаются
                # adress.append(inx)
                listAdresses[0] = inx -1
                flgBeginFound = 1

            if finalMark in line and flgBeginFound == 1:
                listAdresses.append(inx)
                # return adress
            
            
        return listAdresses
    
    
    
    
    @staticmethod
    def get_text_lines_block_by_start_and_end_inx_of_input_list_text_lines_stat (listTextLines, listFirstLastInxsSlice):
        """ 
        TextFormater
        Получить вырезку из общего списка строк текста по начальному и конечному задваемым индексам
        """
        
        # INI
        firstInx = listFirstLastInxsSlice[0]
        
        lastInx =  listFirstLastInxsSlice[1]
        
        textLinesSlicedByFirstendUnices = listTextLines[firstInx, lastInx]
        
        print(f"PR_NC_189 --> textLinesSlicedByFirstendUnices = {textLinesSlicedByFirstendUnices} ")
        
        
        
            
        
        
        
        
            
        
    # def find_txt_block_in_txt_lines_by_begin_end_markers_with_no_marks_in_between (self, baseTxtLines, beginMark, finalMark):
    #     """Найти блок текста по заданным начальному и конечному маркеру в тексте, переведенному в список строк с выходными данными начала
    #      и конца искомого блока в виде начального и конечного индеста в списке строк. ищет первое слвпадение начальной и конечной меток так, что бы между ними не  было
    #      других подобных им меток. То есть именно кратчайший блок, а не блок, который определяется верхней и нижней метками, а внутри могут быть другие стартовые метки. """
    #     #  цикл по строкам
    #     adress = []
    #     adress.append(0) # инициализация первым элементом, в котором будут хранится адрес первой метки блока
    #     flgBeginFound = 0 # Флаг нахождения первой метки в строке по циклу
    #     for inx, line in enumerate(baseTxtLines):

    #         if beginMark in line : # flgBeginFound == 0 условие, которое ограничивает только первым совпадением, все другие - пропускаются
    #             # adress.append(inx)
    #             adress[0] = inx -1
    #             flgBeginFound = 1

    #         if finalMark in line and flgBeginFound == 1:
    #             adress.append(inx)
    #             return adress





    def find_in_text_fragment_by_start_end_marks (self, txtBase, startMark, endMark) :
        """
        Нахождение блока текста в тексте по начальному фрагменту и конечному
        ret: txtBlock - найденный текстовый блок, startidx - индекс старта блока в файле, endIdx - индекс конца блока в файле
        """
        
        # Нахождение индексов начала и конца блока тескстового в общем тексте
        
        try:
            startIdx = txtBase.index(startMark)
            endIdx = txtBase.index( endMark, startIdx)
            txtBlock = txtBase[startIdx : endIdx]  
        except:
            txtBlock = f"PR_954 --> В суб-блоке не найден один из маркеров : {startMark} или {endMark}"
            startIdx = -1
            endIdx = -1
        
        
        
    
        return txtBlock, startIdx, endIdx





    def transform_str_lines_to_text (self, infBlockLines : list) -> str: 
        """Обьединяет все стринговые ряды infBlockLines блока в один текстовый информационный блок
        Возвращает один текстовый блок """
        infTxtBlock = ''
        for i, blocjLine in enumerate(infBlockLines):
            # if i ==0:
            #     infTxtBlock += ';;;;' + blocjLine

            # else:
            infTxtBlock += blocjLine

        infTxtBlock += '\n'


        return infTxtBlock


    def transform_ds_inf_blocks_to_one_text(self, dsInfBlocks):
        """Трансформировать массив информационных блоков в единый текст для обновления в файле"""

        newFileText = '\n'
        blockDelim = ';;;;'
        for blockText in dsInfBlocks:
            newFileText += blockDelim + blockText

        return newFileText






    def add_inf_hints_to_block_where_key_fragment_found(self, dsInfBlocks, strSrchFragm, infHintsList ):
        """Добавить хинты в тот блок, где найден ключевой искомый стринговый фрагмент
        dsInfBlocks - массив информационных блоков формата TLH
        strSrchFragm - ключ , стринговый искомый фрагмент, который ищется в тексте блоков. 
        infHintsList - список хинтов, Которые надо добавть в формате TLH в информационный блок, в котором найдено совпадение по искомомуц фрагменту
        RETURN: Возвращает список исходных информационных блоков, но в одном из них, в котором найден стринговый ключ, добавлены хинты в формате TLH
        """

        infBlockInx = self.find_inx_of_inf_block_in_ds_with_given_str_fragment(dsInfBlocks, strSrchFragm) # Индекс искомого блока, в котором содержится стринговый ключ strSrchFragm

        infBlockToUpdate = dsInfBlocks[infBlockInx] # Искомый блок, в котором содержится стринговый ключ

        infBlockLines = self.get_str_lines_of_inf_block_TLH(infBlockToUpdate) # стринговый линии блока, которые в тексте разделены делиметром '\n'


        newInfBlockLines = self.add_inf_hints_to_tlh_block_lines(infBlockLines, infHintsList) # Добавляем информационные хинты из масиива infHintsList в формате TLH

        return newInfBlockLines


    def update_full_file_text_tlh_with_inf_hints_by_key_str_fragment(self, fileFullTxt, srchStrFragm, dsInfHints ):
        """Обновляет текст файла в формате TLH . Добавляет в блок, в котором найден стринговый ключ (например, ссылка) информационные хинты
        в формате TLH (с маркером хинтов '>>>')
        RETURN: Возвращает обновленный хинтами в нужном информационном блоке текст всего файла """
        # получаем массив инф.блоков текста файла, который в формате TLH
        dsInfBlocks = self.get_inf_blocks_of_txt_TLH (fileFullTxt) 

        # индекс блока в массиве, в котором найден стринговый ключ srchStrFragm
        inxOfBlock = self.find_inx_of_inf_block_in_ds_with_given_str_fragment( dsInfBlocks, srchStrFragm)  
        # Перевод найденного блока в ряды стрингов по делиметру '\n'
        infBlockLines = self.get_str_lines_of_inf_block_TLH (dsInfBlocks[inxOfBlock]) 
        # Добавить в ряды стрингов найденного по стринговому ключу блока ряды с хинтами в формате TLH ('>>>')
        newInfBlockLines = self.add_inf_hints_to_tlh_block_lines(infBlockLines, dsInfHints) 

        # Трансформировать обновленные стринговые ряды в единый текст информационного блока
        newTextOfBlock = self.transform_str_lines_to_text (newInfBlockLines)

        # обновить блок , в котором искался стринговый ключ, новым текстовым содержанием newTextOfBlock
        dsInfBlocks[inxOfBlock] = newTextOfBlock

        # Трансформировать массив информационных блоков в единый текст для обновления в файле
        newFileText = self.transform_ds_inf_blocks_to_one_text(dsInfBlocks)
        
        return newFileText





    def get_title_content_dict_of_infblock_TLH(self, infBlock, filePath = ''):
        """Получить словарь, состоящий из наименования информационного блока, остальной части контенте без названия, а так же из флагов star (*) и TIPs(>>>)
        Флаги говорят о наличии в остаточном контенте меток * и >>> 
        RETURN: infBlockDict с ключами ['title', 'restContent', 'flagStar', 'flagTips']
        title - Название инф.блока (в идеале должно быть уникальным)
        restContent - оставшаяся часть контента инф.блока без его названия
        flagStar - наличие в оставшемся контенте метки *
        flagTips - наличие в оставшемся контенте метки >>>
        restContentLines - список строк из еоторых состоит оставшаяся часть контента без названия

        """

        infBlockDict = {} # Характеристический словарь инф.блока
        flagStar = False
        flagTips = False

        # Определяем title иня.блока
        # Если есть ссылка, отделяющая титульное название блока от прочего, то 
        if '*' in infBlock:
            infBlParts = infBlock.split('*') # TODO: Тут ошибка !!!!!!!!!!!
            blTitle = infBlParts[0]
            infBlockDict['title'] = blTitle
            flagStar = True
            infBlockDict['flagStar'] = flagStar

            infBlSpliByTitleparts = infBlock.split(blTitle) # Разделение инф.блока по делиметру = наименованию блока !!!
            infBlockDict['restContent'] = infBlSpliByTitleparts[1] # Присваиваем оставшуюся часть в значение словаря с ключем 'restContent'

            if '>>>' in infBlParts[1]: 
                infBlockDict['flagTips'] = True
            else: 
                infBlockDict['flagTips'] = False

            tLines = self.get_str_lines_of_text(infBlockDict['restContent'] )    # список строк из еоторых состоит оставшаяся часть контента без названия
            infBlockDict['restContentLines'] = tLines

        elif '>>>' in  infBlock:  # Если нет * , то может есть TIPS '>>>'
            infBlParts = infBlock.split('>>>')
            blTitle = infBlParts[0]
            infBlockDict['title'] = blTitle
            # flagTips = True
            infBlockDict['flagStar'] = flagStar
            infBlockDict['restContent'] = '>>> ' + infBlParts[1] # Восстанавливаем удаленную в split() метку '>>> '
            infBlockDict['flagTips'] = True
          
            tLines = self.get_str_lines_of_text(infBlockDict['restContent'] )    # список строк из еоторых состоит оставшаяся часть контента без названия
            infBlockDict['restContentLines'] = tLines

        else :

            infBlockDict['title'] = 'NONE'
            infBlockDict['flagStar'] = False
            infBlockDict['restContent'] = infBlock
            infBlockDict['flagTips'] = False
            
            tLines = self.get_str_lines_of_text(infBlockDict['restContent'] )    # список строк из еоторых состоит оставшаяся часть контента без названия
            infBlockDict['restContentLines'] = tLines


        # Получаем так же массив строк остаточного контента в виде списка и добавляем  словарь с ключем 'restTextLines'




        return infBlockDict



    def get_list_of_title_content_dict_of_ftext_TLH (self, fText):
        """Получить список слолварей [{title , restContent}, ...] соотвесттвующих разбиению полного текста файла fText на инф.блоки по метке ';;;;' """

        infBlocks = self.get_inf_blocks_of_txt_TLH (fText) # Получаем инф.блоки TLH

        # Преобразовать инф.блоки в характеристические словари TLH
        
        fInfBlockDictList = [] # Список характеристических словарей инф.блоков файла TLH
        for infBlock in infBlocks:

            infBlockDict = self.get_title_content_dict_of_infblock_TLH(infBlock) # словарь, состоящий из наименования информационного блока, остальной части контенте без названия, а так же из флагов star (*) и TIPs(>>>)

            fInfBlockDictList.append(infBlockDict) # Включение текущего по циклу сформирвоанного Х-словаря в список словарей-болков файла   

        return fInfBlockDictList


    








## END TLH формат: Методы для работы с форматирвоанием текста для IAC (Information Assembling Center - центр управления информацией в текстовфх файлах компьюиера, для сохранения различной информации
#       по формату [ ;;;; Title -> * link (or FTP link) -> >>> hints ]. Аббревиатура формата: TLH)




    ## Методы обработки строковых переменных формата TLH  \t\n

    def clear_TLH_lines_to_links(self, dsStarLines):
        """Отчистка строки для хранения ссылок (со звездочками которые в формате ) от всего . Получение чистой ссылки"""
        dsLinks = [x.replace(' ','').replace('*', '').replace('\t','').replace('\n', '') for x in dsStarLines]
        return dsLinks








    ## END Методы обработки строковых переменных 




# ОБЩИЕ ФУНКЦИИ

    def get_str_lines_of_text (self, text):
        """TextFormater
        Разбить infBlock на строки по делиметру '\n' и получить массив строк блока"""

        # Разбить на линии по делиметру '\n' и получить строки блока
        tLines = text.split('\n') # получаем строки текста блока
        # Добавить '\n' к каждой линии в конце, что бы восстановить оригинальные строки, разделенные делиметром '\n'
        tLines = [(x+'\n') for x in tLines] # восстанавливаем split - делиметр
        # Удаляем последнюю, так как она - остаточная от split по '\n'
        tLines = tLines[:-1]
        
        return tLines
    
    
    def get_str_lines_of_text_full (self, text):
        """
        TextFormater
        Разбить infBlock на строки по делиметру '\n' и получить массив строк блока
        ПРИМ: Без удаления последней строки
        """

        # Разбить на линии по делиметру '\n' и получить строки блока
        tLines = text.split('\n') # получаем строки текста блока
        # Добавить '\n' к каждой линии в конце, что бы восстановить оригинальные строки, разделенные делиметром '\n'
        tLines = [(x+'\n') for x in tLines] # восстанавливаем split - делиметр

        
        return tLines
    
    
    
    
    @staticmethod
    def get_str_lines_of_text_static (text):
        """TextFormater
        Разбить text на строки по делиметру '\n' и получить массив строк блока"""
        
        # print(f"&&&&&&&&&&&&&$$$$$$$$$$$  text = {text}")

        # Разбить на линии по делиметру '\n' и получить строки блока
        tLines = text.split('\n') # получаем строки текста блока
        # Добавить '\n' к каждой линии в конце, что бы восстановить оригинальные строки, разделенные делиметром '\n'
        tLines = [(x+'\n') for x in tLines] # восстанавливаем split - делиметр
        # Удаляем последнюю, так как она - остаточная от split по '\n'
        tLines = tLines[:-1]
        
        return tLines


    def convert_str_lines_to_text (self, txtLines : list) -> str: 
        """TextFormater
        Обьединяет все стринговые ряды infBlockLines блока в один текстовый информационный блок
        Возвращает один текстовый блок """
        rtotalText = ''
        for i, strLine in enumerate(txtLines):
            rtotalText += strLine
        return rtotalText
    
    @staticmethod
    def convert_str_lines_to_text_static (txtLines : list) -> str: 
        """TextFormater
        Обьединяет все стринговые ряды infBlockLines блока в один текстовый информационный блок
        Возвращает один текстовый блок """
        rtotalText = ''
        for i, strLine in enumerate(txtLines):
            rtotalText += strLine
        return rtotalText


# END ОБЩИЕ ФУНКЦИИ


# Format for HTML

    @staticmethod
    def convert_text_to_HTML_block(textStr):
        """
        Конвертируем текстовый блок  в формат HTML 
        """
        txtFormatter = TextFormater()
        txtLines = txtFormatter.get_str_lines_of_text(textStr)
        htmlText = ''
        for line in txtLines:
            
            line = line.replace('\n', '<br>')
            line = line.replace('\t', '&emsp;') # табулирование
            htmlText += line 

        # htmlText = htmlText # перевод строки для разделения от заголовка

        return htmlText




# END Format for HTML




# === III. ЧИСТИЛЩИКИ =========================================================

    @staticmethod
    def clear_multiple_spaces_stat (textFragm):
        """ 
        Все мульти-пробелы внутри свести к одному пробелу, включая tabs, newlines, etc
        ~ https://stackoverflow.com/questions/1981349/regex-to-replace-multiple-spaces-with-a-single-space
        """
        
        # This -> you really want to cover only spaces (and thus not tabs, newlines, etc)
        # resText = textFragm.strip().replace(" /  +/g", ' ' ).replace('.#','')  
        
        # you also want to cover tabs, newlines, etc ()
        resText = textFragm.strip().replace("/\s\s+/g", ' ' ).replace('.#','') 
        
        
        return resText



# === END III. ЧИСТИЛЩИКИ =========================










if __name__ == "__main__":
    pass