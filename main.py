import zipfile
import pandas as pd


def extrair_arquivos(zip_dir: str):
    try:
        with zipfile.ZipFile(zip_dir, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            for file_name in file_list:
                if file_name.endswith('.xlsx'):
                    zip_ref.extract(file_name)
            return True
    except FileExistsError as e:
        print(e)
        return False