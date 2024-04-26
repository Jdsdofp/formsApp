from database import *
from config import *
from datetime import datetime, timedelta

mydb = client["mydatabase"]

# Crie uma coleção chamada "customers"
col_solicitacao = mydb["registros"]
col_filiais = mydb["filiais"]
col_usuario = mydb["usuarios"]

# Obter estatísticas do banco de dados
stats = mydb.command("dbStats")

# Extrair o tamanho total do banco de dados em bytes
total_size = stats['dataSize']

# Exibir o tamanho total em uma unidade legível, por exemplo, MB
total_size_mb = total_size / (1024 * 1024)
print(f"Tamanho total do banco de dados: {total_size_mb:.2f} MB")

