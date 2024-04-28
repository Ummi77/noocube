
from noocube.input_output import InputOutput


class TextProcessor():
    """ 
    Класс предназначен для обработки текстовых переменных, парсинга, и все, что связано с анализом и форматированием текстовых переменных string
    """

    def __init__(self, strText):
        self.text = strText



    def string_in_square_brakets_to_list (self, splitMark):
        """ Конвертация текста в квадратных скобках в python list """
        pList = self.text.lstrip('[').rstrip(']').split(splitMark)
        return pList









if __name__ == "__main__":
    pass



# ПРИМЕР: считывание текста из файла и получение списка из тестовых элементов , заключенных в квадратные скобки
    io = InputOutput('a024_inn_last.txt')
    textStr = io.read_from_file()

    textProc = TextProcessor(textStr)
    pList = textProc.string_in_square_brakets_to_list (',')







