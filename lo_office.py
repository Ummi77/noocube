# import uno
import os
from noocube.linux import Linux
#from Obligations.calc_director import CalcDirector
from noocube.settings import *
import subprocess
from time import sleep
# from infor_assembling_center.files_manager import FilesManager

class LibreOffice (Linux):
    """ Настройка канала, открытие либре эксел с каналом, подключение к Либре офис, подключение к Либре эксел """

    # TODO: Разделить открытие офиса с подсоединением канала и дальнейшие открытия через команды к нему документов.
        # Не надо каждый раз запускать офис для работы с документами. Просто подсоединятся к нему через  Python !!!

    # TODO: Создать также статические функции сохранения, открыти и пр управлений документом 

        # Конструктор
    def __init__(self, module, port):
        """ Конструктор. mode  - заготовка , если будет работа с другими инструментами LO , кроме calc. Port -  номер порта для сокета """
        self.module = module
        self.port = port
        self.open_lo_through_socket('__none') # Открытие LibreOffice с подключением к сокету
        self.connect_to_opened_lo() # Подключение к открытому LibreSheets по заданному каналу


    # Открытие LibreOffice с подключением к сокету
    def open_lo_through_socket(self, mode = '__none'):
        """ 
        Открытие LibreOffice с подключением к сокету. Могут быть различные возможности: открытие чистого документа, открытие файла, открытие файла с запуском макросов
         * https://help.libreoffice.org/6.2/he/text/shared/guide/start_parameters.html
        Настройка кодировки. Возвращаемые параметры через stdout <subprocess.Popen> ...
        path : '__blank' or '{absolute path}'  (зарезервированные слова не должны быть в пути к файлу ). Для файла и  макросов потом ввести отдельный параметр  
        Category: Excel
        """

        if '__blank' in mode: # открывает LibreOffice и создает новый spreadsheet
            subprocess.Popen([f"soffice --calc --accept='socket,host=localhost,port={self.port};urp;StarOffice.ServiceManager'" ], encoding='cp866', shell=True, stdout=subprocess.PIPE)
            sleep(3) # !!! Дать время загрузить Либре эксел с каналом
        elif '__none': # Просто открывает LibreOffice 
            subprocess.Popen([f"soffice --accept='socket,host=localhost,port={self.port};urp;StarOffice.ServiceManager'" ], encoding='cp866', shell=True, stdout=subprocess.PIPE)
            sleep(3) # !!! Дать время загрузить Либре эксел с каналом  
        else: 
            raise ValueError("Что-то неправильно в параметре")


    # Подключение к открытому LibreSheets по заданному каналу
    def connect_to_opened_lo(self):
        """ 
        Подключает UNO к открытому LibreOffice через открытый сокет, создание  ServiceManager и Desktop , присваивание их в собственные переменные класса
        Category: Excel
        """
        localContext = uno.getComponentContext() # get the uno component context from the pyUNO runtime
        resolver = localContext.ServiceManager.createInstanceWithContext(
                    "com.sun.star.bridge.UnoUrlResolver", localContext) # create the UnoUrlResolver
        # Connecion to open LibreOffice
        self.ctx = resolver.resolve(f"uno:socket,host=localhost,port={self.port};urp;StarOffice.ComponentContext") # connect to the running office
        # ServiceManager
        self.smgr = self.ctx.ServiceManager 
        # Central desctop object
        self.desktop = self.smgr.createInstanceWithContext("com.sun.star.frame.Desktop", self.ctx) # get the central desctop object


    # Подключение по порту к офису. По умолчанию порт = 2002
    def open_connection(self):
        """ 
        <Устаревший метод>
        Category: Excel
        """
        if self.module == "calc":
            # # открывает либре-эксел и подсоединяется к нему через канал сокета
            subprocess.Popen([f"soffice --calc --accept='socket,host=localhost,port={self.port};urp;StarOffice.ServiceManager'" ], encoding='cp866', shell=True, stdout=subprocess.PIPE)
            sleep(3) # !!! Дать время загрузить Либре эксел с каналом
            output = subprocess.run(["cat /proc/$(xdotool getwindowpid $(xdotool getwindowfocus))/comm"], shell=True, capture_output=True, text = True) # определение текущего активного окна через консольную команду 
            if not ('soffice' in output.stdout) : # проверка активировано окно эксел или нет
                subprocess.run('wmctrl -a libreoffice.libreoffice-calc -x', shell=True) # если нет, то сфокусировать открытое окно эксел
            # Подключение к открытому LibreSheets по заданному каналу
            localContext = uno.getComponentContext() # get the uno component context from the pyUNO runtime
            resolver = localContext.ServiceManager.createInstanceWithContext(
                        "com.sun.star.bridge.UnoUrlResolver", localContext) # create the UnoUrlResolver
            # Connecion to open LibreOffice
            ctx = resolver.resolve(f"uno:socket,host=localhost,port={self.port};urp;StarOffice.ComponentContext") # connect to the running office
            # ServiceManager
            smgr = ctx.ServiceManager 
            # Central desctop object
            self.desctop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx) # get the central desctop object


    def _open_calc_file (self, path):
        """
        Открыть документ
        Category: Excel
        """
        pathURL = uno.systemPathToFileUrl(path)
        self.document = self.desktop.loadComponentFromURL(pathURL, '_default', 0, ())
        self.documentName = os.path.basename(path) # Присваиваем имя файла в собственную переменную
        self.dirName = os.path.dirname(path) # Присваиваем диреторию в собственную переменную
        
        return self.document



    def _new_doc_calc(self):
        self.desktop = self.smgr.createInstanceWithContext('com.sun.star.frame.Desktop', self.ctx)
        path = 'private:factory/scalc'
        self.document = self.desktop.loadComponentFromURL(path, '_default', 0, ())
        self.documentName = "_blank"
        return self.document 



    def _save_doc_as_new_file(self, path):
        """
        Сохранить документ в новом файле
        https://gist.github.com/sandy98/b4afaf9648ec986928a9
        Category: Excel
        """
        pathURL = uno.systemPathToFileUrl(path)
        self.document.storeToURL(pathURL,()) 
        self.documentName = os.path.basename(path) # Присваиваем имя файла в собственную переменную
        self.dirName = os.path.dirname(path) # Присваиваем диреторию в собственную переменную



    def _save(self):
        """
        Сохраняет документ
        https://gist.github.com/sandy98/b4afaf9648ec986928a9
        Category: Excel
        """
        if not self.document:
            return None
        else:
            if self.documentName == "_blank":
                print("File must have a name in order to be saved. Use 'saveAs'first")
                return None
            else:
                self.document.store()
                return self.document



    
if __name__ == "__main__":
    # main()
    pass




    # # ПРОРАБОТКА: Сохранение документа в существующий файл
    # libre = LibreOffice("calc",'2002')
    # path = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/proj_docs/test.ods'
    # doc = libre.open_calc_file (path)

    # print(libre.documentName)
    # # libre.document.store()
    # # libre.save()




    # # # # ПРОРАБОТКА: Сохранение документа в новй файл
    # libre = LibreOffice("calc",'2002')
    # doc = libre.new_doc_calc()
    # fname = 'test.ods'
    # dir = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/proj_docs'
    # newPath = dir + os.path.sep + fname
    # newPathURL = uno.systemPathToFileUrl(newPath)
    # doc.storeToURL(newPathURL,()) 



    # # ПРОРАБОТКА: Открвтие документа
    # libre = LibreOffice("calc",'2002')
    # path = '/home/ak/projects/1_Proj_Obligations_Analitic_Base/bonds/proj_docs/bankrupt_bonds_11_12_2022_07_32_31.xlsx'
    # doc = libre.open_calc_file (path)



    # ПРИМЕР: Открытие заданного документа или пустого (нового)

    # libre = LibreOffice("calc",'2002')
    # libre.open_lo_through_socket('__none') # Без открытия нового документа
    # libre.open_lo_through_socket('__blank') # С открытием нового spreadsheet  calc
    # libre.connect_to_opened_lo()

    # Для модуля lo_calc
    # document  = libre.desktop.loadComponentFromURL(uno.systemPathToFileUrl('/home/ak/projects/1_Proj_Obligations_Analitic_Base/proj_sources/test.ods'), "_blank", 0, tuple([]))

    # or open new blank doc
    # path = 'private:factory/scalc'
    # document = libre.desktop.loadComponentFromURL(path, '_default', 0, ())   

    # sheets = document.getSheets()
    # sheetCurr =  sheets.getByIndex(0)
    # document.getCurrentController().setActiveSheet(sheetCurr)

 

