"""Настройки для работы системы алгоритмов с условным названием ALGORITHM_CUBE"""


# ПЕРЕМЕННЫЕ НАСТРОЙКИ (индивидуальные для каждого проекта)

PROJ_DIR_= '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/algorithms'


# END ПЕРЕМЕННЫЕ НАСТРОЙКИ (индивидуальные для каждого проекта)




# ПОСТОЯННЫЕ НАСТРОЙКИ (остаются одинаковыми для любых проектов)


# НАСТРОЙКА СТРУКТУРНЫХ ШАБЛОНОВ ДЛЯ СОЗДАНИЯ НОВОГО АЛГОРИТМА (настройки для создания отдельного суб-блока ниже)
# Настройки вставки кодов для созданяи структуры нового алгоритма в системный файлы, образующие систему алгоритмов (5 файлов) 

# Вставка в системный файл sysAlgorithmsMain.
# !!! Отступ (intend) в этих константах шаблонов вставного кода структуры алгоритма - ВАЖНА!!! Поэтому не менять отступ после тройной кавычки в константе (а именно д.б. 2 интенда Python)
ALG_STRUCT_FOR_ASYSFILE1 = f"""
        # %ALG_DESCR%
        if ALG_%ALG_ID%: 
            print(f"START: %ALG_ID% ######## STEP ")

            SysAlgorithms.a_%ALG_ID%_%ALG_NAME%()




        """




# Вставка в системный файл sysAlgorithms . 
# !!! Отступ (intend) в этих константах шаблонов вставного кода структуры алгоритма - ВАЖНА!!! Поэтому не менять отступ после тройной кавычки в константе (а именно д.б. 2 интенда Python)
ALG_STRUCT_FOR_ASYSFILE2 = f"""




    @staticmethod
    def a_%ALG_ID%_%ALG_NAME%():
        \"""SysAlgorithms
        %ALG_DESCR%
        \"""
        print("START ALG_%ALG_ID%: SysAlgorithms.a_%ALG_ID%_%ALG_NAME%()   ~~~~~~~~~~ ALGORITHM")

        # %SUBBLOCK_DESCR%
        if SB%ALG_ID%_%SUBBLOCK_INX%:

            SysSubblocks.sb%ALG_ID%_%SUBBLOCK_INX% ()

        # <END SUBBLOCK>




"""



# Вставка в системный файл sysAlgorithmsSettings . 
# !!! Отступ (intend) в этих константах шаблонов вставного кода структуры алгоритма - ВАЖНА!!! Поэтому не менять отступ после тройной кавычки в константе (а именно д.б. 2 интенда Python)
ALG_STRUCT_FOR_ASYSFILE3 = f"""

ALG_%ALG_ID% = True # %ALG_ID%. %ALG_DESCR%






"""


# Вставка в системный файл sysSubblocks . 
# !!! Отступ (intend) в этих константах шаблонов вставного кода структуры алгоритма - ВАЖНА!!! Поэтому не менять отступ после тройной кавычки в константе (а именно д.б. 2 интенда Python)
ALG_STRUCT_FOR_ASYSFILE4 = f"""

    ###  ALG_%ALG_ID%  %ALG_DESCR%
 

    @staticmethod
    def sb%ALG_ID%_%SUBBLOCK_INX% ():
        \"""SysSubblocks%PROJ_NICK%
        
        \"""
        print("START SUB-BLOCK: SysSubblocks.sb%ALG_ID%_%SUBBLOCK_INX%()    ----------- SUBBLOCK")



        print (f"END sb%ALG_ID%_%SUBBLOCK_INX%  ========== END")

    # <END SUBBLOCK>

    ###  END ALG_%ALG_ID%  %ALG_DESCR%





"""




# Вставка в системный файл sysSubblocksSettings . 
# !!! Отступ (intend) в этих константах шаблонов вставного кода структуры алгоритма - ВАЖНА!!! Поэтому не менять отступ после тройной кавычки в константе (а именно д.б. 2 интенда Python)
ALG_STRUCT_FOR_ASYSFILE5 = f"""

###  ALG_%ALG_ID%  %ALG_DESCR%
 

SB%ALG_ID%_%SUBBLOCK_INX% = True # %SUBBLOCK_DESCR%
# <END SUBBLOCK>

### END ALG_%ALG_ID%  %ALG_DESCR%





"""


# END НАСТРОЙКА СТРУКТУРНЫХ ШАБЛОНОВ ДЛЯ СОЗДАНИЯ НОВОГО АЛГОРИТМА 

# словарь с пятью системными модулями, отвечающими за рабооту системы алгоритмов AlgrtmCube
# В  данном случае '' должно было стоять исключистельно добавкой в конце названий файлов
ALG_SYS_MODULES_ = {

        'sysAlgorithmsMain' : ['sys_algorithms_main.py', ALG_STRUCT_FOR_ASYSFILE1],
        'sysAlgorithms' : ['sys_algorithms.py', ALG_STRUCT_FOR_ASYSFILE2],
        'sysAlgorithmsSettings' :  ['sys_algorithms_settings.py', ALG_STRUCT_FOR_ASYSFILE3],
        'sysSubblocks' : ['sys_subblocks.py', ALG_STRUCT_FOR_ASYSFILE4],
        'sysSubblocksSettings' :  ['sys_subblocks_settings.py', ALG_STRUCT_FOR_ASYSFILE5]
    }






# НАСТРОЙКА СТРУКТУРНЫХ ШАБЛОНОВ ДЛЯ ВСТАВКИ ОТДЕЛЬНОГО СУБ-БЛОКА В УЖЕ СУЩЕСТВУЮЩИЙ АЛГОРИТМ
# Вставка в системный файл sysAlgorithms для метода субблока . 
# !!! Отступ (intend) в этих константах шаблонов вставного кода структуры алгоритма - ВАЖНА!!! Поэтому не менять отступ после тройной кавычки в константе (а именно д.б. 2 интенда Python)
SUBBLOCK_STRUCT_FOR_ASYSFILE2 = f"""



        # %SUBBLOCK_DESCR%
        if SB%ALG_ID%_%SUBBLOCK_INX%:# <END SUBBLOCK>

            SysSubblocks.sb%ALG_ID%_%SUBBLOCK_INX% ()

        # <END SUBBLOCK>




"""




# Вставка в системный файл sysSubblocks для метода субблока . 
# !!! Отступ (intend) в этих константах шаблонов вставного кода структуры алгоритма - ВАЖНА!!! Поэтому не менять отступ после тройной кавычки в константе (а именно д.б. 2 интенда Python)
SUBBLOCK_STRUCT_FOR_ASYSFILE4 = f"""



    @staticmethod
    def sb%ALG_ID%_%SUBBLOCK_INX% ():
        \"""SysSubblocks%PROJ_NICK%
        
        \"""
        print("START SUB-BLOCK: SysSubblocks.sb%ALG_ID%_%SUBBLOCK_INX%()")




"""




# Вставка в системный файл sysSubblocksSettings для метода субблока. 
# !!! Отступ (intend) в этих константах шаблонов вставного кода структуры алгоритма - ВАЖНА!!! Поэтому не менять отступ после тройной кавычки в константе (а именно д.б. 2 интенда Python)
SUBBLOCK_STRUCT_FOR_ASYSFILE5 = f"""

SB%ALG_ID%_%SUBBLOCK_INX% = True # %SUBBLOCK_DESCR%
# <END SUBBLOCK>

"""


# END НАСТРОЙКА СТРУКТУРНЫХ ШАБЛОНОВ ДЛЯ ВСТАВКИ ОТДЕЛЬНОГО СУБ-БЛОКА В УЖЕ СУЩЕСТВУЮЩИЙ АЛГОРИТМ




# словарь с тремя системными модулями, отвечающими за структуру суб-блоков в алгоритме
SUBBLOCKS_SYS_MODULES_ = {
        'sysAlgorithms' : ['sys_algorithms.py', SUBBLOCK_STRUCT_FOR_ASYSFILE2],
        'sysSubblocks' : ['sys_subblocks.py', SUBBLOCK_STRUCT_FOR_ASYSFILE4],
        'sysSubblocksSettings' :  ['sys_subblocks_settings.py', SUBBLOCK_STRUCT_FOR_ASYSFILE5]
    }







# END ПОСТОЯННЫЕ НАСТРОЙКИ (остаются одинаковыми для любых проектов)












