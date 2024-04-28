

from infor_assembling_center.text_formater import TextFormater
from infor_assembling_center.files_manager import FilesManager
import bonds.funcs_general as FG
from bonds.switch import Switch
from project_bonds_html.projr.settings_sys_algorithms import *


class AlgorithmStructureManager ():
    """ЗАГОТОВКА: Управление созданием структуры алгоритмов и их суб-блоков
    TODO: Создать отдельный проект для этого модуля. Целый проект пусть занимается созданием и управлением алгоритмов в других проектах
    TODO: Сделать возможность удаления структуры заданного алгоритма
    """


    def __init__(self, newAlgSettings):

        self.sysAlgrmModules = ALG_SYS_MODULES_ # Образующие систему кубиков алгоритмов (AlgorithmCubes) базовые 5 файлов
        self.sysSubblocksModules = SUBBLOCKS_SYS_MODULES_ # Образующие систему кубиков алгоритмов (AlgorithmCubes) базовые 5 файлов
        self.projDir = PROJ_DIR_
        self.newAlgSettings = newAlgSettings # Настройки для создания структуры нового алгоритма
        self.subBlockInx = 1 # дефолтный индекс суб-блока
        self.transform_alg_sis_file_dic_to_full_path_() # Трансформировать словарь с базовыми системными файлами системы алгоритмлов в словарь с файлоами с полными путями
        self.replace_special_marks_in_sys_modules_dic_for_new_algorithm() # Замещение шаблонных меток в заготовках структурных кодов текущим индексным окончанием в словаре self.sysAlgrmModules в соотв. шаблонах 
        # <INSERT NEW FINAL CODE BLOCKES IN FILES>
        # self.create_astructure() # Вставляем в файлы соотвтетствующие структурные коды-добавки с уже готовым кодом и настройками по проекту и создаваемому алгоритму



    def create_astructure(self):
        """
        ЗАГОТОВКА: Создание структуры алгоритма в програмных файлах
        newAlgthmName - название нового алгоритма 
        sysAlgrmModules - словарь с пятью системными модулями, отвечающими за рабооту системы алгоритмов AlgrtmCube
        Category: Конструктор проектов
        """
        # цикл по словарю системных модулей , где хранятся пути к файлам и соотвтествующие шаблоны вставок в эти файлы для каждого  системного файла
        for key, val in self.sysAlgrmModules.items(): 

            currSysFilePathAndTemplate = val # путь и шаблон блока кода в текущем системном модуле по циклу
            sysModuleNick = key # ник-нейм текущего по циклу модуля для дальнейшей дифференцированной обработки данных , соответствующих каждому модулю

            # Вставка вв каждый системный файл своего готового блока кода структуры алгоритмов
            self.insert_alg_srtucture_code_to_file_ (currSysFilePathAndTemplate[0], currSysFilePathAndTemplate[1], sysModuleNick) 




    def add_subblock(self, subBlockInx , algInxAdd = None, subblockDescr = ''):
        """
        ЗАГОТОВКА. Добавление суб-блока в заданный индексной добавкой алгоритм
        algInxAdd - индексная добавка алгоритма, к которому надо добавить суб-блок (пока просто заглушка)
        subBlockInx - индекс добавляемого суб-блок в алгоритме
        subblockDescr - описание суб-блока (пока просто заглушка)
        Category: Конструктор проектов
        """
        print ('START: add_subblock()')

        # @@@ Присваивание индекса создаваемого субблока
        self.subBlockInx = subBlockInx
        self.replace_special_marks_in_sys_modules_dic_for_new_subblock() # Замещение шаблонных меток в заготовках структурных кодов текущим индексным окончанием в словаре self.sysAlgrmModules в соотв. шаблонах 

        # цикл по словарю системных модулей , где хранятся пути к файлам и соотвтествующие шаблоны вставок в эти файлы для каждого  системного файла
        for key, val in self.sysSubblocksModules.items(): 

            currSysFilePathAndTemplate = val # путь и шаблон блока кода в текущем системном модуле по циклу
            sysModuleNick = key # ник-нейм текущего по циклу модуля для дальнейшей дифференцированной обработки данных , соответствующих каждому модулю

            # Вставка вв каждый системный файл своего готового блока кода структуры алгоритмов
            self.insert_subblock_srtucture_code_to_file_ (currSysFilePathAndTemplate[0], currSysFilePathAndTemplate[1], sysModuleNick, subBlockInx) 


        # ДЛЯ ФАЙЛОВ sysAlgorithms:

        # 1.Получение файла в виде строк




        # 2.Нахождение строки, содержаще название алгоритма a_005_get_comp_decription_by_inn ()

        # 3. Нахождение маркера конца суб-блока в этом алгоритме <END SUBBLOCK>

        # 4. Вставка после этого маркера блока с кодом нового суб-блока


        # ДЛЯ ФАЙЛОВ sysSubblocks:

        # 1. Нахождение строки с названием предыдущего субблока, а потом маркера конца субблока <END SUBBLOCK> # TODO: Вставить в шаблон этот маркер

        # 2. Вставка после этого маркера блока с кодом нового суб-блока


        # ДЛЯ ФАЙЛОВ sysSubbloksSettings:
# Настрой

        # 1. Нахождение ситроки с SB005_1

        # 2. Вставка после нее кода субблока





    def insert_alg_srtucture_code_to_file_ (self, filePath, codeInsert, sysModuleNick):
        """
        Вставить структурный код системы алгоритмов в определенное место системного файла алгоритмов
        Вставляем текстовую вставку до найденного фрагмента '__name__' текста в файле, который соотвтетствует строке кода  'if __name__ == '__main__' (то есть - перед ней)
        sysModuleNick - ник или ключ в словаре системных модулей self.sysAlgrmModules
        Category: Конструктор проектов
        """
        

        # SWITCH ... CASE для дифференцированной вставки кода в разнфе системные файлы. В каждый файл место вставки может отличаться
        for case in Switch(sysModuleNick): # SWITCH ... CASE для замещения маркеров в каждой соответствующей вставке кода для своего системного файла своими индексными добавками

            # Вставка блока кода перед поисковой меткой '__name__', которая соотвтетствует строке кода  'if __name__ == '__main__' (то есть - перед ней)
            if case('sysAlgorithmsMain'): pass
            if case('sysAlgorithms'): pass
            if case('sysSubblocks'):
                fileManager = FilesManager(filePath) # создание файлового менеджера своего для каждого системного файла 
                print(f'Вставка кода в  {sysModuleNick}')
                strSearched = '__name__'
                # Вставляем текстовую вставку до найденного фрагмента '__name__' текста в файле, который соотвтетствует строке кода  'if __name__ == '__main__' (то есть - перед ней)
                fileManager.insert_txt_fragm_to_txt_file_before_str_fragm_first_occurence (strSearched, codeInsert)
                break



            # Вставка кода в конец содержимого файла
            if case('sysAlgorithmsSettings'): pass
            if case('sysSubblocksSettings'):
                print('Вставка кода в sysAlgorithmsSettings')
                fileManager = FilesManager(filePath) # создание файлового менеджера своего для каждого системного файла 
                fileManager.add_text_to_end_of_file_data(codeInsert)
                break


            if case(): # default
                print('Не найдено')
                break






    def insert_subblock_srtucture_code_to_file_ (self, filePath, codeInsert, sysModuleNick, subBlockInx):
        """
        Вставить структурный код отвечающий за суб-блок в алгоритме (т.е. вставить новый суб-блок)
        Category: Конструктор проектов
        """
        fileManager = FilesManager(filePath) # создание файлового менеджера своего для каждого системного файла 
        subBlockInx = int(subBlockInx)
        algId_ = self.newAlgSettings['algId']
        algName_ = self.newAlgSettings['algName']
        subBlockInxSrch_ = str(subBlockInx - 1) # Индекс предыдущего субблока в названии его метода искомый

        # SWITCH ... CASE для дифференцированной вставки кода в разнфе системные файлы. В каждый файл место вставки может отличаться
        for case in Switch(sysModuleNick): # SWITCH ... CASE для замещения маркеров в каждой соответствующей вставке кода для своего системного файла своими индексными добавками

            # Вставка блока кода после метки <END BLOCK> в отсеке заданного алгоритма после последнего суб-блока
            if case('sysAlgorithms'): 
                print(f'Вставка кода в  {sysModuleNick}')
                srchBlockStartMarker = f'a_{algId_}_{algName_}' # Начальный маркер искомого блока в тексте
                srchBlockFinalMarker = '<END SUBBLOCK>' # Конечный маркер искомого блока в тексте
                break


            if case('sysSubblocks'):
                print(f'Вставка кода в  {sysModuleNick}')
                srchBlockStartMarker = f'sb{algId_}_{subBlockInxSrch_}' # Начальный маркер искомого блока в тексте
                srchBlockFinalMarker = '<END SUBBLOCK>' # Конечный маркер искомого блока в тексте
                # Вставляем текстовую вставку после метки <END BLOCK> в отсеке заданного алгоритма после последнего суб-блока
                break

            # Вставка кода в конец содержимого файла
            if case('sysSubblocksSettings'):
                print('Вставка кода в sysAlgorithmsSettings')
                srchBlockStartMarker = f'SB{algId_}_{subBlockInxSrch_}' # Начальный маркер искомого блока в тексте
                srchBlockFinalMarker = '<END SUBBLOCK>' # Конечный маркер искомого блока в тексте
                # Вставляем текстовую вставку после метки <END BLOCK> в отсеке заданного алгоритма после последнего суб-блока
                break


            if case(): # default
                print('Не найдено')
                break


        # Вставляем текстовую вставку после метки <END BLOCK> в отсеке заданного алгоритма после последнего суб-блока
        fileManager.insert_block_to_txt_file_by_relative_inx_to_srch_block_first_occurence (srchBlockStartMarker , srchBlockFinalMarker, codeInsert, 1 )






    def transform_alg_sis_file_dic_to_full_path_(self):
        """
        @@@ Трансформировать словарь с базовыми системными файлами системы алгоритмлов в словарь с файлоами с полными путями
        Category: Конструктор проектов"""
        # Трансформация словаря для алгоритмов
        self.sysAlgrmModules = { key :  [f"{self.projDir}/{val[0]}", val[1]]  for key, val in  self.sysAlgrmModules.items() } 

        # Трансформация словаря для суб-блоков    
        self.sysSubblocksModules = { key :  [f"{self.projDir}/{val[0]}", val[1]]  for key, val in  self.sysSubblocksModules.items() }    


    def replace_special_marks_(self, codeBlock):
        """Замещение специальных маркеров в тексте шаблона кода текущими данными проекта и создаваемого алгоритма из словаря настроек self.newAlgSettings"""
        projNick = self.newAlgSettings['projNick'] # ник проекта
        algindx = self.newAlgSettings['algId'] # задаваемое индексное окончание для новой структуры создаваемого алгоритма
        algDescr = self.newAlgSettings['algDescr'] # описание алгоритма
        algName = self.newAlgSettings['algName'] # Название алгоритма
        subBlockInx = str(self.subBlockInx)

        codeBlock = codeBlock.replace('%ALG_DESCR%', algDescr) # Замещаем  маркер ника проекта реальным ником данного проекта
        codeBlock = codeBlock.replace('%PROJ_NICK%', projNick) # Замещаем  маркер ника проекта реальным ником данного проекта
        codeBlock = codeBlock.replace('%ALG_ID%', algindx) # Замещаем  маркер индексного окончания создаваемого алгоритма  реальным индексным окончанием алгоритма
        codeBlock = codeBlock.replace('%ALG_NAME%', algName) # Замещаем маркер названия алгоритма реальным названием алгоритма
        codeBlock = codeBlock.replace('%SUBBLOCK_INX%', subBlockInx) # Замещаем маркер индекса суб-блока в алгоритме, если такой предусмотрен


        return codeBlock


    
    def replace_special_marks_in_sys_modules_dic_for_new_algorithm(self):
        """Замещение шаблонных меток в словаре системных файлов и их шаблонов кода
        Category: Конструктор проектов
        """
        # цикл по словарю системных модулей , где хранятся пути к файлам и соотвтествующие шаблоны вставок в эти файлы для каждого  системного файла
        # Замещения в структурных шаблонах для создания нового алгоритма
        for key, val in self.sysAlgrmModules.items(): 
            sysFileNick = key # ключ в словаре self.sysAlgrmModules - это никнейм системного файла
            print(f'{sysFileNick}')
            currFTemplate = self.sysAlgrmModules[sysFileNick][1] # Шаблонная вставка текущего по циклу файла в словаре
            newRealCode = self.replace_special_marks_(currFTemplate) # Замещение специальных маркеров в тексте шаблона кода текущими данными проекта и создаваемого алгоритма из словаря настроек self.newAlgSettings
            self.sysAlgrmModules[sysFileNick][1] = newRealCode # Присваиваем в словарь новый шаблон блока вставки уже с реальными ником проекта и индексным окончанием алгоритма





    
    def replace_special_marks_in_sys_modules_dic_for_new_subblock(self):
        """
        Замещение шаблонных меток в словаре системных файлов и их шаблонов кода
        Category: Конструктор проектов
        """
        # цикл по словарю системных модулей , где хранятся пути к файлам и соотвтествующие шаблоны вставок в эти файлы для каждого  системного файла
        # Замещения в структурных шаблонах для создания нового алгоритма
        for key, val in self.sysSubblocksModules.items(): 
            sysFileNick = key # ключ в словаре self.sysSubblocksModules - это никнейм системного файла
            print(f'{sysFileNick}')
            currFTemplate = self.sysSubblocksModules[sysFileNick][1] # Шаблонная вставка текущего по циклу файла в словаре
            newRealCode = self.replace_special_marks_(currFTemplate) # Замещение специальных маркеров в тексте шаблона кода текущими данными проекта и создаваемого алгоритма из словаря настроек self.newAlgSettings
            self.sysSubblocksModules[sysFileNick][1] = newRealCode # Присваиваем в словарь новый шаблон блока вставки уже с реальными ником проекта и индексным окончанием алгоритма







if __name__ == '__main__':
    pass















    # ПРОРАБОТКА: метода create_main_algthm_structure() -  Создание структуры алгоритма в програмных файлах
    
    """
        ИТОГО 5 системных файлов в конечном варианте проекта:
        
        - classes/sys_algorithms_main.py
        - classes/sys_algorithms_settings.py
        - classes/sys_algorithms.py
        - classes/sys_subblocks_settings.py
        - classes/sys_subblocks.py
    """



    # TODO: Корни системных файлов всегда должны быть константными, добавляться только окончание в виле ника проекта. Тогда не нужно будет передавать ALG_SYS_MODULES параметром !!!

    # Описание алгоритма
    algDescr = """Фильтрация и вывод облигаций в зависимости от даты первичного их внесения в БД в таблицу bonds_archive при считывании или обновления текущей выборки по облигациям со СМАРТА"""
    

    newAlgSettings = {
        'algName' : 'bonds_inserted_to_archive_by_date',
        'projNick' : '', # Пока не удалять ник-проекта. Оставлять пустым. УДАЛИТЬ СНАЧАЛА ВНУТРИ КОДА ЕГО УПОТРЕБЛЕНИЕ, ЧТО БЫ НЕ ЗАБЮЫТЬ
        'algDescr' : algDescr,
        'algId' : '033' # или вместе с добакой с окончанием, типа ('auxilary' etc)
    }

    algStructMngr = AlgorithmStructureManager(newAlgSettings) # Создание структуры нового алгоритма в 5 системных файлах

    # # Создание структуры алгоритма и первого суб-блока
    # algStructMngr.create_astructure()

    # Проработка метода создания суб-блока
    # TODO: Вносит не туда, если не последний алгоритм 
    # # Pars:
    subBlockInx = '2'
    algStructMngr.add_subblock(subBlockInx)



































