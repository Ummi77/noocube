# created 18-07-2023

import subprocess
import sys


class Subproccess ():
    """ 
    Класс для работы с программой subproccess
    
     """

    def __init__(self):
        pass


    @staticmethod
    def run_subproccess (progrSetList, **subprocargs):
        """
        Subproccess
        Запускает програмуу, переданную в аргументах списка. В списке так же могут быть аргументы для самой программы
        **subprocargs - именные аргументы, для настроек программы запуска и ее воозвратов
        """

        r = subprocess.run(progrSetList, **subprocargs)
        
        return r

















if __name__ == "__main__":
    # main()
    pass




    # # ПРОРАБОТКА: run_subproccess (progrSetList, **subprocargs)
    
    # progrSetList = ['/usr/bin/code', '/home/ak/projects/2_Proj_TLH_Center/project_tlh/projr/classes/html_renderer.py']
    
    # Subproccess.run_subproccess(progrSetList)
    

    
    











