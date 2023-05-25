import zipfile
import pandas as pd
import os


def extrair_arquivos(zip_dir: str):
    try:
        with zipfile.ZipFile(zip_dir, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            for file in file_list:
                if file.endswith('.xlsx'):
                    zip_ref.extract(file)
            return True
    except FileExistsError as e:
        print(e)
        return False
    
def remover_arquivos(folder_dir: str):
    try:
        file_list = os.listdir(folder_dir)
        for file in file_list:
            if file.endswith('.xlsx'):
                os.remove(os.path.join(folder_dir,file))
        os.removedirs(folder_dir)
        return True
    except FileNotFoundError as e:
        print(e)
        return False

extrair_arquivos('Planilhas de Dados.zip')
