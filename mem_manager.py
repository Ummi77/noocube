


class MemManager():
    """ Класс для управления ммемами в системе TLH и вообще """

    # Конструктор
    def __init__(self):
        pass


    
    @staticmethod
    def highlight_mems_in_txt_for_html(txt, givenMem, highlColor = "#FF9C00"):
        """MemManager
        Выделить в тексте все мемы (альтернативно) и один - заданной особым образом в формате html
        """
        
        higlightedMem = f'<span style = "color:{highlColor}";"><b>{givenMem}</b></span>'
        txt = txt.replace(givenMem, higlightedMem)
        
        return txt







if __name__ == '__main__':

    pass













