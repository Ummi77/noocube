

# from project_bonds_html.projr.settings import *
from noocube.sqlite_pandas_processor import SqlitePandasProcessor
import noocube.funcs_general as FG
# from settings import *

class JsonManager ():
    """  Класс для работы с форматами JSON """


    


    ## -- Вспомогательные методы  --------

    def get_list_of_vals_from_dict (self, dict):
        """ Получение списка велечин из словаря """
        valsList = [v for (k, v) in dict.items()]
        return valsList

    def get_list_of_lists_from_list_of_dicts (self, listDicts):
        """ Получение спсика списков из величин списка словарей [dict1, dict2, ...] """

        listOfValsLists = [self.get_list_of_vals_from_dict(x) for x in listDicts]
        return listOfValsLists


    ## -- END Вспомогательные методы  --------


    @staticmethod
    def deserrialization_from_dic_string_type1 (strDicInp, elemDelim, keyValDelim):
        """JsonManager
        Десериализация (превращение обратно в словарь) строки с сериализованным в строку ранее словаря strDic с заданными делиметрами для
        элементов словаря elemDelim и для разделения ключей и велечин словаря keyValDelim
        type1 в названии - это пока один вид дсериализатора, предназначенный конкретно для десериализации описаний компаний из полей descr1 ... descr5 
        таблицы comps_descr проекта bonds ( и зависит от способа сериализации словаря в строку. Возможно этот тип сериализации и оставим в будущем)
        Сериализация для этого десериализатора проводилась простым применением метода: f'dict' - который просто превращал весь словарь в строчку , как при распечатке
        """
        # делим строку на элементы условного словаря, пока в стрингах
        parts = strDicInp.split(f'{elemDelim}",')
        # ppartslist = [] # Элементы словаря, разделенные на условные ключи и величины. Пока не очищенные
        # Делим стринговые элементы стриногового словаря по ключам и величинам, пока не очищенным и формируем двумерный список - прообраз будущего словаря
        resDic = {} # Результирующий словарь
        for part in parts:
            pparts = part.split(f'"{keyValDelim}') # Делим стринговые элементы стриногового словаря по ключам и величинам, пока не очищенным
            # ppartslist.append(pparts)
            dicKey = pparts[0] # ключ будущего словаря
            if len(pparts) == 2:
                dicVal = pparts[1] # значение будущего словаря
            elif len(pparts) == 1:
                dicVal = ''

            # Очищаем стринговые ключи и значения элементов словаря от ненужных символов
            clrKeySimps = ['{', '}', '"', ':'] # Символы для очищения в первом элементе двумерного списка (в ключе будущего словаря)
            clrValSimps = [f'| {elemDelim}', f'{keyValDelim}', '"}', '}'] # Символы для очищения во втором элементе двумерног осписка (в значениях будущего словаря)
            dicKey = FG.clear_from(dicKey.replace(' ',''), clrKeySimps) # Очищаем ключ с заданными символами к отчистке 
            dicVal = FG.clear_from(dicVal, clrValSimps)

            resDic[dicKey] = dicVal

        return resDic



    @staticmethod
    def deserrialization_from_dic_string_type2 (strDicInp, elemDelim, keyValDelim):
        """JsonManager
        Десериализация (превращение обратно в словарь) строки с сериализованным в строку ранее словаря strDic с заданными делиметрами для
        элементов словаря elemDelim и для разделения ключей и велечин словаря keyValDelim
        type2 в названии - для тех случаев, когда в ключах или значениях стрингового словаря есть https - ссылки и в разделителях elemDelim, keyValDelim присутствует ':'
        """

        clrFrom = ['}', '{', ' ', 'https:', '\'', '\"'] # Символы для очищения 
        strDicInp = FG.clear_from(strDicInp, clrFrom) # Очищаем входной стринг словаря от clrFrom
        parts = strDicInp.split(f'{elemDelim}')

        resDic = {} # Результирующий словарь
        for part in parts:
            pparts = part.split(f'{keyValDelim}')
            
            if len(pparts) == 2:
                dicVal = pparts[1] # значение будущего словаря
                dicKey = pparts[0] # ключ будущего словаря
            elif len(pparts) == 1:
                dicVal = ''
                dicKey = pparts[0]

            dicKey = dicKey.replace('//','https://')

            resDic[dicKey] = dicVal

        return resDic





    @staticmethod
    def get_dic_from_frame_by_col(df, colName, elemDelim, keyValDelim):
        """
        Получение словаря из стринового прообраза словаря, находящегося в одномерном фрейме в колонке с названием  colName (после получения данных по одной, например, компании)
        elemDelim - делиметр для разделения стринга на элементы словаря
        keyValDelim - для разделения элементов на ключи - значения (делиметры вставляются в процессе стринговой сериализации словаря методом f'dictionary' - как печать)
        """

        # TODO: Проверить есть ли вообще колонка df[colName]
        dicStr = df[colName].iloc[0] # Значение ячейки colName в фрейме
        # dicStr = None
        if dicStr is not None:
            resDic = JsonManager.deserrialization_from_dic_string_type1(dicStr, elemDelim, keyValDelim)
        else:
            resDic = -1
        return resDic




if __name__ == '__main__':
    pass

    # jm = JsonManager()



## --  ПРИМЕРЫ: --------------







    # # ПРИМЕР: Проработка метода get_list_of_lists_from_list_of_dicts
    # jsonMngr = JsonManager()
    # dsInp = [['4716016979', {'revenue': '247,6 млрд руб.', 'revenueDelta': '8%', 'netProfit': '28,3 млрд руб.', 'netProfitDelta': '28,3 млрд руб.', 'assets': '1,6 трлн руб.', 'assetsDelta': '5%', 'capital': '1,2 трлн руб.', 'capitalDelta': '5%', 'koefKA': '0.74', 'koefWCR': '-1.48', 'koefICR': '0.94', 'koefCLR': '1.73', 'koefQLR': '1.59', 'koefALR': '0.49', 'koefPOS': '11.43%', 'koefROA': '1.72%', 'koefROE': '2.32%', 'finYear': '2021.', 'lastBuhgReportHref': 'https://bo.nalog.ru/download/bfo/pdf/1964159?period=2021'}], ['7816349286', {'revenue': '632,8 млн руб.', 'revenueDelta': '74%', 'netProfit': '580 тыс. руб.', 'netProfitDelta': '580 тыс. руб.', 'assets': '599,1 млн руб.', 'assetsDelta': '139%', 'capital': '157,8 млн руб.', 'capitalDelta': '1%', 'koefKA': '0.26', 'koefWCR': '0.01', 'koefICR': '0.77', 'koefCLR': '3.24', 'koefQLR': '3.23', 'koefALR': '0.01', 'koefPOS': '0.09%', 'koefROA': '0.10%', 'koefROE': '0.37%', 'finYear': '2021.', 'lastBuhgReportHref': 'https://bo.nalog.ru/download/bfo/pdf/10050610?period=2021'}]]        

    # listOfDicts = FG.convert_list_of_list_to_one_dim_list(dsInp, 1)

    # listOfValsLists = jsonMngr.get_list_of_lists_from_list_of_dicts (listOfDicts)


    # # ПРИМЕР: Проработка метода get_list_of_vals_from_dict
    # jsonMngr = JsonManager()
    # dict = {'revenue': '247,6 млрд руб.', 'revenueDelta': '8%', 'netProfit': '28,3 млрд руб.', 'netProfitDelta': '28,3 млрд руб.', 'assets': '1,6 трлн руб.', 'assetsDelta': '5%', 'capital': '1,2 трлн руб.', 'capitalDelta': '5%', 'koefKA': '0.74', 'koefWCR': '-1.48', 'koefICR': '0.94', 'koefCLR': '1.73', 'koefQLR': '1.59', 'koefALR': '0.49', 'koefPOS': '11.43%', 'koefROA': '1.72%', 'koefROE': '2.32%', 'finYear': '2021.', 'lastBuhgReportHref': 'https://bo.nalog.ru/download/bfo/pdf/1964159?period=2021'}

    # # llstVals = [v for (k, v) in dict.items()]

    # llstVals = jsonMngr.get_list_of_vals_from_dict ( dict)

## --  END ПРИМЕРЫ: --------------









