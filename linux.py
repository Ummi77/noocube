import subprocess

class Linux():



    # Открытие документов ЛО
    # https://python-forum.io/thread-33814.html
    @staticmethod
    def open_window(path):
        """ 
        Открытие документов ЛО
        Category: Linux
        """
        subprocess.Popen (['soffice', path])

    # Фокусировка (сделать активным)
    # https://superuser.com/questions/142945/bash-command-to-focus-a-specific-window
    @staticmethod
    def focus_winow(titleFragment):
        """ 
        Фокусировка (сделать активным)
        Category: Linux
        """
        subprocess.run(f'wmctrl -a "{titleFragment}"', shell=True)


    # Закрытие окна
    @staticmethod
    def close_window(titleFragment):
        """ 
        Закрытие окна
        Category: Linux
        """
        subprocess.run(f'wmctrl -c "{titleFragment}"', shell=True)


    @staticmethod
    def activate_window():
        """  
        Активация заданного окна по имени или по классу. Изначально была в модуле lo_office для активации страницы при загрузке.  TODO: Доработать!!! 
        Category: Linux
        """
        output = subprocess.run(["cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/comm"], shell=True, capture_output=True, text = True) # определение текущего активного окна через консольную команду 
        if not ('soffice' in output.stdout) : # проверка активировано окно эксел или нет
            subprocess.run('wmctrl -a libreoffice.libreoffice-calc -x', shell=True) # если нет, то сфокусировать открытое окно эксел




    def run_file_subprocess (progrName, filePath):
        """Linux
        Открыть заданный файл через заданную программу с использованием subprocess
        Category: Linux
        """
        subprocess.run([f'{progrName} {filePath}'], shell=True, stdout=subprocess.PIPE)


if __name__ == "__main__":
    # main()
    pass

    # # # ПРИМЕР : Открытие текстового файла в notepadqq через консольные команды с использованием superproccess

    # progrName = 'notepadqq'
    # filePath = '~/Yandex.Disk_/MY_IT_TLH/KIVY.txt'
    # Linux.run_file_subprocess (progrName, filePath)










