import pandas as pd
from models import *

# Ler a planilha do Excel
excel_file = 'carga.xlsx'
df = pd.read_excel(excel_file)

# Iterar sobre as linhas da planilha e preparar os dados de atualização
updates = []
for index, row in df.iterrows():
    cod_registro = row['cod_registro']
    nr_solicitacao = row['nr_solicitacao']
    oc = row['oc']
    NF = row['NF']
    vlr_oc = row['vlr_oc']

    updates.append({
        'filter': {'cod_registro': cod_registro},
        'update': {'$set': {'nr_solicitacao': nr_solicitacao, 'oc': oc, 'NF': NF, 'vlr_oc': vlr_oc}}
    })

# Atualizar os documentos no MongoDB
for update in updates:
    col_solicitacao.update_many(update['filter'], update['update'])

# Fechar a conexão com o MongoDB
client.close()
