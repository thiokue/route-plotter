import pandas as pd
import os

def data_cleaner(data_folder: str) -> list:
    try:
        data = []
        dir = os.listdir(data_folder)
        for file in dir:
            df = pd.read_excel(os.path.join(data_folder, file))
            df = df.fillna('####')
            data.append(df)
        return data
    except FileExistsError as e:
        print(e)
        return False
    except FileNotFoundError as e:
        print(e)
        return False
    
def get_elegible(data_folder: str) -> list:
    try:
        data = data_cleaner(data_folder)
        elegible_data = []
        for df in data:
            elegible_df = df[df['zone_name'] == 'Pare na Rua']
            elegible_df = elegible_df.sort_values(by='kilometer', ascending=False)
            elegible_data.append(elegible_df[:40])
        return elegible_data
    except Exception as e:
        print(e)
        return False


def write_new_files(data_folder: str) -> bool:
    try:
        data_list = get_elegible(data_folder)
        for i, df in enumerate(data_list):
            df.to_excel(f'./Rotas/Rota_{i+1}.xlsx', index=False)
        return True 
    except Exception as e:
        print(e)
        return False

def rename_files(folder1: str, folder2: str) -> bool:
    try:
        files1 = os.listdir(folder1)
        files2 = os.listdir(folder2)
        for file1, file2 in zip(files1, files2):
            file2_path = os.path.join(folder2, file2)      
            new_file_name = 'Rotas_'+ file1
            os.rename(file2_path, os.path.join(folder2, new_file_name))
        return True
    except FileExistsError as e:
        print(e)
        return False
    except FileNotFoundError as e:
        print(e)
        return False