


from noocube.files_manager import FilesManager



class HTMLSiteManagerJango (): # 
    """ 
    Класс для организации динамических компонентов сайта  и прочих вспомогательных функций на разных уровнях для сайта на базе Jango
    """

    # Конструктор
    def __init__(self):
        pass


    @staticmethod
    def prpare_const_line_from_url_args_matrix_with_exclusions (currRequestDic, listUrlArgsToExclude):
        """
        OBSOLETED : Переносится в модуль RequestManagerJango.prepare_url_const_line_from_request_dic_with_exclusions ()
        Сформировать url-строку с аргументами на основе словаря - матрицы входных аргументов (обычно взятых из request) с вычетом тех аргументов,
        которые указаны в списке исключений
        currRequestDic - словарь типа {<url_arg> : <значение аргумента>}
        listUrlArgsToExclude - список аргументов которые надо исключить, даже если они находятся в входной матрице аргументов, при построении строки для части ссылки на странице
        RET: String
        Category: Request JANGO
        """

        constUrlArgsLine = ''
        for key, val in currRequestDic.items():
            if key in listUrlArgsToExclude: # Исключаем аргументы, которые не нужны в строке URL
                pass
            else:
                constUrlArgsLine += f'&{key}={val}'
                
        return constUrlArgsLine
    
    


        


    @staticmethod
    def get_html_code_of_template_file(fileTemplPath):
        """
        HTMLSiteManagerJango
        Получить html-код шаблонного файла
        Category: Вспомогательные
        """
        
        htmlCode = FilesManager.read_file_data_txt_static(fileTemplPath)
        return htmlCode
    
    


    # STATIC 
    
    @staticmethod
    def get_static_path_of_file_from_its_full_path (fullPath):
        """ 
        HTMLSiteManagerJango
        Получить static- path для статических ресурсных фалов из их полного абсолютного пути
        Category: Вспомогательные
        """
        staticPath = FilesManager.find_subpath_of_file_path (fullPath, 'static')
        
        return staticPath
        
        
    
    # END STATIC













if __name__ == '__main__':
    pass



# ПРОРАБОТКА: Получить часть пути, начиная со статической директории типа static.

# file = '/home/ak/projects/P20_Wildberrys/wildberrys_proj/wildberrys_manager/static/img/163499755.webp'


# from noocube.files_manager import FilesManager



# staticPath = FilesManager.find_subpath_of_file_path (file, 'static')

# print(staticPath)



