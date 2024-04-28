

from markupsafe import Markup
import bonds.funcs_general as FG
import numpy as np
import pandas as pd
from .sqlite_pandas_processor import SqlitePandasProcessor
from bonds.settings import *
from bonds.switch import Switch
from bonds.exceptions import *
from project_bonds_html.projr.classes.dsource_cube import DSourceCube 
from bonds.settings_date_formats import *  
# from classes.local_manager_BH import LocalManager
# from project_bonds_html.projr.classes.html_manager import HTMLSiteManager
# from settings import TB_PORTFOLIO_HISTORY_
# from settings import TB_BONDS_BOUGHT_



class NooGeneralManager(SqlitePandasProcessor):
    """Класс реализующий специализированные  локальные макросы по сущностям , участвующим именно в этом проекте (облигации, компании, процессоры конкретных таблиц и т.д.)
    Относится к надстройкам самого высокого уровня в реализации кода проекта
    Стягивать в этот модуль все специфические конечные методы с конкретными, индивидуальными сущностями 
    Подобный класс путь всегда имеет имя равное общему названию конкретного проекта с добавлением 'Main'
    Ранее его задачи выполнял класс SqliteBondsMacros из файла /home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/sqlite_bonds_macros.py"""

    def __init__(self, dbName): 
        SqlitePandasProcessor.__init__(self, dbName)
        



    



    def main():
        pass




if __name__ == '__main__':
    pass










