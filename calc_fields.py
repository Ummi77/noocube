# Для калькулируемых полей
# calc_fields.py


from .bonds_main_manager import BondsMainManager

class CalcFields (): 
    """ 
    Класс для универсальных калькулируемых полей
    """

    def __init__(self, dBase):
        self.dBase = dBase
    
    
    
    
    @staticmethod
    def calc_id_by_col_val_from_tb_lambda(*args):
        """ 
        FuncsAnalyzerManager
        Калькулируемое значение для лямбда-функции: Получить id записи по значению colVal в колонке colSrc в заданной таблице tb. Функция для  lambda
        tb - таблица (возможный источник FOREIFN KEYS)
        idCol - название идентификатора-ключа-колонки в таблице (по умолчанию равна 'id')
        colSrc - колонка, в которой надо найти значение colVal для получения записи по этому ряду
        colVal - значение в колонке colSrc, которое надо найти для получения записи по этому ряду
        Category: Калькуляторы полей
        """
        tb = 'funcs_analyzer_classes'
        print(f"DDDDDDDDDD******************************** ")
        bmm = BondsMainManager('/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/db.sqlite3')
        print(f"HHHHHHHHHHHHHHHHHH ##################  dBase = {'/home/ak/projects/P17_FUNCTIONS_NCUBE/noocube_functions/db.sqlite3'}")
        # Получить idRecord записи, где в колонке colSrc значение равно colVal
        # Pars:
        colSrc = 'class_name'
        colVal = 'FilesManager'
        idCol = 'id'
        idRecord = bmm.get_id_from_tb_by_col_val(tb, colSrc, colVal, idCol)[0]
        
        print (f"VVVVVVVVVVVVVVVVVVVVVVVVVVVVVv$$$$$$$$$$$$$$$$$$$ idRecord = {idRecord}")
        
        return idRecord
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    pass


















