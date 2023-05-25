import zipfile
import os


def extrair_arquivos(zip_dir: str) -> bool:
    try:
        with zipfile.ZipFile(zip_dir, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            for file in file_list:
                if file.endswith('.xlsx'):
                    zip_ref.extract(file)
            return True
    except FileNotFoundError as e:
        print(e)
        return False
    except FileExistsError as e:
        print(e)
        return False
    
def remover_arquivos(folder_dir: str) -> bool:
    try:
        file_list = os.listdir(folder_dir)
        for file in file_list:
            if file.endswith('.xlsx'):
                os.remove(os.path.join(folder_dir,file))
        return True
    except FileNotFoundError as e:
        print(e)
        return False
    except FileExistsError as e:
        print(e)
        return False


