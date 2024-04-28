

import inspect


class PythonSysManager (): 
    """ 
    Класс для методов работы с  pyhon и системой
    """



    @staticmethod
    def obtain_all_attributes_of_class_object (classObj):
        """ 
        Возвращает все атрибуты обьекта-класса classObj или class instance ()
        ~ https://www.geeksforgeeks.org/how-to-get-a-list-of-class-attributes-in-python/
        
        RET: Список таплов с атрибутами класса-обьекта или обьекта класса (Instance)
        
        Пример RET: listOfAttributesInTuple = [('field1', 'volume_file_name'), ('field2', 'volume_title'), ('volumeFileName', ''), ('volumeTitle', '')]

        """

        listOfAttributesInTuples = []
        # getmembers() returns all the 
        # members of an class object or class instance 
        for i in inspect.getmembers(classObj):
            
            # to remove private and protected
            # functions
            if not i[0].startswith('_'):
                
                # To remove other methods that
                # doesnot start with a underscore
                if not inspect.ismethod(i[1]): 
                    
                    listOfAttributesInTuples.append(i)
                    # print("PR_NC_207 --> ", i)
            
        return listOfAttributesInTuples









