from noocube.sqlite_connection import SqliteConnection
import sqlite3


## 0. -- ОбЩИЕ КОНСТАНТЫ НАСТРОЙКИ ДЛЯ ПРИКЛАДНЫХ МОДУЛЕЙ (должны стоять в самом начале файла!)

DEBUG_ = True


# # ОБЩИЕ НАСТРОЙКИ: БД MSI
# # DB_BONDS = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/bonds.db'
DB_BONDS = '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/db/bonds.db'



# # LENOVO
# # DB_BONDS = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/bonds.db'
# DB_BONDS = '/home/lenovo/projects/P19_Bonds_Django/bonds_django_proj/db/bonds.db'

# # БД для переноса описаний компаний в новую текущую БД (что бы избежать массы интерактива. В новой БД обнулены данные по описанию компаний)
# # Импользуется одноразово, для переноса данных исторических
# DB_SOURCE_HISTOR = '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/db/bonds_200_OLD_SOURCE.db'




TB_COMP_DESCR_ARCHIVE = 'comps_descr_archive'

TB_BONDS_ARCHIVE = 'bonds_archive'

TB_BONDS_CURRENT = 'bonds_current'

TB_BONDS_CURRENT_PREV = 'bonds_current_prev'

TB_OFZ_ARCHIVE = 'ofz_archive'

TB_OFZ_CURRENT = 'ofz_current'

TB_MUNICIP_ARCHIVE = 'municip_archive'

TB_MUNICIP_CURRENT = 'municip_current'

TB_BONDS_BOUGHT = 'bonds_bought'

TB_COMPS = 'comps'

TB_COMPS_DESCR = 'comps_descr'

TB_INDEX_PACKAGES_ = 'index_packages' # OBSOLETED

TB_INDEX_PACKAGES = 'index_packages'

TB_PORTFOLIO_HISTORY_ = 'portfolio_history'

TB_ALGORIYHMS_ = 'algorithms_bonds_db'

TB_GLOBAL_A = 'global_A'

TB_COMP_DESCR = 'comps_descr'

TB_COMPS_FINANCE = 'comps_finance'

TB_BUNKRUPT_BONDS = 'bukrupt_bonds'


TB_REG_ISIN_B = 'reg_isin_B'


TB_INX_PACKAGES_BONDS = 'inx_packgs_bonds'

TB_SYS_DATA = 'sys_data'

TB_SYS_BONDS_SETTINGS = 'sys_bonds_settings'

TB_WWW_DATA_CHECKO = 'comps_descr_checko'

TB_WWW_DATA_FINPLAN = 'comps_descr_finplan'

TB_WWW_DATA_RBC = 'comps_descr_rbc'

TB_WWW_DATA_SPARK = 'comps_descr_spark'

TB_WWW_DATA_RUSBONDS = 'comps_descr_rusbonds'

TB_COMP_ANALISYS = 'comp_analisys'

TB_COMP_BONDS_ANALISYS = 'comp_bond_analisys'

TB_INTERACTIVE_DATA_ = 'interactive_data'




# # https://stackoverflow.com/questions/35368117/how-do-i-check-if-a-sqlite3-database-is-connected-in-python
# def _chk_conn(conn):
#     try:
#         conn.cursor()
#         return True
#     except Exception as ex:
#         return False
    

print (f"PR_567 --> DB_CONNECTION  exists? => {hasattr(SqliteConnection,'DB_CONNECTION')}")


DB_CONNECTION = SqliteConnection(DB_BONDS)

# Коннекшен из истоника исторических описаний компаний
# DB_CONNECTION_HISTOR = SqliteConnection(DB_SOURCE_HISTOR)

# ОБЩИЕ НАСТРОЙКИ: БД


# ОБЩИЕ НАСТРОЙКИ: СОРТИРОВКА ПО ЗАГОЛОВКАМ ТАБЛИЦЫ (ССЫЛКИ В ЗАГОЛОВКАХ)

# Колонки, подлежащие сортировке в выходной HTML-таблице
TABLE_SORT_COLS_FUNCS_ = [
    'Название', 
    'ГКД',
    'кол-во',
    'Smart-rt',
    'HIDDEN__oferta_unix',
    'Оферта до'
    
]


# Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
STANDART_FIELDS_EXCLUDING_WHEN_SORTING_ = [
    'sort_col_name',
    'sort_flag',
    'sort_asc',
    'sort_col',
    'ajax',
    # 'pkg_folder'

]


DEFAULT_SORTING_ = {
    
    'default_sort_col' : 'ГКД',
    'default_sort_dir' : False
}



SORT_SETTINGS = {
    
    'tb_sort_columns' : TABLE_SORT_COLS_FUNCS_,
    'exclude_url_args_sort' : STANDART_FIELDS_EXCLUDING_WHEN_SORTING_,
    'default_setting_sort' : DEFAULT_SORTING_
}





# END ОБЩИЕ НАСТРОЙКИ: СОРТИРОВКИ ПО ЗАГОЛОВКАМ ТАБЛИЦЫ (ССЫЛКИ В ЗАГОЛОВКАХ)



# ОБЩИЕ НАСТРОЙКИ: ШИРИНА КОЛОНОК ТАБЛИЦЫ 
# Пример:  'Название': '300px'

COLS_NAMES_FUNCS_WIDTH_ = {
    # 'Название': '300px', # Ширина колонки с названием
    # 'ИНН': '200', # Ширина колонки с классом
    # 'Категория': 2, # Ширина колонки с категорией
    # 'Файл': 3, # Ширина колонки с файлом
}

# END ОБЩИЕ НАСТРОЙКИ: ШИРИНА КОЛОНОК ТАБЛИЦЫ  




# Настройки раскрытия разделов левой навигационной панели в зависимости от названия View, которое активируется
LEFT_NAVIGATOR_ACTIVE_ = {
    
    'bonds_show' : 'Облигации', # View 'show_bonds'  активирует раскрытие раздела 'Облигации'
    'all_bonds_by_given_coupon_payment_month_show' : 'Облигации',
    
    
    'bonds_bought_general_show' : 'Portfolio', #  View активирует раскрытие раздела 'Portfolio'
    'bought_bonds_payments_matrix' : 'Portfolio', 
    'bonds_show_groupby_aggregate' : 'Portfolio', 
    'bought_bonds_payments_by_month' : 'Portfolio',
    'register_bought_lot' : 'Portfolio',
    'unregister_bought_lot' : 'Portfolio',
    'show_portfolio_bonds_which_out_in_current' : 'Portfolio',
    
    
    'index_packages_portfolio_by_month_folders' : 'Indices', 
    
    
    
    'show_inx_package' : 'Индексные пакеты',
    
    'show_inx_package_v2' : 'Индексные пакеты v2',
    'show_inx_pckgs' : 'Индексные пакеты v2',
    
    'index' : '',
    'algorithms' : ''
    
    
}



##  -- END ОбЩИЕ КОНСТАНТЫ НАСТРОЙКИ ДЛЯ ПРИКЛАДНЫХ МОДУЛЕЙ



### -- ФУНКЦИОНАЛЫ-ДЕКОРАТОРЫ



# Словарь функционалов для процедурного фрейма для модуля класса DjangoViewManager
DF_FUNCTIONAL_NICKS_ASSOC = {
    
    'assoc_titles' : 'df_assoc_titles_and_calcs_dd_through',
    'formatters' : 'df_formatting_dd_through',
    'table_codes' : 'df_table_code_dd_through',
    'sorting' : 'df_sorting_dd_through',
    'filtration' : 'df_filt_dd_through',
    'mask_delete' : 'delete_df_rows_by_column_mask_trhough',
    'paginator' : 'df_paginator_dd_through',
    
    
}



# # Словарь функционалов для процедурного фрейма для модуля класса DjangoViewManager
# DF_FUNCTIONAL_NICKS_ASSOC_THROUGH = {
    
#     'assoc_titles' : 'df_assoc_titles_and_calcs_dd',
#     'formatters' : 'df_formatting_dd',
#     'table_codes' : 'df_table_code_dd',
#     'sorting' : 'df_sorting_dd',
#     'filtration' : 'df_filt_dd',
#     'mask_delete' : 'delete_df_rows_by_column_mask',
#     'paginator' : 'df_paginator_dd',
    
    
# }



DF_FUNCTIONAL_ORDER_DEFAULT = {
        1 : 'assoc_titles', # трансформация названий колонок процедурного фрейма
        2 : 'formatters', # форматирование колонок процедурного фрейма
        3 : 'mask_delete', # удаление рядов в зависимости от колонки-маски 
        4 : 'sorting', # сортировка по колонкам таблицы на странице сайта
        5 : 'filtration', # фильтрация  процедурного фрейма
        6 : 'paginator', # пагинация процедурного фрейма
        7 : 'table_codes', # трансформация названий колонок процедурного фрейма
}


### -- END ФУНКЦИОНАЛЫ-ДЕКОРАТОРЫ








## I. -- НАСТРОЙКИ НАЗВАНИЙ КОЛОНОК В ФРЕЙМАХ
# Словарь заголовков для комплексных облигаций. 
# Прим: {..., 33 : 'HIDDEN__type', ...} - колонка не будет высвечиваться в таблице, но будет присутствовать в фрейме. При этом ее можно использовать с названием 'HIDDEN__type' в любых обработках фрейма
COLS_ASSOC_FOR_COMPLEX_BONDS_ = {   
                4 : 'Название', # Поле 'bond_name'
                1 : 'ISIN', # 'isin'   
                6 : 'Старт', # Дата размещения на бирже
                8: 'Срок', # Осталось до закрытия 
                2 : 'ИНН', # 'inn_ref'
                10 : 'ГКД' ,
                11 : 'Последний ГКД' ,        
                12 : 'Тек.цена',
                14 : 'Купон',
                18 : 'Дата купона', 
                15 : 'Частота' ,       
                19 : 'Оферта',       
                33 : 'Smart_rt',             
                34 : 'HIDDEN__type',
                35 : 'HIDDEN__bg_color'
        } 

# Колонки совокупного фрейма со смешанными облигациями (complex), сохраненная в сессии
"""
0 n
1 isin
2 inn_ref
3 last_trans
4 bond_name
5 forum
6 start_date
7 end_date
8 years_to_end
9 yield
10 annual_yield
11 last_annual_yield
12 curr_price
13 volume
14 coupon
15 frequency
16 nkd
17 durration
18 coupon_date
19 oferta
20 qualif
21 f1
22 f2
23 f3
24 f4
25 f5
26 f6
27 f7
28 f8
29 f9
30 f10
31 okpo
32 f11
33 smart_rate
34 type
35 bg_color


"""



COLS_ASSOC_FOR_BOUGHT_BONDS_ = {   
            27 : 'Название', # Поле 'bond_name'
            0 : 'ISIN', # 'isin'   ,
            2 : 'На руках',
            1 : 'Дата покупки',
            31: 'Срок', # Осталось до закрытия 
            25 : 'ИНН', # 'inn_ref'
            33 : 'ГКД' ,
            35 : 'Тек.цена',
            37 : 'Купон',
            41 : 'Дата купона', 
            38 : 'Частота' ,     
            42 : 'Оферта' ,
            54 : 'HIDDEN__type',
            55 : 'HIDDEN__bg_color'                
        } 


# Словарь соотвтетсвий для вывода сводной таблицы Матрица выплат из табл bonds_bought
COLS_ASSOC_FOR_BOUGHT_BONDS_MONTH_MATRIX_ = {   

                27: 'Название', # Краткое название облигации
                0 : 'ISIN', # 'isin'   ,
                2 : 'qn',
                # 31 : 'ГКД' ,
                21 : 'Купон',
                9 : 'Янв',
                10 : 'Февр',
                11 : 'Март',
                12 : 'Апр',
                13 : 'Май',
                14 : 'Июнь',
                15 : 'Июль',
                16 : 'Август',
                17 : 'Сент',
                18 : 'Окт',
                19 : 'Нояб',
                20 : 'Декаб',

        } 



# Словарь соотвтетсвий для сводных данных, тип 1
COLS_ASSOC_FOR_BOUGHT_BONDS_CONSOLIDATED_1_ = {   
            25 : 'Название', # Поле 'bond_name'
            0 : 'ISIN', # 'isin'   ,
            2 : 'На руках',
            1 : 'Дата покупки',
            29: 'Срок', # Осталось до закрытия 
            23 : 'ИНН', # 'inn_ref'
            31 : 'ГКД' ,
            33 : 'Тек.цена',
            35 : 'Купон',
            39 : 'Дата купона', 
            36 : 'Частота' ,   

            
        } 



## Распечатка индексированных первичных колонок обьединенного фрейма купленных облигаций, расширенных полями таблицы bonds_archive
""" 
0 isin
1 dtime_bought
2 qn
3 nkd_1
4 gen_comission
5 pdate
6 broker
7 total_cost
8 cheque_address
9 jan
10 feb
11 march
12 apr
13 may
14 june
15 july
16 aug
17 sept
18 oct
19 nov
20 dec
21 curr_coupon
22 n
23 inn_ref
24 last_trans
25 bond_name
26 forum
27 start_date
28 end_date
29 years_to_end
30 yield
31 annual_yield
32 last_annual_yield
33 curr_price
34 volume
35 coupon
36 frequency
37 nkd_2
38 durration
39 coupon_date
40 oferta
41 qualif
42 f1
43 f2
44 f3
45 f4
46 f5
47 f6
48 f7
49 f8
50 f9
51 f10
52 okpo
53 f11
54 type
55 bg_color



"""




# индексные пакеты - облмгацмм

""" 
n
1 isin
2 inn_ref
3 last_trans
4 bond_name
5 forum
6 start_date
7 end_date
8 years_to_end
9 yield
10 annual_yield
11 last_annual_yield
12 curr_price
13 volume
14 coupon
15 frequency
16 nkd
17 durration
18 coupon_date
19 oferta
20 qualif
21 f1
22 f2
23 f3
24 f4
25 f5
26 f6
27 f7
28 f8
29 f9
30 f10
31 okpo
32 f11
33 type
34 bg_color


"""




# Словарь соотвтетсвий для индексных пакетов из табл index_packages для prime View: show_inx_pckgs()
COLS_ASSOC_FOR_INDX_PACKAGES_ = {   
            0 : 'Id', # 'isin'   ,
            1 : 'Nick',
            2: 'Название', # Осталось до закрытия 
            3 : 'Описание', # 'inn_ref'
        } 



# Поля фрема для индексных пакетов из табл index_packages для prime View: show_inx_pckgs()

""" 
0 id
1 nick
2 name
3 descr
4 filt
5 raiting
6 cdate


"""



# Поля для для фрейма из функции get_united_atributes_df_of_inx_pckg_bonds_and_its_archive_extension_pbf()
# Для вывода облигаций индексного пакета со всеми расширяющими полями из других таблиц 
# Поля фрейма по запросу: 
#         sql = f"""SELECT *, SUM (bb.qn) 
        #             FROM inx_packgs_bonds AS ipb
        #             INNER JOIN
        #             bonds_archive AS ba
        #             ON ipb.bond_isin  = ba.isin 
        #             INNER JOIN
        #             bonds_bought AS bb
        #             ON ipb.bond_isin  = bb.isin 
        #             GROUP BY ipb.bond_isin
        # """





""" 
0 inx_pckg_id
1 bond_isin
2 points
3 desision
4 notes
5 analisys_date
6 analisys_date_unix
7 status
8 bond_coeff
9 n
10 isin
11 inn_ref
12 last_trans
13 bond_name
14 forum
15 start_date
16 end_date
17 years_to_end
18 yield
19 annual_yield
20 last_annual_yield
21 curr_price
22 volume
23 coupon
24 frequency
25 nkd
26 durration
27 coupon_date
28 oferta
29 qualif
30 f1
31 f2
32 f3
33 f4
34 f5
35 f6
36 f7
37 f8
38 f9
39 f10
40 okpo
41 f11
42 smart_rate
43 isin
44 dtime_bought
45 qn
46 nkd
47 gen_comission
48 pdate
49 broker
50 total_cost
51 cheque_address
52 jan
53 feb
54 march
55 apr
56 may
57 june
58 july
59 aug
60 sept
61 oct
62 nov
63 dec
64 curr_coupon
65 bought_price
66 time_reg_unix
67 inn
68 isin
69 comp_bonds_analisys
70 upd_date
71 upd_date_unix
72 cba_points
73 bond_analis_coeff
74 cba_notes
75 inn:1
76 comp_analisys
77 upd_date:1
78 upd_date_unix:1
79 ip_koeff
80 fapvdo_koeff
81 notes
82 SUM (bb.qn) as sum_qn

"""



COLS_ASSOC_FOR_INDEX_PACKAGE_BONDS_EXTENDED_ = {   
                13 : 'Название', # Поле 'bond_name'
                10 : 'ISIN', # 'isin'   
                15 : 'Старт', # Дата размещения на бирже
                17: 'Срок', # Осталось до закрытия 
                11 : 'ИНН', # 'inn_ref'
                19 : 'ГКД' ,
                # 11 : 'Последний ГКД' ,        
                21 : 'Тек.цена',
                23 : 'Купон',
                # 27 : 'Дата купона', 
                24 : 'Частота' ,       
                28 : 'Оферта до',   
                79  : 'Comp cf',
                80 :  'Fap cf',
                82 : 'кол-во', # ПРИМ: Эта колонка будет еще преобразована в Форматере, что бы выводить ообщее кол-во по данной облигации 
                73 : 'bK'
                # 33 : 'Smart_rt',             
                # 34 : 'HIDDEN__type',
                # 35 : 'HIDDEN__bg_color'
        } 



## END НАСТРОЙКИ НАЗВАНИЙ КОЛОНОК В ФРЕЙМАХ










## II. -- НАСТРОЙКИ ДЛЯ ФОРМИРВОАНИЯ КОНЕЧНОГО HTML-КОДА ВЫХОДНОЙ ТАБЛИЦЫ

# Настройки для формирования табличного кода для вывода общих облигаций 
TABLE_CODE_SET_FOR_BONDS_ = {
    
    # Полный путь к функции для получение обьекта функции через метод oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['prepareTableHtmlFunc'], byClassFilePAth = True)
    # Когда необходимая функция находится вне области видимости FunctionsGeneralClass.get_func_obj_by_its_full_name()
    'prepareTableHtmlFunc' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/local_funcs_bda.py|LocalFunctionsBda|prepare_table_html_for_bonds_t1_v5', 
    'tableStyleClasses' : 'color_table', # Классы для html-таблицы

    'tableColsWidth' : COLS_NAMES_FUNCS_WIDTH_, # Ширина колонок в таблице для каждого заголовка
    'tableSortCols' : TABLE_SORT_COLS_FUNCS_, # Колонки, подлежащие сортировке в выходной HTML-таблице
    'standartExludingSortFields' : STANDART_FIELDS_EXCLUDING_WHEN_SORTING_, # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
    # Настройки для формы в виде словаря с параметрами формы, в которую оборачивается таблица, если это необходимо. Иначе просто не прописывать этот словарь
    # Если в форме нет каких то параметров, то задать ключи с пустыми значениями. Иначе будет ошибка в декораторе 
    'form_for_table' : {
                    'id' : 'save_bonds_wp',
                    'name' : 'save_bonds_wp',
                    'action' : '/save_chosen_bonds_to_inx_pckg'
                    },
    'base_assoc_columns_dic' : COLS_ASSOC_FOR_COMPLEX_BONDS_ # Базовый словарь ассоциаций названий колонок
    
}



# Настройки для формирования табличного кода для вывода общих облигаций 
# Версия 2: Теперь для динамической функции используется такая функция, которая принимает не фрейм , а сквозной словарь декораторов, в котором содержится как фрейм, так и прочие параметры
TABLE_CODE_SET_FOR_BONDS_V2_ = {
    
    # Полный путь к функции для получение обьекта функции через метод oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['prepareTableHtmlFunc'], byClassFilePAth = True)
    # Когда необходимая функция находится вне области видимости FunctionsGeneralClass.get_func_obj_by_its_full_name()
    'prepareTableHtmlFunc' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/local_funcs_bda.py|LocalFunctionsBda|prepare_table_html_for_bonds_t1_v5', 
    'tableStyleClasses' : 'table table-condensed table-bordered table-sm', # Классы для html-таблицы

    'tableColsWidth' : COLS_NAMES_FUNCS_WIDTH_, # Ширина колонок в таблице для каждого заголовка
    'tableSortCols' : TABLE_SORT_COLS_FUNCS_, # Колонки, подлежащие сортировке в выходной HTML-таблице
    'standartExludingSortFields' : STANDART_FIELDS_EXCLUDING_WHEN_SORTING_, # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
    # Настройки для формы в виде словаря с параметрами формы, в которую оборачивается таблица, если это необходимо. Иначе просто не прописывать этот словарь
    # Если в форме нет каких то параметров, то задать ключи с пустыми значениями. Иначе будет ошибка в декораторе 
    'form_for_table' : {
                    'id' : 'save_bonds_wp',
                    'name' : 'save_bonds_wp',
                    'action' : '/save_chosen_bonds_to_inx_pckg'
                    },
    'base_assoc_columns_dic' : COLS_ASSOC_FOR_COMPLEX_BONDS_ # Базовый словарь ассоциаций названий колонок
    
}



# Настройки для формирования табличного кода для вывода приобретенных облигаций для View
TABLE_CODE_SET_FOR_BONDS_BOUGHT_ = {
    # НА ОСНОВЕ АССОЦИАЦИЙ КОЛОНОК: COLS_ASSOC_FOR_BOUGHT_BONDS_
    # Полный путь к функции для получение обьекта функции через метод oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['prepareTableHtmlFunc'], byClassFilePAth = True)
    # Когда необходимая функция находится вне области видимости FunctionsGeneralClass.get_func_obj_by_its_full_name()
    'prepareTableHtmlFunc' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/local_funcs_bda.py|LocalFunctionsBda|prepare_table_html_for_bonds_t1_v5', 
    'tableStyleClasses' : 'table table-condensed table-bordered table-sm', # Классы для html-таблицы

    'tableColsWidth' : COLS_NAMES_FUNCS_WIDTH_, # Ширина колонок в таблице для каждого заголовка
    'tableSortCols' : TABLE_SORT_COLS_FUNCS_, # Колонки, подлежащие сортировке в выходной HTML-таблице
    'standartExludingSortFields' : STANDART_FIELDS_EXCLUDING_WHEN_SORTING_, # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
    # Настройки для формы в виде словаря с параметрами формы, в которую оборачивается таблица, если это необходимо. Иначе просто не прописывать этот словарь
    'form_for_table' : {
                    'id' : 'form_bonds_bought',
                    'name' : '',
                    'action' : '/register_sold_bought'
                    },
    'base_assoc_columns_dic' : COLS_ASSOC_FOR_BOUGHT_BONDS_ # Базовый словарь ассоциаций названий колонок
}




# Настройки для помесячной матрицы выплат по приобретенным облигациям
# ПРИМ: ключ 'addedSummaryRows' - служит для вставки дополнительных рядов в конце таблицы. Это могут быть итоговые или прочие вспомогательные данные для таблицы
TABLE_CODE_SET_FOR_BONDS_PAYMENT_MATRIX_ = {
    
    # Полный путь к функции для получение обьекта функции через метод oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['prepareTableHtmlFunc'], byClassFilePAth = True)
    # Когда необходимая функция находится вне области видимости FunctionsGeneralClass.get_func_obj_by_its_full_name()
    'prepareTableHtmlFunc' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/local_funcs_bda.py|LocalFunctionsBda|prepare_table_html_for_month_payment_matrix', 
    # Вставка дополнительных рядов в таблицу, а именно итоговый суммарный доход по купонам помесячно и общий доход в целом за минусом 13% налога на доход. А так же ссылки на месяцы для фильтров по ним
    'addedSpecialRows' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/local_funcs_bda.py|LocalFunctionsBda|add_summary_rows_to_month_pay_matrix', 
    'tableStyleClasses' : 'table table-condensed table-striped table-bordered table-sm', # Классы для html-таблицы

    'tableColsWidth' : COLS_NAMES_FUNCS_WIDTH_, # Ширина колонок в таблице для каждого заголовка
    'tableSortCols' : TABLE_SORT_COLS_FUNCS_, # Колонки, подлежащие сортировке в выходной HTML-таблице
    'standartExludingSortFields' : STANDART_FIELDS_EXCLUDING_WHEN_SORTING_, # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
    # Настройки для формы в виде словаря с параметрами формы, в которую оборачивается таблица, если это необходимо. Иначе просто не прописывать этот словарь
    # Если в форме нет каких то параметров, то задать ключи с пустыми значениями. Иначе будет ошибка в декораторе 
    'form_for_table' : {
                    'id' : 'save_bonds_wp',
                    'name' : 'save_bonds_wp',
                    'action' : '/save_chosen_bonds_to_inx_pckg'
                    },
    'base_assoc_columns_dic' : COLS_ASSOC_FOR_BOUGHT_BONDS_MONTH_MATRIX_ # Базовый словарь ассоциаций названий колонок
    
}




# Настройки для формирования табличного кода для вывода приобретенных облигаций для View
# Версия 2: Теперь для динамической функции используется такая функция, которая принимает не фрейм , а сквозной словарь декораторов, в котором содержится как фрейм, так и прочие параметры
TABLE_CODE_SET_FOR_BONDS_BOUGHT_V2 = {
    # НА ОСНОВЕ АССОЦИАЦИЙ КОЛОНОК: COLS_ASSOC_FOR_BOUGHT_BONDS_
    # Полный путь к функции для получение обьекта функции через метод oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['prepareTableHtmlFunc'], byClassFilePAth = True)
    # Когда необходимая функция находится вне области видимости FunctionsGeneralClass.get_func_obj_by_its_full_name()
    'prepareTableHtmlFunc' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/local_funcs_bda.py|LocalFunctionsBda|prepare_table_html_for_bonds_t1_v5', 
    'tableStyleClasses' : 'table table-condensed table-bordered table-sm', # Классы для html-таблицы

    'tableColsWidth' : COLS_NAMES_FUNCS_WIDTH_, # Ширина колонок в таблице для каждого заголовка
    'tableSortCols' : TABLE_SORT_COLS_FUNCS_, # Колонки, подлежащие сортировке в выходной HTML-таблице
    'standartExludingSortFields' : STANDART_FIELDS_EXCLUDING_WHEN_SORTING_, # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
    # Настройки для формы в виде словаря с параметрами формы, в которую оборачивается таблица, если это необходимо. Иначе просто не прописывать этот словарь
    'form_for_table' : {
                    'id' : 'form_bonds_bought',
                    'name' : '',
                    'action' : '/register_sold_bought'
                    },
    'base_assoc_columns_dic' : COLS_ASSOC_FOR_BOUGHT_BONDS_ # Базовый словарь ассоциаций названий колонок
}






# Настройки для формирования табличного кода для вывода для сводных данных, тип 1
# Версия 2: Теперь для динамической функции используется такая функция, которая принимает не фрейм , а сквозной словарь декораторов, в котором содержится как фрейм, так и прочие параметры
TABLE_CODE_SET_FOR_BONDS_BOUGHT_CONSOLIDATED_T1_V2_ = {
    # НА ОСНОВЕ АССОЦИАЦИЙ КОЛОНОК: COLS_ASSOC_FOR_BOUGHT_BONDS_
    # Полный путь к функции для получение обьекта функции через метод oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['prepareTableHtmlFunc'], byClassFilePAth = True)
    # Когда необходимая функция находится вне области видимости FunctionsGeneralClass.get_func_obj_by_its_full_name()
    'prepareTableHtmlFunc' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/local_funcs_bda.py|LocalFunctionsBda|prepare_table_html_for_bonds_t1_v5', 
    'tableStyleClasses' : 'table table-condensed table-bordered table-sm', # Классы для html-таблицы

    'tableColsWidth' : COLS_NAMES_FUNCS_WIDTH_, # Ширина колонок в таблице для каждого заголовка
    'tableSortCols' : TABLE_SORT_COLS_FUNCS_, # Колонки, подлежащие сортировке в выходной HTML-таблице
    'standartExludingSortFields' : STANDART_FIELDS_EXCLUDING_WHEN_SORTING_, # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
    # Настройки для формы в виде словаря с параметрами формы, в которую оборачивается таблица, если это необходимо. Иначе просто не прописывать этот словарь
    'form_for_table' : {
                    'id' : 'form_bonds_bought',
                    'name' : '',
                    'action' : '/register_sold_bought'
                    },
    'base_assoc_columns_dic' : COLS_ASSOC_FOR_BOUGHT_BONDS_CONSOLIDATED_1_ # Базовый словарь ассоциаций названий колонок
}



# Настройки для формирования табличного кода для вывода индексных пакетов из табл index_packages
TABLE_CODE_SET_FOR_INDX_PACKAGES_ = {
    
    # Полный путь к функции для получение обьекта функции через метод oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['prepareTableHtmlFunc'], byClassFilePAth = True)
    # Когда необходимая функция находится вне области видимости FunctionsGeneralClass.get_func_obj_by_its_full_name()
    'prepareTableHtmlFunc' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/local_funcs_bda.py|LocalFunctionsBda|prepare_table_html_for_bonds_t1_v5', 
    'tableStyleClasses' : 'color_table', # Классы для html-таблицы

    # 'tableColsWidth' : COLS_NAMES_FUNCS_WIDTH_, # Ширина колонок в таблице для каждого заголовка
    'tableSortCols' : TABLE_SORT_COLS_FUNCS_, # Колонки, подлежащие сортировке в выходной HTML-таблице
    'standartExludingSortFields' : STANDART_FIELDS_EXCLUDING_WHEN_SORTING_, # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
    # # Настройки для формы в виде словаря с параметрами формы, в которую оборачивается таблица, если это необходимо. Иначе просто не прописывать этот словарь
    # # Если в форме нет каких то параметров, то задать ключи с пустыми значениями. Иначе будет ошибка в декораторе 
    # 'form_for_table' : {
    #                 'id' : 'save_bonds_wp',
    #                 'name' : 'save_bonds_wp',
    #                 'action' : '/save_chosen_bonds_to_inx_pckg'
    #                 },
    'base_assoc_columns_dic' : COLS_ASSOC_FOR_INDX_PACKAGES_ # Базовый словарь ассоциаций названий колонок
    
}




# Настройки для формирования табличного кода для вывода облигаций в игндексных пакетах
TABLE_CODE_SET_FOR_BONDS_FROM_INDX_PACKAGE_TYPE1_ = {
    
    # Полный путь к функции для получение обьекта функции через метод oFunc = FunctionsGeneralClass.get_func_obj_by_its_full_name (tkwargs['prepareTableHtmlFunc'], byClassFilePAth = True)
    # Когда необходимая функция находится вне области видимости FunctionsGeneralClass.get_func_obj_by_its_full_name()
    'prepareTableHtmlFunc' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/local_funcs_bda.py|LocalFunctionsBda|prepare_table_html_for_bonds_t1_v5', 
    'tableStyleClasses' : 'color_table', # Классы для html-таблицы

    'tableColsWidth' : COLS_NAMES_FUNCS_WIDTH_, # Ширина колонок в таблице для каждого заголовка
    'tableSortCols' : TABLE_SORT_COLS_FUNCS_, # Колонки, подлежащие сортировке в выходной HTML-таблице
    'standartExludingSortFields' : STANDART_FIELDS_EXCLUDING_WHEN_SORTING_, # Стандартные url-поля, которые исключаются при сортировке при формировании константной url-строки
    # Настройки для формы в виде словаря с параметрами формы, в которую оборачивается таблица, если это необходимо. Иначе просто не прописывать этот словарь
    # Если в форме нет каких то параметров, то задать ключи с пустыми значениями. Иначе будет ошибка в декораторе 
    'form_for_table' : {
                    'id' : 'save_bonds_wp',
                    'name' : 'save_bonds_wp',
                    'action' : '/save_chosen_bonds_to_inx_pckg'
                    },
    'base_assoc_columns_dic' : COLS_ASSOC_FOR_INDEX_PACKAGE_BONDS_EXTENDED_ # Базовый словарь ассоциаций названий колонок
    
}




## END НАСТРОЙКИ ДЛЯ ФОРМИРВОАНИЯ КОНЕЧНОГО HTML-КОДА ВЫХОДНОЙ ТАБЛИЦЫ





## III. -- ФОРМАТИРОВАНИЕ КОЛОНОК 


# Форматирование колонок в фрейме вывода облигаций. Первоначально для View: show_bonds
# TODO: С переходом на функционалы с аргументами в виде рядов, ключ словаря перестает иметь значение. ПРидумать эффективное использование ключа словаря или перейти на список
# Калькулирование существующих или новых колонок. Ключ - название колнки-аргумента фрейма поступающей на вход функции-форматера
# Если одно ключевое название колонки (без дополнения через разделитель '|'), значит форматируется или декорируется сама эта колонка
# Если есть второе имя через | то это значит заводить новую колонку с резултатом в нее. А аргументом служит первое название колонки
#'Старт|Год:3'  - индекс положения новой создаваемой колонки определяется ':3' в конце названия новой колонки. Если отстутствует, то колонка остается в конце фрейма
# Если в названии колонки приутствует '__NOOTITLE' маркер, то заголовок не высвечивается в таблице
COLS_CALC_FORMATERS_FOR_BONDS_ = {
    # формирование месяца следующей выплаты купонов облигаций, по отношению к дате текущего считывания облигаций (показывает вектор месяцев-выплат по облигациям в купе с частотой выплат)
    'Дата купона|Мес.выплат:10' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_column_pay_month_to_bonds_row_arg',
    # Колонка checkboxes в начале рядов в таблице облигаций
    'ISIN|ch__NOTITLE:0' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_isin_checkboxes_to_bonds_row_arg',
    # Колонка иконок открытия popover  окон для сохранения облигации в одну из таблиц пакетов -индексов (пакетов , формирующих какой-то свой Индекс облигаций)
    'ISIN|Ix' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_packages_popover_to_bonds_row_arg',

    # Цветовая дифференциация (или цветовое форматирование колонки 'HIDDEN__bg_color') на предмет наличия облигации в разных индексных пакетах
    # TODO: Должна быть возможность добавлять в этот словарь такой цветовой форматер динамически в заваисимости от выбора пользователя показывать или нет выделение цветом по индексному пакету
    # При наличии нескольких цветовых дифференциаторов-форматеров значение имеет последовательность. Каждый последующий дифференциатор имеет приемущество перед предыдущими
    'HIDDEN__bg_color' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|color_diff_of_inx_packages_bonds',

    # Колонка с иконкой для открытия информационной страницы по облигациям (ПРИМ: Перед форматированием ISIN, последовательность играет роль)
    'ISIN|Inf' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_icon_bond_infor_column',


    # Колонка с иконкой для открытия страницы регистрации покупки выбранной облигации
    'ISIN|Reg' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_icon_bond_lot_register_column',



    # Ник-нейм облигации - открывает инф страницу компании (ПРИМ: Перед форматированием ISIN, последовательность играет роль)
    'Название' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|format_bond_nick_name_col',


    # UNIX date старта облигации
    'Частота|HIDDEN__Старт' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_col_start_unix_hidden',



    # оформить колонку ISIN в ссылку для открытия инф страницы
    'ISIN' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|format_isin_as_smart_link',



}


#  ПРИМ: Если мы хотим отформатировать последовательно одну и ту же колонку, то к ключу в форматтере необходимо добавить конечный маркер 
#  типа <Название колонки фрейма>'_&&01' (обязательно 5 знаков, включающих '&&')(то есть может быть только 100 одинаковых изменений по одному полю в форматтере) 
COLS_CALC_FORMATERS_FOR_BONDS_IN_INX_PCKG_ = {
    # формирование месяца следующей выплаты купонов облигаций, по отношению к дате текущего считывания облигаций (показывает вектор месяцев-выплат по облигациям в купе с частотой выплат)
    # 'Дата купона|Мес.выплат:10' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_column_pay_month_to_bonds_row_arg',
    # Колонка checkboxes в начале рядов в таблице облигаций
    'ISIN|ch__NOTITLE:0' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_isin_checkboxes_to_bonds_row_arg',
    
    # Создать новую колонку для цветовой дифференциации
    'ISIN|HIDDEN__bg_color' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_empty_col',

        ## 2. Важная последовательность форматирования колонок
    # Цветовая дифференциация (или цветовое форматирование колонки 'HIDDEN__bg_color') на предмет наличия облигации в разных индексных пакетах
    # TODO: Должна быть возможность добавлять в этот словарь такой цветовой флормастер динамически в заваисимости от выбора пользователя показывать или нет выделение цветом по индексному пакету
    # При наличии нескольких цветовых дифференциаторов-форматеров значение имеет последовательность. Каждый последующий дифференциатор имеет приемущество перед предыдущими
    'HIDDEN__bg_color' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|color_diff_bonds_inx_packages_in_portfolio',

        ## CONTINUE 2. Важная последовательность форматирования колонок



    # Колонка иконок открытия popover  окон для сохранения облигации в одну из таблиц пакетов -индексов (пакетов , формирующих какой-то свой Индекс облигаций)
    'ISIN|Ix' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_change_bond_inx_package_popover',


    # Колонка иконок открытия popover  окон для сохранения облигации в одну из таблиц пакетов -индексов (пакетов , формирующих какой-то свой Индекс облигаций)
    'ISIN|Del' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_popover_of_delete_bond_from_inx_packg',

    # Колонка с иконкой для открытия информационной страницы по облигациям (ПРИМ: !!! До форматирования ISIN, последовательность играет роль!!!)
    'ISIN|Inf' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_icon_bond_infor_column',

    # Колонка с иконкой для фильтрации множестчвенных облигаций по одному и тому же эмитенту
    'ISIN|Dbl' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_icon_inx_pckg_filter_multiple_bonds',

    # Колонка с иконкой для открытия страницы регистрации покупки выбранной облигации
    'ISIN|Reg' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_icon_bond_lot_register_column',


    # Ник-нейм облигации - открывает инф страницу компании (ПРИМ: Перед форматированием ISIN, последовательность играет роль)
    'Название' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|format_bond_nick_name_col',


    # Добавить колонку с типом оферты, если она есть у облигации
    'ISIN|Тип офрт:11' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_offert_type_col',


    # UNIX date старта облигации
    'Оферта до|HIDDEN__oferta_unix' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_col_oferta_unix_hidden',



        ## 1. Важная последовательность форматирования колонок
    # Колонка с иконкой для открытия информационной страницы по облигациям (ПРИМ: !!! До форматирования ISIN, последовательность играет роль!!!)
    'кол-во' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|inx_package_qn_column',
    # добавить колонку: Норма кол-ва облигаций в соотвтетсвии с индексным коэффициентом по компании и установочного кол-ва облигаций в лоте для индексных пакетов
    '`Comp cf`|QN:16' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_ip_bond_qn_norm_by_comp_coeff_and_bonds_lot_col',
    # Добавить колонку: Дельта разницы между нормой кол-ва облигаций для одного эмитента и суммарного кол-ва  облигаций этого эмитента в портфолио 
    # (TODO: после ввести еще коэфф расчета по текущему номиналу облигации, который может уменьшится и соотвтетсвенно меняется сумма инвестиций по этому эмитенту)
    'QN|Delta:18' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_delta_between_bonds_qn_norm_and_portf_col',
    
    # Добавить колонку с коэфф риска облигации
    'bond_analis_coeff|bQN:19' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_bond_quantity_norm_based_on_its_risk_coeff_col',

    # Добавить колонку с Дельта-разницей между кол-вом облигаций в портфолио и частной нормой по облигации на основе собственного риска облигаций
    'кол-во|bD:21' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_bond_delta_based_on_bond_norm_col',

        
        ## END 1. Важная последовательность форматирования колонок

# The above code is adding a column with the offer type to a bond if it exists.




    # Цветовая дифференциация: Выделить отдельным цветом ряды с позитивным значением дельта в колонке 'Delta'
    # TODO: Должна быть возможность добавлять в этот словарь такой цветовой флормастер динамически в заваисимости от выбора пользователя показывать или нет выделение цветом по индексному пакету
    # При наличии нескольких цветовых дифференциаторов-форматеров значение имеет последовательность. Каждый последующий дифференциатор имеет приемущество перед предыдущими
    'HIDDEN__bg_color_&&01' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|color_diff_bonds_with_positive_delta',




    # Цветовая дифференциация: Выделить отдельным цветом ряды с облигациями, в которых нет анализа эмитентов и коэфф риска 	Comp cf = None (но не для Гос-эмитентов типа ОФЗ или Муницип)
    # TODO: Должна быть возможность добавлять в этот словарь такой цветовой флормастер динамически в заваисимости от выбора пользователя показывать или нет выделение цветом по индексному пакету
    # При наличии нескольких цветовых дифференциаторов-форматеров значение имеет последовательность. Каждый последующий дифференциатор имеет приемущество перед предыдущими
    'HIDDEN__bg_color_&&02' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|color_diff_bonds_with_no_coeff_emitent_risk_not_including_gos_type',




    'ISIN' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|format_isin_as_smart_link',

    
    
}



# Форматирование колонок в таблице вывода приобретенных облигаций (первоначально в View : bonds_bought_general)
# Последовательность форматеров важна, если последующие форматные поля я вляются зависимыми от предыдущих. Или наоборот, зависят от неизмененных пвраметрах поля
COLS_CALC_FORMATERS_FOR_BONDS_BOUGHT = {
    
    # Колонка radio-batton, для индивидуального выбора купленного слота облигаций , для дальнейших возможных процедур , связазнных с этим слотом (например, архивация слота при его продаже)
    'ISIN|ch__NOTITLE:0' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_isin_radiobaton_to_bought_bonds',

    # Колонка иконок открытия popover  окон для сохранения облигации в одну из таблиц пакетов -индексов (пакетов , формирующих какой-то свой Индекс облигаций)
    'ISIN|Ix' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_packages_popover_to_bonds_row_arg',


    # Колонка иконок открытия popover  окон для сохранения облигации в одну из таблиц пакетов -индексов (пакетов , формирующих какой-то свой Индекс облигаций)
    'ISIN|Sell' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_sell_bond_lot_icon',


    # Цветовая дифференциация (или цветовое форматирование колонки 'HIDDEN__bg_color') на предмет наличия облигации в разных индексных пакетах
    # TODO: Должна быть возможность добавлять в этот словарь такой цветовой форматер динамически в заваисимости от выбора пользователя показывать или нет выделение цветом по индексному пакету
    # При наличии нескольких цветовых дифференциаторов-форматеров значение имеет последовательность. Каждый последующий дифференциатор имеет приемущество перед предыдущими
    'HIDDEN__bg_color' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|color_diff_of_inx_packages_bonds',


    'Дата покупки' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|format_date_purchase_in_bought_bonds',

    # Колонка с иконкой для открытия информационной страницы по облигациям (ПРИМ: !!! До форматирования ISIN, последовательность играет роль!!!)
    'ISIN|Inf' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_icon_bond_infor_column',


    # Колонка с иконкой для открытия страницы регистрации покупки выбранной облигации
    'ISIN|Reg' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_icon_bond_lot_register_column',




    # Ник-нейм облигации - открывает инф страницу компании (ПРИМ: Перед форматированием ISIN, последовательность играет роль)
    'Название' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|format_bond_nick_name_col',


    'ISIN' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|format_isin_as_smart_link',





}



COLS_CALC_FORMATERS_FOR_BONDS_COUPON_GIVEN_MONTH = {
    
    
    # формирование месяца следующей выплаты купонов облигаций, по отношению к дате текущего считывания облигаций (показывает вектор месяцев-выплат по облигациям в купе с частотой выплат)
    'Дата купона|Мес.выплат:10' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_column_pay_month_to_bonds_with_row_arg',

    # Создание колонки-маски как результат анализа : подпадает ли данная облигация под выплаты купонов под заданный месяц. Если подпадает, то True, Иначе - False
    'Частота|HIDDEN__if_cmonth' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|set_mask_col_for_given_coupon_month',
}



## END ФОРМАТИРОВАНИЕ  КОЛОНОК 





## IV. -- ДЕКОРИРОВАНИЕ КОЛОНОК ДЛЯ ВЫХОДНОЙ ТАБЛИЦЫ

# Обертки для форматирования колонок на выходе для таблицы (от форматирования отличается тем, что нет никакого процессинга над фреймом после декорирования. Используется обертывание
# уже конечного, обработанного фрейма. Декорируются колонки фрейма уже чисто для вывода данных в таблице визуальных)
COLS_DECOR_FORMATERS_FUNCS_ = {
    # обертка для значений названий функций (прибавление круглых скобок в конце и жирный шрифт) для класса FuncsAnalyzerManager, который не виден из noocube
    'Название' : '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/funcs_analyzer_manager.py|FuncsAnalyzerManager|func_name_wrap_indexed', 
    # Обрезание полного пути к файлу до последних двух доменов и реакция на нажатие - открытие файла в VS CODE
    'Файл' : '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/funcs_analyzer_manager.py|FuncsAnalyzerManager|file_column_df_funcs_wrap', 
    # Раскраска поля Класс в синий цвет
    'Класс' : '/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/funcs_analyzer/classes_fa/funcs_analyzer_manager.py|FuncsAnalyzerManager|class_column_df_funcs_wrap', 

}


## END ДЕКОРИРОВАНИЕ КОЛОНОК ДЛЯ ВЫХОДНЙО ТАБЛИЦЫ



## V. -- НАСТРОЙКИ ПАГИНАТОРА

# Настройки ддля пагинатора базовые
PAGIN_GEN_SET_ = {
    'pagesRowMax' : 5, # максимальное число показа нумерации страниц в ряду
    'dsRowsQnOnPage' : 40 # число записей из входного массива, показываемых на одной странице  
}

# Список url-аргументов, которые должны быть исключены по умолчанию при формировании ссылки для пагинации 
GEN_EXCLUDE_LLIST_FOR_PAGINATOR_ = [
    
    'pg',   
    'sort_flag',
    'sort_col_name',
    'ajax',
    # 'pkg_folder'
]

PAGINATOR_SET_FUNCS_ = {
    
    'paginGenSet' : PAGIN_GEN_SET_,
    'genExcludeListFoPagin' : GEN_EXCLUDE_LLIST_FOR_PAGINATOR_,
}






## END НАСТРОЙКИ ПАГИНАТОРА



## VI. -- ДЕОРАТОР ФИЛЬТРАЦИИ ФРЕЙМА

# Если в формуле присутствует локальная переменная, начинающаяся с @<url-arg == key in filter formula>,  то замещаем эту локальную переменную
# с именем равным ключу в словаре фильтров, а так же равной url-аргументу в request ( так как именно этот фактор связывает нахождение формулы в словаре фильтров: )
# С учетом декораторов значений колонок лучше использовать не == , а типа contain ... 'Класс.str.contains("@class_name")'
# Мульти-фильтр задается таким образом:
# 'srch_str' : 'Название.str.contains("@srch_str", case=False) | ISIN.str.contains("@srch_str", case=False)'  (Используется '&' или '|' )
FILTERS_EXPR_TEMPLATES_FOR_FUNCS_BY_TYPE_V2_ = {

    'bonds_type'  : 'HIDDEN__type.str.contains("@bonds_type", case=False)', 
    'srch_str' : 'Название.str.contains("@srch_str", case=False) | ISIN.str.contains("@srch_str", case=False) | ИНН.str.contains("@srch_str", case=False) | Smart_rt.str.contains("@srch_str", case=False)',
    'flex_filter' : '@flex_filter',
    
}


## END ДЕОРАТОР ФИЛЬТРАЦИИ ФРЕЙМА




## VII. -- НАСТРОЙКИ ЦВЕТОВЫХ ДИФФЕРЕНЦИАТОРОВ

# Настрйока цветовой дифференциации для выделения облигаций , находящихся в индексных пакетах. 
# ПРИМ:  Значениями в словаре служат названия классов для выделения цветом каждого отдельного индексного пакета
INX_PACKAGES_COLOR_DIFF = {
    
    # 'IxMaxSafety' : '#EADDCA',
    'Пакет A' : 'inx_package_row_css_6',
    'Пакет AB' : 'inx_package_row_css_5',
    'Пакет AC' : 'inx_package_row_css_7',
    'Пакет OFERT' : 'inx_package_row_css_8',
    'Пакет LOW_GKD' : 'inx_package_row_css_9',
    'Пакет POTENTIAL' : 'inx_package_row_css_10',
    'Пакет NEGATIVE' : 'inx_package_row_css_11',
    'Пакет OBSERVE' : 'inx_package_row_css_12',
    'Пакет CALL_OFFERT' : 'inx_package_row_css_13',
    
    
}





## END VII. НАСТРОЙКИ ЦВЕТОВЫХ ДИФФЕРЕНЦИАТОРОВ



########################################## ПРОЕКТНЫЕ ПРИКЛАДНЫЕ НАСТРОЙКИ  ############################

#### VIII. НАСТРОЙКИ ДЛЯ РАБОТЫ С ОБЛИГАЦИЯМИ


# Словарь ассоциаций между названяими интерактивных ресурсов и колонками в таблице comps_descr с описанием компаний, берущихся с этих ресурсов , соотвтетсвенно
DIC_WWW_RESOURCES_TO_COMP_DESCR_COLUMNS = {
    
    'CHECKO' : 'descr1',
    'FINPLAN' : 'descr2',
    'RBC' : 'descr3',
    'SPARK' : 'descr4',
    'RUSBONDS' : 'descr5',
}


# Обратный словарь ассоц между названиями колонок с описанием компании в таблице comps_descr и названиями www-ресурсов им соотвтетсвующих
DIC_COMP_DESCR_COLUMNS_TO_WWW_RESOURCES = {
    
    'descr1' : 'CHECKO',
    'descr2' : 'FINPLAN',
    'descr3' : 'RBC',
    'descr4' : 'SPARK',
    'descr5' : 'RUSBONDS',
    
}



# Обратный словарь ассоц между названиями таблиц с данынми от www-ресурсов и названиями www-ресурсов им соотвтетсвующих
DIC_ASSOC_COMP_DESCR_TABLES_AND_WWW_RESOURCES_NICKS = {
    
    'comps_descr_checko' : 'CHECKO',
    'comps_descr_finplan' : 'FINPLAN',
    'comps_descr_rbc' : 'RBC',
    'comps_descr_spark' : 'SPARK',
    'comps_descr_rusbonds' : 'RUSBONDS',
    
}


# Поля с описаниями компаний в таблице comps_descr

COMPS_DESCR_FIELDS_FOR_TEXT= [
    
    'descr1',
    'descr2',
    'descr3',
    'descr4',
    'descr5',
    
]


# Поля с ссылками на описания компаний в таблице comps_descr

COMPS_DESCR_FIELDS_FOR_LINKS= [
    
    'link1',
    'link2',
    'link3',
    'link4',
    'link5',
    
]



# Обратный словарь ассоц между названиями колонок с  ссылками в таблице comps_descr и названиями www-ресурсов им соотвтетсвующих
DIC_COMP_DESCR_COLUMNS_FOR_LINKS_TO_WWW_RESOURCES = {
    
    'link1' : 'CHECKO',
    'link2' : 'FINPLAN',
    'link3' : 'RBC',
    'link4' : 'SPARK',
    'link5' : 'RUSBONDS',
    
}



#### END VIII. НАСТРОЙКИ ДЛЯ РАБОТЫ С ОБЛИГАЦИЯМИ

########################################## END ПРОЕКТНЫЕ ПРИКЛАДНЫЕ НАСТРОЙКИ  ############################




#### Форматы копирования в буфер

DIC_TEMPLATE_FILES = {
    
    # Текстовый файл формата копирования в буфер данных по облигации и эмитента из информационной страницы облигации-компании 
    # View: show_bond_inf_page_v2 | template: ~ /home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/templates/comp_inf_page_v2.html
    'comp_analithics' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/templates/copy_buffer_formats/comp_analithics_format.txt',
    'bond_analithics' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/templates/copy_buffer_formats/bond_analithics_format.txt',

    'bond_analisys_temlate1' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/templates/html_formats/bond_analisys_temlate1.html',
    'comp_analisys_temlate1' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/templates/html_formats/comp_analisys_temlate1.html',
}




#### END Форматы копирования в буфер




# #### Форматы вывода индексных пакетов 

# Обертки для форматирования колонок на выходе для таблицы (от форматирования отличается тем, что нет никакого процессинга над фреймом после декорирования. Используется обертывание
# уже конечного, обработанного фрейма. Декорируются колонки фрейма уже чисто для вывода данных в таблице визуальных)
COLS_FORMATERS_FOR_INDEX_PACKAGES = {

    # Колонка с иконкой для редактирования индексного пакета
    'Id|Edit' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_icon_edit_inx_pckg',
    'Id|Del' : '/home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app/local_classes/columns_formatting_bda.py|ColumnsFormattingBda|add_icon_delete_inx_pckg',


}


# #### END Форматы вывода индексных пакетов 





#### IX. НАСТРОЙКИ НАЗВАНИЙ СТРАНИЦ САЙТА


SITE_PAGES_TITLES = {
    
    'bonds_show_КОРП' : 'Облигации корпоративные',
    'bonds_show_ОФЗ' : 'Облигации ОФЗ',
    'bonds_show_МУНИЦ' : 'Облигации мнуиципальные',
    'bonds_show' : 'Облигации комплексные',
    'bought_bonds_payments_matrix' : 'Матрица распределения купонных доходов',
    'bonds_bought_general_show' : 'Индивидуальные лоты портфолио',
    'show_inx_package_v2_Пакет AB' : 'Индексный пакет AB',
    'show_inx_package_v2_Пакет A' : 'Индексный пакет A',
    'show_inx_package_v2_Пакет AC' : 'Индексный пакет AC',
    'show_inx_package_v2_Пакет OFERT' : 'Индексный пакет OFERT',
    'show_inx_package_v2_Пакет LOW_GKD' : 'Индексный пакет LOW_GKD',
    'show_inx_package_v2_Пакет POTENTIAL' : 'Индексный пакет POTENTIAL',
    'show_inx_package_v2_Пакет NEGATIVE' : 'Индексный пакет NEGATIVE',
    'bonds_show_groupby_aggregate' : 'Сводные данные по Portfolio',
    # 'show_inx_pckgs' : 'Управление индексными пакетами',
    
    
    
}






#### END IX. НАСТРОЙКИ НАЗВАНИЙ СТРАНИЦ САЙТА






