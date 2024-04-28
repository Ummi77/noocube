# Файл служит для настройки необходимых параметров общей программы

DEBUG_ = True # Для вывода на консоль не которых принтов в ходе отладки программы


ALGORITHM_MESSEGES_ = False # Для вывода сообщений только из алгоритмов модуля: AlgorithmsCalc


# Логирование процесса выполнения запускаемого алгоритма
LOG_ALGORITHMS_ = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/log_algorithms.txt'


# БД:
DB_TLH_= '/home/ak/projects/2_Proj_TLH_Center/project_tlh/instance/tlh.db'
DB_BONDS_= '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/bonds.db' 

TB_BONDS_CURRENT_ = 'bonds_current'
TB_BONDS_ARCIVE_ = 'bonds_archive'
TB_COMPS_ = 'comps'
TB_GLOBAL_A_ = 'global_A'
TB_COMP_DESCR_ = 'comps_descr'
TB_COMPS_FINANCE_ = 'comps_finance'
TB_REG_ISIN_B_ = 'reg_isin_B'

TB_OFZ_CURRENT_ = 'ofz_current'
TB_OFZ_ARCIVE_ = 'ofz_archive'

TB_MUNICIP_CURRENT_ = 'municip_current'
TB_MUNICIP_ARCIVE_ = 'municip_archive'

TB_BONDS_CURRENT_PREV_ = 'bonds_current_prev'


TB_FAPVDO_COMPS_RAITINGS_ = 'fapvdo_comp_raitings' # Таблица рейтингов и коэфф компаний из ресурса https://fapvdo.ru/rejting-jemitentov/

TB_RAEX_COMPS_RAITINGS_ = 'raex_comp_ratings' # Таблица рейтингов и коэфф компаний из ресурса https://expert-pages.ru/search/results/


TB_RAEX_COMPS_WITHDROWN_ = 'raex_comps_withdrawn' # Таблица компанйи с отозванными рейтингами по RAEX

TB_BONDS_BOUGHT_ = 'bonds_bought'

TB_PORTFOLIO_HISTORY_ = 'portfolio_history' # Таблица исторических сделок с общими данными по купле-продажи


TB_BUNKRUPT_BONDS_ = 'bukrupt_bonds' # Обанкротившиеся бумаги и их эмитенты

TB_INDEX_PACKAGES_ = 'index_packages' # Индексные пакеты 

TB_DIFFERENCIATOR_ = 'differenciator'

VIEW_BONDS_COMPLEX_ = 'bonds_complex_view' # view , содержащая в себе обьединение 3х таблиц 'bonds_current', 'ofz_current', 'municip_current'






TIME_WAIGHT_ = 10 # Задержка при загрузке новой странице в браузере, помле чего сраюбатываеь остановка загрузки




# Dir for testing 
TEST_DIR_ = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/testing'


# НАСТРОЙКИ ССЫЛОК, УЧАСТВУЮЩИХ В АЛГОРИТМАХ

SMART_LINK_OFZ_ = 'https://smart-lab.ru/q/ofz/'


SMART_LINK_MUNICIP_ = 'https://smart-lab.ru/q/subfed/'


# Ссылка рейтингов по системе ресурса FAPVDO
FAPVDO_RAITHINGS_LINK_ = 'https://fapvdo.ru/rejting-jemitentov/'


# Ссылка рейтингов по системе ресурса RAEX
RAEX_RAITHINGS_LINK_ = 'https://expert-pages.ru/search/results/'



# Разделитель элементов словаря, переведенного в стринговую форму и записываемую в БД для будущей десериализации по этим меткам delim_
DElLIMIT_FOR_DICT_JSAN_ = '$$$' 
# Разделитель между ключем и знаением в словаре в форме JSAN в БД
DElLIMIT_FOR_KEY_VAL_IN_JSAN_ = '&&&' 













