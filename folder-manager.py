import zipfile
import os

# Funcão que acessa e extrai os arquivos zipados
def extrair_arquivos(zip_dir: str) -> bool:
    ''' 
    Acessa o arquivo .zip e extrai seu conteúdo.

        input: Diretório do seu arquivo .zip
        output: Booleano, True para sucesso e False para falha
    '''
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

#Funcão para remover os arquivos utilizados
def remover_arquivos(folder_dir: str) -> bool:
    '''
    Remove os arquivos .xlsx do diretório especificado.

        input: Diretório que deseja excluir o conteúdo .xlsx
        output: Booleano, True para sucesso e False para falha
    '''
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


