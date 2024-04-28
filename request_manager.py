
from noocube.bonds_main_manager import BondsMainManager
from noocube.settings import *
from noocube.funcs_general_class import FunctionsGeneralClass
from .settings import *

class RequestManager (): # 
    """ Менеджер request с сайта HTML
    """


    # @@@@ DJANGO Request 
    
    
    def _print_mark(id, func, mark, markVal, prefix):
        """
        DSourceOutputCube
        Вспомогательыня функция для распечатки принт-маркеров
        ПРИМ: Что бы использовать эту вспомогательныую функцию необходимо добвать ее в кажый класс и заменить константные значения className и file на соотвтетсвующие этому классу
        """

        FunctionsGeneralClass.print_any_mark_by_id(
            PRINT_TERMINAL_START_END_FUNCTIONS_,
            id,
            func = func,
            mark = mark,
            markVal = markVal,
            className = 'RequestManager',
            calssFile = 'noocube/request_manager.py',
            prefix = prefix
        )
    
    
    @staticmethod
    def read_urls_args_matrix_by_request_django (request):
        """
        RequestManager
        Считать словарь текущих матрицу request  аргументов 
        Category: Request FLASK
        """

        urlsArgsMatrix = {}
        for key,val in request.GET.items():
            urlsArgsMatrix[key] = val

        return urlsArgsMatrix
    
    
    
    
    
    
    
    
    # @@@@ END DJANGO Request 




    @staticmethod
    def print_request_pars(request):
        """
        ЗАГОТОВКА
        RequestManager
        Распечатать параметры  request для таблиц облигаций
        Category: Request FLASK
        """
        print(f"Кол-во параметров в request = {len(request.args)}")
        print ("Параметры request:")
        print(request.args)


    @staticmethod
    def get_request_immutable_dict(request):
        """
        RequestManager
        Получить словарь immutable из request
        Category: Request FLASK
        """
        immutDict = request.args
        return immutDict


    @staticmethod
    def get_request_as_dict(request):
        """
        RequestManager
        OBSOLETED: Использовать метод get_request_get_as_dict(request) из-за изменения названия метода для более понятного отображения сущности метода
        Получить словарь  request по существубщим в нем значениям аргументов, переданных через GET
        Category: Request FLASK
        """
        reqDic = dict(request.args)
        return reqDic


    @staticmethod
    def get_request_get_as_dict(request):
        """
        RequestManager
        Получить словарь  request по существубщим в нем значениям аргументов, переданных через GET
        Category: Request FLASK
        """
        reqDic = dict(request.args)
        return reqDic


    @staticmethod
    def get_request_post_as_dict(request):
        """
        RequestManager
        Получить словарь  request по параметрам переданным через POST 
        Category: Request FLASK
        """
        reqPostDic = request.form.to_dict(flat=False)
        return reqPostDic


    @staticmethod
    def get_request_as_dict_ini(request):
        """
        RequestManager
        Параметры request существующие и их альтернативная инициализация в виде ини-словаря
        Category: Request FLASK
        """

        rqIniDic = {}
        # Фильтрационные атрибуты request
        rqIniDic['filtExprDicKey'] = RequestManager.get_request_attr_val(request, 'filtExprDicKey')  if RequestManager.if_attr_in_request_keys(request, 'filtExprDicKey') else ''
        rqIniDic['filtIsin'] = RequestManager.get_request_attr_val(request, 'filtIsin')  if RequestManager.if_attr_in_request_keys(request, 'filtIsin') else '' # input field в левом меню фильтрации по isin
        rqIniDic['filtBondName'] = RequestManager.get_request_attr_val(request, 'filtBondName')  if RequestManager.if_attr_in_request_keys(request, 'filtBondName') else '' # input field в левом меню фильтрации по названии облигации


        rqIniDic['ascTrue'] = int(RequestManager.get_request_attr_val(request, 'ascTrue'))  if RequestManager.if_attr_in_request_keys(request, 'ascTrue') else 1 # Если есть значение в request, то равно ему, если нет, то ini = 1
        rqIniDic['pg'] = 1
        rqIniDic['srchStr'] = ''
        rqIniDic['interp'] = ''
        rqIniDic['filtQuery'] =  RequestManager.get_request_attr_val(request, 'filtQuery')  if RequestManager.if_attr_in_request_keys(request, 'filtQuery') else ''
        rqIniDic['monthSrch'] = ''
        rqIniDic['payMonth'] = ''
        # Флаг переключателя для изменения направления сортировки. Если chSort == '0', то изменение направления сортировки не происходит (например, если с пагинатора)
        rqIniDic['chSort']  = RequestManager.get_request_attr_val(request, 'chSort')  if RequestManager.if_attr_in_request_keys(request, 'chSort') else '0'


        return rqIniDic





    @staticmethod
    def get_request_attr_val(request, attrName):
        """
        RequestManager
        Получить значение получаемого параметра из request
        Category: Request FLASK
        """
        reqDic = RequestManager.get_request_as_dict(request)
        attrVal = reqDic[attrName]
        return attrVal





    @staticmethod
    def get_all_keys_from_request(request):
        """
        RequestManager
        Получить название всех переданных в request параметров, которые являются ключами типа ImmutableDictionary, из чего состоит сам request
        Category: Request FLASK
        """
        immutDict = RequestManager.get_request_immutable_dict(request)
        requestParsNames = list(immutDict.keys())

        return requestParsNames


    @staticmethod
    def if_attr_in_request_keys(request, attrName):
        """
        RequestManager
        Проверить находится ли название искомого аргумента в переданных ключах в словаре атрибутов request
        Category: Request FLASK
        """
        rqKeys = RequestManager.get_all_keys_from_request(request)
        if attrName in rqKeys:
            return True
        else:
            return False



    @staticmethod
    def get_special_pars_from_request(request, strFragm):
        """
        RequestManager
        Получить название всех переданных в request параметров, содержащие в себе заданный фрагмент стринга
        Неоходимо, чтобы выделять определенные группы параметров
        Category: Request FLASK
        """

        requestParsNames = RequestManager.get_all_keys_from_request(request)
        specialRequestPars = [x for x in requestParsNames if strFragm in x]
        
        return specialRequestPars


        
    @staticmethod
    def get_grouped_pars_infor_data_from_request_t1(request, groupStrFragm):
        """
        RequestManager
        Получить информационную часть из группы параметров request, удалив маркерную часть в их названии, для тех параметров, которые имеют структуру типа 1. А именно
        'MARKER_INFPART' (Например, 'inp_SU29019RMFS5' - поле input в форме с названием. В частоности это название checkbox облигации в таблице облигаций )
        Category: Request FLASK
        """
        # Выделить данные по checkbox выранным на странице /bonds_current_ofz , которые имеют имена, начинающиеся с 'inp_'
        groupMarkerPars = RequestManager.get_special_pars_from_request(request, groupStrFragm)

        # Выделить информационную часть из групповых параметров
        inforParamsData = [x.split('_')[1] for x in groupMarkerPars]

        return inforParamsData









    @staticmethod
    def read_df_from_request_params_rm(request):
        """
        Считать парамметры request в data frame
        Category: Request FLASK
        """
        bmm = BondsMainManager(DB_BONDS_)
        reqDict = RequestManager.get_request_as_dict(request) # Словарь request-параметров
        dfRequest = bmm.read_df_from_dictionary(reqDict) # Фрейм из словаря request-параметров
        return dfRequest






if __name__ == '__main__':
    pass















