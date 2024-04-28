# -- GENERAL ALGORITHM SETTINGS -----------
# /media/lenovo/Transcend/ARCHIVE_CURRENT_MAIN_!!!_START_FROM_1204_2023/projects/1_Proj_Obligations_Analitic_Base/bonds/algorithms_settings.py 
# Корпоративные облигации. ИСПОЛЬЗУЕТСЯ ДЛЯ ТЕСТИРОВАНИЯ БЛОКОВ
# MOEX_INI_LINK = 'https://www.moex.com/ru/marketdata/#/mode=groups&group=3&collection=189&boardgroup=58&data_type=current&category=main'
MOEX_INI_LINK = 'https://www.moex.com/ru/issue.aspx?board=TQCB&code=RU000A102LF6&utm_source=www.moex.com&utm_term=%D0%BF%D0%B8%D0%BE%D0%BD%D0%BB%D0%B8%D0%B7%D0%B1%D0%BF4'

# Link to corporate bonds in smart-lab
SML_CBONDS_LK = 'https://smart-lab.ru/q/bonds/'

# ini link to rusbonds.ru 
RUSBONDS_INI_LINK = 'https://rusbonds.ru/filters/bonds/new'

# SPARK_OPKO_LK = 'https://spark-interfax.ru/quick-search/okpo-po-inn' # Поиск ИНН, описания по ОПКО
SPARK_OPKO_LK = 'https://spark-interfax.ru/quick-search' # Поиск ИНН, описания по ОПКО


# -- END GENERAL ALGORITHM SETTINGS -----------


# -- MAIN ALGORITHM settings  ----
# Настройки главного алгорима бота

FIRST_STEP = False # 1. Считывание данных по корп.бондам из https://smart-lab.ru/q/bonds/ в эксел Либре

SECOND_STEP = False # 2. Сортировка по ГКД в убывающем порядке

THIRD_STEP = False # 3. Подключение к МБ

FORTH_STEP = False # 4 Подключение к существующему документу

FIFTH_STEP = False # 5. Вставка ОКПО  компаний, выпустивших акции. Исходник: БАЗОВЫЕ ДАННЫЕ ПО КОРПОРАТИВАМ_modif_005.ods

SIX_STEP = False # 6. Поиск ИНН, описания по ОПКО

SEVEN_STEP = False # 7. Поиск и вставка в таблицу интерактивныъ финансовых показателей и ссылки на страницу компании на сайте checko.ru

EIGHT_STEP = False # 8. Алгоритм считывания ссылок на компании и описания компаний эмитентов на сайте fin-plan.ru

NINE_STEP = False # 9. Вставка данных по компаниям из заполненной предыдущими алгоритмами экселовской сводной таблицы корпоративных облигаций 'БАЗА_ОБЛИГАЦИИ_modif_011.ods' в таблицу 'comps' БД: 'bonds.db' <файл БД sqlite3 находится в текущей директории проекта>

TEN_STEP = False # 10. Считывание данных с заданного региона таблицы эксел для обновления на их основе данных в таблице БД

ELEVEN_STEP_A = False # 11a. Создание таблицы bonds с необходимой структурой для дальнейшего заполнения

ELEVEN_STEP_B = False # 11b. Считывание данных по корп.бондам из https://smart-lab.ru/q/bonds/ в созданную выше таблицу bonds в БД

TWELVE_STEP = False # 12. Занесение ISIN  из прошлых сводных таблиц в новую наполненную таблицу корпоративных облигаций bonds для перманентного использования 

TWELVE_STEP_A = False # 12A. Занесение QUALIF (квалификация брокера для бумаг) из прошлых сводных таблиц в новую наполненную таблицу корпоративных облигаций bonds для перманентного использования 

THIRTEEN_STEP = False # 13. Создание архивной таблицы bonds_archive (с датой внесения записей и полем причины внесения записи в архив)

# THIRTEEN_STEP_B = False # 13B. Функция переноса записи из таблицы bonds в таблицу bonds_archive


FOURTEEN_STEP = False # 14. Заполнение полей isin и qualif в таблице bonds БД ('bonds') нехватающими данными с сайта moex 

FIFTEEN_STEP_AUXILARY_1 = False # 15_AUX_1. Вспомогательный разовый шаг: Присвоить в поле  f1 таблицы bonds_archive значения 'NOT COMPLETED'

FIFTEEN_STEP_AUXILARY_2 = False # 15_AUX_2. Вспомогательный разовый шаг: Проставить в поле f1 в таблице bonds_current метку 'MATCHED', говорящую о том, что все облигации прошли сверку
                               # на сайте moex (М.биржа). Для дальнейшего копирования в таблицу  bonds_archive (чтобы отделить сверенные от не нашедших совпадение на сайте биржы)

FIFTEEN_STEP_AUXILARY_3 = False # 15_AUX_3. Вспомогательный разовый шаг (в будущем будет выполняться при новой загрузке bonds_current): Копирование данных по облигациям, в которых уже проставлены ISIN
                               # в bonds_archive с конфликтом IGNORE , если облигация с названием уже есть в таблице архивов (что бы сохранить их ISIN и qualify, интерактивно найденные на сайте moex при подготовительной работе)

FIFTEEN_STEP_A = False # 15A. Считывание данных по корп.бондам из https://smart-lab.ru/q/bonds/ в БД . Обновление таблицы bonds в БД прямо из сайта smart-lab. 
                    # С проставлением даты обновления в доп. поле и флага обновления в другом доп.поле


FIFTEEN_STEP_B = False # 15B. Произвести сверку вставленных записей с меткой 'NOT VERIFIED' в архиве. Если нет соответствия на moex,  то поставить метку "NOT MATCHED" в архиве для этих бумаг. Если есть на Мбирже, то проставить ISIN, quakify
                        # и поставить метку 'MATCHED'. Удалить из bonds_current бумаги с меткой "NOT MATCHED"


FIFTEEN_STEP_C = False # 15C. Проставить ISIN в таблице bonds_current на основе базовых данных в таблице bonds_archive, после создания и сверки новой современнйо выборки с сайта smart


SIXTEEN_STEP_AUXILARY = False  # 16. Проставить данные по разрешено к тороговле от Сбербанка в bonds_archive и bonds_current для тех бумаг, для которых уже есть данные в таблице Эксел базовой 
                     # (прощлые итоги анализа доступности бумаг в Сбербанке вручную накопленные в таблице эксел)


SEVENTEEN_STEP = False # Вставка данных по компаниям из заполненной предыдущими алгоритмами экселовской сводной таблицы корпоративных облигаций
                        # 'БАЗА_ОБЛИГАЦИИ_modif_011.ods' в таблицу 'comps' БД: 'bonds.db' <файл БД sqlite3 находится в текущей директории проекта>


EIGHTEEN_STEP = False # Проставление  (UPDATE)  ИНН в реферальном поле облигаций в таблице bonds_archive и bonds_current на основе исторических данных в таблице эксел, где проставлены okpo и inn компаний-эмитентов


NINETEEN_STEP = False # 19. Обновление поля okpo в таблице bonds_current (после нового считывания выборки бумаг с сайта smart) из архива бумаг и из сайта 
                        # rusbonds для тех, Которых нет в архиве 

TWENTY_STEP = False # # 20. Простановка okpo в архиве бумаг bonds_archive из обновленной (и свереной на rusbonds по okpo) оперативной таблицы bonds_current для тех записей
            # okpo которых нет в таблице bonds_current (то есть для тех бумаг, которые появились в результате текущего обновления оперативной таблице бумаг
            # и эмитентов которых не было до сих пор в БД)


TWENTY_ONE_STEP = False # 21. Сверка эмитентов бумаг находящихся в bonds_archive и компаний находящихся в comps. если находятся бумаги, чьи эмитенты не присутствуют в comps, то проставить их
        # Обновление ИНН компаний в bonds_archive, эмитенты которых отсутствуют для новых записей по бумагам


TWENTY_TWO_STEP = False # 22. 1. Простановка inn_ref в таблицах bonds_archive  на базе inn в таблице comps там, где есть ОКПО в comps  и bonds_current, но INN есть только в comps
                # inn в comps появились в результате поиска и прописки новых эмитентов на основе анализы новых появившихся бумаг в таблице bonds_current и bonds_archive
                # 2. Простановка всех inn_ref в bonds_current на основе inn_ref в bonds_archive


TWENTY_THREE_AUX = False # 23. ОДНОРАЗОВАЯ ОПЕРАЦИЯ: Наполнение всей совокупности исторической информации по компаниям (links, descriptions and financial data) из прошлых таблиц эксел


TWENTY_FOUR = False # 24.  Поиск ссылкок в интернет рессурсах, связаннх с компаниями-эмитентами, где можно получить необходимые данные и
                     # запсиь этих ссылок в таблицу comps_descr БД


TWENTY_FOUR_AUXILARY_A = False # 24_AUX_A. ВСПОМОГАТЕЛЬНЫЯ: Проверка правильности заполнения ссылок в полях таблицы comps_descr после интерактивного заполнения ссылок на страницы компании
                                # в алгоритме a024


TWENTY_FIVE = False  # 25.  Вставка (Update) полей описаний компании в таблице comps_descr путем интерактивного поиска по ссылкам из источников данных,
                            # которые уже вставлены в поля link1, link2 ... алгоритмом a024_ в СООТВЕТСТВИИ С ЗАДАВАЕМЫМ СПИСКОМ ИНН компаний dsInnsToDescrUpdate


TWENTY_SIX = False # 26. - Считывание и запись в БД в таблицу comps_financial финансовых показателей компаний с сайта CHECKO с маркировкой успешных результатов в
                        # таблице global_A в поле f1


# NEXT_STEP





# -- END MAIN ALGORITHM settings  ----


# -- FOR LINK SRCH COMP CLASS ----

CHECKO_COMP_LINK = 'https://checko.ru/'

FINPLAN_COMP_LINK = 'https://fin-plan.org/lk/obligations/RU000A0ZZ8A2/'

RBK_COMP_LINK = 'https://companies.rbc.ru/'


LINK_BASE = {'CHECKO': CHECKO_COMP_LINK, 'FINPLAN': FINPLAN_COMP_LINK, 'RBK': RBK_COMP_LINK}


# -- END FOR LINK SRCH COMP CLASS ----


# FOR algrtmLibreSmartBondsLocalParsing001:
    # ----- Алгоритм копирования html кода источника в Инете в файл на компе, парсинг локального файла,
    #  вставки таблицы в Либре эксел ----



# цифра задаваемого сокетного канала для порта для открытия либре обьекта
LIBRE_SOCKET_PORT = "2002"


# Запуск части Либре (для разработки). True - для конечного варианта
START_LIBRE_MANAGER = True

# Запуск части smart-lab (для разработки). True - для конечного варианта
START_SMARTLAB_MANAGER = True


# Таблица 01.1. Сводные данные по корпоративным облигациям по адресу https://smart-lab.ru/q/bonds/
TAB01_1_TITLES_TYPES = {
                         "N": "int", 
                         "Последняя сделка": "str", 
                         "Облигация" : "str",
                         "Форум": "str",
                         "Размещение": "str", 
                         "Погашение" :  "str", 
                         "Лет до погашения": "F#.##", 
                         "Доходность": "F#.##",
                         "Год.куп.дох." : "F#.##", 
                         "Куп.дох.посл.": "F#.##", 
                         "Цена": "F#.##", 
                         "Объем, млн.p": "F#.##",
                         "Купон":  "F#.##", 
                         "Частота": "int",
                         "НКД": "F#.##",
                         "Дюрация": "F#.##", 
                         "Дата купона": "str", 
                         "Оферта": "str",
                          "_": "str",
                          "_!!!": "str"
                         }


# END FOR algrtmLibreSmartBondsLocalParsing001:

# -- FOR ELEVEN_STEP_A  / Создание таблицы bonds с необходимой структурой для дальнейшего заполнения

# Поля таблицы bonds в БД bonds (с указанием типа поля, а так же формата числовых данных < типа #.##> там, где это необходимо)
TB_BONDS_11STEP = {
                         "n": "int", 
                         "isin": "str/unq/nnull",
                         "inn_ref" : "str",
                         "last_trans": "str", 
                         "bond_name" : "str",
                         "forum": "str",
                         "start_date": "str", 
                         "end_date" :  "str", 
                         "years_to_end": "F/#.##", 
                         "yield": "F/#.##",
                         "annual_yield" : "F/#.##", 
                         "last_annual_yield": "F/#.##", 
                         "curr_price": "F/#.##", 
                         "volume": "F/#.##",
                         "coupon":  "F/#.##", 
                         "frequency": "int",
                         "nkd": "F/#.##",
                         "durration": "F/#.##", 
                         "coupon_date": "str", 
                         "oferta": "str",
                         "qualif": "str", # квалификация брокера для бумаги (да/нет)
                         "f1" : "str", # вспомогательные поля для возможных будущих дополнительных данных
                         "f2": "str", 
                         "f3" : "str",
                         "f4": "str",
                         "f5": "str",   
                         "f6" : "str",
                         "f7": "str", 
                         "f8" : "str",
                         "f9": "str",
                         "f10": "str",                                                  

                         }


# Карта соответсвий (словарь переводов) абревиатур в характеристиках поля в словаре TB_BONDS_11STEP

FIELD_ABRIVIATION_STEP11 = {
                            'str' : 'TEXT', # тип стрингового поля 
                            'string' : 'TEXT',
                            'text' : 'TEXT',
                            'txt' : 'TEXT',
                            'unq' : 'UNIQUE', # индекс уникальности поля
                            'unique' : 'UNIQUE', 
                            'nnull' : 'NOT NULL', # NOT NULL
                            'nn' : 'NOT NULL',
                            'F' : 'REAL', 
                            'float' : 'REAL', 
                            'real' : 'REAL',
                            'int' : 'INTEGER',
                            'integer' : 'INTEGER',
                            'fk' : 'FOREGN KEY',
                            'FK' : 'FOREGN KEY',
                            'ref' : 'REFERENCES',
                            'REF' : 'REFERENCES',
                            'delcasc' : 'ON DELETE CASCADE',
                            'del' : 'ON DELETE CASCADE',
                            'ON DELETE CASCADE' : 'ON DELETE CASCADE',
                            'updcasc' : 'ON UPDATE CASCADE',
                            'upd' : 'ON UPDATE CASCADE',
                            'ON UPDATE CASCADE' : 'ON UPDATE CASCADE',
                            'auto' : 'AUTOINCREMENT',


                            

                        }




TB_BONDS_KEYS_1 = [
                    {
                        'kname': 'fk_inn',
                        'fk' : ['inn_ref'],
                        'reftb': 'comps',
                        'reffields' : ['inn'],
                        'delcasc' : 'ON DELETE CASCADE',
                        'updcasc' : 'ON UPDATE CASCADE',

                    },
                    ]


# -- END FOR ELEVEN_STEP_A 




# FOR a002_moex_bond_page_data:
    # ----- Алгоритм открытия сайта моск.биржи, прохождения барьеров, нахождения страницы определенной облигации и 
        # считываня данных с этой страницы в таблицу эксел Либре----


NEW_COL = 1 # Номер столбца, за которым будет вставлятся новая колонка

NEW_COL_TITLE = "Квалиф. бр"

NO_QUALIFY_COLOR = 0x9acd32 #  Цвет ячейки, если разрешено для неквалифицированных

YES_QUALIFY_COLOR = 0xe9967a #  Цвет ячейки, если запрещено для неквалифицированных

COL_COLOR_CONDITION = -1 # Колонка, в которой будет идти цветовая дифференциация. -1 - Этот текущая колонка с названиями облигаций


# END FOR algrtmLibreSmartBondsLocalParsing001


# -- FOR RUSBONDS algorithm ----

# < Нумерация инпутов на первой странице >

# no= rusbonds.driver.find_element(By.XPATH, "//*[contains(text(),'Для квалиф')]/..")
# nos = no.find_elements(By.TAG_NAME, "input")

# nos[10].click() # Инпут "Сектор эмитента"

# nos[30].click() Ставка купона, % (2d input)

# nos[33].click() Тип облигации

# nos[35].click() Вид облигации

# nos[46].click() Вид обеспечения


# < 8 блоков фильтров >
# divs_colapse = rusbonds.driver.find_elements(By.CLASS_NAME, "el-collapse-item__content") # 8 блоков с фильтрами

# divs_drop_clickable = divs_colapse[2] - БЛОК Эмитент, заемщик

# input = divs_drop_clickable[1].find_element(By.TAG_NAME, "input") - input поле для ввода группы фильтров [1]


# <STRUCTURE OF FILTERS ABOVE>

# cols = rusbonds.driver.find_elements(By.CLASS_NAME, "col") - две колонки , правая и левая, в которых расположены блоки с фидьтрами


# blocs = cols[1].find_elements(By.CLASS_NAME, "filter-group") - блоки фильтров в колонке справа


# blocs[0] - БЛОК: Купон

# blocs[1].text - БЛОК: КЛАССИФИКАТОР ЭМИССИЙ

# field_groups = blocs[1].find_elements(By.CLASS_NAME, "field-group") - группы полей -вводов для установки в блоке 

# field_groups[2] - ГРУППА: Для квалиф. инвесторов

# input = field_groups[2].find_element(By.CLASS_NAME, "field-input") - поле input грцппы: Для квалиф. инвесторов

# div_radio = field_groups[2].find_element(By.CLASS_NAME, "triple-options") - поле где расположен radio button 3 варианта: Для квалиф. инвесторов

# radio_group = field_groups[2].find_element(By.CLASS_NAME, "radio-buttons") - div где расположен radio buttons 3 варианта: Для квалиф. инвесторов

# radio_labels = field_groups[2].find_elements(By.TAG_NAME, "label") - labels c radio buttons  3 варианта: Для квалиф. инвесторов

# radio_labels[1].click() -  !!!! Нажатие - выбор фильтра НЕТ в группе Квалифицированных инв.

# < END STRUCTURE OF FILTERS ABOVE >



# -- END FOR RUSBONDS algorithm ----













