
# Модуль служит для локальных общих функций разного предназначения

def binary_switch_str_var(var):
    """Бинарное переключение стринговой переменной в зависимости от собственного ее значения
    Ret: (var <1 или 0>, flag <True or False>)
    Используется для переключения сортировки или еще чего-нибудь в HTML - коде, где передается в глобальном параметре request
    """
    if var == None or var == '0':
        var = '1'
        flag = True
    elif var == '1':
        var = '0'
        flag = False
    else:
        var = '1'
        flag = True        
    return var, flag











