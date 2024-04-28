
from datetime import datetime
import time
import math
from random import random
# import pyautogui # НЕ УДАЛЯТЬ, РАЗБЛОКИРОВАТЬ, ЕСЛИ ИСПОЛЬЗУЕТСЯ В МЕСТНОМ ПРОЕКТЕ
from time import sleep
import os
from pathlib import Path
from string import digits, punctuation, ascii_letters, whitespace
import re

# import xlrd
# from bonds.bonds_main_manager import BondsMainManager



#




### ФУНКЦИИ СИСТЕМНОЙ ИНФОРМАЦИИ 

def name_of_variable_as_string_retrieve (var):
    """
    Получить название переменной в виде строкового значения
    Category: Глобальные функции
    """
    import inspect
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]



# def find_func_in_globals_(fClassName, funcName):
#     """
#     ПРОБА, не факт  что будет работать
#     @@@ Найти функцию по названию ее класса и имени , находящихся в проекте
#     Требует модуль импорт 
#     """
#     algClassObj = globals()[fClassName] # Нахождение класса в глобальных переменных  Get class from globals and create an instance
#     algFuncObj = getattr(algClassObj, funcName) # Нахождение функции-обработчика по названию из обьекта-обработчика Get the function (from the instance) that we need to call
#     return algFuncObj



### END ФУНКЦИИ СИСТЕМНОЙ ИНФОРМАЦИИ 


### СЛОВАРИ


def concat_two_dictionaries (dic1, dic2):
    """ 
    Обьединить два словаря в один
    """
    
    dicRes = dic1 | dic2
    
    return dicRes




### END СЛОВАРИ





# Функция выделения всего на активной странице сайта и копирования выделенного в буфер
def highlight_and_copy_keys ():
    """ 
    Функция выделения всего на активной странице сайта и копирования выделенного в буфер
    Category: Динамические методы курсора
    """
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

def paste_from_buffer_keys():
    """ 
    Вставить из буфера в какое-то поле на сайте
    Category: Динамические методы курсора
    """
    pyautogui.hotkey('ctrl', 'v')

def press_enter_key():
    """ 
    Нажать псевдо-клавишу Enter на клавиатуре
    Category: Динамические методы курсора
    """
    pyautogui.press('enter')     


def press_down_key():
    """
    Нажать динамически псевдо-клавишу Down
    Category: Динамические методы курсора
    """
    pyautogui.press('down')  


# Функция фокусировки имитацией нажатия ALT + TAB
def alttab_focus ():
    """ 
    Функция фокусировки имитацией нажатия ALT + TAB
    Category: Динамические методы курсора
    """
    pyautogui.keyDown('alt')
    sleep(.2)
    pyautogui.press('tab')
    sleep(.2)
    pyautogui.keyUp('alt')


# #  END НЕ УДАЛЯТЬ, РАЗБЛОКИРОВАТЬ, ЕСЛИ ИСПОЛЬЗУЕТСЯ В МЕСТНОМ ПРОЕКТЕ


# Create file and save text to it
def save_to_file(fName,text):
    """ 
    Create file and save text to it
    Category: Файлы и директории
    """
    with open(fName, 'w') as file:
        file.write(text)
    path = Path(__file__).parent.absolute()
    print(f"PR_NC_153 --> File {fName} Created successfully")
    return path


def create_and_save_to_file_v2(filePathFull ,text):
    """ 
    Create file and save text to it
    FROM: save_to_file
    ИЗМ: 1. Передается файл в полном абсолютном виде, что бы можно было управлять длиректорией мохранения файла
        
    Category: Файлы и директории
    """
    with open(filePathFull, 'w') as file:
        file.write(text)
    # path = Path(__file__).parent.absolute()
    print(f"PR_NC_154 --> SYS LOG: File {filePathFull} Created successfully")
    # return path




# Remove file
def delete_file(fName):
    """ 
    Remove file
    Category: Файлы и директории
    """
    if(os.path.isfile(fName)):
        os.remove(fName)
        print(f"PR_NC_155 --> File {fName} Deleted successfully")
    else:
        print(f"PR_NC_156 --> File {fName} does not exist")



def html_autosave_ftp (html,ext):
    """ 
    Создает файл копию переданного html кода с какой-нибудь страницы сайта. И выдает ftp адрес этого файла для открытия 
    на локальном браузере 
    Category: Операции с браузером
    """
    
    dt = datetime.datetime.now()
    t_string = dt.strftime("%H_%M_%S")
    randm = random.randint(1,10000000)
    fName = f"auto_{randm}_{t_string}.{ext}"
    curr_path = save_to_file(fName,html)
    sleep(1)
    absolute_path = f"{curr_path}/{fName}" # абсолютный путь с названием файла
    ftp = f"file://{curr_path}/{fName}"  # ftp адрес сохраненного html файла
    return absolute_path, ftp
        


def strip_for_digits_bytearray (text):
    """ 
    OBSOLETED. Use strip_to_digits
    оставить только wцифры, '-','.' и '%' 
    Category: Работа с текстом
    """
    good_chars = (digits + '-' + '.' + '%').encode()
    junk_chars = bytearray(set(range(0x100)) - set(good_chars))
    return text.encode('ascii', 'ignore').translate(None, junk_chars).decode()



def strip_to_digits (text):
    """ 
    оставить только wцифры, '-','.' и '%'
    Повтор Obsoleted функции  strip_for_digits_bytearray, у которой не читабельное название
    Category: Работа с текстом
    """
    good_chars = (digits + '-' + '.' + '%').encode()
    junk_chars = bytearray(set(range(0x100)) - set(good_chars))
    return text.encode('ascii', 'ignore').translate(None, junk_chars).decode()



def strip_by_reg(s):
    """ 
    OBSOLETED. Use strip_to_letters
    оставить только буквы 
    Category: Регулярные выражения
    """
    #s = 'Hello!@#!%!#&&!*!#$#%@*+_{ world!'
    reg = re.compile('[^a-zA-Z ]')
    return reg.sub('', s)


def strip_to_letters(s):
    """ 
    оставить только буквы
    Повтор OBSOLETED функции  strip_by_reg,  которая устарела по читабельности названия
    Category: Регулярные выражения
    """
    #s = 'Hello!@#!%!#&&!*!#$#%@*+_{ world!'
    reg = re.compile('[^a-zA-Z ]')
    return reg.sub('', s)    


def m_array_index(arr, searchItem):
    """ 
    Функция поиска элемента двумерного списка по заданному значению и вывод индексов его местонахождения
    https://stackoverflow.com/questions/6518291/using-index-on-multidimensional-lists 
    Category: Списки
    """

    for i,x in enumerate(arr):
        for j,y in enumerate(x):
            if y == searchItem:
                return i,j
    return -1,-1 #not found


## -- Функции работы с МАСИИВАМИ , СПИСКАМИ И ПР DataSources

def filter_arr_of_lists_with_col_inxs (ds, inxs):
    """ 
    Оставляет только те элементы  в массиве  листов ds (проекция таблицы), которые соответствуют набору индексов inxs колонок массива  
    Category: Списки
    """

    dsRes = [[ x[i] for i in inxs ] for x in ds ]
    return dsRes


def add_cols_with_vals_to_list_of_lists (ds, addColsVals):
    """ 
    Вставить во все ряды списка списков ds (аналог таблицы) заданные дополнительные колонки с величинами-константами или списками listDS addColsVals [val1,listDS2, val3,listDS4...,valN] для всех доп.полей
    listDS - [v1, v2, ...,vN] <N = количеству рядов в ds !!>, ОДНОМЕРНЫЙ!  -  при этом должен по количеству элементов быть равным количеству рядов в ds, что бы для каждого ряда находилось значение из списка дополнительной колонки
    То есть можно не вставлять в доп ряды не только константы, но и вертикальный вектор величин, что необходимо при вставке INSERT часто (например, если если колока - UNIQUE)
    ds - список списков типа [[v00,v01,...,v0N],
    [v10,v11,...,v1N],
    ....
    [vK0, vK1, ... vKN]]

    addColsVals      - список величин-констант (колонок с величинами-константами) для добавки в конец каждого ряда в списке списков  ['5', ds2, ...]
                    Если величина в списке доп величин для доп полей - список, то проставляем для каждого ряда в доп.колонке значение в соответствии со списком заданных величин в listDS
                    Eсли просто константа, то проставляется константа в каждый ряд колонки

    # OR with comprehantion
    # result = [v.copy() + b[i][2:3] for i, v in enumerate(a)] ??? 
    https://stackoverflow.com/questions/69107370/add-a-column-to-a-list-of-lists   
    Category: Списки
    """
    resultDS = [] # результирующий список списков рядов
    for i, v in enumerate(ds): 
        resultDS.append(v.copy())
        for c in addColsVals:
            if type(c) == list: # Если величина в списке доп величин для доп полей - список, то проставляем для каждого ряда в доп.колонке значение в соответствии со списком заданных величин в listDS
                resultDS[-1].append(c[i])
            else:
                resultDS[-1].append(c)  

    return resultDS


def add_constant_to_all_elements_of_1dim_list (ds1Dim, addVal):
    """
    Добавление к каждому элементу  в ОДНОМЕРНОМ списке константной величины . То есть добавление колонки константы и увеличение мерности списка на единицу
    Category: Списки
    """
    dsRes = [[x, addVal] for x in ds1Dim]
    return dsRes

def add_constant_to_all_second_elements_of_2dim_list (ds2Dim, addVal):
    """
    Добавление константы к каждому элементу второго уровня ДВУМЕРНОГО списка
    Category: Списки
    """

    dsRes = [[ ds2Dim[i][j] for j in range(len(ds2Dim[i])) ] + [addVal] for i in range(len(ds2Dim)) ]
    return dsRes


def add_consts_in_ds_to_all_second_elements_of_2dim_list(ds2Dim, dsConsts):
    """
    Добавить каждый элемент-константу из списка dsConsts к каждому элементу второго уровня ДВУМЕРНОГО списка
    Category: Списки
    """
    dsRes = ds2Dim
    for valConst in dsConsts:
        dsRes = add_constant_to_all_second_elements_of_2dim_list (dsRes, valConst)    
    return dsRes


def add_1dim_list_to_2dim_list_as_column (list2Dim, list1Dim):
    """ 
    Добавить одномерный список к двумерному как колонку равных величин и выдать один двумерный список 
    Размер рядов в листах должен быть равен
    Category: Списки
    """

    list2Dim = [ [list1Dim[i]]  + [list2Dim[i][j] for j in range(len(list2Dim[i])) ]   for i in range(len(list1Dim))] # Обьединяем списки INN и величин словарей
    return list2Dim


def concat_two_1Dim_lists_to_one_2dim_list (list1Keys, list2):
    """
    Обьеденить два одномерных списка в один двумерный с двумя колонками. Списки должны быть одинаковой размерности
    [list2 ] + [list1] = [[list1, list2]]
    Category: Списки
    """
    list2Dim = convert_one_dim_list_to_list_of_lists(list2)
    listConc2Dim = add_1dim_list_to_2dim_list_as_column (list2Dim, list1Keys)
    return listConc2Dim






def concat_several_ds_by_colmns_to_list(dsLists):
    """ 
    Складывает несколько двмерных dataSources в один многомерный список по столбцам
    Кол-во рядов должно быть одинаковым в обоих источниках. Кол-во столбцов может быть разным
    dsLists - список двумерных dataSources (могут быть списки таплов или списков) <Перепроверять насчет таплов>
    ds1 = [[4, 3, 5, ], [1, 2, 3], [3, 7, 4]]
    ds2 = [[1, 3], [9, 3, 5, 7], [8]]
    Res:
    [[4, 3, 5, 1, 3], [1, 2, 3, 9, 3, 5, 7], [3, 7, 4, 8]]
    Help: https://www.geeksforgeeks.org/python-concatenate-two-list-of-lists-row-wise/ !!!!!!
    Category: Списки
    """
    dsRes = []
    i = 0
    for ds in dsLists: # Цикл по списку регионов

        if i==0:
            dsRes = ds
        else:
            dsRes = list(sub1 + sub2 for sub1, sub2 in zip(dsRes, ds )) # https://www.geeksforgeeks.org/python-concatenate-two-list-of-lists-row-wise/ !!!!!!
        i+=1
    return dsRes



def convert_tuple_of_tuples_to_list_of_lists (tupTupls):
    """ 
    Преобразует тапл таплов (двумерный тапл) в список списков (двумерный список) 
    Category: Списки
    """
    dsLists = [ [tupTupls[i][j] for j in range(len(tupTupls[i]))  ] for i in range(len(tupTupls))]
    return dsLists


def concat_and_transform_two_lists_in_one(listOfLists):
    """  
    TODO: !!! Проверить правилльность работы 
    ??? Обьединяет списки и переворачивает размерность колонок и рядов
    Прим: listOfLists = [[list1], [list2]]
    Category: Списки
    """
    dsLists = [ [listOfLists[i][j] for j in range(len(listOfLists[i]))  ] for i in range(len(listOfLists))]
    return dsLists


def delete_rows_where_field_val (ds, colInxVal):
    """ 
    Удалить ряды в dataSource (двумерный список или тапл таплов), в задаваемом поле которых находится задаваемая величина 
    Прим: colInxVal = [1, ''] -  фильтр отсева по индексу колонки и задаваемой ей величины для удаления рядов, в которых ыеличина в колонке = задаваемому значению
    Category: Списки
    """
    dsRes = [ds[i] for i in range(len(ds)) if ds[i][colInxVal[0]] != colInxVal[1]] # очистка от пустых строк comprehance
    return dsRes



def decompose_dic_to_two_lists (dic):
    """
    Разложить словарь на список ключей и список величин
    Category: Списки
    """
    keyList = list(dic.keys())
    valList = list(dic.values())
    return keyList, valList


def convert_list_of_list_to_one_dim_list (ds2List, col):
    """ 
    Конвертирует любой двумерный лист в одномерный по указаннйо колонке 
    Или другими словами оставляет одну заданную колонку из входного двумерного массива
    Category: Списки
    """
    resList = [x[col] for x in ds2List]
    return resList



def convert_list_to_2_dim_list_with_columns_size (list, colSize, rowSize = -1):
    """ 
    Конвертировать одномерный список в дыумерный, с заданным кол-вом элементов в первичном списке 
    ПРИМ: output [[5, 2, 3, 4], [1, 6, 1, 6], [7, 2, 3]], где colSize = 4
    Если rowSize = -1, то возвращаются все ряды, даже, если в них не хватает элементов до размера colSize. В ином случае возвращается заданное кол-во рядов
    https://stackoverflow.com/questions/45468611/create-2d-list-from-1d-list-with-given-length-and-width
    Category: Списки
    """
    
    if rowSize == -1:
        result = [list[x:x+colSize] for x in range(0,len(list),colSize)]
    else:
        result = [list[x:x+colSize] for x in range(0,len(list),colSize)][:rowSize]
        
    return result






def convert_list_of_one_tuple_to_list_fg(tupArr):
    """ 
    Конвертация данных из запросов , содержащихся в курсоре, в виде  списка из одного тапла [(x1,x2 .. xN)] 
    в обычный список велечин [x1, x2 ...]
    """
    
    listDS = [x for x in tupArr[0]]  # преобразование в список
    return listDS




def convert_list_of_tuples_to_list_fg(tupArr):
    """ 
    Конвертация данных из запросов, содержащихся в курсоре в виде  списка из нескольких таплов [(x1,),(x2,) ...] 
    в обычный список велечин [x1, x2 ...]
    """
    
    listDS = [x[0] for x in tupArr]  # преобразование в список
    return listDS  



    


def convert_one_dim_list_to_list_of_lists(dsOneDim):
    """ 
    Конвертация одномерного простого списка в список списков: [v1,v2 ... vN] -> [[v1],[v2], ... [vN]] 
    Category: Списки
    """
    dsTwoDimList = [[x] for x in dsOneDim]
    return dsTwoDimList


def remove_duplicates_from_list(dsList):
    """ 
    Удалить дупликаты из двумерного  списка 
    Category: Списки
    """
    newList = list(map(list, {tuple(x) for x in dsList}))
    # newList = list(set(dsList))
    return newList



def remove_duplicates_from_list_by_one_col_key (dsList, colInx):
    """ 
    Удалить дублирующие по одной колонке записи в двумерном списке с несколькими колонкми
    colInx - индекс колонки, по которой нужно удалить дупликаты
    Category: Списки
    """

    colVals = [] # массив для учета величин колонки
    res = [] # результирующий массив
    for x in dsList:
        if x[colInx] not in colVals:
            colVals.append(x[colInx])
            res.append(x)   

    return res



def remove_duplicates_from_1dim_list(list1Dim):
    """ 
    Удаление дупликатов из простого одномерного списка 
    Category: Списки
    """
    temp = []
    resList = []
    for x in list1Dim:
        if x not in temp:
            resList.append(x)        
        temp.append(x)
    return resList




def convert_list_dicts_to_list_str (dsListDicts):
    """ 
    Ковертация одномерного простого списка с обектами словаря  в список стринговой формы словарей (или JSON обьектов) 
    Category: Списки
    """
    dsListDicStrs = [[f'{x}'] for x in dsListDicts]
    return dsListDicStrs


def delete_columns_from_two_dim_list (dsTwoDimList, indxDToDel):
    """ 
    Удалить заданные колонки в двумерном списке списков 
    dsTwoDimList = [[1, 8, 3], [4, 5, 6], [0, 5, 7]]
    indxDToDel = [0,2]
    Category: Списки
    """
    dsRes = [list(x) for x in zip(*[d for i,d in enumerate(zip(*dsTwoDimList)) if i not in indxDToDel])]
    return dsRes


def convert_two_dim_list_with_dicts_to_same_list_with_str(dsTwoDimList, col):
    """ 
    Перевод двумерного списка с колонкой , где хранятся обьекты dictionary в такой же список, но с замещением 
    обьектов dictionary на обьекты JSON или стринговую форму словаря
    col - колонка , которую надо преобразовать в общем массиве
    dsTwoDimList - должен содержать больше одной колонки во втором измерении [[col1, col2],...]
    Category: Списки
    """
    # dsOneDinDicts = convert_list_of_list_to_one_dim_list (dsTwoDimList, col) # отделение столбца со dictionaries
    dsOneDinDicts = convert_list_of_list_to_one_dim_list (dsTwoDimList, col) # отделение столбца со dictionaries    
    dsListDicStrs = convert_list_dicts_to_list_str (dsOneDinDicts) # преобразования отделенного списка простого в список json оьектов 
    dsTwoDimListMinesCols = delete_columns_from_two_dim_list (dsTwoDimList, [col]) # Удаляем исходную колонку из исходного массива
    dsRes = concat_several_ds_by_colmns_to_list([dsTwoDimListMinesCols, dsListDicStrs]) # Присоединяем обработанный столбец к исходному (но который уже без той колонки)
    return dsRes



def convert_two_lists_to_dictionary(list1,list2):
    """
    Конвертировать два одноразмерных простых списка в один словарь, гдк ключами выступают значения list1, а значениями словаря - значения list2
    Category: Списки
    """
    resDict = dict(map(lambda i,j : (i,j) , list1,list2))
    return resDict


def compare_two_list_on_unique(list1, list2):
    """
    ЗАГОТОВКА. Сравнить два списка и получить уникальные значения между ними двумя
    Category: Заготовки
    """
    





def if_list_is_3_dim (ds):
    """ 
    Проверка является ли массив трехмерным или нет. Необходимо для определения были ли эпохи или все шло в одном подходе 
    Category: Списки
    """
    if type(ds[0][0]) == list: # если трехмерный массив
        res = True
    else: # если не трехмерный (а друхмерный или одномерный)
        res = False
    return res



def if_list_is_2_dim (ds):
    """ 
    Проверка является ли массив трехмерным или нет. Необходимо для определения были ли эпохи или все шло в одном подходе 
    НЕ ТЕСТИРОВАНО 
    Category: Списки
    """
    if type(ds[0]) == list: # если трехмерный массив
        res = True
    else: # если не трехмерный (а друхмерный или одномерный)
        res = False
    return res



def get_intersection_of_two_list(lst1, lst2):
    """ 
    Пересечение двух списков равного формата 
    Category: Списки
    """
    lst3 = [value for value in lst1 if value in lst2]
    return lst3



def get_dict_keys_by_value (dict, val):
    """
    Найти  ключи, значения которых равны (или другие операнды?) заданной величине val 
    Category: Словари
    """
    
    listKeys = list(dict.keys())[list(dict.values()).index(val)]
    return listKeys
    


def unite_all_elements_of_2dim_list_to_list (ds2dim):
    """
    обьединить все эелементы всех рядов и колонок двумерного массива в один простой
    Нужно, к примеру, если надо обьеденить однородные списки по эпохам в двумерном массиве в один
    Category: Списки
    """

    dsUnited = []
    for x in ds2dim:
        for y in x:
            dsUnited.append(y)    
    return dsUnited



def get_inx_of_first_occurence_of_given_val_in_2dim_list_row (list2Dim: list, colInx, value) -> int:
    """
    Возвращает индекс ряда в двумерном массиве, где произошло первое совпадение искомой величины с величиной в задаваемой параметром колоке двумерного массива
    https://stackoverflow.com/questions/71481942/python-2d-list-find-corresponding-first-row-index-of-a-value-in-the-array
    Category: Списки
    """
    for i, item in enumerate(list2Dim):
        if item[colInx] == value:
            return i # возвращает индекс ряда, где обнаружилось первого совпадение величины в заданной колонке
    # raise ValueError(f"{value} not in list")    
    return -1 # Значит не найдено вообще совпадения



def get_inx_and_val_of_row_with_max_val_in_col_of_2dim_list (list2Dim:list, colInx) :
    """
    получение индекса ряда в двумерном списке, где находится макимальное значение из всей задаваемой параметром колонки" двумерного массива
    Category: Списки
    """
    maxval = -1
    maxidx = None
    for i, v in enumerate(list2Dim):
        if v[colInx] > maxval:
            maxval = v[colInx]
            maxidx = i
    res = [maxidx, list2Dim[maxidx][colInx]]
    return res



def get_inx_of_first_occurence_of_val_in_1dim_list (list1Dim: list,  value) -> int:
    """
    Возвращает индекс и значение иаксимального элемента в одномерном списке
    Category: Списки
    """
    for i, item in enumerate(list1Dim):
        if item == value:
            return i
    return -1 # Значит не найдено вообще совпадения



def get_inx_and_val_of_max_val_in_1dim_list (list1Dim:list) -> int:
    """
    получение индекса максимального значения в одномерном списке
    Category: Списки
    """
    maxval = -1
    maxidx = None
    for i, v in enumerate(list1Dim):
        if v > maxval:
            maxval = v
            maxidx = i
    return maxidx





def get_dict_key_with_not_none_vals (inpDict):
    """
    Получить ключи словаря, в которых значения не равны None
    Category: Словари
    """
    keysNotNone = {k: v for k, v in inpDict.items() if v is not None}
    return keysNotNone




def insert_list_to_another_list_by_inx (listBase, listInsert, rowInx):
    """
    Сделать вставку списка в другой список между рядами , начиная с определенного индекса
    Category: Списки
    """
    # Вставить textForSysMainBotLines в pageLines перед индексом indexIfName
    listFinal = listBase[:rowInx] + listInsert + listBase[rowInx:]
    return listFinal




def filter_dic_by_keys_contain_str_fragm_FG (dic, strFragm):
    """
    Получить словарь только с теми элементами, ключи которых содержат сринговый фрагмент strFragm
    Category: Словари
    """

    filteredDic = {k:v for k,v in dic.items() if strFragm in k}
    return filteredDic



def compare_two_one_dim_lists (list1, list2):
    """
    Сравнить два одномерных списка и получить элементы, которых нет в первом списке по сравнению со вторым
    Category: Списки
    """

    diffElementsList = list(set(list2) - set(list1))

    return diffElementsList




## -- END Функции работы с МАСИИВАМИ , СПИСКАМИ И ПР DataSources


## -- Функции , связанные со временем time

def get_current_time_format1_d_m_y_h_m_s():
    """
    Получение текущего времени в формате 1: %d_%m_%Y_%H_%M_%S
    21_11_2022_14_02  (%d_%m_%Y_%H_%M_%S)
    Category: Функции времени
    """

    dt = datetime.now()
    dtString = dt.strftime("%d_%m_%Y_%H_%M_%S")
    return dtString



def get_current_time_format2():
    """
    Получение текущего времени в формате 2: %d-%m-%Y %H:%M:%S
    24-11-2022 14:43:35
    Category: Функции времени
    """

    dt = datetime.now()
    dtString = dt.strftime("%d-%m-%Y %H:%M:%S")
    return dtString



def get_current_time_format_1_and_2_and_universal_unix():
    """
    Получение текущего времени в формате dtStringFormat2: %d-%m-%Y %H:%M:%S
    24-11-2022 14:43:35
    Так жк в формате dtStringFormat1: %d_%m_%Y_%H_%M_%S
    И универсальный формат unix universUnix с округлением , то есть без милисекунд
    Category: Функции времени
    """

    dt = datetime.now()
    dtStringFormat1 = dt.strftime("%d_%m_%Y_%H_%M_%S")
    dtStringFormat2 = dt.strftime("%d-%m-%Y %H:%M:%S")
    universUnix = convert_from_date_to_unix_universal (dtStringFormat2, format = '%d-%m-%Y %H:%M:%S', rinteger = True)
    
    return dtStringFormat1, dtStringFormat2, universUnix




def get_current_time_format3():
    """
    Получение текущего времени в формате 1: %d_%m_%Y_%H_%M_%S
    21_11_2022_14_02  (%d_%m_%Y_%H_%M_%S)
    Category: Функции времени
    """

    dt = datetime.now()
    dtString = dt.strftime("%d.%m.%Y_%H.%M.%S")
    return dtString



def get_current_time_format4():
    """
    Получение текущего времени в формате 1:%d-%m-%Y_%H:%M:%S
    21_11_2022_14_02  (%d_%m_%Y_%H_%M_%S)
    Category: Функции времени
    """

    dt = datetime.now()
    dtString = dt.strftime("%d-%m-%Y_%H:%M:%S")
    return dtString



def get_current_time_format4_2():
    """
    Получение текущего времени в формате 1: %d-%m-%Y %H:%M
    Category: Функции времени
    """

    dt = datetime.now()
    dtString = dt.strftime("%d-%m-%Y %H:%M")
    return dtString


def get_current_time_with_format(dFormat):
    """
    Получение текущего времени в любом заданном формате (формат задается через стандартные стринги)
    Category: Функции времени
    """

    dt = datetime.now()
    dtString = dt.strftime(dFormat)
    return dtString




def get_date_format3():
    """
    24.11.2022
    Category: Функции времени
    """
    dt = datetime.now()
    dtString = dt.strftime("%d.%m.%Y")
    return dtString




def get_calend_date_format6():
    """
    24_11_2022
    Category: Функции времени
    """
    dt = datetime.now()
    dtString = dt.strftime("%d_%m_%Y")
    return dtString






def convert_excel_serial_date_to_str(serDate):
    """ 
    !!! НЕ ПРОВЕРЕНО
    Конвертировать экскловсий тип даты под названием serial date в стринг с datetime
    https://stackoverflow.com/questions/6706231/fetching-datetime-from-float-in-python
    https://pypi.org/project/pyxlsb/
    sudo pip install pyxlsb
    Category: Excel
    """
    from pyxlsb import convert_date
    date = format(convert_date(serDate), '%m.%d.%Y')

    return date



def get_curr_timestamp ():
    """
    Получение текущего timestamp
    Category: Функции времени
    """
    return datetime.now()
    


def get_unix_curr_time():
    """
    Получить текущее Юникс-время или секунды с начала 1970 года
    Category: Функции времени
    """
    return int(time.time())

    


def convert_data_to_int_unix_format2 (dt):
    """
    Преобразование календарной даты типа  dt = '18-12-2022 16:20:24' в UNIX timestamp() целочисленный
    !!! С обнулением милисикунд - то есть не точная конверсия!!!. В поиске при знаке '=' совпадения не будет !!! Приводится к целочисленному формату unix_time
    https://linux-notes.org/rabota-s-unix-timestamp-time-na-python/
    Category: Функции времени
    """
    date_format = datetime.strptime(dt, "%d-%m-%Y %H:%M:%S")
    unix_time = int(datetime.timestamp(date_format)) # Обнуление милисекунд приведением к целочисленному
    return unix_time




def convert_data_to_int_unix_format4 (dt):
    """
    Преобразование календарной даты типа  dt = '18-12-2022' в UNIX timestamp() целочисленный
    Без милисикунд, часов, минут, секунд. Только дата. Приводится к целочисленному формату unix_time
    https://linux-notes.org/rabota-s-unix-timestamp-time-na-python/
    Category: Функции времени
    """
    dt = dt + " 00:00:00" # Обнуляем часы, минуты, секунды
    date_format = datetime.strptime(dt, "%d-%m-%Y %H:%M:%S")
    unix_time = int(datetime.timestamp(date_format)) # Обнуление милисекунд приведением к целочисленному
    return unix_time



def convert_data_to_int_unix_format5 (dt):
    """
    Преобразование календарной даты типа  dt = '18-12-2022' в UNIX timestamp() целочисленный
    Без милисикунд, часов, минут, секунд. Только дата. Приводится к целочисленному формату unix_time
    https://linux-notes.org/rabota-s-unix-timestamp-time-na-python/
    Category: Функции времени
    """
    dt = dt + " 00:00:00" # Обнуляем часы, минуты, секунды
    date_format = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    unix_time = int(datetime.timestamp(date_format)) # Обнуление милисекунд приведением к целочисленному
    return unix_time



def convert_data_to_int_unix_format6 (dt):
    """
    Преобразование календарной даты типа  dt = '22.12.2023 в UNIX timestamp() целочисленный
    Без милисикунд, часов, минут, секунд. Только дата. Приводится к целочисленному формату unix_time
    https://linux-notes.org/rabota-s-unix-timestamp-time-na-python/
    Category: Функции времени
    """
    dt = dt + " 00:00:00" # Обнуляем часы, минуты, секунды
    date_format = datetime.strptime(dt, "%d.%m.%Y %H:%M:%S")
    unix_time = int(datetime.timestamp(date_format)) # Обнуление милисекунд приведением к целочисленному
    return unix_time



def convert_int_unix_to_data_format2 (unix_time):
    """
    преобразование из UNIX timestamp в календарную дату типа  dt = '18-12-2022 16:20:00'
    Без милисикунд из целочисленного формата unix_time
    https://linux-notes.org/rabota-s-unix-timestamp-time-na-python/
    Category: Функции времени
    """
    date_time = datetime.fromtimestamp(unix_time)
    dt = date_time.strftime('%d-%m-%Y %H:%M:%S')
    return dt


def convert_from_date_to_unix_universal (cdate, format = '%d-%m-%Y %H:%M:%S', rinteger = False):
    """
    Универсальный метод коныертации календарной даты в UNIX-время
    format - формат заданной даты
    cdate - календарная дата формата format
    rinteger - с округлением до целого числа или нет. По умолчанию - без округления
    В случае слямбда-функциями аргументы могут передаваться в виде списка. В этом случае проверяем тип и получаем их как из списка
    Category: Функции времени
    """
    
    # В случае слямбда-функциями аргументы могут передаваться в виде списка. В этом случае проверяем тип и получаем их как из списка
    if type(cdate) == list: 
        cdate = cdate[0]
    
    # Перевод стринга в тип datetime
    dateTime = datetime.strptime(cdate, format)
    
    unixTime = time.mktime(dateTime.timetuple())
    
    if rinteger:
        unixTime = int(unixTime)
    
    return unixTime


def convert_date_format_to_another_date_format (cdate, formatSrc, formatRes ):
    """
    Универсальный метод конвертации календарной даты из одного формата в другой
    formatSrc - формат заданной даты
    formatRes - необходимый формат результата
    cdate - календарная дата формата format
    В случае слямбда-функциями аргументы могут передаваться в виде списка. В этом случае проверяем тип и получаем их как из списка
    Category: Функции времени
    """
    
    # В случае слямбда-функциями аргументы могут передаваться в виде списка. В этом случае проверяем тип и получаем их как из списка
    if type(cdate) == list: 
        cdate = cdate[0]
    # Перевод стринга в тип datetime
    dateTime = datetime.strptime(cdate, formatSrc)
    cdateRes = dateTime.strftime(formatRes)
    return cdateRes


def convert_date_format_to_another_date_format (cdate, **kwargs):
    """
    Универсальный метод конвертации календарной даты из одного формата в другой с использованием **kwargs
    Использует **kwargs для задания параметров в виде например: kwargs['format']. Это необходимо при использовании лямбда-функций для задания внешних параметров
    formatSrc - формат заданной даты
    formatRes - необходимый формат результата
    cdate - календарная дата формата format
    В случае слямбда-функциями аргументы могут передаваться в виде списка. В этом случае проверяем тип и получаем их как из списка
    Category: Функции времени
    """
    
    # В случае слямбда-функциями аргументы могут передаваться в виде списка. В этом случае проверяем тип и получаем их как из списка
    if type(cdate) == list: 
        cdate = cdate[0]
    # Перевод стринга в тип datetime
    dateTime = datetime.strptime(cdate, kwargs['formatSrc'])
    cdateRes = dateTime.strftime(kwargs['formatRes'])
    return cdateRes




def convert_date_format_to_another_date_format_with_kwargs (cdate, **kwargs):
    """
    Универсальный метод конвертации календарной даты из одного формата в другой
    Использует **kwargs для задания параметров в виде например: kwargs['format']. Это необходимо при использовании лямбда-функций для задания внешних параметров
    formatSrc - формат заданной даты
    formatRes - необходимый формат результата
    cdate - календарная дата формата format
    В случае слямбда-функциями аргументы могут передаваться в виде списка. В этом случае проверяем тип и получаем их как из списка
    Category: Функции времени
    """
    
    # В случае слямбда-функциями аргументы могут передаваться в виде списка. В этом случае проверяем тип и получаем их как из списка
    if type(cdate) == list: 
        cdate = cdate[0]
    # Перевод стринга в тип datetime
    dateTime = datetime.strptime(cdate, kwargs['formatSrc'])
    cdateRes = dateTime.strftime(kwargs['formatRes'])
    return cdateRes




def convert_from_date_to_unix_universal_with_kwargs (cdate, **kwargs):
    """
    Использует **kwargs для задания параметров формата kwargs['format'] и флага округения kwargs['rinteger']. Это необходимо при использовании лямбда-функций для задания 
    внешних параметров
    
    Универсальный метод коныертации календарной даты в UNIX-время
    format - формат заданной даты
    cdate - календарная дата формата format
    rinteger - с округлением до целого числа или нет. По умолчанию - без округления
    В случае слямбда-функциями аргументы могут передаваться в виде списка. В этом случае проверяем тип и получаем их как из списка
    Category: Функции времени
    """
    
    # В случае слямбда-функциями аргументы могут передаваться в виде списка. В этом случае проверяем тип и получаем их как из списка
    if type(cdate) == list: 
        cdate = cdate[0]
    
    # Перевод стринга в тип datetime
    dateTime = datetime.strptime(cdate, kwargs['format'])
    
    unixTime = time.mktime(dateTime.timetuple())
    
    if kwargs['rinteger'] :
        unixTime = int(unixTime)
    
    return unixTime
    
    
    
def convert_from_unix_to_date_universal (unixTime, format):
    """
    Универсальный метод коныертации UNIX-время в календарную дату 
    format - формат заданной даты
    cdate - календарная дата формата format
    Category: Функции времени
    """
    
    date_time = datetime.fromtimestamp(unixTime)
    
    cdate = date_time.strftime(format)
    
    return cdate
    
    


def parsing_data_and_operand(odate, odefault = '=='):
    """
    Парсинг календарной даты с возможным операндом типа <, > , => и т.д. , что бы на выходе была дата и знак отдельно
    Category: Функции времени
    """
    
    # Анализ операнда
    
    # !!! Условия по составным операндам  должны стоять впереди простых операндов 
    if '>=' in odate: 
            parts = str(odate).split('>=')
            operand = '>='
            gdate = parts[1]
            
    elif '<=' in odate:
            # parts = re.split(r"<=", odate)
            parts = str(odate).split('<=')
            operand = '<='
            gdate = parts[1]
    
    elif '>' in odate:
            parts = str(odate).split('>')
            operand = '>'
            gdate = parts[1]
            
    elif '<' in odate:
            parts = str(odate).split('<')
            operand = '<'
            gdate = parts[1]
    elif '=' in odate:
            parts = str(odate).split('=')
            operand = '=='
            gdate = parts[1]
            

    else:
            operand = odefault
            gdate = odate   
            
    return operand, gdate
            
            
    


## -- END Функции , связанные со временем time

## -- Функции связанные с разбиением массивов по порциям и эпохам 


def get_epoch_qn_of_ds_with_given_sample_lim (ds, sampleN):
    """
    Получить кол-во эпох необходимое для проработки заданного массива и кол-ва элементов в порциях эпох
    Category: Эпохи
    """
    dsN = len(ds)
    # sampleN = 2 # Выборка записей из общего массива dsOKPO
    epochsQn = math.ceil(dsN/sampleN) # кол-во эпох, необходимых для обработки всего запрашиваемого списка ЦБ
    return epochsQn



def get_sample_of_ordered_epoch_from_ds (ds, sampleN, epochOrderNumber):
    """
    Получить выборку из массива на основе номера эпохи (количество эпох может быть dsN/sampleN и каждая из них пронумерована по номеру эпохи по умолчанию) 
    и размера порции в эпохе
    ds - исходный массив
    sampleN - порция элементов массива в одной эпохе
    epochOrderNumber - порядковый номер эпохи . МОжет лежать в range(len(math.ceil(dsN/sampleN)))
    Category: Эпохи
    """

    dsEpoch = ds[epochOrderNumber*sampleN:epochOrderNumber*sampleN + sampleN] # выборка для эпохи из общего массива
    return dsEpoch



## -- END Функции связанные с разбиением массивов по поруиям и эпохам 


## -- Определение структур обьектов 

def shape(lst):
    """ 
    Формат списка
    Category: Форматы структур
    """
    length = len(lst)
    shp = tuple(shape(sub) if isinstance(sub, list) else 0 for sub in lst)
    if any(x != 0 for x in shp):
        return length, shp
    else:
        return length


## -- Определение структур обьектов 


# Со стрингами

def count_str_in_word(strToCheck, strToFind):
    """
    Считает сколько раз повторяется символ или стринговый фрагмент в стринге
    Category: Работа с текстом
    """
    if strToFind in strToCheck:
        repeatedQn = strToCheck.count(strToFind)  
    else:
        repeatedQn = 0

    return repeatedQn



def compose_str_with_repeated_simbol(simbol, n):
    """
    Составляет строку из повторяющихся n-раз символов (или строковых фрагментов)
    Category: Работа с текстом
    """
    resStr = ''

    for i in range(n):
        resStr += simbol

    return resStr






def clear_from(val, clrFrom):
    """
    Очистить слово от заданных в спсике clrFrom знаков
    clrFrom - последовательность символов в списке clrFrom играет роль
    Category: Работа с текстом
    """
    for sign in clrFrom:
        val = val.replace(sign, '')
    return val




# END Со стрингами




# С символами названий переменных, функций и классов и т.д.

def get_variable_str_name(localItems, variable):
    """
    Функция получения стрингового имени переменной
    localItems - перечень переменных в локальном пространстве модуля, который задается всегда из САМОГО МОДУЛЯ так: localItems = locals().items()
    variable - просто подставить любую локальную модульную переменную в точке вызова этой функции в модуле
    Category: Глобальные функции
    """    
    # varStrName = ''
    varStrName = [ i for i, a in localItems if a == variable][0]
    # print(f"Name srchTxt varaiable : {varStrName}")
    return varStrName


# END С символами названий переменных, функций и классов и т.д.



# ТИПЫ 

def get_type_in_str_of_var (var):
    """
    Получить стринговое отображение типа переменной
    Category: Форматы структур
    """
    type_name = type(var).__name__
    return type_name




# END ТИПЫ 


# Сортировки массивов

def sort_2dim_list_by_col(ds2Dim, colInx, desc = False):
    """
    Сортировка двумерного списка  по колонкам 
    ds2Dim - Входной lдвумерный список
    colInx - индекс колонки в спсике второго уровня (рядов двумерного массива)
    desc - Если False, то идет сортировка по возрастанию значений поля. Если True - то по убыванию. По умолчанию - сортировка идет по возрастанию значений desc = False
    RET: ds2dimSorted - отсортированный ldevthysq массив по заданной колонке
    https://stackoverflow.com/questions/20183069/how-to-sort-multidimensional-array-by-column
    and by two cols or reverse (desc ) sorting: https://stackoverflow.com/questions/2173797/how-to-sort-2d-array-by-row-in-python
    Category: Списки
    """
    ds2dimSorted = sorted(ds2Dim, key = lambda x: x[colInx], reverse = desc)
    return ds2dimSorted


def binary_switch_str_var_FG(var):
    """
    Бинарное переключение стринговой переменной в зависимости от собственного ее значения [FG - чтобы разделить с использованием подобной фкнкции в дркгой библиотеке]
    Ret: (var <1 или 0>, flag <True or False>)
    Используется для переключения сортировки или еще чего-нибудь в HTML - коде, где передается в глобальном параметре request
    Category: Аналитические методы
    """
    if var == None or var == '0':
        var = '1'
        flag = True
    elif var == '1':
        var = '0'
        flag = False
    return var, flag


# END Сортировки массивов

# HTML полезные функции 

def binary_switch_str_var(var):
    """
    Бинарное переключение стринговой переменной в зависимости от собственного ее значения
    Ret: (var <1 или 0>, flag <True or False>)
    Используется для переключения сортировки или еще чего-нибудь в HTML - коде, где передается в глобальном параметре request
    Category: Аналитические методы
    """
    if var == None or var == '0' or var == 0:
        var = '1'
        flag = True
    elif var == '1' or var == 1:
        var = '0'
        flag = False
    else:
        var = '1'
        flag = True        
    return var, flag


def binary_switch_bool_var(var):
    """
    Бинарное переключение стринговой переменной в зависимости от собственного ее значения
    Ret: (var <1 или 0>, flag <True or False>)
    Используется для переключения сортировки или еще чего-нибудь в HTML - коде, где передается в глобальном параметре request
    Category: Аналитические методы
    """
    if var == True:
        var = False
    elif var == False:
        var = True
    return var


def binary_switch_int_var(var):
    """
    Бинарное переключение по цифровой переменной в зависимости от собственного ее значения
    Ret: (var <1 или 0>, flag <True or False>)
    Используется для переключения сортировки или еще чего-нибудь в HTML - коде, где передается в глобальном параметре request
    Category: Аналитические методы
    """
    if var == None or var == 0:
        var = 1
        flag = True
    elif var == 1:
        var = 0
        flag = False
    else:
        var = 1
        flag = True        
    return var, flag



def sort(myList, reverse = False, sortNone = False):
    """
    Sorts a list that may or may not contain None.
    Special thanks to Andrew Clark and tutuDajuju for how to sort None on https://stackoverflow.com/questions/18411560/python-sort-list-with-none-at-the-end

    reverse (bool) - Determines if the list is sorted in ascending or descending order

    sortNone (bool) - Determines how None is sorted
        - If True: Will place None at the beginning of the list
        - If False: Will place None at the end of the list
        - If None: Will remove all instances of None from the list

    Example Input: sort([1, 3, 2, 5, 4, None, 7])
    Example Input: sort([1, 3, 2, 5, 4, None, 7], reverse = True)
    Example Input: sort([1, 3, 2, 5, 4, None, 7], reverse = True, sortNone = True)
    Example Input: sort([1, 3, 2, 5, 4, None, 7], sortNone = None)
    
    https://stackoverflow.com/questions/18411560/sort-list-while-pushing-none-values-to-the-end
    Category: Списки
    """

    return sorted(filter(lambda item: True if (sortNone != None) else (item != None), myList), 
        key = lambda item: (((item is None)     if (reverse) else (item is not None)) if (sortNone) else
                            ((item is not None) if (reverse) else (item is None)), item), 
        reverse = reverse)


def sort_ds_bonds_by_col(self,dsBonds, colInx, desc = False):
    """
    Сортировка двумерного массива облигаций по колонкам массива
    dsBonds - Входной массив облигаций с атрибутами
    colInx - индекс колонки в спсике второго уровня (рядов двумерного массива)
    desc - Если False, то идет сортировка по возрастанию значений поля. Если True - то по убыванию. По умолчанию - сортировка идет по возрастанию значений desc = False
    RET: dsBondsSorted - отсортированный массив
    https://stackoverflow.com/questions/20183069/how-to-sort-multidimensional-array-by-column
    and by two cols or reverse (desc ) sorting: https://stackoverflow.com/questions/2173797/how-to-sort-2d-array-by-row-in-python
    Category: Облигации
    """
    dsBondsSorted = sorted(dsBonds,key=lambda x: x[colInx], reverse = desc)
    return dsBondsSorted






# END HTML полезные функции 



# Перенесенные из funcs_general.ru проекта PRJ_01 bonds [30-01-2024 16-22]


def concatinate_two_2dim_lists_in_one_list(list1, list2):
    """  TODO: !!! Проверить правилльность работы 
    ??? Обьединяет списки и переворачивает размерность колонок и рядов
    Прим: listOfLists = [[list1], [list2]]
    """
    dsResList = [ list1[i] + list2[i] for i in range(len(list1))]
    return dsResList



# END Перенесенные из funcs_general.ru проекта PRJ_01 bonds [30-01-2024 16-22]



















