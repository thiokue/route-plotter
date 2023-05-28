import pandas as pd
import os
from geopy.geocoders import Nominatim
from loguru import logger
from tqdm import tqdm

#Preenche valores vazios no dataset
def data_cleaner(data_folder: str) -> list:
    '''
    Abre os arquivos .xlsx dentro da pasta e preenche os valores vazios

        input: Diretório da pasta com arquivos .xlsx
        output: Lista de DataFrames
    '''
    try:
        data = []
        dir = os.listdir(data_folder)
        for file in dir:
            df = pd.read_excel(os.path.join(data_folder, file))
            df = df.fillna('####')
            data.append(df)
        return data
    except FileExistsError as e:
        logger.error(e)
        return False
    except FileNotFoundError as e:
        logger.error(e)
        return False

#Filtra pela coluna 'zone_name' e ordena pela colunas 'kilometer'
def get_elegible(data_folder: str) -> list:
    '''
    Os dataframes são criados apenas com os valores 'Pare na Rua' e ordena pela coluna 'kilometer'

        input: Diretório da pasta com arquivos.xlsx
        output: Lista de DataFrames
    '''
    try:
        data = data_cleaner(data_folder)
        elegible_data = []
        for df in tqdm(data):
            elegible_df = df[df['zone_name'] == 'Pare na Rua']
            elegible_df = elegible_df.sort_values(by='kilometer', ascending=False)
            elegible_df = elegible_df.head(40)
            elegible_df['adress'] = elegible_df.apply(lambda row: get_location(row['latitude'], row['longitude']), axis=1)
            elegible_data.append(elegible_df)
        return elegible_data
    except Exception as e:
        logger.error(e)
        return False

#Cria arquivos .xlsx baseado no retorno da função 'get_eligible'
def write_new_files(data_folder: str) -> bool:
    '''
    Cria arquivos .xlsx baseado no retorno da função 'get_eligible'.

        input: Diretório da pasta com arquivos.xlsx
        output: Booleano, True para sucesso e False para falha
    '''
    try:
        data_list = get_elegible(data_folder)
        for i, df in enumerate(data_list):
            df.to_excel(f'./Rotas/Rota_{i+1}.xlsx', index=False)
        return True 
    except Exception as e:
        logger.error(e)
        return False

#Renomeia os arquivos baseado nos arquivos .xlsx originais
def rename_files(folder1: str, folder2: str) -> bool:
    '''
    Renomeia os arquivos baseado nos arquivos .xlsx originais.

        input: Diretório 1 e Diretório 2
        output: Booleano, True para sucesso e False para falha
    '''
    try:
        files1 = os.listdir(folder1)
        files2 = os.listdir(folder2)
        for file1, file2 in zip(files1, files2):
            file2_path = os.path.join(folder2, file2)      
            new_file_name = 'Rotas_'+ file1
            os.rename(file2_path, os.path.join(folder2, new_file_name))
        return True
    except FileExistsError as e:
        logger.error(e)
        return False
    except FileNotFoundError as e:
        logger.error(e)
        return False

def get_location(latitude, longitude):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.reverse((latitude, longitude), exactly_one=True, timeout=None)
    return location.address