from data_handler import write_new_files, rename_files
from arq_manager import extrair_arquivos, remover_arquivos
from route_plot import calculate_tsp, plot_map
import pandas as pd
from loguru import logger
import os

zip_dir = r'./Planilhas de Dados.zip'
from_dir = r'./Planilhas de Dados'
dest_dir = r'./Rotas'



logger.info('Iniciando processo de extração e modelagem de dados...')


logger.info('Extraindo arquivos...')

if extrair_arquivos(zip_dir=zip_dir):
    logger.success('Arquivos extraidos!')
else:
    logger.error('Erro')

logger.info('Modelando dados...')

if write_new_files(from_dir):
    logger.success('Sucesso! 1/2')
    if rename_files(from_dir,dest_dir):
        logger.success('Sucesso! 2/2')

logger.info('Gerando rotas...')

dir = os.listdir(dest_dir)
for arquivo in dir:
    df = pd.read_excel(os.path.join(dest_dir,arquivo), engine='openpyxl')
    reordered_df = calculate_tsp(df)
    if plot_map(reordered_df, (arquivo.rsplit('.', 1)[0])):
        logger.success('Sucesso!')

logger.info('Limpando arquivos...')

if remover_arquivos(from_dir):
    if remover_arquivos(dest_dir):
        logger.success('Arquivos limpos!')


logger.success('Processo executado com sucesso!')


