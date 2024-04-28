# https://ru.stackoverflow.com/questions/460207/Есть-ли-в-python-оператор-switch-case

class Switch(object): 
    """ Аналог оператора switch ... case
    https://ru.stackoverflow.com/questions/460207/Есть-ли-в-python-оператор-switch-case

    Использование:
                for case in Switch(x):
                if case(1): pass
                if case(2): pass
                if case(3): 
                    print('Число от 1 до 3')
                    break
                if case(4): 
                    print('Число 4')
                if case(): # default
                    print('Другое число')
                    break
    """

    def __init__(self, value):
        self.value = value  # значение, которое будем искать
        self.fall = False   # для пустых case блоков

    def __iter__(self):     # для использования в цикле for
        """ Возвращает один раз метод match и завершается """
        yield self.match
        raise StopIteration

    def match(self, *args):
        """ Указывает, нужно ли заходить в тестовый вариант """
        if self.fall or not args:
            # пустой список аргументов означает последний блок case
            # fall означает, что ранее сработало условие и нужно заходить 
            #   в каждый case до первого break
            return True
        elif self.value in args:
            self.fall = True
            return True
        return False

    # # Аналог case...switch  с использованием словаря operations  с функциями . Src: algorithm_calc.py -> a001_smartlab_bonds_localpars
    # # TODO: НЕ УДАЛЯТЬ БЛОК!!! Изучить и использовать
    # # Словарь операторов и функций для них для использования в аналоге case...switch во внутреннем методе operations
    # operations = {
    #     '<': lambda x, y: x < y,
    #     '>': lambda x, y: x > y,
    # }
    # def calc(operation, a, b):
    #     """ Аналог case...switch  с использованием словаря operations  с функциями
    #     Очистка от всех символов, кроме цифр,  '-','.'  """
    #     if type(a) == str:
    #         a = float(FG.strip_for_digits_bytearray(a).strip('%'))
    #     if type(b) == str:
    #         b = float(FG.strip_for_digits_bytearray(b).strip('%'))

    #     return operations[operation](a, b)

    # # Исаользование: Результат сравнения величины в ячейка последнего ряда заданнйо колонки и допустимого предела
    # lim = calc(cond_mark, cond_val, last_row_col_val)        


if __name__ == "__main__":
    x = '4'

    for case in Switch(x):
        if case('1'): 
            pass
        if case('2'): 
            pass
        if case('3'): 
            print('Число от 1 до 3')
            break
        if case('4'): 
            print('Число 4')
        if case(): # default
            print('Другое число')
            break