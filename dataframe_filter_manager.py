# 
from noocube.switch import Switch
from pandas import DataFrame
from noocube.pandas_manager import PandasManager

class DataFrameFilterManager (): 
    """ 
    Класс для организации фильтра фрейма dataframe_filt_manager.py
    """
    
    def __init__(self, df):
        """
        Конструктор
        df - фрейм, по которому осуществляются фильтрации

        """
        self.df = df
    
    
    ### ---  ИНДИВИДУАЛЬНЫЕ ФУНКЦИИ ФИЛЬТРАЦИИ фрейма заданным параметрам. 
    
    # Используются, в частности, при фильтрации фрейма при обработке в обьекте типа DSourceOutputCube, отвечающего за подготовку фрейма к выводу в виде таблице на сайте
    
    @staticmethod
    def df_filter_by_col_val_contains(df, colName, substring):
        """
        DataFrameFilterManager
        Фильтрация фрейма df по заданному стринговому фрагменту substring, который содержат значения ячеек в заданной колонке colName (по названию коллонки) 
        Category: Фреймы
        """
    
        df = df[df[colName].str.contains(substring, case=False)]
        return df
    
    
    
    
    
    ### ---  END ИНДИВИДУАЛЬНЫЕ ФУНКЦИИ ФИЛЬТРАЦИИ
    
    
    @staticmethod
    def filter_df_by_multi_formulas_df_static_fm (df, dfFilters):
        """
        DataFrameFilterManager
        Фильтрация фрейма по набору индивидуальных функций фильтрации фрейма, заданных в фрейме с набором фильтров dfFilters . В каждом ряду - отдельный фильтр
        Используются, в частности, при фильтрации фрейма при обработке в обьекте типа DSourceOutputCube, отвечающего за подготовку фрейма к выводу в виде таблице на сайте
        dfFilters - фрейм, где заданы паарметры мульти-фильтров, в формате Название фильтра условное, условная формула и необходимые атрибуты, которые могут содержать необходимые настройки ,
        входные значения и пр. Названия колонок в dfFilters :['filter', 'filt_columns', 'formula_nick', 'vals', 'description' ] (последние две колонки могут быть пустыми)
        'description' - описание фильтра, может быть пустым. 'vals' - значения величин для функции, например, суб-стринг для поиска
        Если не найдены фильтры или еще какие-нибудь глюки, то процедурный фрейм остается не тронутым
        
        ПРИМ: Метод не завершен и подлежит дальнейшему развитию и проработке
        
        RET: DataFrame
        Category: Фреймы
        """
        
        for index, row in dfFilters.iterrows():

            # Если  название филььтра присутствует в фрейме dfFilters ?
            if PandasManager.if_val_exists_in_col_pandas (dfFilters, 'filter', row['filter']):

                # Получение содержимого в колонки 'filt_columns' (там хранятся , в частности, названия колонок, по которым проводится фильтрация.
                # А если расчетная колонка, то путь к функции-обертки ддля калькулирования колонки)
                filtColumn = row['filt_columns']

                # Если есть маркер 'Calc' калькулируемого поля в ячейке столбца 'filt_columns', то формирование фильтра происходит по алгоритму создания или апдейта для расчетного поля
                if 'Calc' in filtColumn:
                    pass
                    # print(f'Расчетное полe фильтра {filter}')
                    # # # |--> PRINT LOG: 
                    # DSourceOutputCube._print_mark('filtFormula', '__init__()', mark = 'filtFormula', markVal = filtFormula , prefix = '$$$$$$$$ ')
                    
                # Если нет маркера 'Calc' , то значит - это простое поле и формирование выражения фильтрации определен алгоритмом для простого поля    
                else: 
                    # Получить ник (код) формулы по собственной системе кодирования для формулы фильтрации по обычномой колонке для текущего фильтра и поля
                    nicFormula = row['formula_nick']
                    
                    # РАСПРЕДЕЛИТЕЛЬ функций фильтрации для текущих фильтров        
                    # switch ... case для определения функции фильтрации для фрейма по заданному нику функции (частная кодировка для функций фильтрации, своя) для текущего фильтра в цикле
                    for case in Switch(nicFormula):
                        
                        if case('column_contains'): 
                            df = DataFrameFilterManager.df_filter_by_col_val_contains(df, filtColumn, row['vals'])

                        if case(): # default фрейм остается не тронутым
                            print(f'Не найден ник фрмулы для фильтрации по query для фрейма: nicFormula = {nicFormula}')
                            break
                
            # если название фильтра отстутствует в фрейме dfFilters, то фильтрации не происходит и фрейм остается не тронутым
            else:
                print(f"Нет названия фильтра {row['filter']} в фрейме фильтров  dfFilters")
        
    
        return df



    @staticmethod
    def prepare_multi_filter_df_by_filter_formulas_dic_and_filter_vals_dic_fm (filterFormulasDic, filterValsDic):
        """ 
        DataFrameFilterManager
        Подготовить фрейм с мульти-фильтрами на основе словаря с формулами для фильтров filterFormulasDic и словаря со значениями для фильтров filterValsDic.  
        Этот фрейм используется для фильтрации по нему операционного фрейма (каждый ряд описывает какой-то фильтр, Который накладываетя потом на операционный фрейм)
        RET: DataFrame
        Category: Фреймы
        """

        # Создать пустой фрейм с заданными колонками и заполнить формулами мульти-фильтров
        dfFilters = DataFrame(columns=['filter', 'filt_columns', 'formula_nick', 'vals', 'description' ])
        for key, val in filterFormulasDic.items():
            # Список - строка для фрейма
            dfRowList = []
            # Добавить название фильтра
            dfRowList.append(key)
            # распарсить формулу фильтра в val
            formulaParts = val.split('|')
            # Добавить аргументы, а именно названия колонок (в том числе и расчетных. в случае с расчетными колонками + полное название расчетной функции)
            dfRowList.append(formulaParts[0])
            # Добавить формулу фильтра (в случае с расчетными колонками - полное название расчетной функции)
            dfRowList.append(formulaParts[1])
            # Добавить две последний колонки пустыми, так как в них нет пока значений
            dfRowList.append('')
            dfRowList.append('')
            # Создать ряд в фрейме со значениями в ячейках , соотвтетсвующих списку dfRowList
            dfFilters.loc[len(dfFilters)] = dfRowList
            

        # Заполнить колонку со значениеями 'vals' значениями фильтров, полученными из request со страницы сайта, которые находятся в слловаре dicFiltersFormulasVals
        
        # Цикл по словарю со значениями для фильтров из поступившего request со страницы сайта связанного с View для присвоения  значений для фильтров в dfFilters
        for key, val in filterValsDic.items():

            # pars:
            colKeyName = 'filter' # ключевая колонка в dfFilters с названиями филльтров
            keyVal = key # текущее по циклу название фильтра
            colSetName = 'vals' # Колонка 'vals', куда надо записать значения по данному фильтру, пришедшие из request  для этого фильтра
            colSetVal = val # Значение по фильтру из request  для текущего названия фильтра по циклу
            dfFilters = PandasManager.set_value_in_col_with_given_key_col_val_pandas (dfFilters, colKeyName, keyVal, colSetName, colSetVal)
            
        return dfFilters
            

    
    
    
    
if __name__ == '__main__':
    pass
