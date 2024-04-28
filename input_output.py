
import os
from pathlib import Path


class InputOutput():
    """ Класс предназначен для организации считывания  и записи информации во всех формах
    В файлы, в буфер, в потоки и пр
      """

    def __init__(self, fName):
        self.fileName = fName



    # Create file and save text to it
    def save_to_file(self,text):
        """ 
        Create file and save text to it
        Category: Файлы и директории
        """
        with open(self.fileName, 'w') as file:
            file.write(text)
        path = Path(__file__).parent.absolute()
        print(f"File {self.fileName} Created successfully")
        return path


    # Remove file
    def delete_file(self):
        """ 
        Remove file
        Category: Файлы и директории
        """
        if(os.path.isfile(self.fileName)):
            os.remove(self.fileName)
            print(f"File {self.fileName} Deleted successfully")
        else:
            print(f"File {self.fileName} does not exist")


    # Read from file
    def read_from_file(self):
        """ 
        Read from file
        Category: Файлы и директории
        """
        f = open(self.fileName, "r")
        text = f.read()
        return text


if __name__ == "__main__":
    pass


    # # ПРИМЕР: создание файла, считывание
    # io = InputOutput('a024_inn_last.txt')
    # # innListTxt = str([1, 2, 5, 6])
    # # io.save_to_file(innListTxt)

    # text = io.read_from_file()
    # print (text)
