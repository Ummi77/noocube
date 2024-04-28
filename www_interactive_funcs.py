
import math
from time import sleep

from noocube.sqlite_bonds_macros import SqliteBondsMacros 
from noocube.sqlite_processor import SqliteProcessor
import noocube.funcs_general as FG
from noocube.funcs_general_class import FunctionsGeneralClass  # get_func_obj_by_path_to_class_file_static (fileClassPath, expectedClass, funcName)


# Закоментить
# from bonds.bonds_macros import BondsMacros
# from bonds.checko_manager import CheckoManager
# from bonds.finplan_manager import FinplanManager
# from bonds.html_pars_manager import HTMLSeleniumManager
# from bonds.rbc_manager import RbcManager
# from bonds.rusbonds_manager import RusbondsManager
# from bonds.smsrtlab_manager import SmartlabManager
# from bonds.spark_manager import SparkManager
# from bonds.settings import DEBUG_
# from bonds.moex_manager import MoexManager
# from bonds.settings import ALGORITHM_MESSEGES_, DB_BONDS_, DEBUG_, TB_GLOBAL_A_
# End Закоментить

class WWWInteractiveUniversal ():
    """  Класс для универсальных методов работы с вэб-ресурсами """
    

### --- UNIVERSAL EPOCH FUNCTIONS для поиска данных на сайтах БЕЗ ПЕРЕДАЧИ АТРИБУТОВ АТОМАРНОЙ ФУНКЦИИ . ДОЛЖНО УСТАРЕТЬ ПОСТЕПЕННО . НОВЫЙ КОМПЛЕКС ФУНКЦИЙ ДОЛЖЕН ПОЛУЧАТЬ ПАРАМЕТРЫ АТОМАРНОЙ ФУНКЦИИ------------------


        # ПРИМЕР: Не удалять. Формат использования ФНЦИП !!!
        # dsInp = dsOrigList # Входной массив ОКПО тех бумаг, которых нет в архиве bonds_archive
        # # # Поиск данных ИНН и пр по ОКПО на сайте spark с подходом по эпохам (для уменьшения рисков потери данных)
        # # Pars атомарной функции поиска:
        # aifFuncParams = { # Параметры атомарной функции с ее полным название и параметрами к ней, которые позволяют расшифровать соотвествие колонок во входно массиве ключей и данных, связанных с ними
        #     'aifFuncName' : 'SparkManager.get_inn_by_OPKO_aif_PF_SPARK', # Название функции с классом
        #     'aifParams' : {} # соответствия колонок во входном массиве dsCheckoInnLinks
        # }
        # # Pars: Параметры процедурной функции обработки получаемых результатоы в ФНЦИП  в ходе эпох 
        # outputFuncDic = {
        #     'procFuncName' :  'BondsMacros.save_results_INN_from_OKPO_of_SPARK_a021_PF' ,   # Полное название процедурной функции сохранения результатов (ПФСР)
        # }
        # # ФНЦИП - запуск
        # ds = WWWInteractiveUniversal.universal_get_interactive_data_by_epoch_vers2_PF (dsInp, sampleN, aifFuncParams, dsQnLim, outputFuncDic)
        # dsRes = ds[0]
        # print (f'dsRes = {dsRes}')
        # END ПРИМЕР: Не удалять. Формат использования ФНЦИП !!!

    @staticmethod 
    def universal_get_interactive_data_by_epoch_using_universal_while_PF (dsKeys, sampleN, atomFuncName, dsQnLim = -1, outputFuncDic = {}):
        #TODO: Сделать таймер для определения времени выполнения однйо эпохи и подсчет примерного времени на обработку всего массива аргументов
        """ Class: WWWInteractiveUniversal. Считывание данных с сайта на базе списка isin аргументов ЦБ в несколько подъодов (эпох). 
        Используется с функцией - параметром (Parameter Function) : inputFuncDic, outputFuncDic
        sampleN - параметр  определяющий выборки. Три варианта. Если sampleN = -1 - то идет обработка всех элементов в массива аргументов argDS.
                    Если sampleN = n, то образуется несколько подходов -эпох, где размер входного массива-аргументов = n
                    Если sampleN = [n] - список - то весь массив входных аргументов из массива ограничевается первыми n-элементами
        inputFuncDic - словарь с обьектом функции для интерактивной обработки и получения результатов на сайтах и аргументами для нее. 
        outputFuncDic - словарь с обьектом функции-обработчика результатов, полученных интераутивно, и аргументами для нее. По умолчанию функция-обработчик отстутствует. 
        dsKeys - одномерный список входных данных-ключей для идентификации на сайте при интерактивном поиске

        Прим: 
        funcArgs = {
            'tb' : 'bonds_current',
            'fieldsInxs' : {1:'okpo'},
            'unqInxCol' : [3,'isin']
        }

        inputFuncDic = {
            'func' : db_processor.update_rows_from_ds_PF,
            'args' : funcArgs <аргументы функции в виде словаря, составленного выше>
        }

        dsQnLim - ограничение общего входящего ds до размера, указанного в dsQnLim. Если -1, то весь массив без ограничения

        atomFuncName = 'CheckoManager.pif_comp_link_by_inn' < 'Название класса.Название функции' > - название атомарной интерактивной функции поиска
        !!! Обязательно результат такой функции должен возварщаться в виде одномерного списка и с ключем поиска в нем  [keyVal, foundVal1, foundVal2,...] !!!

        !!! В import должен быть класс , который содержит атомарную функцию 

        При завершении каждой эпохи производится вывод полученных результатов и обработка их функцией-обработчиком outputFuncDic
        funcDic - словарь с передаваемой функцией-обработчиком результатов эпохи и ее аргументами извне в виде словаря

        !!! Функции-обьекты  func для передачи в виде параметра должны строится по определенной структуре: В аргументах такой функции-параметра 
        должен сначала идти набор аргументов (которые также может быть получен внутри метода и подставлен, а может быть передан и извне),
        а затем словарь с аргументами , передоваемыми исключительно снаружи , то есть только внешние параметры функции!!!

        outputFuncDic -  Передача результирующего массива genDSRes  данных в обрабтоку фнкцией-параметром-обработчиком outputFuncDic['func'] с параметрами args outputFuncDic['args'] 
        outputFuncDic['func'] - должна быть статической функцией с оберткой @staticmethod   
        Прим: outputFuncDic = { 'func': 'save_comps_data_from_ds_set1_to_tb_comps_descr_PF', 'args': [listOfArgs] }
        """
        dsLinksN = len(dsKeys)
        print(f"Кол-во изначальных считанных обьектов со ссылками = {dsLinksN}")        
        if dsQnLim > 0: # если лимит указан, то ограничиваем входящий ds до этого размера
            dsKeys = dsKeys[:dsQnLim]
            dsKeysN = len(dsKeys)
            print (f"Общий входящий массив ограничен параметром dsQnLim и будут обработаны всего первые {dsKeysN} записи из него" )
        else:
            dsKeysN = len(dsKeys)
            print (f"Кол-во элементов для обработки не ограничено параметром dsQnLim и равно:  {dsKeysN}")

        if type(sampleN) == list: #  Если sampleN передается в списке, то это значит, что ds ограничен только кол-вом, которое указано в листе
            n = sampleN[0] # Кол-во для обработки в одномdsEnter = listLinks потоке записей из маасива-аргумента
            dsN = dsKeys[:n]
            print (dsN)
            # Функция настойчивого цикла while (ФНЦ)
            resDS = WWWInteractiveUniversal.universal_while_cycle_of_interactive_function_for_universal_epoch_F (dsN, atomFuncName) # Считывание данных с сайта на основе списка аргументов , заданных в dsEpoch. resDS - список результатов по всей выборке эпохи
            genDSRes = FG.convert_tuple_of_tuples_to_list_of_lists(resDS) # конвертация списка таплов в список списков

        else: # Если не в списке, то значит включается механизм эпох с выборками кол-вом sampleN или одного потока , если sampleN = -1
            # Анализ есть ли эпохи или все идет в одном подходе:
            if sampleN <0 : # Если sampleN = -1, значит эпох нет и весь массив обрабатывается одним потоком
                # ФУНКЦИЯ НАСТОЙЧИВОГО ЦИКЛА while (ФНЦ)
                resDS = WWWInteractiveUniversal.universal_while_cycle_of_interactive_function_for_universal_epoch_F (dsKeys, atomFuncName) # Считывание данных с сайта на основе списка аргументов , заданных в dsEpoch. resDS - список результатов по всей выборке эпохи
                genDSRes = [FG.convert_tuple_of_tuples_to_list_of_lists(resDS)] # конвертация списка таплов в список списков и вставка в список, как если бы было несколько эпох, что бы избежать разных подходов в обработке конечного массива
                print (f"Нет ограничения по порциям в эпохах и поэтому будет обрабатываться весь массив кол-вом {dsLinksN} без эпох")
                # вставка в БД

                if len(outputFuncDic) > 0: # Если задана функция обработчик

                    outputF_parts = outputFuncDic['func'].split('.') # Вычисление названий класса в которой находится АИФП и  имени атомарной поисковой функции
                    outputFclsName = outputF_parts[0] # названий класса в которой находится АИФП 
                    outputFName = outputF_parts[1] # имени атомарной поисковой функции
                    outputFClassModule = globals()[outputFclsName] # Нахождение класса в глобальных переменных
                    # oOutputFClassProc = outputFClassModule()  # Создание обьекта класса outputFclsName

                    # processF = outputFuncDic['func'] # Название функции-обработчика
                    oFuncProcess = getattr(outputFClassModule, outputFName) # Нахождение функции-обработчика по названию из обьекта-обработчика



                    if 'args' in outputFuncDic: # Проверяем наличие задаваемых аргументов в параметричекой функции. Если есть, то:
                        oFuncProcess(genDSRes, outputFuncDic['args']) # Передача данных в обрабтоку фнкцией-параметром-обработчиком outputFuncDic['func'] с параметрами args outputFuncDic['args']
                    else: # Если нет, то:
                        oFuncProcess(genDSRes) # !!! ОБРАБОТЧИК ВЫХОДНЫХ ДАННЫХ: Передача данных в обрабтоку фнкцией-параметром-обработчиком outputFuncDic['func'] с параметрами args outputFuncDic['args']
                    sleep(.3)

            else: # Если есть деление на эпохи
                dsN = len(dsKeys)
                # sampleN = 2 # Выборка записей из общего массива dsOKPO
                epochs = math.ceil(dsN/sampleN) # кол-во эпох, необходимых для обработки всего запрашиваемого списка ЦБ
                print (f"Есть порционное деления общего массива по эпохам. Кол-во элементов в одной эпох равно : {sampleN}")
                print (f'Кол-во эпох будет равно: {epochs}')
                genDSRes = [] # Общий список результатов по всем эпохам
                for p in range(epochs): # цикл по эпохам с выполнением захода на сайт и считывания данных порциями = sample
                    dsEpoch = dsKeys[p*sampleN:p*sampleN + sampleN] # выборка для эпохи из общего массива авргументов (в данном случае isin)
                    print(f'\n Эпоха {p}')
                    print (dsEpoch)
                    print('\n')
                    # Функция настойчивого цикла while (ФНЦ)
                    resDS = WWWInteractiveUniversal.universal_while_cycle_of_interactive_function_for_universal_epoch_F (dsEpoch, atomFuncName) # Считывание данных с сайта на основе списка аргументов , заданных в dsEpoch. resDS - список результатов по всей выборке эпохи
                    resDSl = FG.convert_tuple_of_tuples_to_list_of_lists(resDS) # конвертация списка таплов в список списков
                    # print (resDSl)
                    genDSRes.append(resDSl)
                    if len(outputFuncDic) > 0: # Если задана функция обработчик

                        outputF_parts = outputFuncDic['func'].split('.') # Вычисление названий класса в которой находится АИФП и  имени атомарной поисковой функции
                        outputFclsName = outputF_parts[0] # названий класса в которой находится АИФП 
                        outputFName = outputF_parts[1] # имени атомарной поисковой функции
                        outputFClassModule = globals()[outputFclsName] # Нахождение класса в глобальных переменных
                        # oOutputFClassProc = outputFClassModule() 

                        # processF = outputFuncDic['func'] # Название функции-обработчика
                        oFuncProcess = getattr(outputFClassModule, outputFName) # Нахождение функции-обработчика по названию из обьекта-обработчика

                        # TODO: Последние изменения : было genDSRes, заменено на resDSl [проверить работу предыдущих модулей, использующих эту функцию]
                        if 'args' in outputFuncDic: # Проверяем наличие задаваемых аргументов в параметричекой функции. Если есть, то:
                            oFuncProcess(resDSl, outputFuncDic['args']) # Передача данных в обрабтоку фнкцией-параметром-обработчиком outputFuncDic['func'] с параметрами args outputFuncDic['args']
                        else: # Если нет, то:
                            oFuncProcess(resDSl) # Передача данных в обрабтоку фнкцией-параметром-обработчиком outputFuncDic['func'] с параметрами args outputFuncDic['args']
                        sleep(.3)
        return genDSRes


    @staticmethod 
    def universal_while_cycle_of_interactive_function_for_universal_epoch_F (argDS, atomFuncName):
        """ WWWInteractiveUniversal: Функция-параметр для эпохальной функции get_interactive_data_by_epoch для параметра < inputFuncDic >  в ней
        Цикл while для настойчивого получения данных с сайта на основе массива аргументов (ФНЦ - Функция настойчивого цикла while)
        В результате выдает список искомых данных с сайта
        Является функцией - параметром для эпохальной функции get_interactive_data_by_epoch в этом же модуле
        Используя ее нужно подставлять в качестве функции - параметра в нее лишь уонечную функцию обработки одного аргумента для интерактивного поиска на сайте,
        избегая каждый раз кодировать цикл настойчивого while

        classObject - обьект класса, в котором находится конечная атомарная функция поиска по одному аргументу на сайте
        atomFuncObj - атомарная функция - обьект класса-обьекта 
        """
        aifp_pars = atomFuncName.split('.') # Вычисление названий класса в которой находится АИФП и  имени атомарной поисковой функции
        clsName = aifp_pars[0] # названий класса в которой находится АИФП 
        aifp = aifp_pars[1] # название атомарной поисковой функции
        classProc = globals()[clsName] # Нахождение класса в глобальных переменных
        dataSet = argDS
        rowsN = len(dataSet)
        print(f'rowsN = {rowsN}')
        resDS = []
        kRow = 0 # счетчик рядов в dataSet
        wI = 0 # счетчиу циклов while
        while kRow <= rowsN -1:  # y1RowSrc - конечный ряд в заданном регионе источника, algoritmCalc.self.kRow - текущая позиция по рядам цикла for
            oClassProc = classProc.ini_from_link()  # Создание обьекта класса, где находится АИФП
            # oClassProc.open_link() # Открываем базовую ссылку  
            # oClassProc.open_link_with_stop_load() # Открываем базовую ссылку open_link_with_stop_load
            n = 0  # порядковый номер в цикле  for по dataSet
            for val in dataSet:  # цикл по списку значений аргументов источника
                print(f'kRow = {kRow}')
                if len(val) == 0:  # Если isin пустой, то проскакиваем виток цикла с инкременированием цикловых счетчиков algoritmCalc.kRow и n
                    kRow += 1  # текущая позиция по рядам цикла for
                    n += 1  # порядковый номер в цикле по isinsList
                    continue
                try:  # ПОИСКОВАЯ ФУНКЦИЯ
                    # Запуск алгоритма -функции, в который передается аргумент из списка-источника

                    # АИФП
                    oAIFP = getattr(oClassProc, aifp) # Атомарная интерактивная поисковая функия - обьект
                    res = oAIFP(val) # !!! РЕЗУЛЬТАТ АТОМАРНЙО ФУНКЦИИ_ПАРАМЕТРА !!!
                except Exception as err:
                    eArgs  = err.args # параметры вызванной ошибки оператором Raise
                    print (f'Ошибка из Raise: {eArgs[0]}')
                    # Анализ вызываемых ошибок, которые могут быть запущены специально (помимо неучтенных и програмных) и дальнейшие действия на основе их кодов
                    if eArgs[0] == 'SP101': # Ошибка была для тестирования и уже обрабатывается в теле oSrchMngr.get_inn_plus_by_OPKO. Можно удалить
                        print(f' Код: {eArgs[0]}. {eArgs[1]} ') # Распечатка кода и сообщения ошибки, вызыванного raise
                        print('Продолжаем цикл for')
                        print (f'Последний элемент перед continue цикла val = {val}')
                        kRow += 1  # текущая позиция по рядам цикла for
                        continue # Продолжить выполнение цикла for
                    else:
                        print( f"Срыв получение ОКПО в {atomFuncName} на ряду: {kRow}")
                        # Отрез списка bNames с теми значениями, которые еще не отработаны циклом for
                        dataSet = dataSet[n:]
                        # Закрываем страницу сайта. Она будет снова открыта по новой по циклу  while после прерывания в for
                        print('Прерываем цикл for')
                        print (f'Последний элемент val = {val}')
                        oClassProc.driver.quit() # Закрыть браузер при полном срыве                       
                        break # Прервать выполнение цикла for 
                resDS.append(res) 
                kRow += 1  # текущая позиция по рядам цикла for

                n += 1  # порядковый номер в цикле по isinsList
                # END for
            oClassProc.driver.quit() # Закрыть браузер  при прохождении всех циклов for
            wI +=1 # Счетчик циклов while
            # END while
        print ('Конец операции')
        if DEBUG_:
            print (f'Кол-во в resDS = {len(resDS)} / WWWInteractiveUniversal.universal_while_cycle_of_interactive_function_for_universal_epoch_F')
        return resDS


    # @staticmethod 
    # def search_and_fill_to_db_comps_data_universal_PF (setPars):
    #     """ OBSOLETED / Delete Перенесена в модуль AlgorithmsSubParts
    #     WWWInteractiveUniversal 
    #     Универсалльная функция интерактивного поиска данных по компаниям в интернет ресурсах и записи результатов в БД
    #     setPars - Параметры настройки функции поиска
    #     Пр:
    #     """
    #     # РАСШИФРОВКА ПАРАМЕТРОВ:

    #     gaMarkerField = setPars['gaMarkerField'] # поле в глобальной таблице global_A ,  по которому производится поиск немаркированных значений для компаний, а так же  поле маркировки в таблице global_A после обработки выхода 
    #     cdlinkField = setPars['cdlinkField'] # поле в таблице comps_descr, откуда считываются ссылки для немаркированных рядов по компаниям на базе найденных ИНН
    #     atomFuncName = setPars['atomFuncName']  # АТОМАРНАЯ ФУНКЦИЯ ПОИСКА
    #     outputFuncName = 'HTMLSeleniumManager.save_comps_links_from_ds_set1_to_tb_comps_descr_PF'  # УНИВЕРСАЛЬНАЯ ФУНКЦИЯ ОБРАБОТКИ РЕЗУЛЬТАТОВ (на входе массив данных из АТОМАРНОЙ ФУНКЦИИ)
    #     dsQnLimCheco = setPars['dsQnLimCheco']  # Ограничение всего массива до этого размера  
    #     sampleNCheco = setPars['sampleNCheco']  # Порция в эпохе из входного массива dsLinks  (для всех интерактивных функций одинаково)
    #     fieldInCompsDescr = setPars['fieldInCompsDescr'] # поле для заполнения в таблице comps_descr полученными данными в результате интерактивного поиска


    #     # Формирование аргументов ФУНКЦИИ ОБРАБОТКИ РЕЗУЛЬТАТОВ
    #     args = {
    #         'fieldInCompsDescr' : fieldInCompsDescr,  # поле для заполнения в таблице comps_descr
    #         'fieldInGlobalA' : gaMarkerField  # поле для заполнения в таблице global_A
    #     }  
    #     outputFuncDic = { 
    #         'func': outputFuncName,
    #         'args' : args # входные параметры для функции обработчика
    #     } # Функция - обработчик результатов на выходе по массиву функии  atomFuncName. Должна находится в том же классе, что и атомарная функия        




    #     ###  Cсылки на страницы компаний заданного ресурса по ИНН, соответствующим немаркированным рядам в таблице global_A для заданного столбца 
    #     db = 'bonds.db'
    #     db_macros = SqliteBondsMacros(db)          
    #     dsLinksNotMarked  = db_macros.get_comp_links_from_tb_comps_descr_by_not_marked_vals_from_global_A (gaMarkerField, cdlinkField)




    #     # Вывод логов на печать
    #     dsLinksN = len(dsLinksNotMarked)
    #     print (f" Осталось для необработанных {dsLinksN} записей ИНН в таблице comps_descr по блоку для сайта " )
    #     if sampleNCheco > 0:
    #         print (f"Задана обработка массива через порционные эпохи равные {sampleNCheco} ")
    #     else:
    #         print(f"Не заданы эпохи и весь массив будет обработан за один подход. Кол-во элементов = {dsLinksN}") 

    #     # ЦИКЛИЧЕСКИЙ ИНТЕРАКТИВНЫЙ ПОИСК на сайте с разделением массива аргументов dsList  по эпохам с порционными выборками (для уменьшения рисков потери данных при каком-либо срыве)
    #     checkoDataRes = WWWInteractiveUniversal.universal_get_interactive_data_by_epoch_using_universal_while_PF(dsLinksNotMarked, sampleNCheco, atomFuncName, dsQnLimCheco, outputFuncDic)
    #     return []
    #     # return checkoDataRes





### --- END UNIVERSAL EPOCH FUNCTIONS  для поиска данных на сайтах ------------------




### --- UNIVERSAL EPOCH FUNCTIONS для поиска данных на сайтах С ПЕРЕДАЧЕЙ АТРИБУТОВ АТОМАРНОЙ ФУНКЦИИ . НОВЫЙ КОМПЛЕКС ФУНКЦИЙ ДОЛЖЕН ПОЛУЧАТЬ ПАРАМЕТРЫ АТОМАРНОЙ ФУНКЦИИ- !!! -----------------

    @staticmethod 
    def universal_get_interactive_data_by_epoch_vers2_PF (dsWithKeys, sampleN, aifFuncParams, dsQnLim = -1, outputFuncPars = {}):
        #TODO: Сделать таймер для определения времени выполнения однйо эпохи и подсчет примерного времени на обработку всего массива аргументов
        """ NEW State_of_art. Заменяет постепенно устаревшую функцию universal_get_interactive_data_by_epoch_using_universal_while_PF (которая без передачи атрибутов атомарной функции)
        С ПЕРЕДАЧЕЙ АТРИБУТОВ ПАРАМЕТРОВ ДЛЯ АТОМАРНОЙ ФУНКЦИИ !!!
        !!! Теперь вместо dsKeys - можно передавать любой массив dsWithKeys. Главное, Чтобы в нем были ключи. А в параметрах данные - как расшифровывать этот входной массив
        aifFuncParams - Параметры атомарной функции с ее полным название и параметрами к ней, которые позволяют расшифровать соотвествие колонок во входно массиве ключей и данных, связанных с ними
        Class: HTMLSeleniumManager. Считывание данных с сайта на базе списка isin аргументов ЦБ в несколько подъодов (эпох). 
        Используется с функцией - параметром (Parameter Function) : inputFuncDic, outputFuncDic
        sampleN - параметр  определяющий выборки. Три варианта. Если sampleN = -1 - то идет обработка всех элементов в массива аргументов argDS.
                    Если sampleN = n, то образуется несколько подходов -эпох, где размер входного массива-аргументов = n
                    Если sampleN = [n] - список - то весь массив входных аргументов из массива ограничевается первыми n-элементами
        inputFuncDic - словарь с обьектом функции для интерактивной обработки и получения результатов на сайтах и аргументами для нее. 
        outputFuncDic - словарь с обьектом функции-обработчика результатов, полученных интераутивно, и аргументами для нее. По умолчанию функция-обработчик отстутствует. 
        dsWithKeys - массив, содержащий ключи в одной из колонок (расшифровка ключей задается в параметрах атомарной функции . Теперь это можно)

        Прим: 
        funcArgs = {
            'tb' : 'bonds_current',
            'fieldsInxs' : {1:'okpo'},
            'unqInxCol' : [3,'isin']
        }

        inputFuncDic = {
            'func' : db_processor.update_rows_from_ds_PF,
            'args' : funcArgs <аргументы функции в виде словаря, составленного выше>
        }

        dsQnLim - ограничение общего входящего ds до размера, указанного в dsQnLim. Если -1, то весь массив без ограничения

        atomFuncName = 'CheckoManager.pif_comp_link_by_inn' < 'Название класса.Название функции' > - название атомарной интерактивной функции поиска
        !!! Обязательно результат такой функции должен возварщаться в виде одномерного списка и с ключем поиска в нем  [keyVal, foundVal1, foundVal2,...] !!!

        !!! В import должен быть класс , который содержит атомарную функцию 

        При завершении каждой эпохи производится вывод полученных результатов и обработка их функцией-обработчиком outputFuncDic
        funcDic - словарь с передаваемой функцией-обработчиком результатов эпохи и ее аргументами извне в виде словаря

        !!! Функции-обьекты  func для передачи в виде параметра должны строится по определенной структуре: В аргументах такой функции-параметра 
        должен сначала идти набор аргументов (которые также может быть получен внутри метода и подставлен, а может быть передан и извне),
        а затем словарь с аргументами , передоваемыми исключительно снаружи , то есть только внешние параметры функции!!!

        outputFuncDic -  Передача результирующего массива genDSRes  данных в обрабтоку фнкцией-параметром-обработчиком outputFuncDic['func'] с параметрами args outputFuncDic['args'] 
        outputFuncDic['func'] - должна быть статической функцией с оберткой @staticmethod   
        Прим: outputFuncDic = { 'func': 'save_comps_data_from_ds_set1_to_tb_comps_descr_PF', 'args': [listOfArgs] }
        """
        dsLinksN = len(dsWithKeys) # кол-во рядов во входном массиве dsWithKeys
        print(f"PR_154 --> Кол-во изначальных считанных обьектов со ссылками = {dsLinksN}")        
        if dsQnLim > 0: # если лимит указан, то ограничиваем входящий ds до этого размера
            dsWithKeys = dsWithKeys[:dsQnLim]
            dsKeysN = len(dsWithKeys)
            print (f"PR_155 --> Общий входящий массив ограничен параметром dsQnLim и будут обработаны всего первые {dsKeysN} записи из него" )
        else:
            dsKeysN = len(dsWithKeys)
            print (f"PR_156 --> Кол-во элементов для обработки не ограничено параметром dsQnLim и равно:  {dsKeysN}")

        if type(sampleN) == list: #  Если sampleN передается в списке, то это значит, что ds ограничен только кол-вом, которое указано в листе
            n = sampleN[0] # Кол-во для обработки в одном потоке записей из маасива-аргумента
            dsEpochPortion = dsWithKeys[:n] # Ограниченный порцией в эпохе входной массив
            print (dsEpochPortion) # PRINT 

            # ФУНКЦИЯ НАСТОЙЧИВОГО ЦИКЛА while (ФНЦ) !!!! 
            resDS = WWWInteractiveUniversal.universal_while_cycle_of_interactive_aif_function_vers2_PF (dsEpochPortion, aifFuncParams) # Считывание данных с сайта на основе списка аргументов , заданных в dsEpoch. resDS - список результатов по всей выборке эпохи
            genDSRes = FG.convert_tuple_of_tuples_to_list_of_lists(resDS) # конвертация списка таплов в список списков

        else: # Если не в списке, то значит включается механизм эпох с выборками кол-вом sampleN или одного потока , если sampleN = -1
            # Анализ есть ли эпохи или все идет в одном подходе:
            if sampleN <0 : # Если sampleN = -1, значит эпох нет и весь массив обрабатывается одним потоком
                # ФУНКЦИЯ НАСТОЙЧИВОГО ЦИКЛА while (ФНЦ)
                resDS = WWWInteractiveUniversal.universal_while_cycle_of_interactive_aif_function_vers2_PF (dsWithKeys, aifFuncParams) # Считывание данных с сайта на основе списка аргументов , заданных в dsEpoch. resDS - список результатов по всей выборке эпохи
                genDSRes = [FG.convert_tuple_of_tuples_to_list_of_lists(resDS)] # конвертация списка таплов в список списков и вставка в список, как если бы было несколько эпох, что бы избежать разных подходов в обработке конечного массива
                print (f"PR_157 --> Нет ограничения по порциям в эпохах и поэтому будет обрабатываться весь массив кол-вом {dsLinksN} без эпох")
                # вставка в БД

                if len(outputFuncPars) > 0: # Если задана функция обработчик

                    # ЗАПУСК ПРОЦЕДУРНОЙ ФУНКЦИЯ СОХРАНЕНИЯ ПОЛУЧЕННЫХ РЕЗУЛЬТАТОВ (genDSRes, outputFuncPars)
                    pfcFuncObj = WWWInteractiveUniversal.get_parametric_func_obj_by_its_full_name (outputFuncPars['procFuncName']) # Получение ПФС как обьект
                    pfcFuncObj (genDSRes, outputFuncPars) # Запуск ПФС с параметрами     
                    sleep(.3)

            else: # Если есть деление на эпохи
                dsN = len(dsWithKeys)
                # sampleN = 2 # Выборка записей из общего массива dsOKPO
                epochs = math.ceil(dsN/sampleN) # кол-во эпох, необходимых для обработки всего запрашиваемого списка ЦБ
                print (f"PR_158 --> Есть порционное деления общего массива по эпохам. Кол-во элементов в одной эпох равно : {sampleN}")
                print (f'PR_159 --> Кол-во эпох будет равно: {epochs}')
                genDSRes = [] # Общий список результатов по всем эпохам
                for p in range(epochs): # цикл по эпохам с выполнением захода на сайт и считывания данных порциями = sample
                    dsEpoch = dsWithKeys[p*sampleN:p*sampleN + sampleN] # выборка для эпохи из общего массива авргументов (в данном случае isin)
                    print(f'\n PR_160 --> Эпоха {p}')
                    print (dsEpoch)
                    print('\n')
                    # Функция настойчивого цикла while (ФНЦ)
                    resDS = WWWInteractiveUniversal.universal_while_cycle_of_interactive_aif_function_vers2_PF (dsEpoch, aifFuncParams) # Считывание данных с сайта на основе списка аргументов , заданных в dsEpoch. resDS - список результатов по всей выборке эпохи
                    resDSl = FG.convert_tuple_of_tuples_to_list_of_lists(resDS) # конвертация списка таплов в список списков
                    # print (resDSl)
                    genDSRes.append(resDSl)
                    if len(outputFuncPars) > 0: # Если задана необходимость обработки выходных результатов

                        # ЗАПУСК ПРОЦЕДУРНОЙ ФУНКЦИЯ СОХРАНЕНИЯ ПОЛУЧЕННЫХ РЕЗУЛЬТАТОВ (genDSRes, outputFuncPars)
                        pfcFuncObj = WWWInteractiveUniversal.get_parametric_func_obj_by_its_full_name (outputFuncPars['procFuncName']) # Получение ПФС как обьект
                        pfcFuncObj (resDSl, outputFuncPars) # Запуск ПФС с параметрами

                        sleep(.3)

        return genDSRes
    
    
    
    
    def universal_get_interactive_data_by_epoch_vers3_PF (dsWithKeys, sampleN, aifFuncParams, dsQnLim = -1, outputFuncPars = {}): # (20.09.2023)
        #TODO: Сделать таймер для определения времени выполнения однйо эпохи и подсчет примерного времени на обработку всего массива аргументов
        """ 
        WWWInteractiveUniversal
        версия 3: Работает с динамическими функциями, которые определяются путем к файлу класса, названием класса и названием функции и 
        находятся в невидимой для программы области. В отличии от версии 2, где функция динамически создается только из названия класса и назв функции
        и находится в видимой обасти для программы. Стринг с путем к классу , названием класса и названием функции должен быть формата:
        '<Путь к файлу класса>|<название класса>|<Название функции>'
        
        NEW State_of_art. Заменяет постепенно устаревшую функцию universal_get_interactive_data_by_epoch_using_universal_while_PF (которая без передачи атрибутов атомарной функции)
        С ПЕРЕДАЧЕЙ АТРИБУТОВ ПАРАМЕТРОВ ДЛЯ АТОМАРНОЙ ФУНКЦИИ !!!
        !!! Теперь вместо dsKeys - можно передавать любой массив dsWithKeys. Главное, Чтобы в нем были ключи. А в параметрах данные - как расшифровывать этот входной массив
        aifFuncParams - Параметры атомарной функции с ее полным название и параметрами к ней, которые позволяют расшифровать соотвествие колонок во входно массиве ключей и данных, связанных с ними
        Class: HTMLSeleniumManager. Считывание данных с сайта на базе списка isin аргументов ЦБ в несколько подъодов (эпох). 
        Используется с функцией - параметром (Parameter Function) : inputFuncDic, outputFuncDic
        sampleN - параметр  определяющий выборки. Три варианта. Если sampleN = -1 - то идет обработка всех элементов в массива аргументов argDS.
                    Если sampleN = n, то образуется несколько подходов -эпох, где размер входного массива-аргументов = n
                    Если sampleN = [n] - список - то весь массив входных аргументов из массива ограничевается первыми n-элементами
        inputFuncDic - словарь с обьектом функции для интерактивной обработки и получения результатов на сайтах и аргументами для нее. 
        outputFuncDic - словарь с обьектом функции-обработчика результатов, полученных интераутивно, и аргументами для нее. По умолчанию функция-обработчик отстутствует. 
        dsWithKeys - массив, содержащий ключи в одной из колонок (расшифровка ключей задается в параметрах атомарной функции . Теперь это можно)

        Прим: 
        funcArgs = {
            'tb' : 'bonds_current',
            'fieldsInxs' : {1:'okpo'},
            'unqInxCol' : [3,'isin']
        }

        inputFuncDic = {
            'func' : db_processor.update_rows_from_ds_PF,
            'args' : funcArgs <аргументы функции в виде словаря, составленного выше>
        }

        dsQnLim - ограничение общего входящего ds до размера, указанного в dsQnLim. Если -1, то весь массив без ограничения

        atomFuncName = 'CheckoManager.pif_comp_link_by_inn' < 'Название класса.Название функции' > - название атомарной интерактивной функции поиска
        !!! Обязательно результат такой функции должен возварщаться в виде одномерного списка и с ключем поиска в нем  [keyVal, foundVal1, foundVal2,...] !!!

        !!! В import должен быть класс , который содержит атомарную функцию 

        При завершении каждой эпохи производится вывод полученных результатов и обработка их функцией-обработчиком outputFuncDic
        funcDic - словарь с передаваемой функцией-обработчиком результатов эпохи и ее аргументами извне в виде словаря

        !!! Функции-обьекты  func для передачи в виде параметра должны строится по определенной структуре: В аргументах такой функции-параметра 
        должен сначала идти набор аргументов (которые также может быть получен внутри метода и подставлен, а может быть передан и извне),
        а затем словарь с аргументами , передоваемыми исключительно снаружи , то есть только внешние параметры функции!!!

        outputFuncDic -  Передача результирующего массива genDSRes  данных в обрабтоку фнкцией-параметром-обработчиком outputFuncDic['func'] с параметрами args outputFuncDic['args'] 
        outputFuncDic['func'] - должна быть статической функцией с оберткой @staticmethod   
        Прим: outputFuncDic = { 'func': 'save_comps_data_from_ds_set1_to_tb_comps_descr_PF', 'args': [listOfArgs] }
        """
        dsLinksN = len(dsWithKeys) # кол-во рядов во входном массиве dsWithKeys
        print(f"PR_161 --> Кол-во изначальных считанных обьектов со ссылками = {dsLinksN}")        
        if dsQnLim > 0: # если лимит указан, то ограничиваем входящий ds до этого размера
            dsWithKeys = dsWithKeys[:dsQnLim]
            dsKeysN = len(dsWithKeys)
            print (f"PR_162 --> Общий входящий массив ограничен параметром dsQnLim и будут обработаны всего первые {dsKeysN} записи из него" )
        else:
            dsKeysN = len(dsWithKeys)
            print (f"PR_163 --> Кол-во элементов для обработки не ограничено параметром dsQnLim и равно:  {dsKeysN}")

        if type(sampleN) == list: #  Если sampleN передается в списке, то это значит, что ds ограничен только кол-вом, которое указано в листе
            n = sampleN[0] # Кол-во для обработки в одном потоке записей из маасива-аргумента
            dsEpochPortion = dsWithKeys[:n] # Ограниченный порцией в эпохе входной массив
            print (dsEpochPortion) # PRINT 

            # ФУНКЦИЯ НАСТОЙЧИВОГО ЦИКЛА while (ФНЦ) !!!! 
            resDS = WWWInteractiveUniversal.universal_while_cycle_of_interactive_aif_function_vers3_PF (dsEpochPortion, aifFuncParams) # Считывание данных с сайта на основе списка аргументов , заданных в dsEpoch. resDS - список результатов по всей выборке эпохи
            genDSRes = FG.convert_tuple_of_tuples_to_list_of_lists(resDS) # конвертация списка таплов в список списков

        else: # Если не в списке, то значит включается механизм эпох с выборками кол-вом sampleN или одного потока , если sampleN = -1
            # Анализ есть ли эпохи или все идет в одном подходе:
            if sampleN <0 : # Если sampleN = -1, значит эпох нет и весь массив обрабатывается одним потоком
                # ФУНКЦИЯ НАСТОЙЧИВОГО ЦИКЛА while (ФНЦ)
                resDS = WWWInteractiveUniversal.universal_while_cycle_of_interactive_aif_function_vers3_PF (dsWithKeys, aifFuncParams) # Считывание данных с сайта на основе списка аргументов , заданных в dsEpoch. resDS - список результатов по всей выборке эпохи
                genDSRes = [FG.convert_tuple_of_tuples_to_list_of_lists(resDS)] # конвертация списка таплов в список списков и вставка в список, как если бы было несколько эпох, что бы избежать разных подходов в обработке конечного массива
                print (f"PR_164 --> Нет ограничения по порциям в эпохах и поэтому будет обрабатываться весь массив кол-вом {dsLinksN} без эпох")
                # вставка в БД

                if len(outputFuncPars) > 0: # Если задана функция обработчик

                    # ЗАПУСК ПРОЦЕДУРНОЙ ФУНКЦИЯ СОХРАНЕНИЯ ПОЛУЧЕННЫХ РЕЗУЛЬТАТОВ (genDSRes, outputFuncPars)
                    classObj, pfcFuncObj = FunctionsGeneralClass.get_func_obj_by_func_name_and_full_class_path_str (outputFuncPars['procFuncName'], delim='|') # Получение ПФС как обьект
                    pfcFuncObj(genDSRes, outputFuncPars) # Запуск динамической функции обработки результатов с параметрами     
                    sleep(.3)

            else: # Если есть деление на эпохи
                dsN = len(dsWithKeys)
                # sampleN = 2 # Выборка записей из общего массива dsOKPO
                epochs = math.ceil(dsN/sampleN) # кол-во эпох, необходимых для обработки всего запрашиваемого списка ЦБ
                print (f"PR_165 --> Есть порционное деления общего массива по эпохам. Кол-во элементов в одной эпох равно : {sampleN}")
                print (f'PR_166 --> Кол-во эпох будет равно: {epochs}')
                genDSRes = [] # Общий список результатов по всем эпохам
                for p in range(epochs): # цикл по эпохам с выполнением захода на сайт и считывания данных порциями = sample
                    dsEpoch = dsWithKeys[p*sampleN:p*sampleN + sampleN] # выборка для эпохи из общего массива авргументов (в данном случае isin)
                    print(f'\n PR_167 --> Эпоха {p}')
                    print (dsEpoch)
                    print('\n')
                    # Функция настойчивого цикла while (ФНЦ)
                    resDS = WWWInteractiveUniversal.universal_while_cycle_of_interactive_aif_function_vers3_PF (dsEpoch, aifFuncParams) # Считывание данных с сайта на основе списка аргументов , заданных в dsEpoch. resDS - список результатов по всей выборке эпохи
                    resDSl = FG.convert_tuple_of_tuples_to_list_of_lists(resDS) # конвертация списка таплов в список списков
                    # print (resDSl)
                    genDSRes.append(resDSl)
                    if len(outputFuncPars) > 0: # Если задана необходимость обработки выходных результатов

                        # ЗАПУСК ПРОЦЕДУРНОЙ ФУНКЦИЯ СОХРАНЕНИЯ ПОЛУЧЕННЫХ РЕЗУЛЬТАТОВ (genDSRes, outputFuncPars)
                        classObj, pfcFuncObj  = FunctionsGeneralClass.get_func_obj_by_func_name_and_full_class_path_str (outputFuncPars['procFuncName'], delim='|') # Получение ПФС как обьект
                        pfcFuncObj (resDSl, outputFuncPars) # Запуск ПФС с параметрами

                        sleep(.3)

        return genDSRes

    
    
    
    


    @staticmethod 
    def universal_while_cycle_of_interactive_aif_function_vers2_PF (dsInput, aifFuncParams):
        """ NEW State_of_art. Заменяет постепенно устаревшую функцию universal_while_cycle_of_interactive_function_for_universal_epoch_F (которая без передачи атрибутов атомарной функции)
        С ПЕРЕДАЧЕЙ АТРИБУТОВ ПАРАМЕТРОВ ДЛЯ АТОМАРНОЙ ФУНКЦИИ!!!
        aifFuncParams - параметры АИФ, где есть полное название АИФ и данные (в частности, помогающие расшифровать входной массив: где ключевое поле, а где дополнительные)
        dsInput - входной массив, любой. АИФ знает, как расшифровывать ряды этого массива

        HTMLSeleniumManager: Функция-параметр для эпохальной функции get_interactive_data_by_epoch для параметра < inputFuncDic >  в ней
        Цикл while для настойчивого получения данных с сайта на основе массива аргументов (ФНЦ - Функция настойчивого цикла while)
        В результате выдает список искомых данных с сайта
        Является функцией - параметром для эпохальной функции get_interactive_data_by_epoch в этом же модуле
        Используя ее нужно подставлять в качестве функции - параметра в нее лишь уонечную функцию обработки одного аргумента для интерактивного поиска на сайте,
        избегая каждый раз кодировать цикл настойчивого while

        classObject - обьект класса, в котором находится конечная атомарная функция поиска по одному аргументу на сайте
        atomFuncObj - атомарная функция - обьект класса-обьекта 
        """

        # Расшифровка  aifFuncParams
        aifFuncName =  aifFuncParams['aifFuncName']
        

        aifp_pars = aifFuncName.split('.') # Вычисление названий класса в которой находится АИФП и  имени атомарной поисковой функции
        clsName = aifp_pars[0] # названий класса в которой находится АИФП 
        aifp = aifp_pars[1] # имени атомарной поисковой функции
        classProc = globals()[clsName] # Нахождение класса в глобальных переменных


        rowsN = len(dsInput)
        print(f'rowsN = {rowsN}')
        resDS = []
        kRow = 0 # счетчик рядов в dataSet
        wI = 0 # счетчиу циклов while
        while kRow <= rowsN -1:  # y1RowSrc - конечный ряд в заданном регионе источника, algoritmCalc.self.kRow - текущая позиция по рядам цикла for
            oClassProc = classProc().ini_from_link()   # Создание обьекта класса, где находится АИФП без открытия ссылки
            # oClassProc.open_link() # Открываем базовую ссылку

            n = 0  # порядковый номер в цикле  for по dataSet
            for val in dsInput:  # цикл по списку значений аргументов источника
                print(f'kRow = {kRow}')
                if len(val) == 0:  # Если isin пустой, то проскакиваем виток цикла с инкременированием цикловых счетчиков algoritmCalc.kRow и n
                    kRow += 1  # текущая позиция по рядам цикла for
                    n += 1  # порядковый номер в цикле по isinsList
                    continue
                try:  # ПОИСКОВАЯ ФУНКЦИЯ
                    # Запуск алгоритма -функции, в который передается аргумент из списка-источника

                    # АИФ !!!!!!
                    oAIFP = getattr(oClassProc, aifp) # Атомарная интерактивная поисковая функия - обьект
                    res = oAIFP(val) # !!! РЕЗУЛЬТАТ АТОМАРНЙО ФУНКЦИИ_ПАРАМЕТРА !!!


                except Exception as err:
                    eArgs  = err.args # параметры вызванной ошибки оператором Raise



                    print (f'Ошибка из Raise: {eArgs[0]}')
                    # Анализ вызываемых ошибок, которые могут быть запущены специально (помимо неучтенных и програмных) и дальнейшие действия на основе их кодов
                    if eArgs[0] == 'SP101' or eArgs[0] == 'SP102' : # Ошибка была для тестирования и уже обрабатывается в теле oSrchMngr.get_inn_plus_by_OPKO. Можно удалить
                        print(f' Код: {eArgs[0]}. {eArgs[1]} ') # Распечатка кода и сообщения ошибки, вызыванного raise
                        print('Продолжаем цикл for')
                        print (f'Последний элемент перед continue цикла val = {val}')
                        kRow += 1  # текущая позиция по рядам цикла for
                        continue # Продолжить выполнение цикла for

                    else:
                        print( f"Срыв получение ОКПО в {aifFuncName} на ряду: {kRow}")
                        # Отрез списка bNames с теми значениями, которые еще не отработаны циклом for
                        dsInput = dsInput[n:]
                        # Закрываем страницу сайта. Она будет снова открыта по новой по циклу  while после прерывания в for
                        print('Прерываем цикл for')
                        print (f'Последний элемент val = {val}')
                        oClassProc.driver.quit() # Закрыть браузер при полном срыве                       
                        break # Прервать выполнение цикла for 





                resDS.append(res) 
                kRow += 1  # текущая позиция по рядам цикла for

                n += 1  # порядковый номер в цикле по isinsList
                # END for
            oClassProc.driver.quit() # Закрыть браузер  при прохождении всех циклов for
            wI +=1 # Счетчик циклов while
            # END while
        print ('Конец операции')
        print (f'Кол-во в resDS = {len(resDS)}')
        return resDS






    @staticmethod 
    def universal_while_cycle_of_interactive_aif_function_vers3_PF (dsInput, aifFuncParams): # (20.09.2023)
        """ 
        версия 3: Работает с динамическими функциями, которые определяются путем к файлу класса, названием класса и названием функции и 
        находятся в невидимой для программы области. В отличии от версии 2, где функция динамически создается только из названия класса и назв функции
        и находится в видимой обасти для программы. Стринг с путем к классу , названием класса и названием функции должен быть формата:
        '<Путь к файлу класса>|<название класса>|<Название функции>'
        
        NEW State_of_art. Заменяет постепенно устаревшую функцию universal_while_cycle_of_interactive_function_for_universal_epoch_F (которая без передачи атрибутов атомарной функции)
        С ПЕРЕДАЧЕЙ АТРИБУТОВ ПАРАМЕТРОВ ДЛЯ АТОМАРНОЙ ФУНКЦИИ!!!
        aifFuncParams - параметры АИФ, где есть полное название АИФ и данные (в частности, помогающие расшифровать входной массив: где ключевое поле, а где дополнительные)
        dsInput - входной массив, любой. АИФ знает, как расшифровывать ряды этого массива

        HTMLSeleniumManager: Функция-параметр для эпохальной функции get_interactive_data_by_epoch для параметра < inputFuncDic >  в ней
        Цикл while для настойчивого получения данных с сайта на основе массива аргументов (ФНЦ - Функция настойчивого цикла while)
        В результате выдает список искомых данных с сайта
        Является функцией - параметром для эпохальной функции get_interactive_data_by_epoch в этом же модуле
        Используя ее нужно подставлять в качестве функции - параметра в нее лишь уонечную функцию обработки одного аргумента для интерактивного поиска на сайте,
        избегая каждый раз кодировать цикл настойчивого while

        classObject - обьект класса, в котором находится конечная атомарная функция поиска по одному аргументу на сайте
        atomFuncObj - атомарная функция - обьект класса-обьекта 
        """

        # Расшифровка  aifFuncParams
        print(f"PR_552 --> aifFuncParams = {aifFuncParams}")
        aifFuncClassPath =  aifFuncParams['aifFuncName']
        print(f"PR_551 --> aifFuncClassPath = {aifFuncClassPath}")
        # динамическое создание обьекта класса и обьекта функции из класса
        classProc, funcObj  = FunctionsGeneralClass.get_func_obj_by_func_name_and_full_class_path_str(aifFuncClassPath, delim='|') # Получение ПФС как обьект
        
        fileClassPath, expectedClass, funcName = FunctionsGeneralClass.get_class_and_method_name_from_path_to_function (aifFuncClassPath, delim='|', type = 'invisibleSpace')
        aifp = funcName # название атомарной функции (что бы получить драйвер и задавать параетры в функцию, нужно подставлять имя функции ниже именно в цикле while ?)
        # oAIFP = getattr(oClassProc, aifp) # Атомарная интерактивная поисковая функия - обьект
        # aifp_pars = aifFuncName.split('.') # Вычисление названий класса в которой находится АИФП и  имени атомарной поисковой функции
        # clsName = aifp_pars[0] # названий класса в которой находится АИФП 
        # aifp = aifp_pars[1] # имени атомарной поисковой функции
        # classProc = globals()[clsName] # Нахождение класса в глобальных переменных
        
        


        rowsN = len(dsInput)
        print(f'rowsN = {rowsN}')
        resDS = []
        kRow = 0 # счетчик рядов в dataSet
        wI = 0 # счетчиу циклов while
        while kRow <= rowsN -1:  # y1RowSrc - конечный ряд в заданном регионе источника, algoritmCalc.self.kRow - текущая позиция по рядам цикла for
            oClassProc = classProc.ini_from_link()   # Создание обьекта класса, где находится АИФП без открытия ссылки
            # oClassProc.open_link() # Открываем базовую ссылку

            n = 0  # порядковый номер в цикле  for по dataSet
            for val in dsInput:  # цикл по списку значений аргументов источника
                print(f'PR_169 --> kRow = {kRow}')
                if len(val) == 0:  # Если isin пустой, то проскакиваем виток цикла с инкременированием цикловых счетчиков algoritmCalc.kRow и n
                    kRow += 1  # текущая позиция по рядам цикла for
                    n += 1  # порядковый номер в цикле по isinsList
                    continue
                try:  # ПОИСКОВАЯ ФУНКЦИЯ
                    # Запуск алгоритма -функции, в который передается аргумент из списка-источника

                    # АИФ !!!!!!
                    oAIFP = getattr(oClassProc, aifp) # Атомарная интерактивная поисковая функия - обьект
                    res = oAIFP(val) # !!! РЕЗУЛЬТАТ АТОМАРНЙО ФУНКЦИИ_ПАРАМЕТРА !!!


                except Exception as err:
                    eArgs  = err.args # параметры вызванной ошибки оператором Raise



                    print (f'PR_170 --> Ошибка из Raise: {eArgs[0]}')
                    # Анализ вызываемых ошибок, которые могут быть запущены специально (помимо неучтенных и програмных) и дальнейшие действия на основе их кодов
                    if eArgs[0] == 'SP101' or eArgs[0] == 'SP102' : # Ошибка была для тестирования и уже обрабатывается в теле oSrchMngr.get_inn_plus_by_OPKO. Можно удалить
                        print(f'PR_171 --> Код: {eArgs[0]}. {eArgs[1]} ') # Распечатка кода и сообщения ошибки, вызыванного raise
                        print('PR_172 --> Продолжаем цикл for')
                        print (f'PR_173 --> Последний элемент перед continue цикла val = {val}')
                        kRow += 1  # текущая позиция по рядам цикла for
                        continue # Продолжить выполнение цикла for

                    else:
                        print( f"PR_174 --> Срыв получение ОКПО в {aifFuncClassPath} на ряду: {kRow}")
                        # Отрез списка bNames с теми значениями, которые еще не отработаны циклом for
                        dsInput = dsInput[n:]
                        # Закрываем страницу сайта. Она будет снова открыта по новой по циклу  while после прерывания в for
                        print('PR_175 --> Прерываем цикл for')
                        print (f'PR_176 --> Последний элемент val = {val}')
                        oClassProc.driver.quit() # Закрыть браузер при полном срыве                       
                        break # Прервать выполнение цикла for 





                resDS.append(res) 
                kRow += 1  # текущая позиция по рядам цикла for

                n += 1  # порядковый номер в цикле по isinsList
                # END for
            oClassProc.driver.quit() # Закрыть браузер  при прохождении всех циклов for
            wI +=1 # Счетчик циклов while
            # END while
        print ('Конец операции')
        print (f'Кол-во в resDS = {len(resDS)}')
        return resDS








    @staticmethod  
    def universal_update_mark_to_global_table (dsIN, tbName, markerField, markerStr):
        """  Class Static Function: WWWInteractiveUniversal   
        Вспомогательная универсальная функция, вставляющий (update) маркер в таблицу глобальных переменных или глобальную таблицу
        dsIN - входной массив ключей, по которым будет проставлен маркер markerStr в поле markerField таблицы tbName
        markerStr - стринговый маркер
        markerField - поле для вставки маркера в таблице tbName
        """
        db = DB_BONDS_
        db_proc = SqliteProcessor(db)
        updFields = [markerField]
        updVals = [markerStr]
        # keyInField = ['x_str']
        # inDS = 'SELECT FROM * '
        whereConds = {'ONE': ['x_str','IN', dsIN]}
        sql = db_proc.update_where_in_simple_exec (tbName, updFields,  updVals, whereConds)
        # print (sql)  


    @staticmethod  
    def universal_get_ds_fields_from_global_table_where_not_marked_in_given_field (tbName, markerField, markerStr, getFields):
        """ Class Static Function: WWWInteractiveUniversal  
        Получение массива ключей в тех рядов глобальной таблицы (например, из glabal_A), в заданном поле markerField которых непроставлен заданный к поиску маркер markerStr
        TODO: НЕ ПРОВЕРЕНА !!!
        """
        db = DB_BONDS_
        db_macros = SqliteBondsMacros(db) 

        # Pars: 
        # tb = 'global_A'
        tb = tbName
        conds = {'OR': [[markerField, 'IS', '&NULL'], [markerField, '=', ''], [markerField, '!=', markerStr]]} # Поле 'l1' соответствуюет маркеру вставление данных в поле 'link1' в таблице comps_descr
        getFields = [getFields]
        cur, sql  = db_macros.select_from_table_with_where_condition (tb, getFields, conds)
        dsInnNotInsertedFetch = cur.fetchall()
        cur.close()
        dsInnNotInserted = FG.convert_tuple_of_tuples_to_list_of_lists(dsInnNotInsertedFetch) # Двумерный список [[ ... ]]   тех ИНН, по которым не проставлена метка 'INSERTED'  в таблицк global_A в поле x-str
        return dsInnNotInserted  # [[ ... ]] 




### --- END UNIVERSAL EPOCH FUNCTIONS для поиска данных на сайтах С ПЕРЕДАЧЕЙ АТРИБУТОВ АТОМАРНОЙ ФУНКЦИИ . НОВЫЙ КОМПЛЕКС ФУНКЦИЙ ДОЛЖЕН ПОЛУЧАТЬ ПАРАМЕТРЫ АТОМАРНОЙ ФУНКЦИИ- !!! -----------------

# --- ВСПОМОГАТЕЛЬНЫЕ  функции для PF


    @staticmethod 
    def get_parametric_func_obj_by_its_full_name (PFName):
        """ Получение обьекта параметрической функции по ее полному имени в формате < ClassName.FunctionName >
        RET: objPF - возвращает обьект параметрической функции готовый к дальнейшему использованию
        """
        apf_parts = PFName.split('.') # Вычисление названий класса в которой находится АИФП и  имени атомарной поисковой функции
        clsName = apf_parts[0] # названий класса в которой находится АИФП 
        pfName = apf_parts[1] # имени атомарной поисковой функции
        classProc = globals()[clsName] # Нахождение класса в глобальных переменных как модуля
        objClassProc = classProc() # Создание обьекта класса PF
        objPF = getattr(objClassProc, pfName) # Атомарная интерактивная поисковая функия как обьект
        return objPF
    
    
    
    



# --- END ВСПОМОГАТЕЛЬНЫЕ  функции для PF

if __name__ == '__main__':
    pass








# ### ---- ПРИМЕРЫ ----------------------------------



#     # ПРИМЕР: Организация принудительного цикла с атомарной функцией с передачей ее параметров <Новый подход>

#     # ERRORO: Последний элемент val = ['7750004136', 'https://checko.ru/company/toyota-bank-1077711000058']

#     # Получение массива dsCheckoLinks из comps_descr по полю link1 dsCheckoLinks
#     db = DB_BONDS_
#     db_macros = SqliteBondsMacros(db)     

#     # ПОлучение INN компаний из таблицы global_A  , которые еще не были обработаны на предмет вставки фин-показателей , анализируя поле f1 , служащее для маркера вставки фин - показателей компаний
#     # Pars:
#     tbName = 'global_A'
#     markerField = 'f1'
#     markerStr = 'INSERTED'
#     getFields = 'x_str' # Стобец с ИНН компаний

#     dsInnsNotInserted = WWWInteractiveUniversal.universal_get_ds_fields_from_global_table_where_not_marked_in_given_field (tbName, markerField, markerStr, getFields)

#     # Получение массива [inn, link1] из таблицы comps_descr с ссылками на страницы компаний в CHECKO и фин-показатели по которым еще не были вставлены в таблицу comps_finance
#     # Pars:
#     tbCompsDescr = 'comps_descr'
#     fields = ['inn', 'link1']
#     conds = {'ONE' : ['inn', 'IN', dsInnsNotInserted]}
#     cur, sql = db_macros.select_from_table_with_where_condition(tbCompsDescr, fields, conds)

#     dsInp = db_macros.get_ds_from_cursor(cur) # Входной, отфильтрованный по маркерам, массив в формате [[inn, link1], ...] для атомарной функции CheckoManager.get_financial_indicators_from_comp_page_link_with_pars_PF

#     # Pars атомарной функции поиска:
#     aifFuncParams = { # Параметры атомарной функции с ее полным название и параметрами к ней, которые позволяют расшифровать соотвествие колонок во входно массиве ключей и данных, связанных с ними
#         'aifFuncName' : 'CheckoManager.get_financial_indicators_from_comp_page_link_with_pars_PF', # Название функции с классом
#         'aifParams' : {} # соответствия колонок во входном массиве dsCheckoInnLinks
#     }

#     # Pars: Для функции настойчивого цикла 
#     sampleN = 4
#     dsQnLim = 8

#     # Pars: Параметры процедурной функции сохранения в БД результатов поиска в массиве
#     outputFuncDic = {
#         'procFuncName' :  'BondsMacros.save_results_of_aif_ds_with_financial_data_to_db_CHECKO_PF' ,   # Полное название процедурной функции сохранения результатов (ПФСР)
#     }
#     checkoFinancialRes = WWWInteractiveUniversal.universal_get_interactive_data_by_epoch_vers2_PF (dsInp, sampleN, aifFuncParams, dsQnLim, outputFuncDic)




    # # ПРИМЕР: Отработка эпохальной универсальной функции HTMLSeleniumManager.get_interactive_data_by_epoch (argDS, sampleN, inputFuncDic, outputFuncDic = {}) с униыерсальной функцией настойчивого цикла
    # # HTMLSeleniumManager.while_cycle_of_interactive_function_PF (argDS, sampleN, classObject, atomFuncObj)

    # ds = [
    #     ['66730355'],
    #     ['40994861'],
    #     ['17698269'],
    #     ['01370354'],
    #     ['18141190'],
    #     ['37192827'],

    #     ]

    # # Pars:
    # dsList = FG.convert_list_of_list_to_one_dim_list (ds, 0)
    # sampleN = 3
    # atomFunc = 'SparkManager.get_inn_plus_by_OPKO'

    # genDSRes = WWWInteractiveUniversal.universal_get_interactive_data_by_epoch_using_universal_while_PF(dsList, sampleN, atomFunc)




### ---- END ПРМИЕРЫ ------------------------



















