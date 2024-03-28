from database import *
from config import *
from datetime import datetime

mydb = client["mydatabase"]

# Crie uma coleção chamada "customers"
col_solicitacao = mydb["registros"]
col_filiais = mydb["filiais"]
col_usuario = mydb["usuarios"]

