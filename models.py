import pandas as pd
from database import *
from datetime import datetime, timedelta


mydb = client["mydatabase"]

# Crie uma coleção chamada "customers"
col_solicitacao = mydb["registros"]
col_filiais = mydb["filiais"]

